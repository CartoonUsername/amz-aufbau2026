# eBay

Alles für eBay liegt in diesem Ordner, getrennt von Amazon, Otto und Shopify.

```
kanaele/ebay/
  README.md
  vorlagen/                         eBay-Uploadvorlage (Seller Hub, Angebote per Datei), hier ablegen
  chargen/
    charge_01_spiegel_sets/
      listing_ebay.csv              Arbeitstabelle der Charge (erzeugt mit scripts/build_channel_batch.py)
      notizen.md                    offene Punkte, Ergebnis nach 14 und 28 Tagen
```

- Nur FBM, GTIN gleich wie bei Amazon, eBay-Titel höchstens 80 Zeichen.
- Offen: Entscheidung zur Werbung (der eBay-Umsatz läuft laut Seller Hub zu ca. 95 % über Anzeigen), Kategorie, Versand- und Rückgaberichtlinie.
- Neue Charge bauen: `python3 scripts/build_channel_batch.py --channel ebay --batch charge_NN_name --listing produkte/<linie>/<datei>_fbm.csv`.
- Uploadvorlage: Im eBay Seller Hub die Vorlage für den Upload per Datei herunterladen (Menüname prüfen) und in `vorlagen/` ablegen.
