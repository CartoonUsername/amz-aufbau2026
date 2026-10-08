# Amazon-Upload in Maßen

Ordner für Uploads in kleinen, geprüften Chargen. Ziel: wenige, saubere Listings statt Masse, die erst nach der Prüfung wächst.

## Struktur

```
templates/amazon/                 Amazon-Vorlagen je Kategorie (.xlsm), aus Seller Central geladen
upload/amazon/charge_NN_name/
  listings.csv                    Listing-Tabelle der Charge (Format data/listing_vorlage.csv), max. 20 Zeilen
  bilder/                         Bilddateien (nur zur Ablage, hochgeladen wird über Shopify-URLs)
  amazon_upload.xlsm              ausgefüllte Amazon-Vorlage
  pruefung.txt                    Ausgabe von scripts/validate_listings.py
  notizen.md                      Besonderheiten, Fehler von Amazon, Ergebnis nach 14 und 28 Tagen
```

## Regeln für Chargen

1. Maximal 20 Zeilen pro Charge und zu Beginn höchstens eine Charge pro Woche.
2. Vor jedem Upload: `python3 scripts/validate_listings.py upload/amazon/charge_NN_name/listings.csv` muss ohne Fehler laufen (keine Platzhalter, Titel bis 150 Zeichen, Bullets bis 500, Suchbegriffe bis 249 Bytes, https-Bilder).
3. Jede SKU und EAN darf nur einmal vorkommen, keine Dopplungen vorhandener Produkte.
4. Nur eigene Bilder und eigene Marke (EmsCraft24), keine fremden Markennamen im Text.
5. Nach 14 und 28 Tagen Auswertung: Sessions pro Tag, Conversion, Umsatz, Retouren, danach Go/No-Go für die nächste Charge (`docs/listing_fabrik.md`).
6. Preise ohne erfundenen UVP, siehe `docs/texte_salzlampen_geschenksets.md`, Abschnitt 7.

## Offene Chargen

| Charge | Inhalt | Texte | Status |
|---|---|---|---|
| 01 | 10 Spiegel-Sets (2er/3er) | `data/spiegel_sets_texte_charge1.csv` | EANs, Bestand, Bilder offen |
| 02 | 8 Salzlampen-Sets | `data/salzlampen_geschenksets_texte.csv` | EANs, Bestand, Bilder, Mini-Fehler offen |
| 03 | 5 Trikotrahmen (Update) | `data/trikotrahmen_texte.csv` | Angaben zu Bügel und Maßen offen |

Bild-URLs eintragen: `scripts/fill_image_urls.py` (siehe `docs/bilder_im_upload.md`).
