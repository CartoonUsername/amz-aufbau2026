#!/usr/bin/env python3
"""Trägt Bild-URLs in die Listing-CSV ein.

Namensschema der Bilddateien: <slug-der-sku>_01.jpg (Hauptbild), _02.jpg ... _07.jpg
Beispiel: S02-KLARO-WEISS-MATT-60x40 -> s02-klaro-weiss-matt-60x40_01.jpg

Aufruf:
  python3 scripts/fill_image_urls.py --csv data/spiegel_sets_texte_charge1.csv \
      --base-url https://cdn.shopify.com/s/files/1/XXXX/files \
      --images-dir /pfad/zu/den/bildern --out data/spiegel_sets_mit_bildern.csv

Ohne --images-dir werden alle 7 URLs eingetragen, mit --images-dir nur die Bilder, die als Datei existieren.
"""
import argparse
import csv
import os
import re
import sys

UML = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}
COLS = ["bild_haupt", "bild_2", "bild_3", "bild_4", "bild_5", "bild_6", "bild_7"]


def slug(text):
    text = text.lower()
    for k, v in UML.items():
        text = text.replace(k, v)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--base-url", required=True, help="öffentliche https-URL des Bildordners, ohne / am Ende")
    ap.add_argument("--images-dir")
    ap.add_argument("--ext", default="jpg")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    base = a.base_url.rstrip("/")
    if not base.startswith("https://"):
        sys.exit("Die Basis-URL muss mit https:// beginnen (Amazon, Otto und eBay verlangen https).")

    with open(a.csv, encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    head = rows[0]
    for c in COLS:
        if c not in head:
            sys.exit(f"Spalte {c} fehlt in der CSV")
    ix = {c: head.index(c) for c in COLS}
    sku_ix = head.index("sku")

    missing = []
    for r in rows[1:]:
        s = slug(r[sku_ix])
        for n, c in enumerate(COLS, start=1):
            fname = f"{s}_{n:02d}.{a.ext}"
            if a.images_dir and not os.path.isfile(os.path.join(a.images_dir, fname)):
                r[ix[c]] = ""
                if n == 1:
                    missing.append(fname)
                continue
            r[ix[c]] = f"{base}/{fname}"

    with open(a.out, "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(rows)

    if missing:
        print("Hauptbild fehlt für:", ", ".join(missing))
    print(f"{len(rows) - 1} Zeilen geschrieben nach {a.out}")


if __name__ == "__main__":
    main()
