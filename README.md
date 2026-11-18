# tasmee3_mushaf

Mushaf data for the Faris (فارس) recitation app, downloaded on demand.

- `layouts/` — line layouts (page → lines → `[surah, ayah, firstWord, lastWord]` runs, `"h<surah>"` banner, `"b"` basmala) built from the QUL line-layout databases by `build_layouts.py`. `layouts/index.json` lists them. The app downloads the ones the user picks.
- `data/` — word-by-word and ayah-by-ayah Quran text in several scripts (Hafs, tajweed, Digital Khatt, Nastaleeq, QPC v4, Warsh, imlaei/uthmani simple), keyed `surah:ayah:word` (or `surah:ayah`). The two `*images*` files link to word images hosted on static-cdn.tarteel.ai.

Source: QUL (Quranic Universal Library) data. Each belongs to its authors and publishers.
