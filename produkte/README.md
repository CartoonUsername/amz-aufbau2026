# Produkte

Eine Produktlinie pro Ordner, unabhängig vom Verkaufskanal. Hier liegen die Produktdaten und die Texte, die Kanäle bedienen sich daraus.

| Ordner | Inhalt |
|---|---|
| `spiegel/` | Fakten des Spiegels, Set-Tabelle `sets_charge1_fbm.csv`, Texte, Sets und Zubehör |
| `salzlampen/` | Set-Tabelle `geschenksets_fbm.csv`, Texte |
| `trikotrahmen/` | Texte und Tabelle (Amazon-Updates, eBay neu) |
| `plissee/` | Entwürfe, Lieferant, Marge, Vorgaben |
| `auslaufware/` | Auslaufende Linien (Akustikpaneele, Lamellenwände), kein Aufbau |
| `_vorlage/` | `listing_vorlage.csv`, Spaltenvorlage für neue Listings |

## Regeln

- Tabellen mit Endung `_fbm.csv` sind die Hauptversion (FBM), die FBA-Kopie wird im Kanalordner erzeugt (`kanaele/amazon/chargen/…/listing_fba.csv`).
- Nur belegte Produktdaten, keine Annahmen (`anleitungen/regeln_keine_erfindungen.md`).
