"""Builds the hook analysis CSVs from a creator-video export + manual_labels.txt.

usage: python3 build_outputs.py <creator_video.csv>
manual_labels.txt = one code per video that has a transcript, in CSV row order.
"""
import csv, re, sys, os

CODES = {
    "Q": "Question",
    "P": "Problem / Pain Point",
    "C": "Curiosity / Open Loop",
    "B": "Bold Claim / Benefit",
    "S": "Shock / Warning / Pattern Interrupt",
    "T": "Social Proof / Testimonial",
    "V": "Personal Story / POV",
    "O": "Offer / Deal / Urgency",
    "D": "Demo / Product Intro",
    "A": "Direct Audience Call-Out",
    "X": "Other / No Clear Hook",
}
NO_TRANSCRIPT = "No Transcript"
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
    v = dict(
        video_id=r["URL"].rstrip("/").split("/")[-1],
        url=r["URL"],
        creator=r["Creator"],
        date=r["Date"][:10],
        hook_first_3s=hook_text(r["Transcript"]) if has else "",
        hook_type=CODES[next(it)] if has else NO_TRANSCRIPT,
        gmv=float(r["Video Revenue"] or 0),
        items_sold=int(float(r["Items Sold"] or 0)),
        views=int(float(r["Views Count"] or 0)),
        likes=int(float(r["Likes Count"] or 0)),
        comments=int(float(r["Comments Count"] or 0)),
    )
    v["engagements"] = v["likes"] + v["comments"]
    v["engagement_rate_pct"] = round(100 * v["engagements"] / v["views"], 3) if v["views"] else 0
    vids.append(v)

def write(name, fields, data):
    with open(os.path.join(here, name), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader(); w.writerows(data)

# 1) every video, labelled, NO url
lab_fields = ["video_id","creator","date","hook_first_3s","hook_type","gmv","items_sold","views","likes","comments","engagements","engagement_rate_pct"]
write("hook_labels_and_metrics.csv", lab_fields, vids)

# 2) per-hook rollup
groups = {}
for v in vids: groups.setdefault(v["hook_type"], []).append(v)
summ = []
for h, g in groups.items():
    n = len(g); gmv = sum(x["gmv"] for x in g); views = sum(x["views"] for x in g)
    eng = sum(x["engagements"] for x in g)
    summ.append(dict(hook_type=h, videos=n, total_gmv=round(gmv,2), avg_gmv_per_video=round(gmv/n,2),
        total_items_sold=sum(x["items_sold"] for x in g), total_views=views, avg_views_per_video=round(views/n),
        total_likes=sum(x["likes"] for x in g), total_comments=sum(x["comments"] for x in g),
        total_engagements=eng, engagement_rate_pct=round(100*eng/views,3) if views else 0,
        gmv_per_1k_views=round(1000*gmv/views,2) if views else 0))
real = [s for s in summ if s["hook_type"] != NO_TRANSCRIPT]
for key, col in [("gmv","total_gmv"),("gmv_avg","avg_gmv_per_video"),("views","total_views"),("views_avg","avg_views_per_video"),("eng_rate","engagement_rate_pct")]:
    ranked = sorted(real, key=lambda s: -s[col])
    for i, s in enumerate(ranked, 1): s[f"rank_{key}"] = i
summ.sort(key=lambda s: (s["hook_type"] == NO_TRANSCRIPT, -s["total_gmv"]))
sf = list(summ[0].keys()); sf = sf[:sf.index("rank_gmv")] if "rank_gmv" in sf else sf
sf = ["hook_type","videos","total_gmv","avg_gmv_per_video","total_items_sold","total_views","avg_views_per_video","total_likes","total_comments","total_engagements","engagement_rate_pct","gmv_per_1k_views","rank_gmv","rank_gmv_avg","rank_views","rank_views_avg","rank_eng_rate"]
write("hook_summary.csv", sf, summ)

# 3) top 3 per hook by GMV, WITH url
top = []
for h in sorted(groups, key=lambda h: -sum(x["gmv"] for x in groups[h])):
    if h == NO_TRANSCRIPT: continue
    for rank, v in enumerate(sorted(groups[h], key=lambda x: -x["gmv"])[:3], 1):
        top.append(dict(v, hook_rank=rank, hook_type=h))
write("top3_videos_per_hook.csv", ["hook_type","hook_rank","url","creator","date","hook_first_3s","gmv","items_sold","views","likes","comments","engagement_rate_pct"], top)

for s in summ: print({k: s[k] for k in ["hook_type","videos","total_gmv","avg_gmv_per_video","total_views","engagement_rate_pct","rank_gmv"] if k in s})
