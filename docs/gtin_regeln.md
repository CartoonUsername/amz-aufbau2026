# GTIN-Regeln (GS1, Basisnummer 4255822)

Quelle der Wahrheit: `data/gtin_register.csv` (alle vergebenen Nummern mit SKU und Produkt). Aufbau einer GTIN: 4255822 + 5-stellige Artikelnummer + Prüfziffer.

## Reihenfolge

1. Nummern werden immer lückenlos nach der höchsten vergebenen Artikelnummer vergeben, nie aus dem Kopf und nie doppelt.
2. Nächste freie Artikelnummer anzeigen: `python3 scripts/ean_tools.py next`
3. Nummern für neue Listings vergeben und gleich ins Register eintragen: `python3 scripts/ean_tools.py assign --listing <listing.csv>` (das Skript lässt vorhandene gültige GTINs unangetastet, vergibt nur für leere oder Platzhalter-Zeilen und kann gefahrlos zweimal laufen).
4. Eine GTIN gehört genau einem Produkt: Sets, Einzelartikel und jede Farbe brauchen eigene Nummern.
5. Jede neue GTIN im GS1-Portal dem Produkt zuordnen (Name, Marke EmsCraft24, Inhalt).

## Stand 8.10.2026

- Register: 93 Nummern, höchste Artikelnummer 60199, nächste freie Artikelnummer: **60200**.
- Artikelnummern 60182 bis 60191 gehören den 10 Spiegel-Sets (2er Weiß Matt bis 3er Gold Glänzend), 60192 bis 60199 den 8 Salzlampen-Sets (GS01 bis GS08), die Zuordnung je SKU steht im Register.
- Prüfziffer prüfen: `python3 scripts/ean_tools.py check <ean>`.

## Auffälligkeit

- Die GTIN 4255822600242 steht auf Otto bei zwei verschiedenen Produkten (Mini-Salzlampe „LampeSet-Kugel-USB-EC24“ und Akustikpaneel „011_Beton_Optik_EC24“). Eine GTIN darf nur ein Produkt kennzeichnen, deshalb im GS1-Portal und bei Otto klären, welches Produkt sie wirklich trägt, und das andere korrigieren.
