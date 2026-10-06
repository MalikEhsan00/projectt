"""Assign each creator to one of 3 brief types from the hooks they use.
usage: python3 assign_creator_types.py   (reads hook_labels_and_metrics.csv)
A = Relatable Parent (Story, Problem/Pain, Direct Question)
B = Promo / Hype Seller (Offer/Urgency, Bold/Shocking Claim, Social Proof)
C = Show-and-Tell / Reveal (Curiosity Gap; default when no hook technique is detected)"""
import csv, collections, os
here = os.path.dirname(os.path.abspath(__file__))
TYPE = {"Story / Personal Experience": "A", "Problem / Pain Point": "A", "Direct Question": "A",
        "Offer / Urgency": "B", "Bold / Shocking Claim": "B", "Social Proof / Results": "B",
        "Curiosity Gap": "C"}
NAME = {"A": "Relatable Parent", "B": "Promo / Hype Seller", "C": "Show-and-Tell / Reveal"}
rows = list(csv.DictReader(open(os.path.join(here, "hook_labels_and_metrics.csv"), encoding="utf-8")))
by = collections.defaultdict(list)
for r in rows: by[r["creator"]].append(r)
out = []
for c, vs in by.items():
    votes = collections.Counter()
    for v in vs:
        if v["hook_type"] in TYPE:  # "Other" = no hook technique, doesn't vote
            votes[TYPE[v["hook_type"]]] += 2 if v["label_source"] == "transcript" else 1  # transcript labels weigh more
    if votes:
        top = votes.most_common()
        t = top[0][0]; share = top[0][1] / sum(votes.values())
        conf = "high" if sum(1 for v in vs if v["label_source"] == "transcript") >= 3 and share >= 0.6 else \
               "medium" if len(vs) >= 3 and share >= 0.5 else "low"
    else:
        t, conf = "C", "low (default: no hook detected)"
    hooks = collections.Counter(v["hook_type"] for v in vs if v["hook_type"] != "Other")
    out.append(dict(creator=c, brief_type=t, brief_type_name=NAME[t], confidence=conf, videos=len(vs),
                    transcript_videos=sum(v["label_source"] == "transcript" for v in vs),
                    top_hooks="; ".join(f"{h} ({n})" for h, n in hooks.most_common(3)),
                    total_gmv=round(sum(float(v["gmv"]) for v in vs), 2)))
out.sort(key=lambda r: -r["total_gmv"])
with open(os.path.join(here, "creator_type_assignments.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(collections.Counter(r["brief_type"] for r in out), collections.Counter(r["confidence"].split(" ")[0] for r in out))
