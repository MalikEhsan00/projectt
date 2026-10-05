# TikTok hook analysis

Run: `python3 build_outputs.py <creator_video.csv>` (needs `manual_labels.txt`, one hook code per transcribed video in CSV row order).

| File | Contents |
|---|---|
| `hook_labels_and_metrics.csv` | every video (9,563): hook label + GMV / views / likes / comments / engagement. **No URLs.** |
| `hook_summary.csv` | per-hook totals, averages and ranks (GMV, views, engagement rate) |
| `top3_videos_per_hook.csv` | top 3 videos per hook by GMV (`Video Revenue`), **with URL** |

- Hook = first ~9 words of the transcript (~3 s of speech). GMV = `Video Revenue`.
- Only 873 of 9,563 rows have a transcript; the other 8,690 are labelled `No Transcript` and left out of the hook rankings.
- Engagement rate = (likes + comments) / views. The export has no shares/saves.
- Hook types are a standard TikTok set, not your own list; swap names in `CODES` in `build_outputs.py` if you have a different one.
