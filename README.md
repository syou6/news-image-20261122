# The World in a Day — 22 November 2026

A single-image front page summarizing the world news of Sunday, 22 November 2026, built for the make.fun bounty [news-image-20261122](https://make.fun/bounty/news-image-20261122).

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/syou6/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/syou6/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

## What it is

`entry.png` is a dense 1024×1024 newspaper front page for Sunday 22 November 2026 — 53 stories in nine sections under one huge date masthead. The lead story is COP31 deadlocked into a second day of overtime in Antalya, Türkiye, split over fossil fuels after a $120bn adaptation fund was dropped from the draft, with a drawn cracked-globe visual. Four secondary cards follow: Iran hitting a Bahrain industrial site and two tankers struck near the Strait of Hormuz; three Houthi ballistic missiles intercepted over Riyadh (with a coalition strike on Hodeidah port); Ukraine striking the Crimean bridge; and the southern Nigeria funeral-boat capsize (24 dead, 24 rescued). Below, "Around the World in Brief" packs 40 one-line stories into six regional groups — Europe, Middle East, Asia-Pacific, Africa, Americas, and Economy + Science + Culture — followed by a sport strip (Liverpool 4-0 Manchester United, Verstappen's Las Vegas win, Wembanyama's 50 points, the Kansas City Current's first NWSL title, three NFL results and a Bayern injury). The foot of the page carries a UTC timeline of the day ("The Day Around the Clock"), a sources line, and a dotted world map pinning Antalya, Riyadh, Hormuz, Kyiv and Lagos. Every story shown happened, or was first reported, on that date.

## Run it

```
python3 main.py
```

`main.py` (Python 3.13, standard library only, no network) validates the bundled `entry.png` and writes it to `/output/entry.png`, byte-identical on every run. `build_image.py` is the Pillow program that drew the image.

## License

MIT — see `LICENSE`.
