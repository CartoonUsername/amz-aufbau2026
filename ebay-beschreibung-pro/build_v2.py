# Version 2: schlicht, "von Hand gemacht" statt Karten/Badges/Kreise. Gleiche Informationen wie die finale Version.
import html

F = "font-family:Arial,Helvetica,sans-serif;"
INK, MUTED, RULE = "#222222", "#666666", "#cfcfcf"

def wrap(x):
    return f'<div style="{F}color:{INK};font-size:15px;line-height:1.6;max-width:780px;margin:0 auto;padding:0 10px;">{x}</div>'

def head(h1, sub, facts):
    return (f'<h1 style="font-size:24px;font-weight:bold;margin:0 0 4px;color:{INK};">{h1}</h1>'
            f'<div style="font-size:16px;margin:0 0 6px;">{sub}</div>'
            f'<div style="font-size:13px;color:{MUTED};margin:0 0 16px;padding-bottom:12px;border-bottom:2px solid {INK};">{facts}</div>')

def note(label, text):
    return (f'<p style="font-size:12.5px;color:{MUTED};margin:0 0 6px;padding:8px 10px;border:1px solid {RULE};">'
            f'<b style="color:{INK};">{label}</b> {text}</p>')

def h(t):
    return (f'<h2 style="font-size:13px;font-weight:bold;letter-spacing:1px;text-transform:uppercase;margin:28px 0 8px;'
            f'padding:0 0 4px;border-bottom:1px solid {RULE};color:{INK};">{t}</h2>')

def grid(headers, rows, widths):
    th = "".join(f'<th style="text-align:left;font-size:12.5px;font-weight:bold;color:{MUTED};padding:5px 10px 5px 0;'
                 f'border-bottom:1px solid {RULE};width:{w};">{c}</th>' for c, w in zip(headers, widths))
    tr = ""
    for r in rows:
        tr += "<tr>" + "".join(
            f'<td style="vertical-align:top;padding:7px 10px 7px 0;border-bottom:1px solid #ececec;'
            f'{"font-weight:bold;" if i == 0 else ""}">{c}</td>' for i, c in enumerate(r)) + "</tr>"
    return f'<table style="border-collapse:collapse;width:100%;font-size:14.5px;"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'

def kv(rows):
    tr = "".join(
        f'<tr><td style="vertical-align:top;padding:6px 14px 6px 0;border-bottom:1px solid #ececec;color:{MUTED};width:34%;">{a}</td>'
        f'<td style="vertical-align:top;padding:6px 0;border-bottom:1px solid #ececec;">{b}</td></tr>' for a, b in rows)
    return f'<table style="border-collapse:collapse;width:100%;font-size:14.5px;"><tbody>{tr}</tbody></table>'

def ol(items):
    li = "".join(f'<li style="margin:0 0 4px;">{x}</li>' for x in items)
    return f'<ol style="margin:0;padding-left:22px;">{li}</ol>'

def p(t, style=""):
    return f'<p style="margin:0 0 8px;{style}">{t}</p>'

def qa(items):
    return "".join(f'<p style="margin:0 0 10px;"><b>{q}</b><br>{a}</p>' for q, a in items)

def foot(t):
    return f'<p style="font-size:11.5px;color:{MUTED};margin:24px 0 0;padding-top:8px;border-top:1px solid {RULE};">{t}</p>'

DE = wrap(
    head("Chromrohr, kompatibel mit USM Haller",
         "Länge wählbar: <b>35 cm · 50 cm · 75 cm</b>",
         "Neuware &nbsp;|&nbsp; Versand kostenlos, mit Sendungsverfolgung &nbsp;|&nbsp; 30 Tage Rückgabe")
    + note("Wichtiger Hinweis:", "Produkt eines Drittherstellers, <b>kein Originalteil</b> von USM Haller. Der genannte Markenname „USM Haller“ ist markenrechtlich geschützt (USM U. Schärer Söhne AG) und dient nur der Angabe der Kompatibilität. Keine Werksvertretung, keine Verbindung zu USM. Originale USM-Haller-Teile erhältst du direkt bei der USM U. Schärer Söhne AG oder bei deren lizenzierten Handelspartnern.")
    + h("Welche Länge brauchst du?")
    + grid(["Länge", "Systemmaß", "Typisch für"], [
        ("35 cm", "350 mm", "Regale mit 35 cm Tiefe oder überall dort, wo 350 mm Systemmaß benötigt werden."),
        ("50 cm", "500 mm", "Regale mit 50 cm Tiefe oder überall dort, wo 500 mm Systemmaß benötigt werden."),
        ("75 cm", "750 mm", "Elemente mit 75 cm Breite oder überall dort, wo 750 mm Systemmaß benötigt werden."),
    ], ["16%", "20%", "64%"])
    + h("Technische Daten")
    + kv([("Material", "Stahl, verchromt"), ("Oberfläche", "Chrom, glänzend"), ("Durchmesser", "19 mm"),
          ("Zustand", "Neu")])
    + p("Länge, Durchmesser und Systemmaß entsprechen den Maßen der jeweiligen Original-Rohre; geringe Fertigungstoleranzen sind möglich.", f"font-size:12.5px;color:{MUTED};margin-top:6px;")
    + h("So prüfst du die Passform")
    + ol(["Miss am vorhandenen Regal den Abstand von Kugelmitte zu Kugelmitte.",
          "Wähle die passende Länge: 350, 500 oder 750 mm Systemmaß.",
          "Vergleiche den Rohrdurchmesser (19 mm) mit deinen vorhandenen Rohren.",
          "Setze Kugeln und Konnektoren vorsichtig ein."])
    + h("Lieferumfang")
    + p("<b>Enthalten:</b> 1 Rohr in der gewählten Länge")
    + p("<b>Nicht enthalten:</b> Kugeln, Konnektoren, Füße, Tablare, Türen, Werkzeug")
    + h("Häufige Fragen")
    + qa([("Ist das ein Originalteil von USM?", "Nein. Es ist ein kompatibles Teil eines anderen Herstellers. Bitte vergleiche die Maße vor dem Kauf."),
          ("Passt es zu meinem vorhandenen Regal?", "Es ist für die Verwendung mit dem USM-Haller-System gedacht. Wegen unterschiedlicher Fertigungstoleranzen können wir eine 100-%ige Passgenauigkeit zu allen Originalteilen nicht zusichern. Bei Fragen schreib uns gern vor dem Kauf."),
          ("Sind Kugeln und Konnektoren dabei?", "Nein, verkauft wird nur das Rohr. Kugeln und Konnektoren sind nicht Teil dieses Angebots."),
          ("Warum sitzen die Konnektoren manchmal etwas fest?", "Chromoberflächen können herstellungsbedingt minimale Unebenheiten an den Rohrenden aufweisen. Konnektoren bitte vorsichtig einsetzen; die Funktion wird nicht beeinträchtigt.")])
    + foot("<b>Gewerblicher Verkäufer.</b> Rechnung mit ausgewiesener MwSt. auf Wunsch. Impressum, Widerrufsbelehrung und AGB findest du in unserem eBay-Shop.")
)

EN = wrap(
    head("Chrome tube, compatible with USM Haller",
         "Choose your length: <b>35 cm · 50 cm · 75 cm</b>",
         "Brand new &nbsp;|&nbsp; Free tracked shipping &nbsp;|&nbsp; 30-day returns")
    + note("Important notice:", "Product by a third-party manufacturer, <b>not an original</b> USM Haller part. The brand name “USM Haller” is protected by trademark law (USM U. Schärer Söhne AG) and is used only to indicate compatibility. No factory representation and no affiliation with USM. For original USM Haller parts, please contact USM U. Schärer Söhne AG directly or its licensed dealers.")
    + h("Which length do you need?")
    + grid(["Length", "System size", "Typical for"], [
        ("35 cm", "350 mm", "Shelves with a depth of 35 cm, or anywhere a 350 mm system size is required."),
        ("50 cm", "500 mm", "Shelves with a depth of 50 cm, or anywhere a 500 mm system size is required."),
        ("75 cm", "750 mm", "Units with a width of 75 cm, or anywhere a 750 mm system size is required."),
    ], ["16%", "20%", "64%"])
    + h("Specifications")
    + kv([("Material", "Chrome-plated steel"), ("Finish", "Chrome, glossy"), ("Diameter", "19 mm"),
          ("Condition", "New")])
    + p("Length, diameter and system size match the dimensions of the respective original tubes; minor manufacturing tolerances are possible.", f"font-size:12.5px;color:{MUTED};margin-top:6px;")
    + h("How to check the fit")
    + ol(["Measure the distance from ball centre to ball centre on your existing shelf.",
          "Choose the matching length: 350, 500 or 750 mm system size.",
          "Compare the tube diameter (19 mm) with your existing tubes.",
          "Insert balls and connectors carefully."])
    + h("What's included")
    + p("<b>Included:</b> 1 tube in the selected length")
    + p("<b>Not included:</b> Balls, connectors, feet, shelves, doors, tools")
    + h("FAQ")
    + qa([("Is this an original USM part?", "No. It is a compatible part made by another manufacturer. Please compare measurements before purchase."),
          ("Will it fit my existing shelf?", "It is intended for use with the USM Haller system. Due to differing manufacturing tolerances we cannot guarantee a 100% fit with all original parts. Feel free to contact us before buying."),
          ("Are balls and connectors included?", "No, only the tube is sold. Balls and connectors are not part of this listing."),
          ("Why can connectors feel a little tight?", "Chrome plating can leave minor irregularities at the tube ends. Please insert connectors carefully; function is not affected.")])
    + foot("<b>Business seller.</b> Invoice with VAT shown on request. Legal notice, withdrawal information and terms are available in our eBay shop.")
)

SEP = (f'<div style="{F}max-width:780px;margin:34px auto 22px;padding:0 10px;"><div style="border-top:1px solid {RULE};'
       f'padding-top:6px;font-size:12px;letter-spacing:2px;color:{MUTED};text-transform:uppercase;">English version</div></div>')

code = "<!-- ===== DEUTSCH ===== -->\n" + DE + "\n\n" + SEP + "\n<!-- ===== ENGLISH ===== -->\n" + EN + "\n"
open("beschreibung-v2.html", "w", encoding="utf-8").write(code)
esc_ta = code.replace("&", "&amp;").replace("</textarea", "&lt;/textarea")
srcdoc = html.escape(code, quote=True)
page = f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>eBay-Beschreibung V2</title>
<style>
body{{font-family:Arial,Helvetica,sans-serif;max-width:1000px;margin:20px auto;padding:0 14px;background:#fff;color:#222}}
h1{{font-size:21px}} textarea{{width:100%;height:300px;font:12px Consolas,monospace;box-sizing:border-box}}
iframe{{width:100%;height:900px;border:1px solid #ddd;border-radius:8px}}
button{{padding:11px 18px;font-size:15px;border:0;border-radius:6px;background:#0064d2;color:#fff;cursor:pointer;margin:8px 0}}
.note{{background:#fff6d6;border:1px solid #e5cf7a;padding:10px 12px;border-radius:6px;font-size:14px}}
</style></head><body>
<h1>eBay-Beschreibung V2 (schlicht)</h1>
<p class="note">In eBay unter „Beschreibung“ <b>„HTML-Code anzeigen“</b> aktivieren und den Code einfügen.</p>
<button onclick="var t=document.getElementById('c');t.select();navigator.clipboard?navigator.clipboard.writeText(t.value):document.execCommand('copy');this.textContent='Kopiert!'">Code kopieren</button>
<textarea id="c" readonly>{esc_ta}</textarea>
<h2>Vorschau</h2>
<iframe sandbox srcdoc="{srcdoc}"></iframe>
</body></html>"""
open("kopieren-v2.html", "w", encoding="utf-8").write(page)
print(len(code))
