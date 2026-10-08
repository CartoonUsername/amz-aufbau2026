#!/usr/bin/env python3
"""Prüft Listing-CSVs vor dem Amazon-Upload (Format: data/listing_vorlage.csv).

Aufruf: python3 scripts/validate_listings.py [--nur-neu] data/spiegel_sets_texte_charge1.csv [weitere.csv ...]

--nur-neu: Amazon-Zeilen müssen in der Spalte asin_oder_neu den Wert "neu" haben (keine Updates bestehender ASINs).

Prüft: Titel-Länge, Bullets, Backend-Suchbegriffe, Preis, Platzhalter in eckigen Klammern,
https-Bild-URLs, doppelte SKUs und die Chargengröße (max. 20 Zeilen je Datei).
Exit-Code 1, wenn Fehler gefunden wurden.
"""
import csv
import re
import sys

MAX_ROWS = 20
MAX_TITLE = 150
MAX_BULLET = 500
MAX_KEYWORD_BYTES = 249
BULLETS = ["bullet_1", "bullet_2", "bullet_3", "bullet_4", "bullet_5"]
IMAGES = ["bild_haupt", "bild_2", "bild_3", "bild_4", "bild_5", "bild_6", "bild_7"]
PLACEHOLDER = re.compile(r"\[[^\]]+\]")


def check_file(path, nur_neu=False):
    errors, warnings = [], []
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) > MAX_ROWS:
        errors.append(f"{len(rows)} Zeilen, Chargengrenze ist {MAX_ROWS}")
    seen = set()
    for i, r in enumerate(rows, start=2):
        sku = r.get("sku", "").strip()
        tag = f"Zeile {i} ({sku or 'ohne SKU'})"
        if not sku:
            errors.append(f"{tag}: SKU fehlt")
        elif sku in seen:
            errors.append(f"{tag}: SKU doppelt")
        seen.add(sku)
        if nur_neu and "amazon" in r.get("marktplatz", "").lower() and r.get("asin_oder_neu", "").strip().lower() != "neu":
            errors.append(f"{tag}: ist kein neues Listing (asin_oder_neu = {r.get('asin_oder_neu', '')})")
        fk = r.get("fulfillment", "").upper()
        if fk.startswith("FBA") != sku.startswith("FBA_"):
            errors.append(f"{tag}: SKU-Präfix FBA_ und fulfillment passen nicht zusammen ({fk})")
        title = r.get("titel", "")
        if not title:
            errors.append(f"{tag}: Titel fehlt")
        elif len(title) > MAX_TITLE:
            errors.append(f"{tag}: Titel {len(title)} Zeichen (max. {MAX_TITLE})")
        for b in BULLETS:
            v = r.get(b, "")
            if not v:
                errors.append(f"{tag}: {b} fehlt")
            elif len(v) > MAX_BULLET:
                errors.append(f"{tag}: {b} {len(v)} Zeichen (max. {MAX_BULLET})")
        kw = r.get("suchbegriffe", "")
        if len(kw.encode("utf-8")) > MAX_KEYWORD_BYTES:
            errors.append(f"{tag}: Suchbegriffe {len(kw.encode('utf-8'))} Bytes (max. {MAX_KEYWORD_BYTES})")
        try:
            float(r.get("preis_eur", "").replace(",", "."))
        except ValueError:
            errors.append(f"{tag}: Preis ungültig")
        for k, v in r.items():
            if k and v and PLACEHOLDER.search(v):
                errors.append(f"{tag}: Platzhalter in {k}: {PLACEHOLDER.search(v).group(0)}")
        ready = r.get("status", "").lower() in ("bereit", "ready")
        urls = [r.get(c, "") for c in IMAGES if r.get(c)]
        if not urls:
            (errors if ready else warnings).append(f"{tag}: keine Bild-URLs")
        for u in urls:
            if not u.startswith("https://"):
                errors.append(f"{tag}: Bild-URL ohne https: {u}")
    return len(rows), errors, warnings


def main():
    args = [a for a in sys.argv[1:] if a != "--nur-neu"]
    nur_neu = "--nur-neu" in sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    failed = False
    for p in args:
        n, errors, warnings = check_file(p, nur_neu)
        print(f"\n{p}: {n} Zeilen, {len(errors)} Fehler, {len(warnings)} Hinweise")
        for e in errors[:15]:
            print("  FEHLER", e)
        if len(errors) > 15:
            print(f"  ... und {len(errors) - 15} weitere Fehler")
        for w in warnings[:3]:
            print("  HINWEIS", w)
        failed = failed or bool(errors)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
