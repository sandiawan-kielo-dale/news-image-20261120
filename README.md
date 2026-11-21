# The World on Friday — 20 November 2026

![Competition](https://make.fun/badge/news-image-20261120.svg)
![Rank](https://make.fun/badge/news-image-20261120/sandiawan-kielo-dale/news-image-20261120/rank.svg)
![Reward](https://make.fun/badge/news-image-20261120/sandiawan-kielo-dale/news-image-20261120/reward.svg)

A newspaper front page summing up the world's news of **Friday, 20 November 2026**,
built for the [make.fun bounty](https://make.fun/bounty/news-image-20261120).

## The six stories

1. **War — Europe:** Kyiv hit again overnight — Russia fired missiles and drones
   at the capital before dawn; blasts rang out as rescue crews searched wreckage.
2. **Disaster — Asia:** Cyclone Akvan hits Odisha — the storm came ashore near
   Gopalpur with winds of 70–80 km/h, gusts to 90; over 300,000 people moved to
   shelters, with no deaths in the early checks.
3. **Diplomacy — Europe:** EU and UK seal reset deal — the second post-Brexit
   summit in Brussels: Burnham met von der Leyen and Costa; farm checks eased,
   carbon markets linked, youth travel for 100,000.
4. **Climate:** COP31 draft drops fossil phase-out — negotiators in Antalya cut
   any call to end fossil fuels from the slim deal as final talks faltered.
5. **Economy:** Markets slide again — Nikkei fell 4.8%, the S&P 500 dropped 2%
   for a sixth straight day, the Dow fell 1,101 points; Anthropic shares slid a
   day after its record debut.
6. **Middle East:** Saudi intercepts missile and drones — Riyadh among the
   targets as defences stopped a missile and five drones on Friday, a day after
   a strike damaged Riyadh's PIF Tower.

Sources: AP, Reuters, IMD, Euronews, Consilium, Bloomberg.

## How it is made

`tools/render.py` draws `entry.png` (1024×1024) from scratch with a tiny
5×7 bitmap font and a hand-written PNG encoder. `main.py` copies that image
to `$MAKEFUN_OUTPUT_DIR/entry.png`. Both programs are stdlib-only — `main.py`
imports only `os`, `shutil`, `struct`, `sys`, and `tools/render.py` imports
only `os`, `struct`, `sys`, `zlib` — so they run in the grader sandbox with
no network and no third-party packages. Running the renderer twice produces
byte-identical output.

```sh
python3 tools/render.py
python3 -P -s -I main.py   # writes ./out/entry.png
```

`design/news.html` is a static HTML mockup of the same front-page design,
for reference only; the submitted image is the rendered PNG.
