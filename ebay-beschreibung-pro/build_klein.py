# Kompakte Version: Wichtiger Hinweis unverändert, alles andere auf das Nötigste gekürzt.
import html
F = "font-family:Arial,Helvetica,sans-serif;"
INK, MUTED, NAVY, SOFT, LINE = "#222222", "#667180", "#1f3a5f", "#eef1f4", "#d5dbe1"

def wrap(x):
    return f'<div style="{F}color:{INK};font-size:14px;line-height:1.5;max-width:800px;margin:0 auto;padding:0 8px;">{x}</div>'

def title(t, sub, facts):
    return (f'<div style="font-size:22px;line-height:1.25;font-weight:bold;color:{NAVY};margin:0 0 3px;">{t}</div>'
            f'<div style="font-size:15px;margin:0 0 4px;">{sub}</div>'
            f'<div style="font-size:12.5px;color:{MUTED};margin:0 0 10px;padding-bottom:8px;border-bottom:2px solid {NAVY};">{facts}</div>')

def notice(label, text):
    return (f'<div style="background:#fafafa;border:1px solid {LINE};padding:9px 12px;font-size:12.5px;color:{MUTED};margin:0 0 12px;">'
            f'<b style="color:{INK};">{label}</b> {text}</div>')

def table(headers, rows):
    th = "".join(f'<td style="background:{NAVY};color:#fff;font-size:12px;font-weight:bold;padding:5px 10px;">{h}</td>' for h in headers)
    body = ""
    for i, row in enumerate(rows):
        bg = "#ffffff" if i % 2 == 0 else "#f7f8fa"
        cells = ""
        for j, c in enumerate(row):
            extra = f"font-weight:bold;color:{NAVY};" if j == 0 else ""
            cells += f'<td style="background:{bg};padding:6px 10px;border-bottom:1px solid {LINE};{extra}">{c}</td>'
        body += f"<tr>{cells}</tr>"
    return f'<table style="width:100%;border-collapse:collapse;border:1px solid {LINE};margin:0 0 8px;"><tr>{th}</tr>{body}</table>'

def kv(rows):
    body = ""
    for i, (a, b) in enumerate(rows):
        bg = "#ffffff" if i % 2 == 0 else "#f7f8fa"
        body += (f'<tr><td style="background:{bg};padding:5px 10px;border-bottom:1px solid {LINE};color:{MUTED};width:45%;">{a}</td>'
                 f'<td style="background:{bg};padding:5px 10px;border-bottom:1px solid {LINE};font-weight:bold;">{b}</td></tr>')
    return f'<table style="width:100%;border-collapse:collapse;border:1px solid {LINE};margin:0 0 8px;">{body}</table>'

def p(t, size="14px", color=INK, mb="6px"):
    return f'<div style="font-size:{size};color:{color};margin:0 0 {mb};">{t}</div>'

def foot(t):
    return f'<div style="font-size:11.5px;color:{MUTED};margin:12px 0 0;padding-top:8px;border-top:1px solid {LINE};">{t}</div>'

def bar(t):
    return (f'<div style="{F}max-width:800px;margin:0 auto 10px;padding:0 8px;"><div style="background:{NAVY};color:#fff;font-size:12px;'
            f'font-weight:bold;letter-spacing:2px;text-transform:uppercase;padding:5px 12px;">{t}</div></div>')

DE = wrap(
    title("Chromrohr, kompatibel mit USM Haller", "Länge wählbar: ca. <b>35 cm · 50 cm · 75 cm</b> (Systemmaß)",
          "Spurenfreie Oberfläche, wird jedoch als gebraucht verkauft")
    + notice("Wichtiger Hinweis:", "Produkt eines Drittherstellers, <b>kein Originalteil</b> von USM Haller. Der genannte Markenname „USM Haller“ ist markenrechtlich geschützt (USM U. Schärer Söhne AG) und dient nur der Angabe der Kompatibilität. Keine Werksvertretung, keine Verbindung zu USM. Originale USM-Haller-Teile erhältst du direkt bei der USM U. Schärer Söhne AG oder bei deren lizenzierten Handelspartnern.")
    + table(["Variante", "Systemmaß (Nominallänge)", "Effektive Länge"], [("ca. 35 cm", "ca. 350 mm", "ca. 332 mm"), ("ca. 50 cm", "ca. 500 mm", "ca. 482 mm"), ("ca. 75 cm", "ca. 750 mm", "ca. 732 mm")])
    + p("Die effektive Länge der Rohre ergibt sich aus der Nominallänge (Achsenmaß) minus 18 mm (z. B. 750 mm – 18 mm = 732 mm).", "12.5px", MUTED, "8px")
    + kv([("Material", "Präzisionsstahlrohr, verchromt"), ("Oberfläche", "verchromt, glänzend"), ("Außendurchmesser", "ca. 19 mm"), ("Wandstärke", "ca. 1,2 mm"), ("Rohrenden", "an jeder Endung innen und außen angeschrägt"), ("Zustand", "Spurenfreie Oberfläche, wird jedoch als gebraucht verkauft")])
    + p("Systemmaß und Durchmesser entsprechen den Maßen der jeweiligen Original-Rohre; geringe Fertigungstoleranzen sind möglich. Eine 100-%ige Passgenauigkeit zu allen Originalteilen können wir nicht zusichern, bitte vergleiche die Maße vor dem Kauf.", "12.5px", MUTED, "8px")
    + p("<b>Lieferumfang:</b> 1 Stück Rohr in der gewählten Länge. <b>Nicht enthalten:</b> Kugeln, Konnektoren, Füße, Tablare, Türen, Werkzeug.")
)

EN = wrap(
    title("Chrome tube, compatible with USM Haller", "Choose your length: ca. <b>35 cm · 50 cm · 75 cm</b> (system size)",
          "Trace-free surface, but sold as used")
    + notice("Important notice:", "Product by a third-party manufacturer, <b>not an original</b> USM Haller part. The brand name “USM Haller” is protected by trademark law (USM U. Schärer Söhne AG) and is used only to indicate compatibility. No factory representation and no affiliation with USM. For original USM Haller parts, please contact USM U. Schärer Söhne AG directly or its licensed dealers.")
    + table(["Variant", "System size (nominal length)", "Effective length"], [("ca. 35 cm", "ca. 350 mm", "ca. 332 mm"), ("ca. 50 cm", "ca. 500 mm", "ca. 482 mm"), ("ca. 75 cm", "ca. 750 mm", "ca. 732 mm")])
    + p("The effective length of the tubes is the nominal length (axis dimension) minus 18 mm (e.g. 750 mm – 18 mm = 732 mm).", "12.5px", MUTED, "8px")
    + kv([("Material", "Precision steel tube, chrome-plated"), ("Finish", "chrome-plated, glossy"), ("Outer diameter", "ca. 19 mm"), ("Wall thickness", "ca. 1.2 mm"), ("Tube ends", "chamfered inside and outside at each end"), ("Condition", "Trace-free surface, but sold as used")])
    + p("System size and diameter match the dimensions of the respective original tubes; minor manufacturing tolerances are possible. We cannot guarantee a 100% fit with all original parts, please compare measurements before purchase.", "12.5px", MUTED, "8px")
    + p("<b>Included:</b> 1 piece of tube in the selected length. <b>Not included:</b> balls, connectors, feet, shelves, doors, tools.")
)

code = ("<!-- ===== DEUTSCH ===== -->\n" + bar("Deutsch") + "\n" + DE + "\n\n<div style=\"height:18px;\"></div>\n"
        "<!-- ===== ENGLISH ===== -->\n" + bar("English") + "\n" + EN + "\n")
open("beschreibung-klein.html", "w", encoding="utf-8").write(code)
esc_ta = code.replace("&", "&amp;").replace("</textarea", "&lt;/textarea")
srcdoc = html.escape(code, quote=True)
page = f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>eBay-Beschreibung klein</title>
<style>
body{{font-family:Arial,Helvetica,sans-serif;max-width:1000px;margin:20px auto;padding:0 14px;background:#fff;color:#222}}
h1{{font-size:21px}} textarea{{width:100%;height:260px;font:12px Consolas,monospace;box-sizing:border-box}}
iframe{{width:100%;height:700px;border:1px solid #ddd}}
button{{padding:11px 18px;font-size:15px;border:0;border-radius:6px;background:#0064d2;color:#fff;cursor:pointer;margin:8px 0}}
.note{{background:#fff6d6;border:1px solid #e5cf7a;padding:10px 12px;border-radius:6px;font-size:14px}}
</style></head><body>
<h1>eBay-Beschreibung klein</h1>
<p class="note">In eBay unter „Beschreibung“ <b>„HTML-Code anzeigen“</b> aktivieren und den Code einfügen.</p>
<button onclick="var t=document.getElementById('c');t.select();navigator.clipboard?navigator.clipboard.writeText(t.value):document.execCommand('copy');this.textContent='Kopiert!'">Code kopieren</button>
<textarea id="c" readonly>{esc_ta}</textarea>
<h2>Vorschau</h2>
<iframe sandbox srcdoc="{srcdoc}"></iframe>
</body></html>"""
open("kopieren-klein.html", "w", encoding="utf-8").write(page)
print(len(code))
