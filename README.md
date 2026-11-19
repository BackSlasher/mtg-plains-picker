# Plains Picker

A static page for sorting Magic: The Gathering "Plains" artworks into yes / maybe / no,
to choose about 120 for a wall display.

- `index.html` is the whole app. Verdicts are kept in the browser's localStorage;
  "Export JSON" downloads them as `plains-picks.json`.
- `meta.json` lists the artworks: one per distinct illustration whose cheapest non-foil
  printing costs at most EUR 1 at Scryfall's market price, cheapest first. Card images are
  loaded from Scryfall's image CDN.
- `tools/build_meta.py` regenerates `meta.json` from the Scryfall API.

## Run locally

    python3 -m http.server

then open http://localhost:8000. Opening `index.html` as a file does not work, because the
page fetches `meta.json`.

## Publish

GitHub Pages, served from the root of the default branch. `.nojekyll` makes Pages serve
the files as they are.

Card images are © Wizards of the Coast and served by Scryfall. This is unofficial fan
content, not approved or endorsed by Wizards.
