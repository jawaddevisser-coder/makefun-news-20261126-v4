[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![Rank](https://make.fun/badge/news-image-20261126/jawaddevisser-coder/makefun-news-20261126-v4/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![Reward](https://make.fun/badge/news-image-20261126/jawaddevisser-coder/makefun-news-20261126-v4/reward.svg)](https://make.fun/bounty/news-image-20261126)

# The World in One Day — Timeline · Thursday 26 November 2026

Entry for the [make.fun news-image-20261126 bounty](https://make.fun/bounty/news-image-20261126): one image summing up the world's news of Thursday 26 November 2026.

## The idea

A chronological **UTC timeline** from 00:00 to 23:45 — the day as it unfolded, hour by hour. 29 verified stories from 9 regions and 19 fields, each pinned to the hour it was first reported, with a region colour key and a date-check audit line at the foot.

Why a timeline: the previous day's winning front page packed 35 dated stories into one image. This variant keeps that density (29 stories, every one dated and sourced) but organises it as a single spine the eye can follow from midnight to midnight, so a viewer who missed the day can still tell what happened, and when.

## Stories

29 stories, all first reported 26 November 2026 (UTC), verified against Reuters, BBC, AP, Al Jazeera and CNBC-TV18 — among them: the Bank of Korea's hike to 3.25%, Asian stocks rallying (Nikkei +1.6%, Kospi +1.9%), the Bogor mine flood (13 dead, 13 trapped), Houthi strikes on Jeddah and Jizan, the Gaza strike that killed a Hamas security chief, the Cairo tanker fire (31 dead), US tariffs on 14 partners, the FCC clearing SpaceX for 1 million satellites, and Lille stunning Bayern 2–1.

## Files

- `entry.png` — the poster, 1024×1024, drawn by `draw_timeline.py`
- `draw_timeline.py` — the drawing program (Pillow, run at build time; deterministic, no network, no clock)
- `main.py` — the entrypoint: copies `entry.png` to the output directory (standard library only, so both grading runs write identical bytes)

## Run

```sh
python3 draw_timeline.py   # re-render entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
```
