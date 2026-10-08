# EmsCraft24 – Plan pro ASIN (v3, ohne Bilderrahmen)

Ersetzt v2. Bilderrahmen und TrikotFrame sind nicht Teil des Plans (laufen unverändert weiter, werden aber nicht gezählt oder gefördert). Basis: `data/business_report_asin_2026-10-08.csv` (Sessions, Conversion, Buy Box je ASIN, ca. 30 Tage), `data/kennzahlenmonitor_verkaeufe_2026-10-08.csv`, Lagerbestandsbericht. Ziele je ASIN in `data/plan_pro_asin.csv`. Keine Werbung, keine Einkaufspreise.

## Rechenmodell

Umsatz/Tag = Sessions/Tag × Conversion × realisierter Preis; Sessions wachsen nur organisch (Suchbegriffe, Variationen, FBA/Prime, Reviews), Conversion bleibt auf heutigem Niveau (Stufe D: 4 % angesetzt).

- Heute: gesamt ca. 194 Sessions/Tag, 7,3 % Conversion, ca. 24 € Umsatz pro Einheit.
- Ziel 5.000 €/Tag: bei diesen Werten ca. 2.900 Sessions/Tag (15× heute).
- Die 23 ASINs der Stufen A–D (Spiegel, Salzlampen, Rollroste, Cityroller, Katzenbaum) liefern heute ca. 239 €/Tag.

## Preise (Hinweis)

Realisierte Preise liegen unter den Listenpreisen (Spiegel Weiß 24,67 € gegenüber 29,99 € Listenpreis, Salzlampe 1–2 kg 16,81 € gegenüber 19,90 €), deshalb zuerst den Preisverlauf in Seller Central prüfen und danach einen einheitlichen Preis je ASIN festlegen, ohne ihn ohne Test zu erhöhen.

## Stufen

| Stufe | ASINs | Heute Sessions/Tag | Conversion | Hebel |
|---|---|---|---|---|
| A | 3: Spiegel Weiß, Spiegel Schwarz, Salzlampe 1–2 kg | 70 | 6,5–7,8 % | Sessions ×2 → ×3,5 → ×6 |
| B | 7: Spiegel Eiche Catania/Eiche Natur, Kinderspiegel ×2, Salzlampen 2–3/3–5/5–7 kg | 31 | 4–12 % | Sessions ×1,5 → ×2,5 → ×4 |
| C | 9: 5 Rollroste, 3 Cityroller, Katzenbaum | 25 | 1,4–11 % | Sessions ×2 → ×4 → ×7, Buy Box der Rollroste auf ≥ 95 % |
| D | 4: Salzlampen 4–6 kg, 6–9 kg, Helios, Luna | 11 | 0–3 % | Listing/Preis reparieren, Ziel 4 % Conversion |

## Ergebnis (Umsatz/Tag)

| Zeitpunkt | Einheiten/Tag | A | B | C | D | Summe |
|---|---|---|---|---|---|---|
| Heute | 8,1 | 105 € | 50 € | 80 € | 4 € | ca. 239 € |
| Woche 8 | 15,6 | 211 € | 75 € | 160 € | 25 € | ca. 471 € |
| Monat 4 | 27,4 | 368 € | 125 € | 319 € | 34 € | ca. 846 € |
| Monat 8 | 46,4 | 632 € | 200 € | 558 € | 50 € | ca. 1.440 € |

Sessions dieser 23 ASINs: heute 137/Tag, Ziel Monat 8: ca. 752/Tag.

## Die Lücke zu 5.000 €/Tag

Nach Monat 8 fehlen ca. 3.560 €/Tag, davon sollen ca. 320 €/Tag aus Spiegel-Sets und Zubehör kommen (`docs/sets_zubehoer_spiegel.md`, Annahme), der Rest von ca. 3.240 €/Tag aus anderen neuen Listings.

| Szenario für die Lücke | Bedarf |
|---|---|
| Nur Hochpreis-Listings (ca. 70 €, 1 Einheit/Tag) | ca. 51 Listings |
| Nur Mittelpreis-Listings (ca. 30 €, 1 Einheit/Tag) | ca. 119 Listings |
| Mischung | ca. 30 Hochpreis + ca. 50 Mittelpreis |

Ohne die Rahmen (hohe Conversion, aber wenig Umsatz pro Stück) ist das 5.000-€-Ziel allein über Spiegel, Salzlampen und neue Listings eher ein Ziel für 12+ Monate als für 8.

## Wichtigste Befunde je Gruppe

- **Spiegel:** 2.289 Sessions und 6,2 % Conversion, Spiegel Weiß ist mit 32 Sessions/Tag der traffic-stärkste ASIN, jede Variation und jeder Review wirkt hier am stärksten.
- **Salzlampen:** Conversion 4,8 %, die vier Varianten der Stufe D haben 0–3 % trotz Sessions und brauchen neue Bilder, Titel und Preisprüfung.
- **Rollroste:** Buy Box nur 70 % (90×200), 76 % (160×200), 89 % (100×200), die Preise gegen Konkurrenzangebote prüfen und die Listings als Familie neu aufsetzen.
- **Katzenbäume (130 €):** 4,6 Sessions/Tag bei 1,4 % Conversion, Listing-Texte und Bilder überarbeiten oder auslisten.
- **Akustikpaneele/Lamellenwände (22 ASINs):** 96 Sessions und 0 Verkäufe in 30 Tagen, zu einer Variationsfamilie bündeln, sonst ruhen lassen.
- **Buy Box der Bestseller:** 94–100 %, deshalb ist die Buy Box nicht Ursache des Einbruchs am 1.–4.10.

## Bestand und Nachschub (Ziele Monat 4)

| ASIN | Einheiten/Tag Monat 4 | Bestand FBM-Bericht | Reichweite |
|---|---|---|---|
| Spiegel Weiß | 7,2 | 87 (+13 FBA) | ca. 14 Tage |
| Spiegel Schwarz | 4,0 | 82 (+33 FBA) | ca. 29 Tage |
| Salzlampe 1–2 kg | 5,5 | 90 (+5 FBA) | ca. 17 Tage |

Spiegel Weiß und Salzlampe 1–2 kg müssen also vor Woche 8 nachbestellt werden, 3–4 Wochen Vorlauf einplanen.

## Wochenplan

| Woche | Aufgaben |
|---|---|
| 1 | Preisverlauf der Spiegel/Salzlampen prüfen, FBA/FBM-Doppel-SKUs prüfen (FBM bleibt als Rückfall, Preis gleich oder höher als FBA), Rollrost-Warnung und Buy Box prüfen, Nachbestellung Spiegel Weiß und Salzlampe 1–2 kg anstoßen |
| 2 | FBA-Sendung 1: Spiegel Weiß/Schwarz/Eiche Catania, Salzlampe 1–2 und 2–3 kg |
| 3–4 | Titel, Suchbegriffe, Bilder, A+ für Stufe A; Stufe D neu texten und bebildern; Rollroste als Familie neu aufsetzen |
| 5–6 | Variationsfamilien Spiegel und Salzlampen; Vine für Stufe A; erste Charge neuer Listings (10) |
| 7–8 | Zweite Charge (15), Auswertung gegen die Woche-8-Werte, Sessions-Ziel je ASIN prüfen |

## Prüfwerte nach Woche 8

- Stufe A: ≥ 140 Sessions/Tag insgesamt (heute 70) bei gleicher Conversion.
- Stufe C: Buy Box der Rollroste ≥ 95 %.
- Stufe D: Conversion ≥ 4 %, sonst Listing neu bauen oder auslisten.
- Neue Listings: mindestens 0,5 Einheiten/Tag nach 28 Tagen.
