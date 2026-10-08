# Otto

Alles für Otto liegt in diesem Ordner, getrennt von Amazon, eBay und Shopify.

```
kanaele/otto/
  README.md
  analyse_2026-10-08.md             Analyse der Otto-Exporte
  vorlagen/                         Otto-Importvorlage(n) aus Partner Connect (Excel/CSV), hier ablegen
  chargen/
    charge_01_spiegel_sets/
      listing_otto.csv              Arbeitstabelle der Charge (erzeugt mit scripts/build_channel_batch.py)
      notizen.md                    offene Punkte, Ergebnis nach 14 und 28 Tagen
```

- Rohdaten: `../../daten/otto/` (Produktstatus, Performance).
- Nur FBM (Otto hat kein FBA), GTIN gleich wie bei Amazon.
- Offene Punkte im Konto: 58 nicht verkaufsfähige SKUs, doppelte GTIN 4255822600242, Merkmal „Maße“ statt „Farbe“ bei den Salzlampen, 9 von 17 Trikot-SKUs nicht verkaufsfähig.
- Neue Charge bauen: `python3 scripts/build_channel_batch.py --channel otto --batch charge_NN_name --listing produkte/<linie>/<datei>_fbm.csv`.
- Importvorlage: In Otto Partner Connect unter Produkte die Excel- oder CSV-Vorlage für den Produktimport herunterladen (Menüname prüfen) und in `vorlagen/` ablegen, danach übertrage ich `listing_otto.csv` wie bei Amazon in die Vorlage.
