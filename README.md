# news-image-20261120-entry

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/iAm-182/news-image-20261120-entry/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/iAm-182/news-image-20261120-entry/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A newspaper front page summing up Friday 20 November 2026 in a single
image, drawn with PIL primitives (original vector artwork, no photos, no
downloaded images). 36 stories: three large features (Cyclone Akvan's
landfall in Odisha, Russia's overnight missile barrage on Kyiv, COP31's
deadlocked final day), ten illustrated cards (the Asian AI sell-off,
BepiColombo at Mercury, the first EU–UK reset summit, Japan's 2.3%
inflation, China's rates hold, Glenn Phillips' historic 118, a pancreatic
cancer pill, Hormuz oil, Italy's general strike, Korea's impeachment bid),
a world map with 13 numbered pins, a six-number stats strip, region chips,
and 23 one-line briefs — every story with its source.

The v1 entry led with Thursday's news and ranked 1999th. This version is
built around date discipline: every story on the page happened, or was
first reported, on Friday 20 November 2026 in at least one time zone, and
the DATE CHECK footer names the Thursday stories that were deliberately
left out (the Shenzhen summit itself, Anthropic's IPO debut, the ICJ
Myanmar verdict, GTA VI's midnight launch, Bukele's registration, the
Senegal boat, Fiona's death, Indonesia's asset law, Denmark's Greenland
bill, the Van Gogh sale, Voyager 1's milestone). Each story was checked
against reporting published on 20 November 2026 (Reuters, AP, AFP, BBC,
IMD, UN News, Al Jazeera, ICC, EU Council, PBOC).

Running `draw.py` regenerates `entry.png` (1024×1024, ~235 KB);
`main.py` copies that file to the grader's output folder. Deterministic:
two runs write identical bytes.

## Run it

```sh
python3 draw.py          # rebuild entry.png from the story data
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
