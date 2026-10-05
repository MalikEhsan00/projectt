"""Builds the hook analysis CSVs from a creator-video export + manual_labels.txt.

usage: python3 build_outputs.py <creator_video.csv>
manual_labels.txt = one code per video that has a transcript, in CSV row order.
"""
import csv, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from caption_rules import classify as caption_class, clean as caption_clean

CODES = {  # names/definitions from ../tiktok_hook_types.md
    "P": "Problem / Pain Point",
    "C": "Curiosity Gap",
    "S": "Social Proof / Results",
    "B": "Bold / Shocking Claim",
    "Q": "Direct Question",
    "V": "Story / Personal Experience",
    "O": "Offer / Urgency",
    "X": "Other",
}
here = os.path.dirname(os.path.abspath(__file__))

def hook_text(t, n=9):
    """~first 3 seconds of speech (about 3 words/sec)."""
    t = re.sub(r"\b\d{0,2}:\d{2}(\.\d+)?\b", " ", t)
    return " ".join(t.split()[:n])

rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8-sig")))
labels = open(os.path.join(here, "manual_labels.txt")).read().split()
assert len(labels) == sum(1 for r in rows if r["Transcript"].strip()), "label count mismatch"

it = iter(labels)
vids = []
for r in rows:
    has = bool(r["Transcript"].strip())
    cap = caption_clean(r["Description"])
    src = "transcript" if has else ("caption" if cap else "none")
    v = dict(
        video_id=r["URL"].rstrip("/").split("/")[-1],
        url=r["URL"],
        creator=r["Creator"],
        date=r["Date"][:10],
        hook_first_3s=hook_text(r["Transcript"]) if has else hook_text(cap),
        label_source=src,
        hook_type=CODES[next(it)] if has else (CODES[caption_class(cap)] if cap else "Other"),
        gmv=float(r["Video Revenue"] or 0),
        items_sold=int(float(r["Items Sold"] or 0)),
        views=int(float(r["Views Count"] or 0)),
        likes=int(float(r["Likes Count"] or 0)),
        comments=int(float(r["Comments Count"] or 0)),
    )
    if v["hook_type"] == "Other":
        if src == "none":
            v["other_reason"] = "no transcript or caption text"
        elif src == "caption":
            v["other_reason"] = "caption is a product name / generic text, no hook technique"
        elif re.match(r"^[\(\[]|^:?\d|^\W*$", v["hook_first_3s"]) or len(v["hook_first_3s"].split()) <= 2:
            v["other_reason"] = "no spoken hook / sound only"
        else:
            v["other_reason"] = "product intro / demo / mild benefit statement, no hook technique"
    v["engagements"] = v["likes"] + v["comments"]
    v["engagement_rate_pct"] = round(100 * v["engagements"] / v["views"], 3) if v["views"] else 0
    vids.append(v)

def write(name, fields, data):
    with open(os.path.join(here, name), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader(); w.writerows(data)

# 1) every video, labelled, NO url
lab_fields = ["video_id","creator","date","hook_first_3s","label_source","hook_type","other_reason","gmv","items_sold","views","likes","comments","engagements","engagement_rate_pct"]
write("hook_labels_and_metrics.csv", lab_fields, vids)

# 2) per-hook rollup, on two bases: transcript-only (reliable) and all videos (adds caption-based labels)
def rollup(basis, data):
    g = {}
    for v in data: g.setdefault(v["hook_type"], []).append(v)
    rows = []
    for h, items in g.items():
        n = len(items); gmv = sum(x["gmv"] for x in items); views = sum(x["views"] for x in items)
        eng = sum(x["engagements"] for x in items)
        rows.append(dict(basis=basis, hook_type=h, videos=n, total_gmv=round(gmv,2), avg_gmv_per_video=round(gmv/n,2),
            total_items_sold=sum(x["items_sold"] for x in items), total_views=views, avg_views_per_video=round(views/n),
            total_likes=sum(x["likes"] for x in items), total_comments=sum(x["comments"] for x in items),
            total_engagements=eng, engagement_rate_pct=round(100*eng/views,3) if views else 0,
            gmv_per_1k_views=round(1000*gmv/views,2) if views else 0))
    named = [s for s in rows if s["hook_type"] != "Other"]  # ranks cover named hooks only
    for key, col in [("gmv","total_gmv"),("gmv_avg","avg_gmv_per_video"),("views","total_views"),("views_avg","avg_views_per_video"),("eng_rate","engagement_rate_pct")]:
        for i, s in enumerate(sorted(named, key=lambda s: -s[col]), 1): s[f"rank_{key}"] = i
    return sorted(rows, key=lambda s: (s["hook_type"] == "Other", -s["total_gmv"]))

sf = ["basis","hook_type","videos","total_gmv","avg_gmv_per_video","total_items_sold","total_views","avg_views_per_video","total_likes","total_comments","total_engagements","engagement_rate_pct","gmv_per_1k_views","rank_gmv","rank_gmv_avg","rank_views","rank_views_avg","rank_eng_rate"]
summ = rollup("transcript_only", [v for v in vids if v["label_source"] == "transcript"]) + rollup("all_videos", vids)
write("hook_summary.csv", sf, summ)

# 3) top 3 per hook by GMV, WITH url (transcript-labelled videos only)
groups = {}
for v in vids:
    if v["label_source"] == "transcript": groups.setdefault(v["hook_type"], []).append(v)
top = []
for h in sorted(groups, key=lambda h: (h == "Other", -sum(x["gmv"] for x in groups[h]))):
    for rank, v in enumerate(sorted(groups[h], key=lambda x: -x["gmv"])[:3], 1):
        top.append(dict(v, hook_rank=rank))
write("top3_videos_per_hook.csv", ["hook_type","hook_rank","url","label_source","creator","date","hook_first_3s","gmv","items_sold","views","likes","comments","engagement_rate_pct"], top)

for s in summ: print(s["basis"][:4], s["hook_type"], s["videos"], s["total_gmv"], s["avg_gmv_per_video"], s["total_views"], s["engagement_rate_pct"], s.get("rank_gmv"))
