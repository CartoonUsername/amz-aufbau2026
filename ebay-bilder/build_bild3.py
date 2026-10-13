from PIL import Image, ImageDraw, ImageFont
import numpy as np, math
from scipy import ndimage as ndi

src = Image.open('src.png').convert('RGB')
im = np.array(src).astype(np.uint8)
keep = np.load('keep.npy')
keep = ndi.binary_fill_holes(keep)
keep = ndi.binary_dilation(keep, iterations=3)

# --- axis (shadow-free estimate)
d = np.array([0.79601175, -0.60528117]); n = np.array([0.60528117, 0.79601175])
r = 78.0
off0 = -15.0
tip0 = np.array([187.33, 1635.84]); tip1 = np.array([1785.48, 420.62])
C0 = tip0 + d * r * 0.55 + n * off0
C1 = tip1 - d * r * 0.55 + n * off0
print('C0', C0, 'C1', C1)

# --- protect tube with capsule + mask
yy, xx = np.mgrid[0:2000, 0:2000]
P0 = (C0 - d * r * 0.55); P1 = (C1 + d * r * 0.55)
vx = xx - P0[0]; vy = yy - P0[1]
t = np.clip((vx * d[0] + vy * d[1]) / np.linalg.norm(P1 - P0), 0, 1)
qx = P0[0] + t * (P1[0] - P0[0]); qy = P0[1] + t * (P1[1] - P0[1])
caps = (xx - qx) ** 2 + (yy - qy) ** 2 <= (r + 4) ** 2
keep = keep | caps
# --- erase annotations (dark pixels outside the tube)
g = im.min(axis=2)
dark = (g < 200) & (~keep)
dark = ndi.binary_dilation(dark, iterations=4) & (~keep)
im[dark] = 255
import cv2
gimg = im.min(axis=2).astype(int)
lm = np.zeros(gimg.shape, np.uint8)
for x0, y0, y1 in ((265, 1300, 1612), (152, 1300, 1546)):
    for y in range(y0, y1):
        row = gimg[y]
        for x in range(x0 - 6, x0 + 7):
            if row[x] < min(row[x - 6], row[x + 6]) - 12:
                lm[y, x - 2:x + 3] = 255
for bx0, by0, bx1, by1 in ((258, 1660, 290, 1696), (1778, 466, 1804, 496)):
    sub = gimg[by0:by1, bx0:bx1] < 225
    lm[by0:by1, bx0:bx1][sub] = 255
lm = lm | cv2.dilate(lm, np.ones((3, 3), np.uint8))
im = cv2.inpaint(im, lm, 4, cv2.INPAINT_TELEA)
# remove faint AI noise/smudges outside the tube (keeps the real shadow)
faint = (im.min(axis=2) >= 238) & (~ndi.binary_dilation(keep, iterations=2))
im[faint] = 255
base = Image.fromarray(im)

# --- draw clean annotations (supersampled)
S = 2
W = 2000
layer = Image.new('RGBA', (W * S, W * S), (255, 255, 255, 0))
dr = ImageDraw.Draw(layer)
col = (60, 60, 60, 255)
lw = 3 * S
def P(p): return (float(p[0]) * S, float(p[1]) * S)
def line(a, b): dr.line([P(a), P(b)], fill=col, width=lw)
def arrow(tip, direction, size=26):
    dirv = np.array(direction) / np.linalg.norm(direction)
    nv = np.array([-dirv[1], dirv[0]])
    base_pt = np.array(tip) - dirv * size
    dr.polygon([P(tip), P(base_pt + nv * size * 0.32), P(base_pt - nv * size * 0.32)], fill=col)

font_b = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 66 * S)
font_r = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Regular.otf', 46 * S)
font_h = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Bold.otf', 118 * S)

# long length dimension, parallel to tube, offset to the lower right
off = r + 150
L0 = C0 + n * off; L1 = C1 + n * off
line(L0, L1)
arrow(L0, L0 - L1); arrow(L1, L1 - L0)
for E in (C0, C1):                       # extension lines
    line(E + n * (r + 25), E + n * (off + 28))

def rot_text(txt, font, center, angle_deg, fill=col):
    tmp = Image.new('RGBA', (900 * S, 220 * S), (255, 255, 255, 0))
    td = ImageDraw.Draw(tmp)
    bb = td.textbbox((0, 0), txt, font=font)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    td.text((450 * S - w / 2 - bb[0], 110 * S - h / 2 - bb[1]), txt, font=font, fill=fill)
    tmp = tmp.rotate(angle_deg, resample=Image.BICUBIC, expand=True)
    layer.alpha_composite(tmp, (int(center[0] * S - tmp.width / 2), int(center[1] * S - tmp.height / 2)))

ang = math.degrees(math.atan2(-d[1], d[0]))   # counter-clockwise angle for PIL
Mid = (L0 + L1) / 2
rot_text('350 / 500 / 750 mm', font_b, Mid - n * 52, ang)
rot_text('Systemmaß', font_r, Mid + n * 48, ang, fill=(95, 95, 95, 255))

# diameter dimension at the far end (across the tube, beyond its end)
Dm = C1 + d * (r + 88)
A = Dm - n * r; B = Dm + n * r
line(A, B)
arrow(A, A - B, 22); arrow(B, B - A, 22)
for sgn in (-1, 1):
    E = C1 + n * (sgn * r)
    line(E + d * (r * 0.9 + 14), Dm + n * (sgn * r) + d * 22)
tmp = ImageDraw.Draw(layer)
txt = 'Ø 19 mm'
bb = tmp.textbbox((0, 0), txt, font=font_b)
tx = (A[0] - 28) * S - (bb[2] - bb[0])
ty = (A[1] - 70) * S - (bb[3] - bb[1]) / 2
tmp.text((tx - bb[0], ty - bb[1]), txt, font=font_b, fill=col)

# headline
hb = tmp.textbbox((0, 0), 'Maße', font=font_h)
tmp.text(((W * S - (hb[2] - hb[0])) / 2 - hb[0], 150 * S - hb[1]), 'Maße', font=font_h, fill=(50, 50, 50, 255))

layer = layer.resize((W, W), Image.LANCZOS)
out = base.convert('RGBA'); out.alpha_composite(layer)
out = out.convert('RGB')
out.save('/home/user/amz-aufbau2026/ebay-bilder/bild3-masse.png')
out.save('/home/user/amz-aufbau2026/ebay-bilder/bild3-masse.jpg', quality=93)
out.resize((1000, 1000)).save('preview3.png')
