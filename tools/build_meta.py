# Writes meta.json: one entry per distinct Plains artwork whose cheapest non-foil
# printing costs at most MAX_EUR at Scryfall's market price, cheapest first.
# Usage: python3 tools/build_meta.py [cached-scryfall-search.json]
import json, sys, time, urllib.parse, urllib.request

MAX_EUR = 1.0
UA = "plains-picker/1.0 (static site build; python-urllib)"


def fetch():
    url = "https://api.scryfall.com/cards/search?" + urllib.parse.urlencode(
        {"q": '!"Plains" game:paper', "unique": "prints", "order": "released"})
    cards = []
    while url:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        page = json.load(urllib.request.urlopen(req, timeout=30))
        cards += page["data"]
        url = page.get("next_page")
        time.sleep(0.2)
    return cards


cards = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else fetch()
arts = {}
for c in cards:
    art = c.get("illustration_id") or c["id"]
    eur = (c.get("prices") or {}).get("eur")
    if eur is None or not c.get("nonfoil", True) or "image_uris" not in c or c.get("oversized"):
        continue
    if art not in arts or float(eur) < arts[art][0]:
        arts[art] = (float(eur), c)
rows = sorted((a for a in arts.values() if a[0] <= MAX_EUR), key=lambda a: (a[0], a[1]["released_at"]))
meta = [{"id": c["id"], "i": i, "p": p, "s": c["set"].upper(), "n": c["set_name"],
         "c": c["collector_number"], "y": c["released_at"][:4], "a": c.get("artist") or "",
         "f": bool(c.get("full_art")), "u": c["scryfall_uri"].split("?")[0],
         "img": c["image_uris"]["normal"]}
        for i, (p, c) in enumerate(rows)]
json.dump(meta, open("meta.json", "w"), ensure_ascii=False, separators=(",", ":"))
print(len(meta), "artworks")
