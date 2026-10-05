"""
Hook Analyzer: Calodata CSV -> hook classification -> per-hook performance -> analytical draft.

Setup:
    pip install pandas anthropic
    export ANTHROPIC_API_KEY="your-key"

Run:
    python hook_analyzer.py calodata_export.csv
"""

import json
import re
import sys
import time

import anthropic
import pandas as pd

# ----------------------------------------------------------------------
# CONFIG: edit these
# ----------------------------------------------------------------------
MODEL = "claude-sonnet-5-5"
HOOK_WORDS = 12  # ~3 seconds of speech

# Map the names used here -> the exact column names in your Calodata CSV
COLUMNS = {
    "url": "Video URL",
    "transcript": "Transcript",
    "gmv": "GMV",
    "sales": "Sales",
    "likes": "Likes",
    "comments": "Comments",
}

# Your predefined hooks: name -> short definition (the definitions matter a lot)
HOOKS = {
    "Problem/Pain": "Opens by naming a pain point or frustration the viewer has.",
    "Curiosity Gap": "Teases something without revealing it, so the viewer must keep watching.",
    "Social Proof": "Opens with results, reviews, numbers, or 'everyone is buying this'.",
    "Shock/Bold Claim": "Surprising, extreme, or controversial statement.",
    "Question": "Opens by directly asking the viewer a question.",
    "Story/Personal": "Starts a personal story or experience ('I used to...').",
    "Offer/Urgency": "Leads with a deal, discount, or limited-time scarcity.",
    "Other": "Does not clearly fit any of the above.",
}

OUT_CLASSIFIED = "classified_videos.csv"
OUT_SUMMARY = "hook_summary.csv"
OUT_REPORT = "hook_report.md"

client = anthropic.Anthropic()


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def to_number(v):
    """Parse '$1,234.50', '1.2K', '3M', '12%' etc. into a float."""
    if pd.isna(v):
        return 0.0
    s = re.sub(r"[^\d.KkMm]", "", str(v))
    if not s:
        return 0.0
    mult = 1
    if s[-1] in "Kk":
        mult, s = 1_000, s[:-1]
    elif s[-1] in "Mm":
        mult, s = 1_000_000, s[:-1]
    try:
        return float(s) * mult
    except ValueError:
        return 0.0


def extract_hook(transcript, n_words=HOOK_WORDS):
    words = str(transcript).split()
    return " ".join(words[:n_words])


def call_claude(system, user, max_tokens=1000, retries=3):
    for attempt in range(retries):
        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
            return resp.content[0].text
        except Exception as e:
            print(f"  API error ({e}); retry {attempt + 1}/{retries}")
            time.sleep(2 * (attempt + 1))
    return ""


def parse_json(text):
    text = re.sub(r"```json|```", "", text).strip()
    return json.loads(text)


# ----------------------------------------------------------------------
# Step 1: load and clean
# ----------------------------------------------------------------------
def load(path):
    df = pd.read_csv(path)
    missing = [c for c in COLUMNS.values() if c not in df.columns]
    if missing:
        sys.exit(f"Missing columns in CSV: {missing}\nFound: {list(df.columns)}")

    out = pd.DataFrame(
        {
            "url": df[COLUMNS["url"]],
            "transcript": df[COLUMNS["transcript"]].fillna("").astype(str),
            "gmv": df[COLUMNS["gmv"]].map(to_number),
            "sales": df[COLUMNS["sales"]].map(to_number),
            "likes": df[COLUMNS["likes"]].map(to_number),
            "comments": df[COLUMNS["comments"]].map(to_number),
        }
    )
    out = out[out["transcript"].str.strip() != ""].reset_index(drop=True)
    out["hook_text"] = out["transcript"].map(extract_hook)
    return out


# ----------------------------------------------------------------------
# Step 2: classify hooks (batched to save calls)
# ----------------------------------------------------------------------
def classify(df, batch_size=15):
    hook_defs = "\n".join(f"- {k}: {v}" for k, v in HOOKS.items())
    system = (
        "You classify the opening hook of short-form TikTok Shop videos by the "
        "psychological technique used. Use ONLY these categories:\n"
        f"{hook_defs}\n\n"
        "Return ONLY a JSON array, no preamble or markdown. One object per input: "
        '{"id": <int>, "hook": "<category name exactly as listed>", '
        '"confidence": <0-1>, "reason": "<one short sentence>"}'
    )

    results = {}
    for start in range(0, len(df), batch_size):
        chunk = df.iloc[start : start + batch_size]
        payload = [{"id": int(i), "hook_text": r.hook_text} for i, r in chunk.iterrows()]
        print(f"Classifying {start + 1}-{start + len(chunk)} of {len(df)}...")
        raw = call_claude(system, json.dumps(payload), max_tokens=2000)
        try:
            for item in parse_json(raw):
                results[item["id"]] = item
        except Exception as e:
            print(f"  Could not parse batch ({e}); marking as Other")

    df["hook"] = [results.get(i, {}).get("hook", "Other") for i in df.index]
    df["confidence"] = [results.get(i, {}).get("confidence", 0) for i in df.index]
    df["reason"] = [results.get(i, {}).get("reason", "") for i in df.index]
    df.loc[~df["hook"].isin(HOOKS), "hook"] = "Other"
    return df


# ----------------------------------------------------------------------
# Step 3: aggregate and top 3
# ----------------------------------------------------------------------
def summarize(df):
    df["engagement"] = (df["likes"] + df["comments"])
    g = df.groupby("hook").agg(
        videos=("url", "count"),
        total_gmv=("gmv", "sum"),
        avg_gmv=("gmv", "mean"),
        median_gmv=("gmv", "median"),
        total_sales=("sales", "sum"),
        avg_sales=("sales", "mean"),
        avg_likes=("likes", "mean"),
        avg_comments=("comments", "mean"),
    )
    return g.sort_values("avg_gmv", ascending=False).round(2)


def top_videos(df, n=3):
    return (
        df.sort_values("gmv", ascending=False)
        .groupby("hook")
        .head(n)
        .sort_values(["hook", "gmv"], ascending=[True, False])
    )


# ----------------------------------------------------------------------
# Step 4: analytical draft
# ----------------------------------------------------------------------
def write_report(summary, tops):
    top_block = []
    for hook, grp in tops.groupby("hook"):
        top_block.append(f"## {hook}")
        for _, r in grp.iterrows():
            top_block.append(
                f"- GMV {r.gmv:,.0f} | Sales {r.sales:,.0f} | Likes {r.likes:,.0f} | "
                f"Comments {r.comments:,.0f}\n  Hook: \"{r.hook_text}\"\n  URL: {r.url}"
            )
    data = (
        "HOOK SUMMARY (sorted by average GMV):\n"
        + summary.to_string()
        + "\n\nTOP 3 VIDEOS PER HOOK:\n"
        + "\n".join(top_block)
    )

    system = (
        "You are a TikTok Shop creative strategist writing an analytical draft for an agency. "
        "Be specific, grounded only in the data given, and honest about weak evidence."
    )
    user = f"""Using the data below, write a markdown report with:

1. Executive summary (3-5 bullets)
2. Hook performance ranking (table: hook, videos, avg GMV, median GMV, avg sales, verdict)
3. For each hook: what the top 3 videos have in common (wording, structure, product type) and why it likely works
4. Caveats: flag any hook with fewer than 5 videos, and any case where one outlier drives the average
5. Recommendations: which hooks to scale, test, or drop, plus 3 example hook scripts for the best performer
6. Limitations: this analysis uses spoken transcript only, not on-screen text or visuals

DATA:
{data}"""
    return call_claude(system, user, max_tokens=4000)


# ----------------------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python hook_analyzer.py calodata_export.csv")

    df = load(sys.argv[1])
    print(f"Loaded {len(df)} videos with transcripts.")

    df = classify(df)
    df.to_csv(OUT_CLASSIFIED, index=False)

    summary = summarize(df)
    summary.to_csv(OUT_SUMMARY)
    print("\n", summary, "\n")

    tops = top_videos(df)
    report = write_report(summary, tops)
    with open(OUT_REPORT, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Done. Files: {OUT_CLASSIFIED}, {OUT_SUMMARY}, {OUT_REPORT}")


if __name__ == "__main__":
    main()
