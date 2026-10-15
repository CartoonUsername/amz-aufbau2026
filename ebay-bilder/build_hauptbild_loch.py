"""Hauptbild 75 cm: Basisbild (hauptbild-basis.webp) + ein kleines Stanzloch pro Rohr, mittig auf der Oberseite."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SS = 4
base = Image.open('hauptbild-basis.webp').convert('RGB')
W, H = base.size

ENDS = [(840, 1630), (1090, 1480), (1326, 1344), (1560, 1206), (1790, 1076)]   # Mittelpunkte der Rohröffnungen
DIR = (-0.825, -0.565)                                                           # Rohrachse (nach oben links)
PERP = 48                                                                        # Korrektur senkrecht zur Achse (Perspektive), nach oben rechts
DIST = 800                                                                       # Abstand Öffnung -> Loch
HOLE_A, HOLE_B = 30, 24                                                          # Halbachsen (längs / quer)
ANG = math.degrees(math.atan2(DIR[1], DIR[0]))

layer = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
shadow = Image.new('L', (W, H), 0)
sd = ImageDraw.Draw(shadow)

def hole(cx, cy, ang):
    size = 140 * SS
    t = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    ar = np.zeros((size, size, 4), np.float32)
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    x = xx - size / 2
    y = yy - size / 2
    a, b = HOLE_A * SS, HOLE_B * SS
    e = (x / a) ** 2 + (y / b) ** 2
    # Rand (glänzende Lochkante)
    rim = (e <= 1.30) & (e > 0.98)
    inside = e <= 0.98
    # Innenseite: oben fast schwarz, unten (Innenwand) etwas heller
    t_ = np.clip((y / b + 1) / 2, 0, 1)
    inner = 10 + 55 * (t_ ** 2.2) * np.clip(1 - e, 0, 1) ** 0.4
    ar[inside, :3] = inner[inside][:, None]
    ar[inside, 3] = 255
    # Kante: hell, oben dunkler (Schattenseite)
    rv = 215 - 60 * (1 - t_)
    ar[rim, :3] = rv[rim][:, None]
    ar[rim, 3] = 255
    # weicher Übergang
    im = Image.fromarray(np.clip(ar, 0, 255).astype(np.uint8), 'RGBA')
    im = im.rotate(-ang, resample=Image.BICUBIC, expand=False)
    layer.alpha_composite(im, (int(cx * SS - size / 2), int(cy * SS - size / 2)))

# Rohrmitten (gemessen): Schnitt quer durch alle Rohre; Mitte = Mitte zwischen den Rohrgrenzen
# (rechte Silhouette, drei Fugen zwischen den Rohren). Die dunkle Reflexionsbahn liegt bei jedem Rohr gleich dicht an dieser Mitte.
VP = (-6974.0, -5100.0)    # Fluchtpunkt der Rohrachsen (aus den Außenkanten)
HOLES = [(196, 1056), (439, 916), (664, 787), (879, 664), (1085, 545)]
for (cx, cy) in HOLES:
    ang = math.degrees(math.atan2(cy - VP[1], cx - VP[0]))
    hole(cx, cy, ang + 180)
    sd.ellipse([cx - 44, cy - 38, cx + 44, cy + 38], fill=255)

shadow = shadow.filter(ImageFilter.GaussianBlur(14))
sh = np.array(shadow).astype(np.float32) / 255.0
arr = np.array(base).astype(np.float32)
arr *= (1 - 0.22 * sh[..., None])
base2 = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert('RGBA')
lay = layer.resize((W, H), Image.LANCZOS)
base2.alpha_composite(lay)
out = base2.convert('RGB')
out.save('hauptbild-75cm-loch.png')
out.save('hauptbild-75cm-loch.jpg', quality=93)
print('ok')
