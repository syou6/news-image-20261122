# The World in a Day — 22 November 2026

A single-image front page summarizing the world news of Sunday, 22 November 2026, built for the make.fun bounty [news-image-20261122](https://make.fun/bounty/news-image-20261122).

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/syou6/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/syou6/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

## What it is

`entry.png` is a 1024×1024 newspaper-style front page for 22 November 2026: a large date masthead, the day's lead story (COP31 deadlocked in overtime in Antalya), four secondary cards (Iran hitting a Bahrain site and tankers in Hormuz, Houthi missiles downed over Riyadh, Ukraine striking the Crimean bridge, the Nigeria funeral-boat capsize) and a bottom strip (an Indonesia factory fire, a Peru M6.7 quake, protests in France). Every story shown was reported on that date.

## Run it

```
python3 main.py
```

`main.py` (Python 3.13, standard library only, no network) validates the bundled `entry.png` and writes it to `/output/entry.png`, byte-identical on every run. `build_image.py` is the Pillow program that drew the image.

## License

MIT — see `LICENSE`.
