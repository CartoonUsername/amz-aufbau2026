# Erzeugt eine Kopier-Seite (Code + Button + Desktop- und Handy-Vorschau) aus einer Beschreibungsdatei.
# Aufruf: python3 build_kopieren.py beschreibung-klein-82.html kopieren-klein-82.html
import html, sys
src, out = sys.argv[1], sys.argv[2]
code = open(src, encoding="utf-8").read()
esc_ta = code.replace("&", "&amp;").replace("</textarea", "&lt;/textarea")
srcdoc = html.escape(code, quote=True)
page = f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>eBay-Beschreibung zum Kopieren</title>
<style>
body{{font-family:Arial,Helvetica,sans-serif;max-width:1000px;margin:20px auto;padding:0 14px;background:#fff;color:#222}}
h1{{font-size:21px}} textarea{{width:100%;height:300px;font:12px Consolas,monospace;box-sizing:border-box}}
.row{{display:flex;gap:20px;flex-wrap:wrap;align-items:flex-start}}
iframe{{border:1px solid #ddd;border-radius:8px;background:#fff}}
.desk{{flex:1 1 560px;height:900px}} .mob{{width:390px;height:800px}}
button{{padding:11px 18px;font-size:15px;border:0;border-radius:6px;background:#0064d2;color:#fff;cursor:pointer;margin:8px 0}}
.note{{background:#fff6d6;border:1px solid #e5cf7a;padding:10px 12px;border-radius:6px;font-size:14px}}
</style></head><body>
<h1>eBay-Beschreibung (Deutsch + English in einem Block)</h1>
<p class="note">In eBay unter „Beschreibung“ <b>„HTML-Code anzeigen“</b> aktivieren und den Code einfügen.</p>
<button onclick="var t=document.getElementById('c');t.select();navigator.clipboard?navigator.clipboard.writeText(t.value):document.execCommand('copy');this.textContent='Kopiert!'">Code kopieren</button>
<textarea id="c" readonly>{esc_ta}</textarea>
<h2>Vorschau Desktop und Handy</h2>
<div class="row"><iframe class="desk" sandbox srcdoc="{srcdoc}"></iframe><iframe class="mob" sandbox srcdoc="{srcdoc}"></iframe></div>
</body></html>"""
open(out, "w", encoding="utf-8").write(page)
