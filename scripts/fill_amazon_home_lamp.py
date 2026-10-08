#!/usr/bin/env python3
"""Füllt die Amazon-Vorlage LAMP (Tischlampen/Salzlampen, Amazon.de) mit den Salzlampen-Sets.

Aufruf:
  python3 scripts/fill_amazon_home_lamp.py \
      --template kanaele/amazon/vorlagen/home_lamp.xlsm \
      --csv produkte/salzlampen/geschenksets_fbm.csv \
      --out kanaele/amazon/chargen/charge_02_salzlampen_sets/amazon_upload_FBM.xlsm

Wie beim Spiegel-Skript: nur Angaben aus der Listing-Tabelle, nichts erfunden, Unbekanntes bleibt leer und
wird als OFFEN gemeldet. Die Profilzeile (Zeile 8) gilt für EINE bestimmte Lampe; Werte, die bei Sets nicht
stimmen (Farbe, Artikelmaße, Anzahl), werden geleert beziehungsweise überschrieben.
"""
import argparse
import csv
import re
import sys

import openpyxl

FIRST_DATA_ROW = 8


def norm(t):
    t = re.sub(r"\[marketplace_id=[^\]]*\]", "", t or "")
    return re.sub(r"\[language_tag=[^\]]*\]", "", t)


def count_of(sku):
    s = sku.upper()
    if "TRIO" in s:
        return 3
    return 2  # DUO, MOND-DUO, PLUS-MINI: jeweils zwei Lampen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", required=True)
    ap.add_argument("--csv", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--versandvorlage", default="Prime Mustervorlage")
    a = ap.parse_args()

    wb = openpyxl.load_workbook(a.template, keep_vba=True)
    ws = wb["Vorlage"]
    tech = {c: ws.cell(row=5, column=c).value for c in range(1, ws.max_column + 1)}
    by_norm = {}
    for c, t in tech.items():
        by_norm.setdefault(norm(t), []).append(c)

    def col(name):
        if name not in by_norm:
            sys.exit(f"Spalte nicht gefunden: {name}")
        return by_norm[name][0]

    price_col = next(c for c, t in tech.items() if t and "audience=ALL" in t and "our_price" in t and t.endswith("value_with_tax"))
    defaults = {c: ws.cell(row=FIRST_DATA_ROW, column=c).value for c in range(1, ws.max_column + 1)}
    labels = {c: ws.cell(row=4, column=c).value for c in range(1, ws.max_column + 1)}
    allowed = {}
    for r in wb["Gültige Werte"].iter_rows(min_row=1, values_only=True):
        name = re.sub(r"\s*-\s*\[.*$", "", str(r[1] or "")).strip()
        if name:
            vals = {str(v) for v in r[2:] if v not in (None, "")}
            for c, lab in labels.items():
                if lab == name and vals:
                    allowed.setdefault(c, set()).update(vals)

    with open(a.csv, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    warnings = []
    for i, r in enumerate(rows):
        row = FIRST_DATA_ROW + i
        sku = r["sku"]
        n = count_of(sku)
        v = dict(defaults)

        def put(c, val):
            v[c] = val

        def put_dd(c, val, feld):
            val = (val or "").strip()
            if not val:
                v[c] = None
                warnings.append(f"{sku}: {feld} fehlt")
            elif c in allowed and val not in allowed[c]:
                v[c] = None
                warnings.append(f"{sku}: {feld} \"{val}\" steht nicht in der Dropdown-Liste der Vorlage")
            else:
                v[c] = val

        put(col("contribution_sku#1.value"), sku)
        put(col("product_type#1.value"), "LAMP")
        put(col("item_name#1.value"), r["titel"])
        put(col("brand#1.value"), "EmsCraft24")
        put(col("manufacturer#1.value"), "EmsCraft24")
        gtin = re.sub(r"\D", "", r.get("gtin_ean", ""))
        if len(gtin) in (8, 12, 13, 14):
            put(col("amzn1.volt.ca.product_id_type"), "EAN" if len(gtin) == 13 else "GTIN")
            put(col("amzn1.volt.ca.product_id_value"), gtin)
        else:
            put(col("amzn1.volt.ca.product_id_type"), None)
            put(col("amzn1.volt.ca.product_id_value"), None)
            warnings.append(f"{sku}: EAN fehlt")
        warnings.append(f"{sku}: Stöbern-Kategorie (Browse Node) eintragen")
        for k in range(1, 6):
            put(col(f"bullet_point#{k}.value"), r[f"bullet_{k}"])
        put(col("product_description#1.value"), r["beschreibung_a_plus"])
        put(col("generic_keyword#1.value"), r["suchbegriffe"])
        put(col("number_of_items#1.value"), n)
        put(col("condition_type#1.value"), "Neu")
        # Profilwerte einer Einzellampe, die bei Sets nicht gelten
        put(col("color#1.value"), r.get("farbe") or None)
        if not r.get("farbe"):
            warnings.append(f"{sku}: Farbe fehlt (Profilwert wurde entfernt)")
        for name in ("item_depth_width_height#1.depth.value", "item_depth_width_height#1.depth.unit",
                     "item_depth_width_height#1.height.value", "item_depth_width_height#1.height.unit",
                     "item_depth_width_height#1.width.value", "item_depth_width_height#1.width.unit"):
            put(col(name), None)
        warnings.append(f"{sku}: Artikelmaße und Artikelgewicht eintragen (Profilmaße einer Einzellampe entfernt)")
        put(price_col, r["preis_eur"])
        fba = r.get("fulfillment", "").upper().startswith("FBA")
        put(col("fulfillment_availability#1.fulfillment_channel_code"), "Versand durch Amazon (EU)" if fba else "Versand durch Händler (Standard)")
        put(col("merchant_shipping_group#1.value"), None if fba else a.versandvorlage)
        qty = re.sub(r"\D", "", r.get("bestand", "")) or "100"
        put(col("fulfillment_availability#1.quantity"), None if fba else int(qty))
        put(col("main_product_image_locator#1.media_location"), r.get("bild_haupt") or None)
        for k in range(1, 8):
            put(col(f"other_product_image_locator_{k}#1.media_location"), r.get(f"bild_{k + 1}") or None)
        if not r.get("bild_haupt"):
            warnings.append(f"{sku}: Hauptbild-URL fehlt")
        warnings.append(f"{sku}: Paketmaße und Paketgewicht eintragen")
        for c, val in v.items():
            ws.cell(row=row, column=c).value = val

    wb.save(a.out)
    print(f"{len(rows)} Zeilen in {a.out} geschrieben")
    for w in warnings:
        print("OFFEN:", w)


if __name__ == "__main__":
    main()
