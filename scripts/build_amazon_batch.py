#!/usr/bin/env python3
"""Baut eine komplette Amazon-Charge in einem Schritt (FBM zuerst, FBA als Kopie).

Aufruf:
  python3 scripts/build_amazon_batch.py --batch charge_01_spiegel_sets \
      --listing data/spiegel_sets_texte_charge1.csv --versandvorlage "Schneller Versand" \
      [--base-url https://cdn.shopify.com/.../files --images-dir /pfad/bilder]

Schritte:
  1. GTINs vergeben (ean_tools assign, nur für Zeilen ohne gültige GTIN, Register wird fortgeschrieben)
  2. optional Bild-URLs eintragen (fill_image_urls)
  3. Prüfung der FBM-Tabelle (validate_listings --nur-neu)
  4. FBA-Kopie erzeugen (make_fba_copies, SKU-Präfix FBA_, gleiche GTIN)
  5. Amazon-Vorlage befüllen: upload/amazon/<batch>/amazon_upload_FBM.xlsm und amazon_upload_FBA.xlsm

Hochladen: zuerst die FBM-Datei, nach Annahme (Uploadstatus) die FBA-Datei.
"""
import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def run(*args, check=True):
    cmd = [sys.executable, "-I", *args]
    print("\n$", " ".join(os.path.relpath(c, ROOT) if os.path.exists(c) else c for c in cmd[2:]))
    res = subprocess.run(cmd, cwd=ROOT)
    if check and res.returncode:
        sys.exit(res.returncode)
    return res.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    ap.add_argument("--listing", required=True, help="FBM-Hauptversion der Listing-Tabelle")
    ap.add_argument("--template", default="templates/amazon/home_mirror.xlsm")
    ap.add_argument("--versandvorlage")
    ap.add_argument("--base-url")
    ap.add_argument("--images-dir")
    a = ap.parse_args()

    out_dir = os.path.join("upload", "amazon", a.batch)
    os.makedirs(os.path.join(ROOT, out_dir), exist_ok=True)

    run("scripts/ean_tools.py", "assign", "--listing", a.listing)
    listing = a.listing
    if a.base_url:
        listing_img = listing.replace(".csv", "_mit_bildern.csv")
        cmd = ["scripts/fill_image_urls.py", "--csv", listing, "--base-url", a.base_url, "--out", listing_img]
        if a.images_dir:
            cmd += ["--images-dir", a.images_dir]
        run(*cmd)
        listing = listing_img
    bad = run("scripts/validate_listings.py", "--nur-neu", listing, check=False)
    fba_csv = listing.replace(".csv", "_fba.csv")
    run("scripts/make_fba_copies.py", "--in", listing, "--out", fba_csv)
    for name, csv_path in (("FBM", listing), ("FBA", fba_csv)):
        cmd = ["scripts/fill_amazon_home_mirror.py", "--template", a.template, "--csv", csv_path,
               "--out", os.path.join(out_dir, f"amazon_upload_{name}.xlsm")]
        if a.versandvorlage:
            cmd += ["--versandvorlage", a.versandvorlage]
        run(*cmd)
    print("\nFertig:", out_dir)
    if bad:
        print("ACHTUNG: Die Prüfung der FBM-Tabelle meldet Fehler, die Dateien sind ein ENTWURF und noch nicht hochladefertig.")


if __name__ == "__main__":
    main()
