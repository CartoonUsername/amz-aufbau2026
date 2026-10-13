# Erzeugt kopieren.html (Vorschau + Kopier-Button) aus der finalen beschreibung-pro.html.
# Die Beschreibung selbst ist von Hand final gepflegt (Inline-CSS, kein JS, keine externen Links).
import html
code = open("beschreibung-pro.html", encoding="utf-8").read()
esc_ta = code.replace("&", "&amp;").replace("</textarea", "&lt;/textarea")
srcdoc = html.escape(code, quote=True)
page = f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>eBay-Beschreibung Final</title>
<style>
body{{font-family:Arial,Helvetica,sans-serif;max-width:1000px;margin:20px auto;padding:0 14px;background:#fff;color:#222}}
h1{{font-size:21px}} textarea{{width:100%;height:300px;font:12px Consolas,monospace;box-sizing:border-box}}
iframe{{width:100%;height:900px;border:1px solid #ddd;border-radius:8px}}
button{{padding:11px 18px;font-size:15px;border:0;border-radius:6px;background:#0064d2;color:#fff;cursor:pointer;margin:8px 0}}
.note{{background:#fff6d6;border:1px solid #e5cf7a;padding:10px 12px;border-radius:6px;font-size:14px}}
</style></head><body>
<h1>eBay-Beschreibung (Deutsch + English in einem Block)</h1>
<p class="note">In eBay unter „Beschreibung“ <b>„HTML-Code anzeigen“</b> aktivieren und den Code einfügen.</p>
<button onclick="var t=document.getElementById('c');t.select();navigator.clipboard?navigator.clipboard.writeText(t.value):document.execCommand('copy');this.textContent='Kopiert!'">Code kopieren</button>
<textarea id="c" readonly>{esc_ta}</textarea>
<h2>Vorschau</h2>
<iframe sandbox srcdoc="{srcdoc}"></iframe>
</body></html>"""
open("kopieren.html", "w", encoding="utf-8").write(page)
