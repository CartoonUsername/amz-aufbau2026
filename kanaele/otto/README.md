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
- Stand 8.10.2026: Otto bietet keine Importvorlage zum Herunterladen an. Priorität hat Amazon, `listing_otto.csv` dient bis dahin als geordnete Eingabehilfe für die manuelle Anlage in Partner Connect. Sobald Otto einen Importweg (Datei oder Schnittstelle) anbietet, kommt die Vorlage in `vorlagen/`.
