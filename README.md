# tasmee3-mushaf

Mushaf files for the **Faris** (فارس) Quran recitation app: https://sayedfares.github.io/tasmee3/ — downloaded by the app on demand.

## `ligature-basd-svg/` — King Fahd Complex mushaf pages
SVG pages of the Madinah mushaf, one file per page (`001.svg` ... `604.svg`). Each word and ayah mark is a group tagged with its surah / ayah / word index (`data-surah`, `data-aya`, `data-word-index-in-ayah`), which the app uses to follow the reader word by word.
The files are published as received by the repository owner. Check the original source for the terms of use before reusing them elsewhere.

## `layouts/` — line layouts
Page → lines → `[surah, ayah, firstWord, lastWord]` runs (`"h<surah>"` banner, `"b"` basmala), built from the QUL line-layout databases by `build_layouts.py`. `layouts/index.json` lists them; the app downloads the ones the user picks.

## `data/` — Quran text in several scripts
Word-by-word and ayah-by-ayah text (Hafs, tajweed, Digital Khatt, Nastaleeq, QPC v4, Warsh, imlaei / uthmani simple), keyed `surah:ayah:word` (or `surah:ayah`). `catalog.json` lists the files. The two `*images*` files link to word images hosted on static-cdn.tarteel.ai.

Layout and text data: QUL (Quranic Universal Library). Each belongs to its authors and publishers.
