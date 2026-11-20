# news-image-20261120-entry

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/iAm-182/news-image-20261120-entry/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/iAm-182/news-image-20261120-entry/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A dense newspaper front page summing up Friday 20 November 2026 in a
single image, drawn with PIL primitives (original artwork, no AI image
generation, no external images). 50 stories: a hero lead (Trump defers
the Iran decision to 2027), three illustrated leads (the Trump–Xi–Putin
summit in Shenzhen, the ICJ's genocide ruling against Myanmar, Cyclone
Akvan bearing down on Odisha), a world map with 12 numbered pins, a
by-the-numbers strip, and 38 one-line briefs from space to sport.

Every story was verified against reports published on 20 November 2026
(Reuters, BBC, AP, The Hindu, MarketWatch and others). Nothing is
invented: where a story's outcome was still pending at build time, the
wording states only what was reported.

`draw.py` generates `entry.png` (1024×1024, under 1 MiB); `main.py`
copies it to the grader's output directory. Deterministic: two runs
write identical bytes.

## Run it

```sh
python3 draw.py          # regenerate entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
