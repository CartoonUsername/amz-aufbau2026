"""Hauptbild 75 cm: Basisbild (hauptbild-basis.webp, unverändert) + ein Stanzloch pro Rohr.
Positionen und Größe der Löcher exakt nach der Vorgabe-Markierung (schwarze Punkte, Durchmesser ca. 54 px bei 2000 px)."""
import numpy as np
from PIL import Image

SS = 6
base = Image.open('hauptbild-basis.webp').convert('RGB')
W, H = base.size
arr = np.array(base).astype(np.float32)

# Mittelpunkte der Markierungen (1250-px-Vorlage x 1,6)
HOLES = [(774.6, 250.2), (600.8, 367.2), (415.0, 499.7), (214.9, 628.3), (-1.0, 790.7)]
R = 27.2          # Lochradius in Pixel (2000 px)


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def paint(cx, cy):
    global arr
    pad = int(R) + 10
    x0, y0 = int(round(cx)) - pad, int(round(cy)) - pad
    size = 2 * pad
    g = (np.arange(size * SS) + 0.5) / SS
    xx, yy = np.meshgrid(g, g)
    px = xx + x0 - cx      # relativ zum Lochmittelpunkt
    py = yy + y0 - cy
    r = np.sqrt(px ** 2 + py ** 2)

    # Innenkreis (Öffnung) leicht nach unten rechts verschoben -> sichtbare Schnittkante oben links
    ox, oy = 2.4, 3.4
    ri = np.sqrt((px - ox) ** 2 + (py - oy) ** 2)
    Ri = R - 4.6

    col = np.zeros(px.shape + (3,), np.float32)
    alpha = np.zeros(px.shape, np.float32)

    # 1) Kontaktschatten außen (sanft)
    ao = np.clip(1 - (r - R) / 7.0, 0, 1) ** 2 * (r > R)
    # 2) Schnittkante / Rand (Chrom, hell oben links, dunkler unten rechts)
    ang = np.arctan2(py, px)
    lit = 0.5 + 0.5 * np.cos(ang - np.deg2rad(-135))            # 1 oben links
    rim_v = 150 + 95 * lit
    rim_v = np.where(r > R - 1.1, rim_v * 0.55 + 40, rim_v)     # feine dunkle Außenlinie
    # 3) Öffnung: Innenwand des Rohres (gegenüberliegende Seite), sonst fast schwarz
    t = np.clip((py - oy) / Ri, -1, 1)
    inner_v = 6 + 58 * smoothstep(-0.2, 1.0, t) ** 1.6 + 10 * smoothstep(0.2, 1.0, ri / Ri)
    inner_v *= 1 - 0.55 * smoothstep(0.75, 1.0, ri / Ri) * (1 - smoothstep(-0.6, 0.4, t))  # Kante oben dunkler
    inside = ri <= Ri
    ring = (r <= R) & ~inside

    v = np.where(inside, inner_v, rim_v)
    col[..., 0] = v; col[..., 1] = v; col[..., 2] = v * 1.01
    a_disc = smoothstep(R + 0.8, R - 0.8, r)
    alpha = a_disc
    # Übergang Öffnung/Rand antialiasen
    blend = smoothstep(Ri + 0.8, Ri - 0.8, ri)
    v = rim_v * (1 - blend) + inner_v * blend
    col[..., 0] = v; col[..., 1] = v; col[..., 2] = v * 1.01

    # runterskalieren (Supersampling)
    def down(a):
        return a.reshape(size, SS, size, SS, *a.shape[2:]).mean(axis=(1, 3))
    col_d = down(col)
    al_d = down(alpha)
    ao_d = down(ao.astype(np.float32))

    # in Bild einsetzen (mit Clipping an Bildrändern)
    xs0, ys0 = max(x0, 0), max(y0, 0)
    xs1, ys1 = min(x0 + size, W), min(y0 + size, H)
    sx0, sy0 = xs0 - x0, ys0 - y0
    sx1, sy1 = sx0 + (xs1 - xs0), sy0 + (ys1 - ys0)
    reg = arr[ys0:ys1, xs0:xs1]
    reg *= (1 - 0.28 * ao_d[sy0:sy1, sx0:sx1, None])
    a_ = al_d[sy0:sy1, sx0:sx1, None]
    arr[ys0:ys1, xs0:xs1] = reg * (1 - a_) + col_d[sy0:sy1, sx0:sx1] * a_


for cx, cy in HOLES:
    paint(cx, cy)

out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
out.save('hauptbild-75cm-loch.png')
out.save('hauptbild-75cm-loch.jpg', quality=94)
print('ok')
