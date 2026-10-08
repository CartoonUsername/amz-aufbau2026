# EmsCraft24 – Plan pro ASIN (v2, mit Business-Report-Daten)

Ersetzt die erste Fassung. Basis: `data/business_report_asin_2026-10-08.csv` (Sessions, Conversion, Buy Box je ASIN, ca. 30 Tage), `data/kennzahlenmonitor_verkaeufe_2026-10-08.csv`, Lagerbestandsbericht. Ziel je ASIN in `data/plan_pro_asin.csv`. Keine Werbung, keine Einkaufspreise.

## Rechenmodell

Umsatz/Tag = Sessions/Tag × Conversion × realisierter Preis; Sessions wachsen nur organisch (Suchbegriffe, Variationen, FBA/Prime, Reviews), Conversion bleibt auf heutigem Niveau (Stufe D: 4 % angesetzt).

- Heute: 5.832 Sessions in 30 Tagen (ca. 194/Tag), 7,3 % Conversion, ca. 24 € Umsatz pro Einheit.
- Ziel 5.000 €/Tag: bei diesen Werten ca. 2.900 Sessions/Tag (15× heute).
- Die 33 ASINs der Stufen A–D liefern heute ca. 324 €/Tag (von insgesamt ca. 339 €/Tag); alle anderen ca. 90 Listings zusammen nur ca. 15 €/Tag.

## Korrektur zur ersten Fassung (Preise)

Der Business Report zeigt realisierte Preise von nur 24,67 € (Spiegel Weiß), 24,62 € (Spiegel Schwarz) und 16,81 € (Salzlampe 1–2 kg), die Listenpreise (29,99 € / 19,90 €) liegen darüber, also wurde im Zeitraum offenbar auch billiger verkauft. Meine frühere Empfehlung „einen Preis 29,99 €“ nehme ich zurück: Zuerst im Preisverlauf prüfen (Seller Central → Preisgestaltung → Preisverlauf bzw. „Preisänderungen“), dann einen einheitlichen Preis je ASIN festlegen, ohne ihn ohne Test zu erhöhen.

## Stufen

| Stufe | ASINs | Heute Sessions/Tag | Conversion | Hebel |
|---|---|---|---|---|
| A | 7: Spiegel Weiß/Schwarz, Rahmen 59×84 / 21×29 / 42×59 / 50×70, Salzlampe 1–2 kg | 90 | 6,5–33 % | Sessions ×2 → ×3,5 → ×6 |
| B | 11: weitere Spiegelfarben, Kinderspiegel, kleine Rahmen, Salzlampen 2–5 kg | 31 | 4–29 % | Sessions ×1,5 → ×2,5 → ×4 |
| C | 10: 5 Rollroste, 3 Cityroller, Katzenbaum, TrikotFrame | 26 | 1,4–11 % | Sessions ×2 → ×4 → ×7, Buy Box der Rollroste auf ≥ 95 % |
| D | 4: Salzlampen 4–6 kg, 6–9 kg, Helios, Luna | 11 | 0–3 % | Listing/Preis reparieren, Ziel 4 % Conversion |

## Ergebnis (Umsatz/Tag, Stufen A–D)

| Zeitpunkt | Einheiten/Tag | A | B | C | D | Summe |
|---|---|---|---|---|---|---|
| Heute | 14,0 | 177 € | 62 € | 81 € | 4 € | ca. 324 € |
| Woche 8 | 26,3 | 354 € | 93 € | 164 € | 25 € | ca. 636 € |
| Monat 4 | 46,0 | 620 € | 155 € | 327 € | 34 € | ca. 1.135 € |
| Monat 8 | 78,0 | 1.063 € | 248 € | 572 € | 50 € | ca. 1.933 € |

Das ist niedriger als in v1 (ca. 2.460 € in Monat 8), weil die Zahlen jetzt an den echten Sessions und Conversions hängen und die Stufe-C-Artikel mit 1–9 % Conversion weniger bringen als angenommen. Sessions der 33 ASINs: heute 164/Tag, Ziel Monat 8: ca. 905/Tag.

## Die Lücke zu 5.000 €/Tag

Nach Monat 8 fehlen ca. 3.070 €/Tag, die aus neuen Listings und den bisher nicht verkaufenden ASINs kommen müssen.

| Szenario für die Lücke | Bedarf |
|---|---|
| Neue Hochpreis-Listings (ca. 70 €, 1 Einheit/Tag) | ca. 44 Listings |
| Mittelpreis-Listings (ca. 30 €, 1 Einheit/Tag) | ca. 100 Listings |
| Rahmen-/Spiegel-Variationen (ca. 15–25 €, 0,5 Einheiten/Tag) | ca. 250 Listings (unrealistisch) |

Realistisch ist eine Mischung aus ca. 25 Hochpreis-Listings und ca. 40 Mittelpreis-Listings, die jeweils nach dem Muster der Bilderrahmen (hohe Conversion) und Spiegel (viel Traffic) gebaut werden (siehe `docs/listing_fabrik.md`).

## Wichtigste Befunde je Gruppe

- **Bilderrahmen:** Conversion 12–33 % bei nur 1–9 Sessions/Tag je ASIN, hier ist Sichtbarkeit der Hebel (Titel, Suchbegriffe, Variationsfamilie, FBA/Prime).
- **Spiegel:** 2.289 Sessions und 6,2 % Conversion, Spiegel Weiß ist mit 32 Sessions/Tag der traffic-stärkste ASIN, jede Variation und jeder Review wirkt hier am stärksten.
- **Salzlampen:** Conversion 4,8 %, die vier Varianten der Stufe D haben 0–3 % trotz Sessions und brauchen neue Bilder, Titel und Preisprüfung.
- **Rollroste:** Buy Box nur 70 % (90×200), 76 % (160×200), 89 % (100×200), die Preise gegen Konkurrenzangebote prüfen und das Listing mit einheitlicher Familie neu aufsetzen.
- **Katzenbäume (130 €):** 4,6 Sessions/Tag bei 1,4 % Conversion, Listing-Texte und Bilder überarbeiten oder auslisten.
- **Akustikpaneele/Lamellenwände (22 ASINs):** 96 Sessions und 0 Verkäufe in 30 Tagen, praktisch unsichtbar; zu einer Variationsfamilie mit Haupt-ASIN bündeln, sonst ruhen lassen.
- **Buy Box der Bestseller:** 94–100 %, deshalb ist die Buy Box nicht Ursache des Einbruchs am 1.–4.10.

## Bestand und Nachschub (Zielwerte Monat 4)

| ASIN | Einheiten/Tag Monat 4 | Bestand FBM-Bericht | Reichweite |
|---|---|---|---|
| Spiegel Weiß | 7,2 | 87 (+13 FBA) | ca. 14 Tage |
| Spiegel Schwarz | 4,0 | 82 (+33 FBA) | ca. 29 Tage |
| Salzlampe 1–2 kg | 5,5 | 90 (+5 FBA) | ca. 17 Tage |
| Rahmen 21×29 | 5,5 | 51 | ca. 9 Tage |
| Rahmen 59×84 | 4,6 | 60 | ca. 13 Tage |
| Rahmen 42×59 | 3,2 | 72 | ca. 23 Tage |
| Rahmen 50×70 | 2,7 | 77 | ca. 29 Tage |

Die Stufe-A-ASINs müssen also schon vor Woche 8 nachbestellt werden, mindestens 3–4 Wochen Vorlauf einplanen.

## Wochenplan

| Woche | Aufgaben |
|---|---|
| 1 | Preisverlauf der Top-10 prüfen, Doppel-SKUs bereinigen, Rollrost-Warnung und Buy Box prüfen, Nachbestellung Stufe A anstoßen |
| 2 | FBA-Sendung 1: Spiegel Weiß/Schwarz, Rahmen 21×29/59×84/42×59/50×70, Salzlampe 1–2 kg |
| 3–4 | Titel, Suchbegriffe, Bilder, A+ für Stufe A; Stufe D neu texten und bebildern; Stufe-C-Rollroste als Familie neu aufsetzen |
| 5–6 | Variationsfamilien Spiegel, Rahmen, Salzlampen; Vine für Stufe A; erste Charge neuer Listings (10) |
| 7–8 | Zweite Charge (15), Auswertung gegen die Woche-8-Werte, Sessions-Ziel je ASIN prüfen |

## Prüfwerte nach Woche 8

- Stufe A: ≥ 90 Sessions/Tag insgesamt (heute 90 → Ziel 180) und Conversion nicht unter dem heutigen Wert.
- Stufe C: Buy Box der Rollroste ≥ 95 %.
- Stufe D: Conversion ≥ 4 %, sonst Listing auslisten oder neu bauen.
- Neue Listings: mindestens 0,5 Einheiten/Tag nach 28 Tagen.
