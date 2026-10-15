"""Bild 2: 5 Rohre nebeneinander (35/50/75 cm), je 1 Stanzloch mittig. Reines Python-Rendering, echte Inter-Schrift."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 2                      # Supersampling
W = H = 2000
LENGTHS = [75, 75, 50, 50, 35]      # cm, von oben nach unten
PX_PER_CM = 23.0
DIA = 124                  # Darstellungs-Durchmesser (nicht maßstäblich zur Länge)
GAP = 248
HOLE_D = 26
HOLE_GAP = 8.4 * PX_PER_CM               # Lochdurchmesser in der Darstellung
X0 = 100
Y0 = 580

font_h = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Bold.otf', 84 * S)
font_s = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Regular.otf', 44 * S)
font_l = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 46 * S)

# Hintergrund: weiß mit sanftem Verlauf
yy = np.linspace(0, 1, H * S)[:, None]
bg = 255 - 14 * yy ** 2
canvas = np.repeat(bg[:, :, None], W * S, axis=1).repeat(3, axis=2) if False else None
img = np.zeros((H * S, W * S, 3), np.float32)
img[:] = bg[:, :, None]


def env(phi):
    """Studio-Umgebung für Chrom: phi in [-pi, pi] (Spiegelrichtung), weich verlaufend."""
    v = 0.58 + 0.10 * np.cos(phi - 0.6)
    v += 0.40 * np.exp(-((phi - 1.0) / 0.42) ** 2)      # Softbox oben
    v += 0.30 * np.exp(-((phi + 0.8) / 0.34) ** 2)      # Aufheller unten
    v -= 0.46 * np.exp(-((phi - 0.05) / 0.20) ** 2)     # Horizont
    v -= 0.30 * np.exp(-((phi + 1.9) / 0.30) ** 2)
    v -= 0.26 * np.exp(-((phi - 2.5) / 0.26) ** 2)
    return np.clip(v, 0.08, 1.0)


def draw_tube(y_center, length_cm):
    L = int(length_cm * PX_PER_CM * S)
    D = DIA * S
    x0 = X0 * S
    yc = int(y_center * S)
    ys = np.arange(-D // 2 - 6 * S, D // 2 + 6 * S)
    xs = np.arange(L)
    v = np.clip(ys / (D / 2), -1.0, 1.0)
    inside = (np.abs(ys) <= D / 2)
    theta = np.arcsin(v)
    phi = 2 * theta
    shade = env(phi)
    # leichte Querstreifen entlang der Rohrlänge (Verlauf in x)
    xr = xs / L
    xmod = 1 + 0.06 * np.sin(xr * 9 + 1.0) + 0.05 * np.exp(-((xr - 0.18) / 0.05) ** 2)
    tube = shade[:, None] * xmod[None, :]
    tube = np.clip(tube, 0, 1)
    col = np.stack([tube * 236 + 14, tube * 238 + 15, tube * 244 + 11], axis=2)
    # Schatten
    sh_y = yc + int(D * 0.66)
    shadow = np.zeros((H * S, W * S), np.float32)
    shadow[sh_y - int(D * 0.09):sh_y + int(D * 0.09), x0 + int(L * 0.01):x0 + int(L * 0.99)] = 1
    shadow = np.array(Image.fromarray((shadow * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(9 * S))) / 255.0
    img[:] = img * (1 - 0.22 * shadow[:, :, None])
    # Rohr einsetzen (mit weicher Kante)
    for k, y in enumerate(ys):
        if not inside[k]:
            continue
        edge = min(1.0, (D / 2 - abs(y)) / 1.5)
        row = col[k]
        img[yc + y, x0:x0 + L] = img[yc + y, x0:x0 + L] * (1 - edge) + row * edge
    # Rohrenden: schmale Fase
    for xe, sign in ((x0, 1), (x0 + L - 1, -1)):
        for d in range(5 * S):
            a = 0.35 * (1 - d / (5 * S))
            for y in range(-D // 2, D // 2):
                img[yc + y, xe + sign * d] = img[yc + y, xe + sign * d] * (1 - a) + 255 * a * (0.9 if d < 2 * S else 0.5)
    # offenes Rohrende links (Ellipse)
    rx, ry = 0.17 * D, D / 2
    for dy in range(-int(ry) - 2, int(ry) + 3):
        for dx in range(-int(rx) - 2, int(rx) + 3):
            e = (dx / rx) ** 2 + (dy / ry) ** 2
            px, py = x0 + dx, yc + dy
            if e <= 1.0:
                if e <= 0.62:
                    t = (dy / ry + 1) / 2
                    img[py, px] = 12 + 40 * t * t
                else:
                    img[py, px] = 232 - 40 * abs(dy / ry)
    # zwei Stanzlöcher mittig (Draufsicht), Abstand wie im Referenzbild ca. 8,4 cm
    mid = x0 + L // 2
    for off in (-HOLE_GAP * S / 2, HOLE_GAP * S / 2):
        cx = int(mid + off)
        r = HOLE_D * S / 2
        for dy in range(-int(r) - 8 * S, int(r) + 8 * S):
            for dx in range(-int(r) - 8 * S, int(r) + 8 * S):
                dist = (dx * dx + dy * dy) ** 0.5
                if dist <= r + 4 * S:
                    py, px = yc + dy, cx + dx
                    if dist <= r:
                        # Innenseite dunkel, unten innerer Rand heller
                        t = (dy + r) / (2 * r)
                        base = 14 + 52 * max(0.0, t - 0.55) / 0.45
                        img[py, px] = base
                    else:
                        # glänzender Rand des Lochs
                        a = 1 - (dist - r) / (4 * S)
                        img[py, px] = img[py, px] * (1 - 0.5 * a) + 250 * 0.5 * a

    cx = mid
    return cx / S, x0 / S + L / S


pil_text_layer = []
centers = []
for i, cm in enumerate(LENGTHS):
    yc = Y0 + i * GAP
    cx, xend = draw_tube(yc, cm)
    centers.append((yc, cx, xend, cm))

out = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
d = ImageDraw.Draw(out)
INK = (34, 34, 34)
MUTED = (96, 104, 114)
NAVY = (31, 58, 95)

d.text((X0 * S, 112 * S), '3 Längen, Stanzlöcher mittig', font=font_h, fill=NAVY)
d.text((X0 * S, 222 * S), 'Rohr verchromt · Systemmaß 350 / 500 / 750 mm', font=font_s, fill=MUTED)

for yc, cx, xend, cm in centers:
    lab = f'{cm} cm'
    d.text((X0 * S, (yc - DIA // 2 - 52) * S), lab, font=font_l, fill=INK)

# Callout zum ersten Loch
yc, cx, xend, cm = centers[0]
tx, ty = cx + 70, yc - DIA // 2 - 105
d.line([(cx * S, (yc - HOLE_D / 2 - 4) * S), (tx * S, (ty + 38) * S)], fill=NAVY, width=3 * S)
d.text((tx * S + 12 * S, ty * S), '2 Stanzlöcher mittig', font=font_l, fill=NAVY)

out = out.resize((W, H), Image.LANCZOS)
out.save('bild2-rohre.png')
out.convert('RGB').save('bild2-rohre.jpg', quality=92)
print('ok')
