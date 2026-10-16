"""A+-Bilder für das Chromrohr (Amazon). Ausgabe: banner, col1-4, passform, wide (JPG)."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

IB = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'
IS = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
IR = '/usr/share/fonts/opentype/inter/Inter-Regular.otf'
NAVY = (31, 58, 95); INK = (34, 34, 34); MUTED = (96, 104, 114)
base = Image.open('hauptbild-basis.webp').convert('RGB')


def font(p, s):
    return ImageFont.truetype(p, s)


def save(im, name, q=93):
    im.convert('RGB').save(name + '.jpg', quality=q)


def bgrad(w, h, a=246, b=232):
    y = np.linspace(0, 1, h)[:, None]
    v = (a - (a - b) * y ** 1.3) * np.ones((1, w))
    return Image.fromarray(np.stack([v, v, v + 1], -1).clip(0, 255).astype(np.uint8))


def env(phi):
    v = 0.58 + 0.12 * np.cos(phi - 0.6)
    v += 0.40 * np.exp(-((phi - 1.0) / 0.40) ** 2)
    v += 0.30 * np.exp(-((phi + 0.85) / 0.30) ** 2)
    v -= 0.46 * np.exp(-((phi - 0.05) / 0.18) ** 2)
    v -= 0.28 * np.exp(-((phi + 1.9) / 0.28) ** 2)
    v -= 0.24 * np.exp(-((phi - 2.5) / 0.24) ** 2)
    return np.clip(v, 0.08, 1.0)


def tube_strip(L, D):
    """horizontales Chromrohr als RGB-Array (D x L)."""
    ys = (np.arange(D) + 0.5 - D / 2) / (D / 2)
    th = np.arcsin(np.clip(ys, -1, 1))
    sh = env(2 * th)[:, None] * np.ones((1, L))
    sh *= 1 + 0.04 * np.sin(np.linspace(0, 8, L))[None, :]
    return np.stack([sh * 236 + 14, sh * 238 + 15, sh * 244 + 11], -1).clip(0, 255)


def paste_tube(im, x, y, L, D, openend=True):
    arr = np.array(im).astype(np.float32)
    strip = tube_strip(L, D)
    # Silhouette (abgerundete Kanten durch Alpha)
    yy = (np.arange(D) + 0.5 - D / 2) / (D / 2)
    al = np.clip((1 - np.abs(yy)) * D / 2 / 1.5, 0, 1)[:, None] * np.ones((1, L))
    # Schatten
    sh = Image.new('L', im.size, 0)
    ImageDraw.Draw(sh).rectangle([x + 6, y + D * 0.78, x + L - 6, y + D * 1.02], fill=255)
    sh = np.array(sh.filter(ImageFilter.GaussianBlur(D * 0.14))).astype(np.float32) / 255
    arr *= (1 - 0.22 * sh[..., None])
    reg = arr[y:y + D, x:x + L]
    arr[y:y + D, x:x + L] = reg * (1 - al[..., None]) + strip * al[..., None]
    out = Image.fromarray(arr.clip(0, 255).astype(np.uint8))
    if openend:
        d = ImageDraw.Draw(out)
        rx = D * 0.17
        d.ellipse([x - rx, y, x + rx, y + D], fill=(226, 228, 232))
        d.ellipse([x - rx * 0.62, y + D * 0.09, x + rx * 0.62, y + D * 0.91], fill=(14, 14, 16))
    return out


# ---------- Banner 1940x1200 ----------
b = base.crop((0, 380, 2000, 380 + 1237)).resize((1940, 1200), Image.LANCZOS)
save(b, 'banner')

# ---------- Spalte 1: drei Längen ----------
S = 2
W = H = 440 * S
im = bgrad(W, H)
D = 62 * S
pxcm = 4.1 * S
lengths = [75, 50, 35]
y0 = 118 * S
for i, cm in enumerate(lengths):
    L = int(cm * pxcm)
    im = paste_tube(im, 40 * S, y0 + i * 100 * S, L, D)
d = ImageDraw.Draw(im)
f = font(IS, 22 * S)
for i, cm in enumerate(lengths):
    L = int(cm * pxcm)
    d.text((40 * S + L + 14 * S, y0 + i * 100 * S + D / 2 - 15 * S), f'{cm} cm', font=f, fill=INK)
d.text((40 * S, 36 * S), 'Drei Längen', font=font(IB, 34 * S), fill=NAVY)
d.text((40 * S, 78 * S), 'Systemmaß 350 · 500 · 750 mm', font=font(IR, 19 * S), fill=MUTED)
save(im.resize((440, 440), Image.LANCZOS) if False else im, 'col1')

# ---------- Spalte 2: Nahaufnahme Rohrenden ----------
c = base.crop((1090, 900, 1770, 1580)).resize((880, 880), Image.LANCZOS)
save(c, 'col2')

# ---------- Spalte 3: Querschnitt mit Maßen ----------
W = H = 880
S3 = 2
im = bgrad(W * S3, H * S3)
d = ImageDraw.Draw(im)
cx, cy = 440 * S3, 380 * S3
R_o = 235 * S3
R_i = R_o * (1 - 2 * 1.2 / 19)
# Ring (Chrom-Verlauf)
ring = np.zeros((H * S3, W * S3, 3), np.float32)
yy, xx = np.mgrid[0:H * S3, 0:W * S3].astype(np.float32)
rr = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
ang = np.arctan2(yy - cy, xx - cx)
for ch, v0 in enumerate((0, 0, 0)):
    pass
shade = 0.62 + 0.30 * np.cos(ang + 2.4) + 0.12 * np.cos(2 * ang - 0.6)
shade = np.clip(shade, 0.15, 1)
ringcol = np.stack([shade * 236 + 14, shade * 238 + 15, shade * 244 + 11], -1)
bore = np.stack([np.full_like(rr, 18) + 40 * np.clip((yy - cy) / R_i, 0, 1) ** 2] * 3, -1)
a_ring = np.clip((R_o - rr) / 2, 0, 1)
a_bore = np.clip((R_i - rr) / 2, 0, 1)
arr = np.array(im).astype(np.float32)
arr = arr * (1 - a_ring[..., None]) + ringcol * a_ring[..., None]
arr = arr * (1 - a_bore[..., None]) + bore * a_bore[..., None]
im = Image.fromarray(arr.clip(0, 255).astype(np.uint8))
d = ImageDraw.Draw(im)
# Durchmesser-Bemaßung
yd = cy + R_o + 60 * S3
def arrow(d, p0, p1, col, w=3 * S3, h=16 * S3):
    d.line([p0, p1], fill=col, width=w)
    for (a, bq) in ((p0, p1), (p1, p0)):
        ang_ = math.atan2(bq[1] - a[1], bq[0] - a[0])
        pts = [a, (a[0] + h * math.cos(ang_ + 0.3), a[1] + h * math.sin(ang_ + 0.3)), (a[0] + h * math.cos(ang_ - 0.3), a[1] + h * math.sin(ang_ - 0.3))]
        d.polygon(pts, fill=col)
d.line([(cx - R_o, cy + 4 * S3), (cx - R_o, yd + 12 * S3)], fill=MUTED, width=2 * S3)
d.line([(cx + R_o, cy + 4 * S3), (cx + R_o, yd + 12 * S3)], fill=MUTED, width=2 * S3)
arrow(d, (cx - R_o, yd), (cx + R_o, yd), NAVY)
f = font(IB, 50 * S3)
t = 'Ø ca. 19 mm'
bb = d.textbbox((0, 0), t, font=f)
d.text((cx - (bb[2] - bb[0]) / 2, yd + 26 * S3), t, font=f, fill=NAVY)
# Wandstärke
wx, wy = cx + (R_o + R_i) / 2 * math.cos(-0.5), cy + (R_o + R_i) / 2 * math.sin(-0.5)
d.line([(wx, wy), (wx + 30 * S3, wy - 70 * S3)], fill=NAVY, width=3 * S3)
d.ellipse([wx - 5 * S3, wy - 5 * S3, wx + 5 * S3, wy + 5 * S3], fill=NAVY)
f2 = font(IS, 28 * S3)
t = 'Wandstärke ca. 1,2 mm'
bb = d.textbbox((0, 0), t, font=f2)
d.text((wx + 30 * S3 - (bb[2] - bb[0]) / 2 + 40 * S3, wy - 70 * S3 - 44 * S3), t, font=f2, fill=NAVY)
save(im.resize((880, 880), Image.LANCZOS), 'col3')

# ---------- Spalte 4: Systemmaß (Kugelmitte zu Kugelmitte) ----------
S4 = 2
W = H = 880
im = bgrad(W * S4, H * S4)
x1, x2 = 130 * S4, 750 * S4
yc = 440 * S4
Rb = 78 * S4
Dt = 62 * S4
# Rohr (unter den Kugeln)
tube_L = x2 - x1
im = paste_tube(im, x1, int(yc - Dt / 2), int(tube_L), int(Dt), openend=False)
# Kugeln
arr = np.array(im).astype(np.float32)
yy, xx = np.mgrid[0:H * S4, 0:W * S4].astype(np.float32)
for bx in (x1, x2):
    nx = (xx - bx) / Rb; ny = (yy - yc) / Rb
    r2 = nx ** 2 + ny ** 2
    m = r2 <= 1
    nz = np.sqrt(np.clip(1 - r2, 0, 1))
    # Spiegelrichtung aus Kamera (0,0,1)
    rx_, ry_, rz_ = 2 * nz * nx, 2 * nz * ny, 2 * nz * nz - 1
    el = np.arcsin(np.clip(-ry_, -1, 1))
    v = env(el * 1.2 + 0.25 * rx_)
    col = np.stack([v * 236 + 14, v * 238 + 15, v * 244 + 11], -1)
    al = np.clip((1 - np.sqrt(r2)) * Rb / 1.5, 0, 1)
    arr = arr * (1 - al[..., None]) + col * al[..., None]
im = Image.fromarray(arr.clip(0, 255).astype(np.uint8))
d = ImageDraw.Draw(im)
# Mittellinien
for bx in (x1, x2):
    d.line([(bx, yc - Rb - 20 * S4), (bx, yc - Rb - 150 * S4)], fill=MUTED, width=2 * S4)
arrow(d, (x1, yc - Rb - 110 * S4), (x2, yc - Rb - 110 * S4), NAVY, w=3 * S4, h=18 * S4)
f = font(IB, 40 * S4)
t = 'Systemmaß 750 mm'
bb = d.textbbox((0, 0), t, font=f)
d.text(((x1 + x2) / 2 - (bb[2] - bb[0]) / 2, yc - Rb - 108 * S4 - 62 * S4), t, font=f, fill=NAVY)
f = font(IR, 26 * S4)
t = 'Abstand der Achsmitten (Kugelmitte – Kugelmitte)'
bb = d.textbbox((0, 0), t, font=f)
d.text(((x1 + x2) / 2 - (bb[2] - bb[0]) / 2, yc - Rb - 108 * S4 + 14 * S4), t, font=f, fill=MUTED)
# effektive Länge
ex1, ex2 = x1 + 9 * (x2 - x1) / 750, x2 - 9 * (x2 - x1) / 750
yl = yc + Rb + 100 * S4
for ex in (ex1, ex2):
    d.line([(ex, yc + Dt / 2 + 6 * S4), (ex, yl + 14 * S4)], fill=MUTED, width=2 * S4)
arrow(d, (ex1, yl), (ex2, yl), INK, w=3 * S4, h=18 * S4)
f = font(IB, 36 * S4)
t = 'effektive Länge ca. 732 mm'
bb = d.textbbox((0, 0), t, font=f)
d.text(((x1 + x2) / 2 - (bb[2] - bb[0]) / 2, yl + 26 * S4), t, font=f, fill=INK)
f = font(IR, 26 * S4)
t = 'Systemmaß minus ca. 18 mm'
bb = d.textbbox((0, 0), t, font=f)
d.text(((x1 + x2) / 2 - (bb[2] - bb[0]) / 2, yl + 76 * S4), t, font=f, fill=MUTED)
save(im.resize((880, 880), Image.LANCZOS), 'col4')

# ---------- Passform: echtes Foto ----------
p = Image.open('foto-rohre-1799.jpg').convert('RGB')
w, h = p.size
sq = p.crop((200, 0, 200 + 640, 640)).resize((900, 900), Image.LANCZOS)
save(sq, 'passform')

# ---------- Breites Bild 1940x600 (Textfeld rechts von Amazon) ----------
wd = base.crop((0, 120, 2000, 120 + 619)).resize((1940, 600), Image.LANCZOS)
save(wd, 'wide')
print('ok')
