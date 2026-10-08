#!/usr/bin/env python3
"""Erzeugt aus einer FBM-Listing-Tabelle die FBA-Kopie.

FBM-Tabelle = Hauptversion (SKU ohne Präfix, fulfillment = FBM, Bestand = Eigenbestand).
FBA-Kopie   = gleiche Zeilen mit SKU "FBA_<SKU>", fulfillment = FBA, ohne Bestand, mit DERSELBEN GTIN
              (derselbe Artikel, dieselbe Produktseite, ein zweites Angebot).

Aufruf: python3 scripts/make_fba_copies.py --in data/spiegel_sets_texte_charge1.csv --out data/spiegel_sets_texte_charge1_fba.csv
"""
import argparse
import csv
import sys

PREFIX = "FBA_"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    with open(a.inp, encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    h = rows[0]
    ix = {k: h.index(k) for k in ("sku", "fulfillment", "bestand", "gtin_ean")}
    out = [h]
    for r in rows[1:]:
        if r[ix["fulfillment"]].upper() != "FBM":
            sys.exit(f"{r[ix['sku']]}: Hauptversion muss fulfillment = FBM haben")
        if r[ix["sku"]].startswith(PREFIX):
            sys.exit(f"{r[ix['sku']]}: FBM-SKU darf nicht mit {PREFIX} beginnen")
        c = list(r)
        c[ix["sku"]] = PREFIX + r[ix["sku"]]
        c[ix["fulfillment"]] = "FBA"
        c[ix["bestand"]] = ""
        out.append(c)
    with open(a.out, "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(out)
    print(f"{len(out) - 1} FBA-Kopien in {a.out}")


if __name__ == "__main__":
    main()
