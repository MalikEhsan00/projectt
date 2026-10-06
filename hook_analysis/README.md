# TikTok hook analysis

Run: `python3 build_outputs.py <creator_video.csv>` (needs `manual_labels.txt`, one hook code per transcribed video in CSV row order).

| File | Contents |
|---|---|
| `hook_labels_and_metrics.csv` | every video (9,563): hook label + GMV / views / likes / comments / engagement. **No URLs.** |
| `hook_summary.csv` | per-hook totals, averages and ranks (GMV, views, engagement rate) |
| `top3_videos_per_hook.csv` | top 3 transcript-labelled videos per hook by GMV (`Video Revenue`), **with URL** |

- Hook = first ~9 words (first-sentence tie-break rules from the guide applied by hand) of the transcript (~3 s of speech). GMV = `Video Revenue`.
- Only 873 of 9,563 rows have a transcript. The other 8,690 are labelled from the video **caption** (`Description`, hashtags and disclaimers stripped) using keyword rules in `caption_rules.py` (6,437 rows). 2,253 rows have neither transcript nor caption text and are `Other`. `label_source` says which one was used.
- **Caption labels are a proxy for the spoken hook and are lower confidence** (about 80% agreement with my own judgement on a 130-caption sample; the Other bucket is large). `hook_summary.csv` reports `transcript_only` (reliable) and `all_videos` separately.
- Engagement rate = (likes + comments) / views. The export has no shares/saves.
- Hook types and tie-break rules come from `../tiktok_hook_types.md` (8 hooks). "Other" is the fallback (232 videos, mostly product intros/demos) and is excluded from the rank columns; its reason is in `other_reason`.

## Content briefs (3 creator types)
- `creator_types.md`: the 3 types, the evidence behind them, and how creators are assigned.
- `assign_creator_types.py` -> `creator_type_assignments.csv` (type + confidence per creator).
- `brief_templates/` (A, B, C) + `brief_config.json` (product, selling points, deal) + `generate_briefs.py` -> `creator_briefs.csv`, one filled brief per creator.
- Per run: edit `brief_config.json` (set `deal.active` to true when a promo is live), then `python3 generate_briefs.py` (`--creators a,b` or `--limit N` for a subset).
