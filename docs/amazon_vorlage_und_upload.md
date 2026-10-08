# Amazon-Vorlage für den Upload in Maßen

Ja, die Amazon-Vorlage brauche ich, und zwar je Produktgruppe eine.

## Welche Vorlagen

| Gruppe | Kategorie in Amazon (Suche im Vorlagen-Dialog) |
|---|---|
| Spiegel-Sets | Wandspiegel / Spiegel |
| Salzlampen-Sets | Tischlampen / Beleuchtung |
| Trikotrahmen | Bilderrahmen |

## So lädst du sie

1. Seller Central → Produkte → Produkte hinzufügen (oder Katalog → Produkte hinzufügen) → Produkte per Upload hinzufügen.
2. Die Vorlage der Kategorie herunterladen, die Menüs heißen je nach Ansicht leicht unterschiedlich.
3. Die Datei (`.xlsm`) unverändert in `templates/amazon/` legen, zum Beispiel `wandspiegel.xlsm`, `tischlampe.xlsm`, `bilderrahmen.xlsm`.

## Was ich damit mache

- Ich lese die Spaltenüberschriften und Pflichtfelder der Vorlage und ordne sie den Spalten der Listing-Tabelle zu (Mapping in `docs/bilder_im_upload.md`).
- Ich fülle die Vorlage mit Titel, Bullets, Beschreibung, Suchbegriffen, Preis, Bestand, EAN und Bild-URLs und lasse sie von `scripts/validate_listings.py` prüfen.
- Die Datei lädst du selbst in Seller Central hoch, ich lade nichts bei Amazon hoch.

## Ordner

Die Struktur und die Chargenregeln stehen in `upload/amazon/README.md`: höchstens 20 Listings pro Charge, vorher Prüfung ohne Fehler, nach 14 und 28 Tagen Auswertung.

## Stand der Prüfung heute

Das Prüfskript meldet bei allen drei Chargen Platzhalter (EAN, Bestand, Bügel-Angaben bei den Trikotrahmen) und fehlende Bilder, die Texte selbst sind innerhalb der Längengrenzen.

## Nur neue Listings (8.10.2026)

- Die Chargen im Upload-Ordner enthalten nur neue Listings mit neuer SKU, neuer EAN und neuer Produktseite.
- Neu sind: Spiegel-Sets (2er/3er), Salzlampen-Sets, später Zubehör oder neue Bündel, denn ein Set ist ein anderes Produkt als der Einzelartikel.
- Nicht neu sind die Trikotrahmen auf Amazon: Es gibt die 5 Farben schon als ASINs, ein zweites Listing desselben Rahmens würde als doppelte Produktseite gelten, deshalb sind die Texte in `data/trikotrahmen_texte.csv` Updates der bestehenden Seiten (Amazon) und neue Listings nur bei eBay.
- Für neue Trikot-Listings auf Amazon braucht es ein anderes Produkt, zum Beispiel ein 2er-Set oder ein Set mit zwei Farben.
- `python3 scripts/validate_listings.py --nur-neu <datei>` meldet Amazon-Zeilen, die kein neues Listing sind.
