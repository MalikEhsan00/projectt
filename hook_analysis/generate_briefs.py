"""Fill the type A/B/C brief templates for every creator.

usage: python3 generate_briefs.py [--creators handle1,handle2] [--limit N]
Reads  creator_type_assignments.csv, hook_labels_and_metrics.csv, brief_config.json, brief_templates/*.md
Writes creator_briefs.csv (one brief per creator; no URLs).
Edit brief_config.json (product, selling points, deal) before each run.
"""
import csv, json, os, sys, collections

here = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(here, "brief_config.json"), encoding="utf-8"))
TPL = {"A": "A_relatable_parent.md", "B": "B_promo_hype_seller.md", "C": "C_show_and_tell.md"}
tpl = {k: open(os.path.join(here, "brief_templates", f), encoding="utf-8").read() for k, f in TPL.items()}

arg = lambda name: sys.argv[sys.argv.index(name) + 1] if name in sys.argv else None
only = set(arg("--creators").split(",")) if arg("--creators") else None
limit = int(arg("--limit")) if arg("--limit") else None

# each creator's best own opener (highest-GMV video with a transcript or caption hook) = style reference
best = {}
for r in csv.DictReader(open(os.path.join(here, "hook_labels_and_metrics.csv"), encoding="utf-8")):
    if not r["hook_first_3s"] or r["hook_type"] == "Other": continue  # only real hooks are worth echoing back
    key = (r["label_source"] == "transcript", float(r["gmv"]))
    if r["creator"] not in best or key > best[r["creator"]][0]: best[r["creator"]] = (key, r["hook_first_3s"], r["hook_type"])

pts = (cfg["selling_points"] + [""] * 3)[:3]
deal = cfg["deal"]
deal_on = deal.get("active")
SWING = {  # one high-ceiling alternative per type
    "A": "Swing option: a curiosity opener told as a story, e.g. \"I found out why my kid suddenly asks to brush.\"",
    "B": "Swing option: a bold claim that withholds the answer, e.g. \"Stop buying a new toothbrush. Here's why.\"",
    "C": "Swing option: tease the result with \"nobody tells you\" or \"wait for it\" before the reveal.",
}
rows = []
for r in csv.DictReader(open(os.path.join(here, "creator_type_assignments.csv"), encoding="utf-8")):
    if only and r["creator"] not in only: continue
    own = best.get(r["creator"])
    style = (f"your best past hook was \"{own[1]}\" ({own[2]}). Keep that voice." if own
             else "no clear past hook found; use your natural voice.")
    out = tpl[r["brief_type"]].format(
        creator=r["creator"], product=cfg["product"], style_line=style,
        swing_line=SWING[r["brief_type"]], point_1=pts[0], point_2=pts[1], point_3=pts[2], cta=cfg["cta"],
        deal_line=(f"\n5. **Deal:** mention the {deal['text']} and that it {deal['deadline']}." if deal_on else ""),
        deal_hook=(f"Because the {deal['text']} is live, put the deadline in the next 2 seconds: \"{deal['deadline']}\"." if deal_on
                   else "No deal is live: skip urgency lines."))
    rows.append(dict(creator=r["creator"], brief_type=r["brief_type"], brief_type_name=r["brief_type_name"],
                     confidence=r["confidence"], brief=out))
    if limit and len(rows) >= limit: break

with open(os.path.join(here, "creator_briefs.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["creator", "brief_type", "brief_type_name", "confidence", "brief"])
    w.writeheader(); w.writerows(rows)
print(len(rows), "briefs ->", "creator_briefs.csv", dict(collections.Counter(r["brief_type"] for r in rows)))
