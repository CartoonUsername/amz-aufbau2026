# Amazon – Charge 02: Salzlampen-Sets (8 Listings)

- Quelle (FBM-Hauptversion): `produkte/salzlampen/geschenksets_fbm.csv`, Texte in `produkte/salzlampen/texte_geschenksets.md`. Hier liegt `listing_fba.csv` (FBA-Kopie, SKU `FBA_...`, dieselbe GTIN).
- Bestand 100, Versandvorlage "Prime Mustervorlage" (FBM).
- Upload-Dateien: `amazon_upload_FBM.xlsm` und `amazon_upload_FBA.xlsm`, gebaut mit `scripts/fill_amazon_home_lamp.py` aus der Vorlage `kanaele/amazon/vorlagen/home_lamp.xlsm` (Produkttyp LAMP). Profilwerte einer Einzellampe (Farbe, Artikelmaße) wurden bei den Sets entfernt, Material, EPREL-Nummer und Energielabel stammen aus deinem Profil und müssen zum Set passen.
- Neu bauen: `python3 scripts/fill_amazon_home_lamp.py --template kanaele/amazon/vorlagen/home_lamp.xlsm --csv <Tabelle> --out <Datei>`.
- Offen: Stöbern-Kategorie (Browse Node), Farbe, Artikelmaße und -gewicht, Paketmaße und -gewicht je Set, Bild-URLs, FBM/FBA-Entscheidung (FBA frisst bei günstigen Artikeln die Marge, siehe `planung/gewinnanalyse_2026-10-08.md`).
- Ergebnis nach 14 Tagen:
- Ergebnis nach 28 Tagen:
