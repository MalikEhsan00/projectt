# Creator brief types

Three types cover every creator. Assign with `assign_creator_types.py` (majority vote over the hooks the creator already uses), then send the matching brief.

## Read this first: what the data really says

Hook-level GMV is dominated by a handful of videos (transcript-labelled, n = 873; 69% of videos earned $0). Curiosity Gap looked like the winner on totals, but one video ($72K) is 82% of its GMV. Without the top 3 videos per hook:

| Hook | Videos | Videos earning > $0 | Avg GMV excl. top 3 | Top video's share of total |
|---|---|---|---|---|
| Bold / Shocking Claim | 101 | 41% | $211 | 59% |
| Other (plain product intro / demo) | 232 | 31% | $208 | 20% |
| Offer / Urgency | 71 | 41% | $144 | 38% |
| Direct Question | 74 | 36% | $167 | 29% |
| Problem / Pain Point | 129 | 30% | $99 | 72% |
| Curiosity Gap | 61 | 34% | $81 | 82% |
| Story / Personal Experience | 148 | 32% | $58 | 65% |
| Social Proof / Results | 57 | 23% | $42 | 73% |

So: Bold Claim and Offer are the most dependable (41% of videos earn something). Curiosity Gap is a high-ceiling, low-floor bet. Story and Social Proof are the weakest. Differences are directional (small samples, one product), so treat them as defaults to test, not rules.

---

## Type A: Relatable Parent
**Who:** talks to camera about kids/family/daily life. Opens with a story, a frustration or a question. Warm, conversational.
**Hooks they already use:** Story, Problem / Pain, Direct Question.

**Lead hook: Direct Question tied to a pain** (best stable performer in this group: $167 avg excl. top 3).
**Swing hook: Curiosity Gap told as a story** ("I found out why my kid suddenly asks to brush").
**Drop:** plain Story openers with no pain or question (lowest performer, $58).

**Brief**
1. **Hook (0-3 s):** a question naming the pain, e.g. "Does your kid fight you every night over brushing?" Do not start with "So yesterday..." and no product name.
2. **Beat 1 (3-8 s):** one real moment from their house (the fight, the tears), in their own words.
3. **Beat 2 (8-20 s):** the product in use, on the kid, showing the one claim from the selling points (30-second clean).
4. **Beat 3:** the result in their words ("now she asks for it"). One concrete detail beats a general "it's great".
5. **CTA:** one line, with the deal if there is one running.
**Avoid:** more than one pain in the opener; reading specs.

## Type B: Promo / Hype Seller
**Who:** high-energy, fast cuts, sales language. Often posts deals and "get it before it's gone".
**Hooks they already use:** Offer / Urgency, Bold / Shocking Claim, Social Proof.

**Lead hook: Bold / Shocking Claim** (41% of videos earn, $211 avg excl. top 3), with **Offer / Urgency** as the second line when a promo is live (41%, $144).
**Swing hook:** Bold claim that withholds the answer ("Stop buying X. Here's why").
**Drop:** Social Proof-only openers ("this changed our routine"): weakest hit rate (23%).

**Brief**
1. **Hook (0-3 s):** one extreme or contrarian line that is true for the product ("You'll never use a weed wacker again", "Stop brushing like this"). If a promo is live, put the deadline in the next 2 s.
2. **Proof (3-10 s):** show the claim on screen immediately (demo or number on screen). Claim without proof drops engagement (this group has the lowest engagement rate, ~0.1%).
3. **Offer (10-20 s):** price/deal, the deadline, the link.
4. **CTA:** "tap the basket" style, repeat the deadline.
**Avoid:** vague claims, a deal with no reason to care about the product first.

## Type C: Show-and-Tell / Reveal
**Who:** product-first creators: unboxing, demo, "look at this". Less personality-driven, more visual.
**Hooks they already use:** Curiosity Gap, or none (plain "this is the X"). Also the default for creators with no detectable hook.

**Lead hook: Curiosity Gap built on a visible action** ("They said to click it, toothpaste on both sides", "wait until you see what this does") and a **clean product demo** as the fallback (plain demos earn a stable $208 avg excl. top 3, with the lowest outlier dependence).
**Drop:** a bare product intro with no tease (e.g. "This is the Autobrush, it has 58,000 bristles"). It is the reason Other underperforms its volume.

**Brief**
1. **Hook (0-3 s):** a physical action plus a withheld result ("watch what happens when I click this"). Product visible, result hidden.
2. **Payoff (3-10 s):** reveal the result within 10 s. The loop must close.
3. **Demo (10-25 s):** one benefit shown, not listed (full-mouth clean in 30 s on a timer).
4. **CTA:** one line.
**Avoid:** explaining before showing; opening with the product name.

---

## How to assign a creator
1. Label their last 5-10 openers with the 8 hook types (transcript preferred).
2. Vote: Story / Pain / Question → A; Offer / Bold / Social Proof → B; Curiosity → C. "Other" doesn't vote.
3. Majority wins. No detectable hook → C. `assign_creator_types.py` does this for the export in this folder.

`creator_type_assignments.csv`: 3,640 creators → A: 863, B: 630, C: 2,147. Only 40 have "high" confidence and 500 "medium". Most creators have only 1-2 videos in this export, so the assignment is a starting point, and C is inflated by the default.
