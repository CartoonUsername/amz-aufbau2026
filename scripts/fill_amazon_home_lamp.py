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


# Lampengewichte in kg je Set. Große Lampen: oberer Wert der kg-Spanne aus dem SKU-Namen, Mini: ca. 650 g (Mini-Listings).
# Paketgewicht = Summe der Lampen + 0,5 kg (Angabe des Nutzers).
LAMPEN_KG = {
    "GS01-SALZ-DUO-1-2KG": [2, 2],
    "GS02-SALZ-DUO-2-3KG": [3, 3],
    "GS03-SALZ-DUO-3-5KG": [5, 5],
    "GS04-SALZ-DUO-WEISS-2-3KG": [3, 3],
    "GS05-SALZ-MINI-TRIO": [0.65] * 3,
    "GS06-SALZ-MINI-MOND-DUO": [0.65] * 2,
    "GS07-SALZ-1-2KG-PLUS-MINI": [2, 0.65],
    "GS08-SALZ-2-3KG-PLUS-MINI": [3, 0.65],
}
VERPACKUNG_KG = 0.5


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
        # Kategorie aus der Listing-Tabelle ("Beleuchtung > Tischlampen") -> Eintrag der Vorlage-Dropdown-Liste
        bn = col("recommended_browse_nodes#1.value")
        match = [x for x in sorted(allowed.get(bn, [])) if x.startswith("Beleuchtung > Innenbeleuchtung > Tisch- & Stehleuchten > Tischlampen (")]
        put_dd(bn, match[0] if match and "Tischlampen" in r.get("kategorie", "") else "", "Stöbern-Kategorie")
        for k in range(1, 6):
            put(col(f"bullet_point#{k}.value"), r[f"bullet_{k}"])
        put(col("product_description#1.value"), r["beschreibung_a_plus"])
        put(col("generic_keyword#1.value"), r["suchbegriffe"])
        put(col("number_of_items#1.value"), n)
        put(col("condition_type#1.value"), "Neu")
        # Profilwerte einer Einzellampe, die bei Sets nicht gelten
        # Farbe: weiße Lampen (Bialy) "Weiß", sonst Profilfarbe deiner Lampen
        if "WEISS" in sku.upper():
            put(col("color#1.value"), "Weiß")
        elif r.get("farbe"):
            put(col("color#1.value"), r["farbe"])
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
        lamps = LAMPEN_KG.get(sku.replace("FBA_", "", 1))
        if lamps:
            put(col("item_package_weight#1.value"), round(sum(lamps) + VERPACKUNG_KG, 2))
            put(col("item_package_weight#1.unit"), "Kilogramm")
        else:
            warnings.append(f"{sku}: Paketgewicht eintragen (Lampengewichte unbekannt)")
        warnings.append(f"{sku}: Paketmaße eintragen")
        for c, val in v.items():
            ws.cell(row=row, column=c).value = val

    wb.save(a.out)
    print(f"{len(rows)} Zeilen in {a.out} geschrieben")
    for w in warnings:
        print("OFFEN:", w)


if __name__ == "__main__":
    main()
