# EmsCraft24 – Aufbauplan 2026 (ohne Werbung)

Ziel: 5.000 € Umsatz/Tag über alle Kanäle. Das Repo ist nach Zweck getrennt, jeder Ordner hat eine eigene README.

## Aufbau

| Ordner | Inhalt |
|---|---|
| `planung/` | Strategie, Pläne, Szenarien, Analysen (Kernsortiment, 4-Linien-Plan, Ambitionsszenario, Wochenpläne) |
| `produkte/` | Produktdaten je Linie, unabhängig vom Kanal: Spiegel, Salzlampen, Trikotrahmen, Plissee, Auslaufware, Listing-Vorlage |
| `kanaele/` | Je Verkaufskanal getrennt: `amazon/`, `otto/`, `ebay/`, `shopify/` (Vorlagen, Chargen, Uploads, Analysen) |
| `daten/` | Rohdaten und Exporte, getrennt nach Quelle (`amazon/`, `otto/`) |
| `register/` | Stammregister: GTIN-Register, Wertezuordnung für Dropdown-Felder, Feldliste der Amazon-Vorlage |
| `anleitungen/` | Regeln und Anleitungen (keine erfundenen Daten, GTIN-Regeln, Bilder beim Upload) |
| `scripts/` | Werkzeuge: GTIN vergeben, Prüfen, FBA-Kopie, Amazon-Vorlage füllen, Bild-URLs eintragen, Charge bauen |

## Stand 8.10.2026

- Gesamtumsatz ca. 700–900 €/Tag (7-Tage-Werte: Amazon ca. 324 €, Otto ca. 495 €, eBay ca. 76 €), davon liegt ein großer Teil auf auslaufenden Linien (`planung/kernsortiment_2026-10-08.md`).
- Kernsortiment: Wandspiegel, Salzlampen, Trikotrahmen, Plissees; Basis ca. 315 €/Tag (`planung/plan_4_linien.md`).
- Ziele bis 14.12.: Basis ca. 1.070 €/Tag gesamt, Ambition ca. 1.650 €/Tag (`planung/ambitionsszenario.md`); 5.000 €/Tag nur als Spitzentag (Black Friday 27.11., Cyber Monday 30.11.).
- Erste Charge: 10 Spiegel-Sets (`kanaele/amazon/chargen/charge_01_spiegel_sets/`), offen sind Bestand, Versandvorlage, Paketmaße und -gewicht, Bilder.

## Regeln

1. Keine erfundenen Produktdaten (`anleitungen/regeln_keine_erfindungen.md`).
2. FBM zuerst, FBA nur als Kopie mit SKU `FBA_…` und derselben GTIN (`kanaele/amazon/massenupload_workflow.md`).
3. GTINs nur über das Register vergeben, nächste freie Artikelnummer 60200 (`anleitungen/gtin_regeln.md`).
4. Höchstens 20 Listings pro Charge, Prüfung vor dem Upload (`kanaele/amazon/README.md`).

## Schnellstart neue Charge

```
python3 scripts/build_amazon_batch.py --batch charge_NN_name --listing produkte/<linie>/<datei>_fbm.csv --versandvorlage "<Name>"
```

Ergebnis liegt in `kanaele/amazon/chargen/charge_NN_name/`.
