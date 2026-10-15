"""Hauptbild: 5 verchromte Rohre, diagonal, offene Enden, ohne Löcher. Analytisches Ray-Casting (numpy)."""
import numpy as np
from PIL import Image, ImageFilter

OUT = 2000
SS = 1.5
N = int(OUT * SS)
R = 150.0 * SS                 # Rohrradius in Pixel
WALL = 0.085                   # Wandstärke relativ zum Radius (Rand sichtbar)
LEN = 9000.0 * SS
NTUBES = 5
CX = CY = N / 2

a = np.array([0.50, 0.78, -0.40])
a /= np.linalg.norm(a)
v = np.array([0.87, 0.49, 0.0])
b = v - v.dot(a) * a
b /= np.linalg.norm(b)
P0_first = np.array([-560 * SS, -380 * SS, 0.0])
pitch = 2 * R * 1.015
Z0 = 6000.0


def norm(x):
    return x / (np.linalg.norm(x, axis=-1, keepdims=True) + 1e-9)


def env(Rv):
    """Studio-Umgebung (Spiegelrichtung Rv, Einheitsvektoren, y = oben)."""
    elev = np.arcsin(np.clip(Rv[..., 1], -1, 1))
    az = np.arctan2(Rv[..., 0], Rv[..., 2])
    val = 0.62 + 0.30 * np.clip(Rv[..., 1], -0.2, 1) - 0.10 * np.clip(-Rv[..., 1], 0, 1)
    val -= 0.50 * np.exp(-((elev - 0.02) / 0.11) ** 2)          # Horizont dunkel
    val -= 0.30 * np.exp(-((elev + 0.55) / 0.10) ** 2)
    val += 0.42 * np.exp(-((az - 0.9) / 0.22) ** 2) * (elev > -0.1)   # Softbox rechts
    val += 0.32 * np.exp(-((az + 1.1) / 0.18) ** 2) * (elev > -0.1)   # Softbox links
    val -= 0.28 * np.exp(-((az + 0.1) / 0.10) ** 2)                    # dunkler Streifen
    return np.clip(val, 0.06, 1.0)


def render():
    ys, xs = np.mgrid[0:N, 0:N].astype(np.float32)
    X = xs - CX
    Y = -(ys - CY)
    best_t = np.full((N, N), np.inf, np.float32)
    color = np.zeros((N, N), np.float32)
    mask = np.zeros((N, N), bool)
    d = np.array([0.0, 0.0, -1.0])
    for i in range(NTUBES):
        P0 = P0_first + i * pitch * b
        Ox, Oy, Oz = X, Y, np.full_like(X, Z0)
        wx, wy, wz = Ox - P0[0], Oy - P0[1], Oz - P0[2]
        wa = wx * a[0] + wy * a[1] + wz * a[2]
        wpx, wpy, wpz = wx - wa * a[0], wy - wa * a[1], wz - wa * a[2]
        da = d.dot(a)
        dp = d - da * a
        A = dp.dot(dp)
        Bq = wpx * dp[0] + wpy * dp[1] + wpz * dp[2]
        C = wpx ** 2 + wpy ** 2 + wpz ** 2 - R ** 2
        disc = Bq ** 2 - A * C
        hit = disc > 0
        sq = np.sqrt(np.where(hit, disc, 0))
        t1 = (-Bq - sq) / A
        t2 = (-Bq + sq) / A
        s1 = wa + t1 * da
        s2 = wa + t2 * da
        # Endfläche (Ringfläche) bei s=0
        t_end = -wa / da
        ex, ey, ez = Ox - P0[0] + 0 * t_end, Oy - P0[1], Oz + t_end * d[2] - P0[2]
        rad_end = np.sqrt((wx + t_end * d[0]) ** 2 + (wy + t_end * d[1]) ** 2 + (wz + t_end * d[2]) ** 2)
        # radialer Abstand zur Achse am Endpunkt = Abstand zum Mittelpunkt (Ebene senkrecht zur Achse)
        rim = (rad_end <= R) & (rad_end >= R * (1 - WALL))
        bore = rad_end < R * (1 - WALL)
        outer = hit & (s1 >= 0) & (s1 <= LEN)
        inner = hit & ~outer & (s2 >= 0) & (s2 <= LEN) & (t2 > 0)
        # Innenwand sichtbar nur durch die Bohrung
        inner &= bore | (rad_end < R)
        # Kandidaten
        cand_t = np.full((N, N), np.inf, np.float32)
        cand_c = np.zeros((N, N), np.float32)
        # Außenfläche
        px = wx + t1 * d[0]
        py = wy + t1 * d[1]
        pz = wz + t1 * d[2]
        ps = px * a[0] + py * a[1] + pz * a[2]
        nx, ny, nz = px - ps * a[0], py - ps * a[1], pz - ps * a[2]
        n = np.stack([nx, ny, nz], -1) / R
        dd = (n * d).sum(-1, keepdims=True)
        Rv = d - 2 * dd * n
        shade = env(Rv)
        # leichte Längsvariation
        shade = shade * (1 + 0.04 * np.sin(s1 / (900 * SS)))
        m = outer
        cand_t = np.where(m, t1, cand_t)
        cand_c = np.where(m, shade, cand_c)
        # Rand
        edge_shade = 0.88 - 0.10 * (rad_end - R * (1 - WALL)) / (R * WALL + 1e-6)
        m2 = rim & (t_end < cand_t) & (s1 < 0)
        m2 = rim & ((t_end < cand_t) | ~outer)
        cand_t = np.where(m2, t_end, cand_t)
        cand_c = np.where(m2, np.clip(edge_shade, 0.6, 1.0), cand_c)
        # Innenwand: dunkel, mit Verlauf
        depth = np.clip(s2 / (1500 * SS), 0, 1)
        pxi = wx + t2 * d[0]
        pyi = wy + t2 * d[1]
        pzi = wz + t2 * d[2]
        psi = pxi * a[0] + pyi * a[1] + pzi * a[2]
        ni = np.stack([-(pxi - psi * a[0]), -(pyi - psi * a[1]), -(pzi - psi * a[2])], -1) / R
        ddi = (ni * d).sum(-1, keepdims=True)
        Ri = d - 2 * ddi * ni
        inner_shade = (0.02 + 0.14 * env(Ri)) * (1 - 0.8 * depth)
        m3 = inner & bore & (t_end < np.inf)
        m3 &= ~outer
        t_in = np.where(m3, np.minimum(t_end + 1e-3, t2), np.inf)
        cand_t = np.where(m3 & (t_end < cand_t), t_end + 1e-3, cand_t)
        cand_c = np.where(m3 & (t_end + 1e-3 <= cand_t), inner_shade, cand_c)
        take = cand_t < best_t
        best_t = np.where(take, cand_t, best_t)
        color = np.where(take, cand_c, color)
        mask |= take & np.isfinite(cand_t)
    return color, mask


color, mask = render()

# Hintergrund
yy, xx = np.mgrid[0:N, 0:N].astype(np.float32)
bgv = 242 - 10 * (((xx - N * 0.55) / N) ** 2 + ((yy - N * 0.45) / N) ** 2) * 2
bg = np.stack([bgv, bgv, bgv + 1], -1)

# weicher Schatten (nach rechts unten versetzt)
sh = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(26 * SS))
sh = np.array(sh).astype(np.float32) / 255.0
dy_, dx_ = int(46 * SS), int(34 * SS)
sh2 = np.zeros_like(sh)
sh2[dy_:, dx_:] = sh[:-dy_, :-dx_]
sh = sh2
bg = bg * (1 - 0.26 * sh[..., None])

# Chromfarbe (leicht kühl)
tone = np.stack([color * 238 + 12, color * 240 + 13, color * 246 + 12], -1)
# Anti-Aliasing-Kante über Maske
m = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8 * SS))
mm = (np.array(m).astype(np.float32) / 255.0)[..., None]
final = bg * (1 - mm) + tone * mm
img = Image.fromarray(np.clip(final, 0, 255).astype(np.uint8)).resize((OUT, OUT), Image.LANCZOS)
img.save('hauptbild-rohre.png')
img.convert('RGB').save('hauptbild-rohre.jpg', quality=93)
print('ok')
