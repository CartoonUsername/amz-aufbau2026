#!/usr/bin/env python3
"""Baut aus der FBM-Hauptversion eine Arbeitstabelle für Otto oder eBay.

Aufruf:
  python3 scripts/build_channel_batch.py --channel otto --batch charge_01_spiegel_sets --listing produkte/spiegel/sets_charge1_fbm.csv
  python3 scripts/build_channel_batch.py --channel ebay --batch charge_01_spiegel_sets --listing produkte/spiegel/sets_charge1_fbm.csv

Ergebnis: kanaele/<kanal>/chargen/<charge>/listing_<kanal>.csv (nur Angaben aus der Hauptversion und aus den
bestehenden Otto-Listings, nichts erfunden; fehlende Angaben bleiben leer und werden als OFFEN gemeldet).
Otto und eBay haben kein FBA, es wird nur die FBM-Hauptversion verwendet, die GTIN ist dieselbe wie bei Amazon.
"""
import argparse
import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# aus den bestehenden Otto-Spiegel-SKUs (daten/otto/produkte_status_2026-10-08.csv)
OTTO_PROVISIONSBEREICH = "Einrichten & Wohnen"
OTTO_PROVISIONSGRUPPE = "Möbel"
OTTO_VERSANDPROFIL = "Schneller Versand"

EBAY_MAX_TITLE = 80


def ist_spiegel(r):
    return r.get("produkttyp", "").strip().lower() == "wandspiegel"


def n_of(sku):
    m = re.match(r"S0?(\d)", sku.upper().removeprefix("FBA_"))
    return int(m.group(1)) if m else None


def ebay_title(r, n):
    if not ist_spiegel(r):
        # andere Linien: Titelteil vor dem ersten " | " aus der Hauptversion, nichts hinzugefügt
        t = r["titel"].split(" | ")[0].strip()
        return t if len(t) <= EBAY_MAX_TITLE else ""
    farbe = r["farbe"]
    kandidaten = [
        f"EmsCraft24 Wandspiegel {n}er Set 60x40 cm {farbe} Kunststoffspiegel MDF-Rahmen",
        f"Wandspiegel {n}er Set 60x40 cm {farbe} Kunststoffspiegel MDF-Rahmen Hoch Quer",
        f"Wandspiegel {n}er Set 60x40 cm {farbe} Kunststoffspiegel MDF-Rahmen",
        f"Wandspiegel {n}er Set 60x40 cm {farbe} Kunststoff MDF",
    ]
    for t in kandidaten:
        if len(t) <= EBAY_MAX_TITLE:
            return t
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--channel", choices=["otto", "ebay"], required=True)
    ap.add_argument("--batch", required=True)
    ap.add_argument("--listing", required=True)
    ap.add_argument("--provisionsgruppe", default=OTTO_PROVISIONSGRUPPE, help="Otto, z. B. \"Lampen & Leuchten\" (aus bestehenden Otto-Lampen-SKUs)")
    a = ap.parse_args()

    with open(os.path.join(ROOT, a.listing), encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    out_dir = os.path.join(ROOT, "kanaele", a.channel, "chargen", a.batch)
    os.makedirs(out_dir, exist_ok=True)

    common = ["sku", "gtin", "titel", "marke"]
    if a.channel == "otto":
        cols = common + ["provisionsbereich", "provisionsgruppe", "versandprofil", "preis_eur", "bestand", "farbe", "masse",
                         "anzahl", "form", "material", "rahmenmaterial", "montageart", "raumtyp",
                         "bullet_1", "bullet_2", "bullet_3", "bullet_4", "bullet_5", "beschreibung",
                         "bild_1", "bild_2", "bild_3", "bild_4", "bild_5", "bild_6", "bild_7", "status"]
    else:
        cols = common + ["kategorie", "zustand", "preis_eur", "menge", "versandrichtlinie", "rueckgabe", "farbe", "masse",
                         "anzahl", "form", "material", "rahmenmaterial", "montageart",
                         "beschreibung", "bild_1", "bild_2", "bild_3", "bild_4", "bild_5", "bild_6", "bild_7", "status"]

    out, offen = [], []
    for r in rows:
        n = n_of(r["sku"])
        o = {c: "" for c in cols}
        o.update({
            "sku": r["sku"], "gtin": r["gtin_ean"], "marke": "EmsCraft24", "preis_eur": r["preis_eur"],
            "farbe": r["farbe"], "masse": "60 x 40 cm" if ist_spiegel(r) else r.get("groesse", ""),
            "anzahl": str(n) if n and ist_spiegel(r) else "", "form": r.get("form", ""),
            "material": r.get("material", ""), "rahmenmaterial": r.get("rahmenmaterial", ""),
            "montageart": r.get("montageart", ""), "status": "Entwurf",
        })
        bilder = [r.get(c, "") for c in ("bild_haupt", "bild_2", "bild_3", "bild_4", "bild_5", "bild_6", "bild_7")]
        for k, b in enumerate(bilder, start=1):
            o[f"bild_{k}"] = b
        desc = r["beschreibung_a_plus"]
        if a.channel == "otto":
            o.update({
                "titel": (f"EmsCraft24 Wandspiegel {n}er Set 60x40 cm {r['farbe']} Hoch- und Querformat Kunststoffspiegel"
                          if ist_spiegel(r) else r["titel"].replace(" | ", " – ")),
                "provisionsbereich": OTTO_PROVISIONSBEREICH, "provisionsgruppe": a.provisionsgruppe,
                "versandprofil": OTTO_VERSANDPROFIL, "raumtyp": r.get("raumtyp", ""), "beschreibung": desc,
            })
            for k in range(1, 6):
                o[f"bullet_{k}"] = r[f"bullet_{k}"]
        else:
            t = ebay_title(r, n)
            o.update({"titel": t, "zustand": "Neu", "beschreibung": desc})
            if not t:
                offen.append(f"{r['sku']}: eBay-Titel passt nicht in {EBAY_MAX_TITLE} Zeichen")
            offen.append(f"{r['sku']}: Kategorie, Versandrichtlinie und Rückgabe festlegen")
        # nicht bekannte Angaben melden
        if not r["gtin_ean"]:
            offen.append(f"{r['sku']}: GTIN fehlt")
        if not o["bild_1"]:
            offen.append(f"{r['sku']}: Hauptbild-URL fehlt")
        o["menge" if a.channel == "ebay" else "bestand"] = "100"  # Standardbestand immer 100
        out.append(o)

    path = os.path.join(out_dir, f"listing_{a.channel}.csv")
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(out)
    print(f"{len(out)} Zeilen in {os.path.relpath(path, ROOT)}")
    if a.channel == "ebay":
        print("Längster eBay-Titel:", max(len(o["titel"]) for o in out), "Zeichen (Grenze 80)")
    for x in sorted(set(offen)):
        print("OFFEN:", x)


if __name__ == "__main__":
    main()
