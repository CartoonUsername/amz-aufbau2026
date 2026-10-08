# Bilder beim Hochladen mitgeben

Ja, das geht. Amazon, Otto und eBay laden Bilder nicht aus der Datei, sondern von öffentlichen https-Adressen. In die Listing-Tabelle kommen also nur die URLs, die Bilder selbst liegen auf einem Server.

## 1. Ablauf

1. Bilder produzieren und nach dem Namensschema benennen (siehe Abschnitt 2).
2. Alle Bilder auf einen öffentlichen Bilderspeicher hochladen (Abschnitt 3).
3. Das Skript `scripts/fill_image_urls.py` trägt die URLs in die Spalten `bild_haupt` bis `bild_7` der CSV ein.
4. Die gefüllte CSV in die Upload-Datei des Kanals übertragen (Abschnitt 4).

## 2. Namensschema

- Dateiname: SKU in Kleinbuchstaben, Leerzeichen und Sonderzeichen als Bindestrich, ä/ö/ü/ß als ae/oe/ue/ss, danach `_01` bis `_07`.
- Beispiel: SKU `S02-KLARO-WEISS-MATT-60x40` → `s02-klaro-weiss-matt-60x40_01.jpg` (Hauptbild), `_02.jpg` bis `_07.jpg`.
- Bild 01 ist immer das Hauptbild auf weißem Hintergrund.

## 3. Wohin mit den Bildern

| Speicher | Eignung |
|---|---|
| Shopify (Einstellungen → Dateien) | Empfohlen, existiert schon, liefert öffentliche https-Adressen über das Shopify-CDN |
| Eigener Webspace oder Cloud-Speicher mit öffentlichem Link | geht, der Link muss direkt auf die Bilddatei zeigen und ohne Login erreichbar sein |
| GitHub-Repository | nicht empfohlen, bei einem privaten Repo sind die Bilder von außen nicht abrufbar |

Die Adresse muss bei Amazon, Otto und eBay mit `https://` beginnen und auf die Datei direkt zeigen, nicht auf eine Seite.

## 4. Welche Spalten im Kanal

| Kanal | Bildspalten der Upload-Datei (Namen je nach Vorlage prüfen) | Hinweis |
|---|---|---|
| Amazon | `main_image_url`, `other_image_url1` bis `other_image_url8` | Amazon-Vorlage der Kategorie aus Seller Central laden, Spalten aus der Listing-Tabelle zuordnen |
| Otto | Bild-URLs im Produktdaten-Import (CSV, Excel oder Schnittstelle) | Mindestgrößen und Formate in Partner Connect prüfen |
| eBay | Spalte `PicURL` (mehrere Bilder mit `\|` getrennt) im Massenupload | Mindestens 500 px, besser über 1.000 px |

Weitere Zuordnung der Listing-Spalten zu Amazon-Feldern:

| Listing-Tabelle | Amazon-Vorlage |
|---|---|
| sku | `item_sku` |
| titel | `item_name` |
| bullet_1 bis bullet_5 | `bullet_point1` bis `bullet_point5` |
| beschreibung_a_plus | `product_description` |
| suchbegriffe | `generic_keywords` |
| preis_eur | `standard_price` |
| bestand | `quantity` (nur bei FBM) |
| gtin_ean | `external_product_id` |
| bild_haupt | `main_image_url` |
| bild_2 bis bild_7 | `other_image_url1` bis `other_image_url6` |

## 5. Bildanforderungen (Kurzfassung)

- Amazon: Hauptbild auf reinem Weiß ohne Text und Logo, längste Seite mindestens 1.000 px (für Zoom), JPEG oder PNG, Produkt füllt den größten Teil des Bildes.
- Otto und eBay: Anforderungen vor dem ersten Upload in Partner Connect und im Seller Hub prüfen.
- Keine fremden Bilder oder Marken in den Bildern.

## 6. Aufruf des Skripts

```
python3 scripts/fill_image_urls.py \
  --csv data/spiegel_sets_texte_charge1.csv \
  --base-url https://cdn.shopify.com/s/files/1/XXXX/files \
  --images-dir /pfad/zu/den/bildern \
  --out data/spiegel_sets_mit_bildern.csv
```

- Mit `--images-dir` trägt das Skript nur URLs für Bilder ein, die als Datei existieren, und meldet fehlende Hauptbilder.
- Ohne `--images-dir` werden alle 7 URLs für jede Zeile eingetragen.
- Das Skript wurde mit Testdateien geprüft (Namensbildung, fehlende Bilder, https-Pflicht).

## 7. Offen

- Die Shopify-Datei-Adresse (`--base-url`) und die Frage, wer die Bilder produziert.
- Die Amazon-Vorlage der Kategorie (Spiegel, Tischlampen, Bilderrahmen), damit das Mapping exakt auf die Spaltennamen passt.
