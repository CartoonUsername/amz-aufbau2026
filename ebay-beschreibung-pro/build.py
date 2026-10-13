# Generiert die eBay-Beschreibung (DE + EN) mit reinem Inline-CSS (kein JS, keine externen Ressourcen).
import html

FONT = "font-family:Arial,Helvetica,sans-serif;"
INK = "#1d2430"      # Text
MUTED = "#5b6573"    # Nebentext
LINE = "#e3e7ec"     # Linien
SOFT = "#f4f6f8"     # Flächen
ACCENT = "#1f4f8f"   # Akzent (Blau)

def wrap(inner):
    return (f'<div style="{FONT}color:{INK};font-size:15px;line-height:1.55;max-width:860px;margin:0 auto;padding:0 8px;">'
            f'{inner}</div>')

def hero(h1, sub, badges):
    b = "".join(
        f'<span style="display:inline-block;margin:4px 6px 0 0;padding:5px 11px;background:#ffffff;color:{INK};'
        f'border:1px solid {LINE};border-radius:20px;font-size:12.5px;font-weight:bold;">{x}</span>' for x in badges)
    return (f'<div style="background:{INK};color:#ffffff;border-radius:10px;padding:22px 22px 18px;margin:0 0 14px;">'
            f'<h1 style="margin:0 0 6px;font-size:25px;line-height:1.25;color:#ffffff;">{h1}</h1>'
            f'<div style="font-size:16px;color:#d5dbe3;margin:0 0 10px;">{sub}</div>{b}</div>')

def notice(title, text):
    return (f'<div style="background:{SOFT};border-left:4px solid {ACCENT};border-radius:6px;padding:11px 14px;margin:0 0 18px;'
            f'font-size:12.5px;color:{MUTED};"><b style="color:{INK};">{title}</b> {text}</div>')

def h2(t):
    return (f'<h2 style="font-size:19px;margin:26px 0 10px;padding:0 0 6px;border-bottom:2px solid {LINE};color:{INK};">{t}</h2>')

def cards(items):
    out = []
    for size, sys_, txt in items:
        out.append(
            f'<div style="flex:1 1 210px;box-sizing:border-box;'
            f'border:1px solid {LINE};border-radius:10px;padding:14px 14px 12px;background:#ffffff;">'
            f'<div style="font-size:30px;font-weight:bold;color:{ACCENT};line-height:1.1;">{size}</div>'
            f'<div style="font-size:12.5px;color:{MUTED};margin:2px 0 8px;">{sys_}</div>'
            f'<div style="font-size:14px;">{txt}</div></div>')
    return '<div style="display:flex;flex-wrap:wrap;gap:12px;">' + "".join(out) + "</div>"

def table(rows):
    tr = "".join(
        f'<tr><td style="padding:8px 12px;border-bottom:1px solid {LINE};background:{SOFT};width:38%;font-weight:bold;">{a}</td>'
        f'<td style="padding:8px 12px;border-bottom:1px solid {LINE};">{b}</td></tr>' for a, b in rows)
    return f'<table style="border-collapse:collapse;width:100%;font-size:14px;border:1px solid {LINE};">{tr}</table>'

def steps(items):
    out = []
    for i, t in enumerate(items, 1):
        out.append(
            f'<div style="margin:0 0 8px;"><span style="display:inline-block;width:26px;height:26px;line-height:26px;text-align:center;'
            f'background:{ACCENT};color:#fff;border-radius:50%;font-weight:bold;font-size:13px;margin-right:9px;">{i}</span>{t}</div>')
    return "".join(out)

def two_col(left_title, left_items, right_title, right_items, left_color="#1b7f4b", right_color="#a33a3a"):
    def box(title, items, color, mark):
        li = "".join(f'<div style="margin:0 0 5px;"><b style="color:{color};">{mark}</b> {x}</div>' for x in items)
        return (f'<div style="flex:1 1 240px;box-sizing:border-box;'
                f'border:1px solid {LINE};border-radius:10px;padding:12px 14px;"><div style="font-weight:bold;margin:0 0 8px;">{title}</div>{li}</div>')
    return '<div style="display:flex;flex-wrap:wrap;gap:12px;">' + box(left_title, left_items, left_color, "✓") + box(right_title, right_items, right_color, "✗") + "</div>"

def faq(items):
    out = []
    for q, a in items:
        out.append(f'<div style="margin:0 0 12px;"><div style="font-weight:bold;">{q}</div>'
                   f'<div style="color:{MUTED};">{a}</div></div>')
    return "".join(out)

def small(t):
    return f'<div style="font-size:11.5px;color:{MUTED};margin:22px 0 0;padding-top:10px;border-top:1px solid {LINE};">{t}</div>'

DE = wrap(
    hero("Chromrohr, kompatibel mit USM Haller",
         "Länge wählbar: <b style=\"color:#fff;\">35 cm · 50 cm · 75 cm</b>",
         ["Neuware", "Versand kostenlos, mit Sendungsverfolgung", "30 Tage Rückgabe"])
    + notice("Wichtiger Hinweis:",
             "Kompatibles Ersatz- und Ergänzungsteil, <b>kein Originalteil</b> der USM U. Schärer Söhne AG. „USM“ und „USM Haller“ sind Marken "
             "der USM U. Schärer Söhne AG. Wir sind nicht mit USM verbunden; die Nennung dient ausschließlich der Angabe der Kompatibilität.")
    + h2("Welche Länge brauchst du?")
    + cards([
        ("35 cm", "Systemmaß 350 mm", "Typisch für Regale mit 35 cm Tiefe oder überall dort, wo 350 mm Systemmaß benötigt werden."),
        ("50 cm", "Systemmaß 500 mm", "Typisch für Regale mit 50 cm Tiefe oder überall dort, wo 500 mm Systemmaß benötigt werden."),
        ("75 cm", "Systemmaß 750 mm", "Typisch für Elemente mit 75 cm Breite oder überall dort, wo 750 mm Systemmaß benötigt werden."),
    ])
    + h2("Technische Daten")
    + table([
        ("Material", "Stahl, verchromt [PRÜFEN]"),
        ("Oberfläche", "Chrom, glänzend"),
        ("Durchmesser", "19 mm [PRÜFEN]"),
        ("Tatsächliche Länge", "35 cm: [PRÜFEN] mm · 50 cm: [PRÜFEN] mm · 75 cm: [PRÜFEN] mm"),
        ("Zustand", "Neu"),
    ])
    + f'<div style="font-size:12.5px;color:{MUTED};margin:6px 0 0;">Das Systemmaß ist der Abstand der Kugelmittelpunkte im Regal. Die tatsächliche Rohrlänge ist daher etwas kürzer und kann um wenige Millimeter abweichen.</div>'
    + h2("So prüfst du die Passform")
    + steps([
        "Miss am vorhandenen Regal den Abstand von Kugelmitte zu Kugelmitte.",
        "Wähle die passende Länge: 350, 500 oder 750 mm Systemmaß.",
        "Vergleiche den Rohrdurchmesser (19 mm) mit deinen vorhandenen Rohren.",
        "Setze Kugeln und Konnektoren vorsichtig ein.",
    ])
    + h2("Lieferumfang")
    + two_col("Enthalten", ["1 Rohr in der gewählten Länge"],
              "Nicht enthalten", ["Kugeln", "Konnektoren", "Füße, Tablare, Türen", "Werkzeug"])
    + h2("Häufige Fragen")
    + faq([
        ("Ist das ein Originalteil von USM?", "Nein. Es ist ein kompatibles Teil eines anderen Herstellers. Bitte vergleiche die Maße vor dem Kauf."),
        ("Passt es zu meinem vorhandenen Regal?", "Es ist für die Verwendung mit dem USM-Haller-System gedacht. Wegen unterschiedlicher Fertigungstoleranzen können wir eine 100-%ige Passgenauigkeit zu allen Originalteilen nicht zusichern. Bei Fragen schreib uns gern vor dem Kauf."),
        ("Sind Kugeln und Konnektoren dabei?", "Nein, verkauft wird nur das Rohr. Kugeln und Konnektoren sind nicht Teil dieses Angebots."),
        ("Warum sitzen die Konnektoren manchmal etwas fest?", "Chromoberflächen können herstellungsbedingt minimale Unebenheiten an den Rohrenden aufweisen. Konnektoren bitte vorsichtig einsetzen; die Funktion wird nicht beeinträchtigt."),
    ])
    + small("<b>Gewerblicher Verkäufer.</b> Rechnung mit ausgewiesener MwSt. auf Wunsch. Impressum, Widerrufsbelehrung und AGB findest du in unserem eBay-Shop.<br>"
            "<b>Hersteller / Verantwortliche Person (EU):</b> [FIRMA, ANSCHRIFT, E-MAIL – PRÜFEN]. Produkt: Chromrohr 35/50/75 cm (Art.-Nr. RH-USM-350 / -500 / -750). "
            "Kein Spielzeug. Rohrenden können scharfkantig sein – bitte vorsichtig handhaben.")
)

EN = wrap(
    hero("Chrome tube, compatible with USM Haller",
         "Choose your length: <b style=\"color:#fff;\">35 cm · 50 cm · 75 cm</b>",
         ["Brand new", "Free tracked shipping", "30-day returns"])
    + notice("Important notice:",
             "Compatible replacement / add-on part, <b>not an original part</b> by USM U. Schärer Söhne AG. “USM” and “USM Haller” are trademarks "
             "of USM U. Schärer Söhne AG. We are not affiliated with USM; the names are used solely to indicate compatibility.")
    + h2("Which length do you need?")
    + cards([
        ("35 cm", "System size 350 mm", "Typical for shelves with a depth of 35 cm, or anywhere a 350 mm system size is required."),
        ("50 cm", "System size 500 mm", "Typical for shelves with a depth of 50 cm, or anywhere a 500 mm system size is required."),
        ("75 cm", "System size 750 mm", "Typical for units with a width of 75 cm, or anywhere a 750 mm system size is required."),
    ])
    + h2("Specifications")
    + table([
        ("Material", "Chrome-plated steel [CHECK]"),
        ("Finish", "Chrome, glossy"),
        ("Diameter", "19 mm [CHECK]"),
        ("Actual length", "35 cm: [CHECK] mm · 50 cm: [CHECK] mm · 75 cm: [CHECK] mm"),
        ("Condition", "New"),
    ])
    + f'<div style="font-size:12.5px;color:{MUTED};margin:6px 0 0;">System size is the distance between the ball centres in the shelf. The actual tube length is therefore slightly shorter and may vary by a few millimetres.</div>'
    + h2("How to check the fit")
    + steps([
        "Measure the distance from ball centre to ball centre on your existing shelf.",
        "Choose the matching length: 350, 500 or 750 mm system size.",
        "Compare the tube diameter (19 mm) with your existing tubes.",
        "Insert balls and connectors carefully.",
    ])
    + h2("What's included")
    + two_col("Included", ["1 tube in the selected length"],
              "Not included", ["Balls", "Connectors", "Feet, shelves, doors", "Tools"])
    + h2("FAQ")
    + faq([
        ("Is this an original USM part?", "No. It is a compatible part made by another manufacturer. Please compare measurements before purchase."),
        ("Will it fit my existing shelf?", "It is intended for use with the USM Haller system. Due to differing manufacturing tolerances we cannot guarantee a 100% fit with all original parts. Feel free to contact us before buying."),
        ("Are balls and connectors included?", "No, only the tube is sold. Balls and connectors are not part of this listing."),
        ("Why can connectors feel a little tight?", "Chrome plating can leave minor irregularities at the tube ends. Please insert connectors carefully; function is not affected."),
    ])
    + small("<b>Business seller.</b> Invoice with VAT shown on request. Legal notice, withdrawal information and terms are available in our eBay shop.<br>"
            "<b>Manufacturer / responsible person (EU):</b> [COMPANY, ADDRESS, EMAIL – CHECK]. Product: chrome tube 35/50/75 cm (item no. RH-USM-350 / -500 / -750). "
            "Not a toy. Tube ends may be sharp – handle with care.")
)

DIVIDER = (f'<div style="text-align:center;margin:30px 0 22px;color:{MUTED};font-family:Arial,Helvetica,sans-serif;font-size:13px;letter-spacing:2px;">'
           f'──────  ENGLISH  ──────</div>')

code = ("<!-- ===== DEUTSCH ===== -->\n" + DE + "\n\n" + DIVIDER + "\n<!-- ===== ENGLISH ===== -->\n" + EN + "\n")
open("beschreibung-pro.html", "w", encoding="utf-8").write(code)
print(len(code), "Zeichen")

# Kopier-Seite mit Live-Vorschau (nur lokal, nicht für eBay)
esc_ta = code.replace("&", "&amp;").replace("</textarea", "&lt;/textarea")
srcdoc = html.escape(code, quote=True)
page = f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>eBay-Beschreibung Pro</title>
<style>
body{{font-family:Arial,Helvetica,sans-serif;max-width:1000px;margin:20px auto;padding:0 14px;background:#fff;color:#222}}
h1{{font-size:21px}} textarea{{width:100%;height:300px;font:12px Consolas,monospace;box-sizing:border-box}}
iframe{{width:100%;height:900px;border:1px solid #ddd;border-radius:8px}}
button{{padding:11px 18px;font-size:15px;border:0;border-radius:6px;background:#0064d2;color:#fff;cursor:pointer;margin:8px 0}}
.note{{background:#fff6d6;border:1px solid #e5cf7a;padding:10px 12px;border-radius:6px;font-size:14px}}
</style></head><body>
<h1>eBay-Beschreibung (Deutsch + English in einem Block)</h1>
<p class="note">Erst die <b>[PRÜFEN]</b>/<b>[CHECK]</b>-Stellen im Code ersetzen, dann in eBay unter „Beschreibung“ <b>„HTML-Code anzeigen“</b> aktivieren und einfügen. Der Code nutzt nur Inline-CSS, kein JavaScript und keine externen Links, wie eBay es verlangt.</p>
<button onclick="var t=document.getElementById('c');t.select();navigator.clipboard?navigator.clipboard.writeText(t.value):document.execCommand('copy');this.textContent='Kopiert!'">Code kopieren</button>
<textarea id="c" readonly>{esc_ta}</textarea>
<h2>Vorschau</h2>
<iframe sandbox srcdoc="{srcdoc}"></iframe>
</body></html>"""
open("kopieren.html", "w", encoding="utf-8").write(page)
