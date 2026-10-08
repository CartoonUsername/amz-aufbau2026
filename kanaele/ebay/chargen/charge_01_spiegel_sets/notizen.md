# eBay – Charge 01: Spiegel-Sets (10 Listings)

- Arbeitstabelle: `listing_ebay.csv` (erzeugt mit `scripts/build_channel_batch.py --channel ebay`, Quelle `produkte/spiegel/sets_charge1_fbm.csv`).
- Hauptversion FBM, kein FBA bei eBay. Die GTINs sind dieselben wie bei Amazon (Register `register/gtin_register.csv`).
- Titel höchstens 80 Zeichen, die erzeugten Titel sind 65–80 Zeichen lang, bei Änderungen die Grenze prüfen.
- Preise 49,99 € und 74,99 € sind Vorschläge (Summe der Einzelpreise), kein UVP.
- Hinweis: eBay bietet keine Uploadvorlage an, vorerst manuelle Anlage, Reihenfolge: erst Amazon.
- Offen: eBay-Kategorie, Versandrichtlinie, Rückgabebedingungen, Menge, Bild-URLs (mindestens 500 px), Entscheidung zur eBay-Werbung (bisher laufen ca. 95 % der eBay-Verkäufe über Anzeigen).
- Ergebnis nach 14 Tagen:
- Ergebnis nach 28 Tagen:
