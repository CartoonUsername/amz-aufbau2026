# Version 3: übersichtlich (Kopfzeile mit Kurzinfos, Balken-Überschriften, Tabellen), aber ohne Karten/Pillen/Kreise.
# Nur Tabellen und Divs mit Inline-CSS (kein h1/h2, damit eBay die Überschriften nicht umstylt), kein JS, keine externen Links.
import html

F = "font-family:Arial,Helvetica,sans-serif;"
INK, MUTED, NAVY, SOFT, LINE = "#222222", "#667180", "#1f3a5f", "#eef1f4", "#d5dbe1"

def wrap(x):
    return f'<div style="{F}color:{INK};font-size:15px;line-height:1.55;max-width:800px;margin:0 auto;padding:0 8px;">{x}</div>'

def title(t, sub):
    return (f'<div style="font-size:25px;line-height:1.25;font-weight:bold;color:{NAVY};margin:0 0 4px;">{t}</div>'
            f'<div style="font-size:16px;margin:0 0 12px;">{sub}</div>')

def facts(items):
    cells = "".join(
        f'<td style="width:{100//len(items)}%;padding:9px 8px;text-align:center;vertical-align:top;border-right:1px solid {LINE};">'
        f'<div style="font-size:11px;color:{MUTED};text-transform:uppercase;letter-spacing:.5px;">{k}</div>'
        f'<div style="font-size:14px;font-weight:bold;color:{INK};line-height:1.3;">{v}</div></td>' for k, v in items)
    cells = cells.rsplit("border-right:1px solid " + LINE + ";", 1)
    cells = "".join(cells)
    return (f'<table style="width:100%;border-collapse:collapse;border:1px solid {LINE};border-top:3px solid {NAVY};margin:0 0 14px;">'
            f'<tr>{cells}</tr></table>')

def notice(label, text):
    return (f'<div style="background:#fafafa;border:1px solid {LINE};padding:9px 12px;font-size:12.5px;color:{MUTED};margin:0 0 4px;">'
            f'<b style="color:{INK};">{label}</b> {text}</div>')

def sec(t):
    return (f'<div style="background:{SOFT};border-left:4px solid {NAVY};padding:8px 12px;margin:24px 0 10px;'
            f'font-size:15px;font-weight:bold;color:{NAVY};letter-spacing:.3px;">{t}</div>')

def variants(headers, rows):
    th = "".join(f'<td style="background:{NAVY};color:#fff;font-size:12.5px;font-weight:bold;padding:7px 10px;">{h}</td>' for h in headers)
    body = ""
    for i, (a, b, c) in enumerate(rows):
        bg = "#ffffff" if i % 2 == 0 else "#f7f8fa"
        body += (f'<tr><td style="background:{bg};padding:10px;border-bottom:1px solid {LINE};font-size:20px;font-weight:bold;color:{NAVY};white-space:nowrap;vertical-align:top;">{a}</td>'
                 f'<td style="background:{bg};padding:10px;border-bottom:1px solid {LINE};vertical-align:top;white-space:nowrap;">{b}</td>'
                 f'<td style="background:{bg};padding:10px;border-bottom:1px solid {LINE};font-size:14px;vertical-align:top;">{c}</td></tr>')
    return f'<table style="width:100%;border-collapse:collapse;border:1px solid {LINE};"><tr>{th}</tr>{body}</table>'

def spec(rows):
    out = ""
    for i, (a, b) in enumerate(rows):
        bg = "#ffffff" if i % 2 == 0 else "#f7f8fa"
        out += (f'<tr><td style="background:{bg};padding:8px 12px;border-bottom:1px solid {LINE};width:36%;color:{MUTED};vertical-align:top;">{a}</td>'
                f'<td style="background:{bg};padding:8px 12px;border-bottom:1px solid {LINE};font-weight:bold;vertical-align:top;">{b}</td></tr>')
    return f'<table style="width:100%;border-collapse:collapse;border:1px solid {LINE};font-size:14.5px;">{out}</table>'

def small(t, extra=""):
    return f'<div style="font-size:12.5px;color:{MUTED};margin:6px 0 0;{extra}">{t}</div>'

def steps(items):
    out = ""
    for i, t in enumerate(items, 1):
        out += (f'<tr><td style="width:38px;background:{NAVY};color:#fff;font-size:20px;font-weight:bold;text-align:center;vertical-align:middle;'
                f'border-bottom:2px solid #ffffff;">{i}</td>'
                f'<td style="background:#f7f8fa;padding:9px 12px;border-bottom:2px solid #ffffff;">{t}</td></tr>')
    return f'<table style="width:100%;border-collapse:collapse;">{out}</table>'

def includes(t1, a, t2, b):
    li1 = "".join(f'<div style="margin:0 0 4px;"><b style="color:#1b7f4b;">✓</b> {x}</div>' for x in a)
    li2 = "".join(f'<div style="margin:0 0 4px;"><b style="color:#a33a3a;">✗</b> {x}</div>' for x in b)
    return (f'<table style="width:100%;border-collapse:collapse;border:1px solid {LINE};"><tr>'
            f'<td style="width:50%;vertical-align:top;padding:0;border-right:1px solid {LINE};">'
            f'<div style="background:#e9f3ed;padding:7px 12px;font-weight:bold;">{t1}</div><div style="padding:9px 12px;">{li1}</div></td>'
            f'<td style="width:50%;vertical-align:top;padding:0;">'
            f'<div style="background:#f5e9e9;padding:7px 12px;font-weight:bold;">{t2}</div><div style="padding:9px 12px;">{li2}</div></td></tr></table>')

def faq(items):
    return "".join(
        f'<div style="border-left:3px solid {LINE};padding:2px 0 2px 12px;margin:0 0 12px;">'
        f'<div style="font-weight:bold;color:{NAVY};">{q}</div><div>{a}</div></div>' for q, a in items)

def foot(t):
    return f'<div style="font-size:11.5px;color:{MUTED};margin:26px 0 0;padding-top:9px;border-top:1px solid {LINE};">{t}</div>'

def lang_bar(t):
    return (f'<div style="{F}max-width:800px;margin:0 auto 14px;padding:0 8px;"><div style="background:{NAVY};color:#fff;font-size:13px;'
            f'font-weight:bold;letter-spacing:2px;text-transform:uppercase;padding:6px 12px;">{t}</div></div>')

IMG_MASS = '<!-- Optional: Maß-Bild hier einfügen (eBay-Bild-URL eintragen)\n<div style="text-align:center;margin:10px 0;"><img src="EBAY-BILD-URL" alt="Maße" style="max-width:100%;height:auto;"></div>\n-->'

DE = wrap(
    title("Chromrohr, kompatibel mit USM Haller", "Länge wählbar: <b>35 cm · 50 cm · 75 cm</b>")
    + facts([("Zustand", "Neuware"), ("Versand", "kostenlos, mit Sendungsverfolgung"), ("Rückgabe", "30 Tage")])
    + notice("Wichtiger Hinweis:", "Kompatibles Ersatz- und Ergänzungsteil, <b>kein Originalteil</b> der USM U. Schärer Söhne AG. „USM“ und „USM Haller“ sind Marken der USM U. Schärer Söhne AG. Wir sind nicht mit USM verbunden; die Nennung dient ausschließlich der Angabe der Kompatibilität.")
    + sec("Welche Länge brauchst du?")
    + variants(["Länge", "Systemmaß", "Typisch für"], [
        ("35 cm", "350 mm", "Regale mit 35 cm Tiefe oder überall dort, wo 350 mm Systemmaß benötigt werden."),
        ("50 cm", "500 mm", "Regale mit 50 cm Tiefe oder überall dort, wo 500 mm Systemmaß benötigt werden."),
        ("75 cm", "750 mm", "Elemente mit 75 cm Breite oder überall dort, wo 750 mm Systemmaß benötigt werden."),
    ])
    + sec("Technische Daten")
    + spec([("Material", "Stahl, verchromt"), ("Oberfläche", "Chrom, glänzend"), ("Durchmesser", "19 mm"),
            ("Tatsächliche Länge", "35 cm: 350 mm · 50 cm: 500 mm · 75 cm: 750 mm"), ("Zustand", "Neu")])
    + small("Das Systemmaß ist der Abstand der Kugelmittelpunkte im Regal. Die tatsächliche Rohrlänge ist daher etwas kürzer und kann um wenige Millimeter abweichen.")
    + IMG_MASS
    + sec("So prüfst du die Passform")
    + steps(["Miss am vorhandenen Regal den Abstand von Kugelmitte zu Kugelmitte.",
             "Wähle die passende Länge: 350, 500 oder 750 mm Systemmaß.",
             "Vergleiche den Rohrdurchmesser (19 mm) mit deinen vorhandenen Rohren.",
             "Setze Kugeln und Konnektoren vorsichtig ein."])
    + sec("Lieferumfang")
    + includes("Enthalten", ["1 Rohr in der gewählten Länge"], "Nicht enthalten", ["Kugeln", "Konnektoren", "Füße, Tablare, Türen", "Werkzeug"])
    + sec("Häufige Fragen")
    + faq([("Ist das ein Originalteil von USM?", "Nein. Es ist ein kompatibles Teil eines anderen Herstellers. Bitte vergleiche die Maße vor dem Kauf."),
           ("Passt es zu meinem vorhandenen Regal?", "Es ist für die Verwendung mit dem USM-Haller-System gedacht. Wegen unterschiedlicher Fertigungstoleranzen können wir eine 100-%ige Passgenauigkeit zu allen Originalteilen nicht zusichern. Bei Fragen schreib uns gern vor dem Kauf."),
           ("Sind Kugeln und Konnektoren dabei?", "Nein, verkauft wird nur das Rohr. Kugeln und Konnektoren sind nicht Teil dieses Angebots."),
           ("Warum sitzen die Konnektoren manchmal etwas fest?", "Chromoberflächen können herstellungsbedingt minimale Unebenheiten an den Rohrenden aufweisen. Konnektoren bitte vorsichtig einsetzen; die Funktion wird nicht beeinträchtigt.")])
    + foot("<b>Gewerblicher Verkäufer.</b> Rechnung mit ausgewiesener MwSt. auf Wunsch. Impressum, Widerrufsbelehrung und AGB findest du in unserem eBay-Shop.")
)

EN = wrap(
    title("Chrome tube, compatible with USM Haller", "Choose your length: <b>35 cm · 50 cm · 75 cm</b>")
    + facts([("Condition", "Brand new"), ("Shipping", "free, tracked"), ("Returns", "30 days")])
    + notice("Important notice:", "Compatible replacement / add-on part, <b>not an original part</b> by USM U. Schärer Söhne AG. “USM” and “USM Haller” are trademarks of USM U. Schärer Söhne AG. We are not affiliated with USM; the names are used solely to indicate compatibility.")
    + sec("Which length do you need?")
    + variants(["Length", "System size", "Typical for"], [
        ("35 cm", "350 mm", "Shelves with a depth of 35 cm, or anywhere a 350 mm system size is required."),
        ("50 cm", "500 mm", "Shelves with a depth of 50 cm, or anywhere a 500 mm system size is required."),
        ("75 cm", "750 mm", "Units with a width of 75 cm, or anywhere a 750 mm system size is required."),
    ])
    + sec("Specifications")
    + spec([("Material", "Chrome-plated steel"), ("Finish", "Chrome, glossy"), ("Diameter", "19 mm"),
            ("Actual length", "35 cm: 350 mm · 50 cm: 500 mm · 75 cm: 750 mm"), ("Condition", "New")])
    + small("System size is the distance between the ball centres in the shelf. The actual tube length is therefore slightly shorter and may vary by a few millimetres.")
    + sec("How to check the fit")
    + steps(["Measure the distance from ball centre to ball centre on your existing shelf.",
             "Choose the matching length: 350, 500 or 750 mm system size.",
             "Compare the tube diameter (19 mm) with your existing tubes.",
             "Insert balls and connectors carefully."])
    + sec("What's included")
    + includes("Included", ["1 tube in the selected length"], "Not included", ["Balls", "Connectors", "Feet, shelves, doors", "Tools"])
    + sec("FAQ")
    + faq([("Is this an original USM part?", "No. It is a compatible part made by another manufacturer. Please compare measurements before purchase."),
           ("Will it fit my existing shelf?", "It is intended for use with the USM Haller system. Due to differing manufacturing tolerances we cannot guarantee a 100% fit with all original parts. Feel free to contact us before buying."),
           ("Are balls and connectors included?", "No, only the tube is sold. Balls and connectors are not part of this listing."),
           ("Why can connectors feel a little tight?", "Chrome plating can leave minor irregularities at the tube ends. Please insert connectors carefully; function is not affected.")])
    + foot("<b>Business seller.</b> Invoice with VAT shown on request. Legal notice, withdrawal information and terms are available in our eBay shop.")
)

code = ("<!-- ===== DEUTSCH ===== -->\n" + lang_bar("Deutsch") + "\n" + DE + "\n\n<div style=\"height:26px;\"></div>\n"
        "<!-- ===== ENGLISH ===== -->\n" + lang_bar("English") + "\n" + EN + "\n")
open("beschreibung-v3.html", "w", encoding="utf-8").write(code)
esc_ta = code.replace("&", "&amp;").replace("</textarea", "&lt;/textarea")
srcdoc = html.escape(code, quote=True)
page = f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>eBay-Beschreibung V3</title>
<style>
body{{font-family:Arial,Helvetica,sans-serif;max-width:1000px;margin:20px auto;padding:0 14px;background:#fff;color:#222}}
h1{{font-size:21px}} textarea{{width:100%;height:300px;font:12px Consolas,monospace;box-sizing:border-box}}
iframe{{width:100%;height:900px;border:1px solid #ddd}}
button{{padding:11px 18px;font-size:15px;border:0;border-radius:6px;background:#0064d2;color:#fff;cursor:pointer;margin:8px 0}}
.note{{background:#fff6d6;border:1px solid #e5cf7a;padding:10px 12px;border-radius:6px;font-size:14px}}
</style></head><body>
<h1>eBay-Beschreibung V3 (übersichtlich)</h1>
<p class="note">In eBay unter „Beschreibung“ <b>„HTML-Code anzeigen“</b> aktivieren und den Code einfügen.</p>
<button onclick="var t=document.getElementById('c');t.select();navigator.clipboard?navigator.clipboard.writeText(t.value):document.execCommand('copy');this.textContent='Kopiert!'">Code kopieren</button>
<textarea id="c" readonly>{esc_ta}</textarea>
<h2>Vorschau</h2>
<iframe sandbox srcdoc="{srcdoc}"></iframe>
</body></html>"""
open("kopieren-v3.html", "w", encoding="utf-8").write(page)
print(len(code))
