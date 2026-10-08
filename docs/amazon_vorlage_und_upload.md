# Amazon-Vorlage für den Upload in Maßen

Ja, die Amazon-Vorlage brauche ich, und zwar je Produktgruppe eine.

## Welche Vorlagen

| Gruppe | Kategorie in Amazon (Suche im Vorlagen-Dialog) |
|---|---|
| Spiegel-Sets | Wandspiegel / Spiegel |
| Salzlampen-Sets | Tischlampen / Beleuchtung |
| Trikotrahmen | Bilderrahmen |

## So lädst du sie

1. Seller Central → Produkte → Produkte hinzufügen (oder Katalog → Produkte hinzufügen) → Produkte per Upload hinzufügen.
2. Die Vorlage der Kategorie herunterladen, die Menüs heißen je nach Ansicht leicht unterschiedlich.
3. Die Datei (`.xlsm`) unverändert in `templates/amazon/` legen, zum Beispiel `wandspiegel.xlsm`, `tischlampe.xlsm`, `bilderrahmen.xlsm`.

## Was ich damit mache

- Ich lese die Spaltenüberschriften und Pflichtfelder der Vorlage und ordne sie den Spalten der Listing-Tabelle zu (Mapping in `docs/bilder_im_upload.md`).
- Ich fülle die Vorlage mit Titel, Bullets, Beschreibung, Suchbegriffen, Preis, Bestand, EAN und Bild-URLs und lasse sie von `scripts/validate_listings.py` prüfen.
- Die Datei lädst du selbst in Seller Central hoch, ich lade nichts bei Amazon hoch.

## Ordner

Die Struktur und die Chargenregeln stehen in `upload/amazon/README.md`: höchstens 20 Listings pro Charge, vorher Prüfung ohne Fehler, nach 14 und 28 Tagen Auswertung.

## Stand der Prüfung heute

Das Prüfskript meldet bei allen drei Chargen Platzhalter (EAN, Bestand, Bügel-Angaben bei den Trikotrahmen) und fehlende Bilder, die Texte selbst sind innerhalb der Längengrenzen.

## Nur neue Listings (8.10.2026)

- Die Chargen im Upload-Ordner enthalten nur neue Listings mit neuer SKU, neuer EAN und neuer Produktseite.
- Neu sind: Spiegel-Sets (2er/3er), Salzlampen-Sets, später Zubehör oder neue Bündel, denn ein Set ist ein anderes Produkt als der Einzelartikel.
- Nicht neu sind die Trikotrahmen auf Amazon: Es gibt die 5 Farben schon als ASINs, ein zweites Listing desselben Rahmens würde als doppelte Produktseite gelten, deshalb sind die Texte in `data/trikotrahmen_texte.csv` Updates der bestehenden Seiten (Amazon) und neue Listings nur bei eBay.
- Für neue Trikot-Listings auf Amazon braucht es ein anderes Produkt, zum Beispiel ein 2er-Set oder ein Set mit zwei Farben.
- `python3 scripts/validate_listings.py --nur-neu <datei>` meldet Amazon-Zeilen, die kein neues Listing sind.

## Vorlage HOME_MIRROR (Heim-Spiegel) erhalten und befüllt (8.10.2026)

- Datei: `templates/amazon/home_mirror.xlsm` (Amazon.de, 325 Spalten in Blatt „Vorlage“, Zeile 4 Bezeichnung, Zeile 5 technischer Name, Daten ab Zeile 8). Alle Felder mit Pflichtstatus und Beispiel stehen in `data/amazon_home_mirror_felder.csv`.
- Von Amazon vorausgefüllte Profilzeile (Zeile 8): Marke und Hersteller EmsCraft24, Größe „Mittelgroße“, Montage „Ja“, Ursprungsland Deutschland, Batterien „Nein“, Gefahrgut „Nicht zutreffend“, Artikelmaße 60 × 40 cm.
- Entwürfe: `upload/amazon/charge_01_spiegel_sets/amazon_upload_FBM.xlsm` und `amazon_upload_FBA.xlsm` (Ablauf in `docs/massenupload_workflow.md`) mit den 10 Spiegel-Sets, erzeugt mit `scripts/fill_amazon_home_mirror.py` aus `data/spiegel_sets_texte_charge1.csv`. Die Kopfzeilen 1 bis 7 sind unverändert, die Dropdown-Prüfungen (650) und Namen (1.081) sind erhalten.
- Einschränkung: Beim Speichern gingen 21 Beispielbilder im Blatt „Bilder“ (nur Anleitung) verloren, das hat keinen Einfluss auf die Tabelle, ob Amazon die Datei annimmt, zeigt der Upload unter „Uploadstatus überprüfen“.

### Wie die Felder gefüllt sind

| Feld | Wert |
|---|---|
| Produkttyp | HOME_MIRROR |
| Browse Node | Küche, Haushalt & Wohnen > Möbel > Diele & Flur > Wandspiegel (2970878031), Alternative Bad: Badspiegel > Wandspiegel (13944741031) |
| Anzahl der Artikel / Anzahl von Einheiten | 2 oder 3 (nach SKU S02 oder S03), Typ „stück“ |
| Enthaltene Komponenten | „2 Spiegel, Aufhängeset (Aufhänger, Schrauben, Dübel)“ bzw. 3 |
| Montageart | Wandmontage |
| Form, Material, Zustand | Rechteckig, Kunststoff, Neu |
| Fulfillment | „Versand durch Amazon (EU)“ bei FBA, sonst „Versand durch Händler (Standard)“ |
| Preis | Spalte „Ihr Preis EUR (Bei Amazon verkaufen, DE)“ |
| Listenpreis (UVP) | bleibt leer (kein erfundener UVP) |
| Variationen | leer, die Sets sind eigenständige Listings |

### Noch offen vor dem Upload

1. ~~EANs der 10 Sets~~ erledigt am 8.10.2026: GTINs 4255822601829 bis 4255822601911 (Artikelnummern 60182 bis 60191) sind in Tabelle und Entwurf eingetragen, Regeln in `docs/gtin_regeln.md`.
2. Paketlänge, -breite, -höhe und -gewicht je Set (die Profilwerte gelten für einen einzelnen Spiegel und sind bewusst leer).
3. Bestand bei FBM oder Versandvorlage („Prime Mustervorlage“, „Schneller Versand“, „Standardvorlage Amazon“ und weitere in deinem Konto), bei FBA stattdessen die Sendung.
4. Bild-URLs (`scripts/fill_image_urls.py`, dann die Vorlage neu füllen).
5. Ob „Größe: Mittelgroße“ und „Farbe“ so stimmen und ob „Rahmenfarbe“ oder „Rahmenmaterial“ relevant sind.
6. Prüfung mit `python3 scripts/validate_listings.py --nur-neu data/spiegel_sets_texte_charge1.csv` ohne Fehler.

Hochladen: Seller Central → Produkte hinzufügen → Tabelle → Datei hochladen → „Produkte übermitteln“, danach Uploadstatus prüfen.

## EANs über GS1 (8.10.2026)

- Eure vorhandenen GTINs beginnen mit 4255822 (74 genutzte Nummern, Artikelnummern 60006 bis 60181, alle mit korrekter Prüfziffer), das ist eure GS1-Basisnummer.
- Jedes Set braucht eine neue GTIN, denn ein 2er- oder 3er-Set ist ein anderes Produkt als der Einzelspiegel und darf die EAN des Einzelartikels nicht übernehmen.
- `scripts/ean_tools.py` prüft die Prüfziffer (`check`), zählt genutzte Nummern (`used`) und macht Vorschläge für freie Nummern (`propose`), die Vorschläge für die 10 Spiegel-Sets und die 8 Salzlampen-Sets stehen in `data/gtin_register.csv`.
- Die Nummern wurden bestätigt (genug freie Nummern vorhanden) und über `ean_tools.py assign` vergeben und im Register eingetragen, im GS1-Portal sind sie noch den Produkten (Name, Marke EmsCraft24, Inhalt) zuzuordnen, denn Amazon gleicht GTIN und Marke mit dem GS1-Register ab.
- Danach die bestätigten Nummern in die Spalte `gtin_ean` der Listing-Tabelle übernehmen und die Amazon-Vorlage neu füllen.

## Mehrere Kategorien für dasselbe Produkt (8.10.2026)

- Ein Produkt bekommt bei Amazon genau eine Produktseite, dieselbe Ware unter mehreren Produkttypen oder als zweites Listing anzulegen gilt als doppelte Produktseite und kann zur Sperrung führen.
- Mehrere Kategorien erreicht man über die „Empfohlenen Stöbern-Kategorien“ derselben Produktseite (in der Vorlage bis zu 5 Spalten), die Seite erscheint dann in jeder Kategorie.
- Für Heim-Spiegel bietet die Vorlage drei Kategorien an: Möbel > Diele & Flur > Wandspiegel (2970878031), Badausstattung > Badaccessoires > Badspiegel > Wandspiegel (13944741031) und Wohnaccessoires & Deko > Spiegel > Standspiegel (2970875031).
- Die Spiegel-Sets stehen in den ersten beiden (Wandspiegel), Standspiegel ist ausgelassen, weil die Sets für die Wand sind. Die Spalte `kategorien` der Listing-Tabelle nimmt die Dropdown-Werte mit `;` getrennt auf, Werte außerhalb der Dropdown-Liste werden nicht eingetragen.
- Material der Spiegelfläche: Kunststoff (bestätigt), Rahmenmaterial: Holzwerkstoff (aus „MDF-Holzwerkstoff“ im Listing).
