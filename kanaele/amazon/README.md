# Amazon

Alles für Amazon.de liegt in diesem Ordner, getrennt von Otto, eBay und Shopify.

## Struktur

```
kanaele/amazon/
  README.md                         diese Datei (Regeln für Chargen)
  vorlage_und_upload.md             Vorlage, Felder, Kategorien, GTINs, Uploadablauf
  massenupload_workflow.md          FBM zuerst, FBA als Kopie, ein Befehl pro Charge
  listing_status_2026-10-08.md      Zustand der bestehenden Listings
  vorlagen/                         Amazon-Vorlagen je Produkttyp (.xlsm), aus Seller Central geladen
    home_mirror.xlsm                Heim-Spiegel
  chargen/
    charge_NN_name/
      listing_fba.csv               erzeugte FBA-Kopie (SKU FBA_…, gleiche GTIN)
      amazon_upload_FBM.xlsm        ausgefüllte Vorlage, Hauptversion (Eigenversand)
      amazon_upload_FBA.xlsm        FBA-Kopie, erst nach der FBM-Datei hochladen
      notizen.md                    Besonderheiten, Fehler von Amazon, Ergebnis nach 14 und 28 Tagen
```

Die Hauptversion der Listing-Tabelle (FBM) liegt bei der Produktlinie, z. B. `produkte/spiegel/sets_charge1_fbm.csv`.

## Regeln für Chargen

1. Maximal 20 Zeilen pro Charge und zu Beginn höchstens eine Charge pro Woche.
2. Vor jedem Upload muss `python3 scripts/validate_listings.py --nur-neu <FBM-Tabelle>` ohne Fehler laufen (keine Platzhalter, Titel bis 150 Zeichen, Bullets bis 500, Suchbegriffe bis 249 Bytes, https-Bilder).
3. Jede SKU und GTIN nur einmal, nur neue Listings (neue Produkte wie Sets oder Zubehör). Dieselbe Ware bekommt bei Amazon keine zweite Produktseite, mehrere Kategorien laufen über die Stöbern-Kategorien einer Seite.
4. Nur eigene Bilder und eigene Marke (EmsCraft24), keine fremden Markennamen im Text.
5. Nach 14 und 28 Tagen Auswertung (Sessions, Conversion, Umsatz, Retouren), danach Go/No-Go für die nächste Charge (`../../planung/listing_fabrik.md`).
6. Keine erfundenen Preise oder UVPs, keine erfundenen Produktdaten (`../../anleitungen/regeln_keine_erfindungen.md`).

## Chargen

| Charge | Inhalt | Tabelle | Status |
|---|---|---|---|
| 01 | 10 Spiegel-Sets (2er/3er, 5 Farben) | `../../produkte/spiegel/sets_charge1_fbm.csv` | GTINs, Material, Kategorien gefüllt; offen: Bestand, Versandvorlage, Paketmaße und -gewicht, Bilder |
| 02 | 8 Salzlampen-Sets | `../../produkte/salzlampen/geschenksets_fbm.csv` | Amazon-Vorlage Tischlampe fehlt, Mini-Lampen-Fehler beheben |
| – | Trikotrahmen: nur Updates der 5 bestehenden ASINs, kein neues Listing | `../../produkte/trikotrahmen/texte.csv` | Angaben zu Bügel und Maßen offen |
- `chargen/charge_02_salzlampen_sets/`: Entwurf (FBA-Kopie), Upload-Datei fehlt bis zur Tischlampen-Vorlage.
