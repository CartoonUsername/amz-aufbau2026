#!/usr/bin/env python3
"""Füllt die Amazon-Vorlage HOME_MIRROR (Heim-Spiegel, Amazon.de) mit den Spiegel-Sets.

Aufruf:
  python3 scripts/fill_amazon_home_mirror.py \
      --template templates/amazon/home_mirror.xlsm \
      --csv data/spiegel_sets_texte_charge1.csv \
      --out upload/amazon/charge_01_spiegel_sets/amazon_upload_ENTWURF.xlsm

Die Vorlage bleibt unverändert, Kopfzeilen 1 bis 7 werden nicht angefasst. Ab Zeile 8 steht je Set eine Zeile.
Werte aus der von Amazon vorausgefüllten Profilzeile (Zeile 8) werden für alle Zeilen übernommen und nur
überschrieben, wenn die Listing-Tabelle einen Wert hat.
"""
import argparse
import csv
import re
import sys

import openpyxl

BROWSE = "Küche, Haushalt & Wohnen > Möbel > Diele & Flur > Wandspiegel (2970878031)"
FIRST_DATA_ROW = 8


def norm(t):
    t = re.sub(r"\[marketplace_id=[^\]]*\]", "", t or "")
    t = re.sub(r"\[language_tag=[^\]]*\]", "", t)
    return t


def put_checked(values, c, value, feld, sku, warnings):
    """Trägt nur Werte ein, die in der Tabelle stehen UND in der Dropdown-Liste der Vorlage vorkommen."""
    value = (value or "").strip()
    mapped = ZUORDNUNG.get((feld, value))
    if mapped:
        value = mapped
    allowed = ALLOWED.get(c)
    if not value:
        values[c] = None
        warnings.append(f"{sku}: {feld} fehlt (kein Wert in der Listing-Tabelle)")
    elif allowed is not None and value not in allowed:
        values[c] = None
        warnings.append(f"{sku}: {feld} \"{value}\" steht nicht in der Dropdown-Liste der Vorlage")
    else:
        values[c] = value


ALLOWED = {}
ZUORDNUNG = {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", required=True)
    ap.add_argument("--csv", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--versandvorlage", help="Name der Versandvorlage für FBM-Zeilen, z. B. \"Schneller Versand\"")
    a = ap.parse_args()

    wb = openpyxl.load_workbook(a.template, keep_vba=True)
    ws = wb["Vorlage"]
    tech = {c: ws.cell(row=5, column=c).value for c in range(1, ws.max_column + 1)}
    by_norm = {}
    for c, t in tech.items():
        by_norm.setdefault(norm(t), []).append(c)

    def col(name, nth=0):
        cols = by_norm.get(name)
        if not cols:
            sys.exit(f"Spalte nicht gefunden: {name}")
        return cols[nth]

    price_col = next(c for c, t in tech.items() if t and "audience=ALL" in t and "our_price" in t and t.endswith("value_with_tax"))
    defaults = {c: ws.cell(row=FIRST_DATA_ROW, column=c).value for c in range(1, ws.max_column + 1)}
    # Dropdown-Listen aus dem Blatt "Gültige Werte" (Zeile = Feld, Werte ab Spalte 3)
    labels = {c: ws.cell(row=4, column=c).value for c in range(1, ws.max_column + 1)}
    for r in wb["Gültige Werte"].iter_rows(min_row=1, values_only=True):
        name = re.sub(r"\s*-\s*\[.*$", "", str(r[1] or "")).strip()
        if name:
            vals = {str(v) for v in r[2:] if v not in (None, "")}
            for c, lab in labels.items():
                if lab == name and vals:
                    ALLOWED.setdefault(c, set()).update(vals)

    with open(a.csv, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    # bestätigte Zuordnungen "deine Angabe" -> Dropdown-Wert (data/amazon_wertezuordnung.csv)
    try:
        with open("data/amazon_wertezuordnung.csv", encoding="utf-8", newline="") as f:
            for z in csv.DictReader(f):
                if z["bestaetigt"].strip().lower() == "ja" and z["dropdown_wert"]:
                    ZUORDNUNG[(z["feld"], z["deine_angabe"])] = z["dropdown_wert"]
    except FileNotFoundError:
        pass

    warnings = []
    for i, r in enumerate(rows):
        row = FIRST_DATA_ROW + i
        values = dict(defaults)
        n = 2 if r["sku"].upper().startswith("S02") else 3 if r["sku"].upper().startswith("S03") else 1

        def put(c, v):
            values[c] = v

        put(col("contribution_sku#1.value"), r["sku"])
        put(col("product_type#1.value"), "HOME_MIRROR")
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
            warnings.append(f"{r['sku']}: EAN fehlt")
        put(col("recommended_browse_nodes#1.value"), BROWSE)
        for k in range(1, 6):
            put(col(f"bullet_point#{k}.value"), r[f"bullet_{k}"])
        put(col("product_description#1.value"), r["beschreibung_a_plus"])
        put(col("generic_keyword#1.value"), r["suchbegriffe"])
        put(col("number_of_items#1.value"), n)
        put(col("color#1.value"), r["farbe"])
        put_checked(values, col("item_shape#1.value"), r.get("form"), "form", r["sku"], warnings)
        put_checked(values, col("material#1.value"), r.get("material"), "material", r["sku"], warnings)
        for fc in by_norm.get("frame#1.material#1.value", []) + by_norm.get("frame_material#1.value", []):
            put_checked(values, fc, r.get("rahmenmaterial"), "rahmenmaterial", r["sku"], warnings)
        put(col("unit_count#1.value"), f"{n}.0")
        put(col("unit_count#1.type.value") if "unit_count#1.type.value" in by_norm else col("unit_count#1.type#1.value"), "stück")
        put(col("included_components#1.value"), f"{n} Spiegel, Aufhängeset (Aufhänger, Schrauben, Dübel)")
        put_checked(values, col("room_type#1.value"), r.get("raumtyp"), "raumtyp", r["sku"], warnings)
        put_checked(values, col("mounting_type#1.value"), r.get("montageart"), "montageart", r["sku"], warnings)
        put(col("condition_type#1.value"), "Neu")
        put(price_col, r["preis_eur"])
        fba = r.get("fulfillment", "").upper().startswith("FBA")
        put(col("fulfillment_availability#1.fulfillment_channel_code"), "Versand durch Amazon (EU)" if fba else "Versand durch Händler (Standard)")
        if not fba and a.versandvorlage:
            put(col("merchant_shipping_group#1.value"), a.versandvorlage)
        elif not fba:
            put(col("merchant_shipping_group#1.value"), None)
            warnings.append(f"{r['sku']}: Versandvorlage fehlt (--versandvorlage)")
        qty = re.sub(r"\D", "", r.get("bestand", ""))
        put(col("fulfillment_availability#1.quantity"), int(qty) if qty and not fba else None)
        if not fba and not qty:
            warnings.append(f"{r['sku']}: Bestand fehlt")
        put(col("main_product_image_locator#1.media_location"), r.get("bild_haupt") or None)
        for k in range(1, 7):
            put(col(f"other_product_image_locator_{k}#1.media_location"), r.get(f"bild_{k + 1}") or None)
        if not r.get("bild_haupt"):
            warnings.append(f"{r['sku']}: Hauptbild-URL fehlt")
        # Paketmaße und Gewicht der Sets sind nicht bekannt, die Profilwerte gelten für einen einzelnen Spiegel
        for name in ("item_package_dimensions#1.length.value", "item_package_dimensions#1.width.value", "item_package_dimensions#1.height.value"):
            put(col(name), None)
        for name in ("item_package_dimensions#1.length.unit", "item_package_dimensions#1.width.unit", "item_package_dimensions#1.height.unit"):
            put(col(name), None)
        warnings.append(f"{r['sku']}: Paketmaße und Paketgewicht eintragen")
        for c, v in values.items():
            ws.cell(row=row, column=c).value = v

    wb.save(a.out)
    print(f"{len(rows)} Zeilen in {a.out} geschrieben")
    for w in warnings:
        print("OFFEN:", w)


if __name__ == "__main__":
    main()
