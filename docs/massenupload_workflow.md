# Massenupload-Workflow: FBM zuerst, FBA als Kopie

Ziel: viele saubere Listings mit wenig Handarbeit hochladen und so schneller zu mehr Umsatz kommen. Eine Charge hat höchstens 20 Listings (siehe `upload/amazon/README.md`).

## Regeln

1. Hauptversion ist immer FBM: SKU ohne Präfix (z. B. `S02-KLARO-WEISS-MATT-60x40`), Spalte `fulfillment` = FBM, Bestand = Eigenbestand.
2. FBA wird nur als Kopie gebaut: SKU `FBA_<SKU>` (z. B. `FBA_S02-KLARO-WEISS-MATT-60x40`), `fulfillment` = FBA, kein Bestand, **dieselbe GTIN** wie die FBM-Version.
3. Das Präfix `FBA_` steht nur bei echten FBA-SKUs, das war bisher in den alten SKUs vermischt (der Prüfer meldet jede Abweichung).
4. FBM und FBA sind zwei Angebote auf einer Produktseite: eine GTIN, eine ASIN, zwei SKUs. Neue GTINs gibt es nur für neue Produkte (`docs/gtin_regeln.md`).
5. Preise von FBM und FBA gleich halten, bei Abweichung FBM gleich oder höher als FBA.

## Ein Befehl pro Charge

```
python3 scripts/build_amazon_batch.py --batch charge_01_spiegel_sets \
    --listing data/spiegel_sets_texte_charge1.csv \
    --versandvorlage "Schneller Versand" \
    --base-url https://cdn.shopify.com/s/files/1/XXXX/files --images-dir /pfad/zu/bildern
```

Das Skript erledigt der Reihe nach:

1. GTINs für Zeilen ohne Nummer vergeben und im Register eintragen (`data/gtin_register.csv`).
2. Bild-URLs eintragen (nur mit `--base-url`).
3. FBM-Tabelle prüfen (Längen, Platzhalter, SKU-Dopplungen, https-Bilder, FBA_-Präfix).
4. FBA-Kopie als CSV erzeugen (`..._fba.csv`).
5. Beide Amazon-Dateien aus der Vorlage befüllen: `upload/amazon/<charge>/amazon_upload_FBM.xlsm` und `amazon_upload_FBA.xlsm`.

Meldet die Prüfung Fehler, sind die Dateien ein Entwurf und noch nicht hochladefertig.

## Upload-Reihenfolge bei Amazon

1. Zuerst `amazon_upload_FBM.xlsm` hochladen (Produkte hinzufügen → Tabelle) und unter „Uploadstatus überprüfen“ abwarten, bis die Produktseiten angelegt sind.
2. Danach `amazon_upload_FBA.xlsm` hochladen, die FBA-Angebote hängen sich über die GTIN an dieselben Produktseiten.
3. Für die FBA-SKUs die Sendung an Amazon anlegen (Lagerbestand verwalten → Sendungen), erst mit eingelagerter Ware sind sie kaufbar.

## Neues Produkt in vier Schritten

1. Texte in eine Listing-Tabelle schreiben (Format `data/listing_vorlage.csv`, fulfillment FBM).
2. Bilder nach Namensschema ablegen und auf Shopify hochladen (`docs/bilder_im_upload.md`).
3. `build_amazon_batch.py` aufrufen, Fehler beheben, bis die Prüfung sauber ist.
4. Dateien hochladen (FBM, dann FBA), Otto und eBay mit der FBM-Tabelle bedienen.

## Einschränkung

- Das Befüllen ist bisher nur für die Vorlage HOME_MIRROR (Heim-Spiegel) gebaut, für Tischlampen und Bilderrahmen braucht es deren Amazon-Vorlage, danach ist ein Füllskript in etwa derselben Größe nötig (Feldzuordnung, Dropdown-Werte, Browse Node).
- Paketmaße und -gewicht je Set fehlen noch in den Tabellen und stehen deshalb als „OFFEN“ im Ausgabeprotokoll.
- Otto und eBay verwenden andere Dateiformate, die Listing-Tabelle ist dafür die gemeinsame Quelle.
