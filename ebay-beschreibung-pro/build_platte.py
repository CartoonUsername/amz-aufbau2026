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
    title("Beschichtete Schreibtischplatte, kompatibel mit USM Haller", "Farbe wählbar: <b>Weiß/Grau · Schwarz (Holzoptik)</b>",
          "Neu")
    + notice("Wichtiger Hinweis:", "Dieses Produkt stammt von einem Drittanbieter und ist <b>kein Original</b> von USM Haller. „USM Haller“ ist eine geschützte Marke der USM U. Schärer Söhne AG und wird hier ausschließlich genannt, um die Kompatibilität zu beschreiben. Wir sind kein Vertriebspartner von USM. Original-Teile erhältst du beim Hersteller selbst oder bei dessen autorisierten Händlern.")
    + table(["Variante", "Länge × Breite (Außenmaß)", "Stärke", "Gewicht"], [("Größe 1", "ca. 150 × 75 cm (1500 × 750 mm)", "ca. 20 mm", "ca. 15 kg"), ("Größe 2", "ca. 175 × 75 cm (1750 × 750 mm)", "ca. 20 mm", "ca. 19,6 kg"), ("Größe 3", "ca. 200 × 100 cm (2000 × 1000 mm)", "ca. 20 mm", "ca. 29 kg")])
    + kv([("Farben", "Weiß/Grau · Schwarz (Holzoptik)"), ("Material", "Spanplatte, beschichtet"), ("Oberfläche Weiß/Grau", "glatt"), ("Oberfläche Schwarz", "Holzoptik mit Holzstruktur"), ("Eckaussparungen", "an allen vier Ecken für die Rohre"), ("Kanten", "abgeschrägt"), ("Zustand", "Neu")])
    + p("Bitte vergleiche Länge, Breite und die Eckaussparungen vor dem Kauf mit deinem Tischgestell. Eine 100-%ige Passgenauigkeit zu allen Originalteilen können wir nicht zusichern, geringe Fertigungstoleranzen sind möglich.", "12.5px", MUTED, "8px")
    + p("<b>Lieferumfang:</b> 1 Schreibtischplatte in der gewählten Größe und Farbe. <b>Nicht enthalten:</b> Rohre, Kugeln, Konnektoren, Füße, Tischgestell, Werkzeug.")
    + p("<b>Größere Mengen oder andere Maße:</b> auf Anfrage möglich. Bitte senden Sie uns dazu eine Nachricht.", "13px", "#222222", "6px")
)

EN = wrap(
    title("Coated desk top, compatible with USM Haller", "Choose your colour: <b>White/grey · Black (wood look)</b>",
          "New")
    + notice("Important notice:", "This product comes from a third-party supplier and is <b>not an original</b> USM Haller part. “USM Haller” is a protected trademark of USM U. Schärer Söhne AG and is mentioned here only to describe compatibility. We are not a distributor of USM. Original parts are available from the manufacturer itself or from its authorised dealers.")
    + table(["Variant", "Length × width (outer dimensions)", "Thickness", "Weight"], [("Size 1", "ca. 150 × 75 cm (1500 × 750 mm)", "ca. 20 mm", "ca. 15 kg"), ("Size 2", "ca. 175 × 75 cm (1750 × 750 mm)", "ca. 20 mm", "ca. 19.6 kg"), ("Size 3", "ca. 200 × 100 cm (2000 × 1000 mm)", "ca. 20 mm", "ca. 29 kg")])
    + kv([("Colours", "White/grey · Black (wood look)"), ("Material", "Coated chipboard"), ("Finish white/grey", "smooth"), ("Finish black", "wood look with wood-grain texture"), ("Corner cut-outs", "at all four corners for the tubes"), ("Edges", "bevelled"), ("Condition", "New")])
    + p("Please compare length, width and the corner cut-outs with your table frame before purchase. We cannot guarantee a 100% fit with all original parts; minor manufacturing tolerances are possible.", "12.5px", MUTED, "8px")
    + p("<b>Included:</b> 1 desk top in the selected size and colour. <b>Not included:</b> tubes, balls, connectors, feet, table frame, tools.")
    + p("<b>Larger quantities or other sizes:</b> available on request. Please send us a message.", "13px", "#222222", "6px")
)

code = ("<!-- ===== DEUTSCH ===== -->\n" + bar("Deutsch") + "\n" + DE + "\n\n<div style=\"height:18px;\"></div>\n"
        "<!-- ===== ENGLISH ===== -->\n" + bar("English") + "\n" + EN + "\n")
open("beschreibung-platte.html", "w", encoding="utf-8").write(code)
print(len(code))
