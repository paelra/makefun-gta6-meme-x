#!/usr/bin/env python3
"""Create a square Vice City inspired GTA VI waiting meme."""
from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1080
img = Image.new("RGB", (W, H))
pix = img.load()
stops = [(0, (35, 13, 78)), (0.38, (176, 31, 133)), (0.70, (245, 91, 93)), (1, (255, 164, 69))]
for y in range(H):
    t = y / (H - 1)
    for i in range(len(stops) - 1):
        if stops[i][0] <= t <= stops[i + 1][0]:
            a, ca = stops[i]; b, cb = stops[i + 1]
            f = (t - a) / (b - a)
            color = tuple(round(ca[k] * (1 - f) + cb[k] * f) for k in range(3))
            break
    for x in range(W):
        pix[x, y] = color

d = ImageDraw.Draw(img)
# Low pale sun behind the loading bar and skyline.
d.ellipse((356, 226, 724, 594), fill=(255, 220, 168))
# Sun stripes give the disc a retro sunset treatment.
for yy in range(452, 586, 24):
    d.rectangle((356, yy, 724, yy + 10), fill=(243, 116, 125))

# Palm silhouettes: curved trunks with sweeping fronds.
def palm(base_x, base_y, lean, scale):
    points = []
    for i in range(17):
        t = i / 16
        points.append((base_x + lean * t * t, base_y - 330 * scale * t))
    d.line(points, fill=(21, 12, 35), width=max(8, int(19 * scale)), joint="curve")
    cx, cy = points[-1]
    for angle in [-165, -135, -105, -75, -45, -15]:
        rad = math.radians(angle)
        ex, ey = cx + math.cos(rad) * 150 * scale, cy + math.sin(rad) * 105 * scale
        d.line((cx, cy, ex, ey), fill=(21, 12, 35), width=max(6, int(12 * scale)))
        for j in range(1, 5):
            t = j / 5
            px, py = cx + (ex - cx) * t, cy + (ey - cy) * t
            side = (1 if angle < -90 else -1) * 24 * scale
            d.line((px, py, px + side, py + 19 * scale), fill=(21, 12, 35), width=max(4, int(7 * scale)))
palm(42, 880, 80, 1.0)
palm(1040, 850, -50, 0.88)

# Distant city strip.
d.rectangle((0, 820, W, H), fill=(19, 13, 33))
for x, width, top in [(0, 80, 762), (72, 72, 792), (145, 55, 740), (196, 94, 785), (284, 62, 755), (347, 66, 800), (412, 85, 770), (492, 52, 738), (542, 74, 790), (612, 82, 750), (688, 48, 786), (732, 92, 735), (815, 70, 780), (875, 62, 746), (930, 80, 785), (1000, 80, 760)]:
    d.rectangle((x, top, x + width, 858), fill=(25, 16, 42))
    if width > 60:
        for wx in range(x + 12, x + width - 8, 20):
            for wy in range(top + 16, 850, 24):
                d.rectangle((wx, wy, wx + 5, wy + 8), fill=(250, 151, 121))
d.rectangle((0, 858, W, H), fill=(16, 11, 29))

bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def fitted(text, max_width, start, minimum):
    for size in range(start, minimum - 1, -1):
        font = ImageFont.truetype(bold, size)
        if d.textbbox((0, 0), text, font=font, stroke_width=6)[2] <= max_width:
            return font
    return ImageFont.truetype(bold, minimum)

def outlined_center(text, y, font, fill="white", stroke=7):
    box = d.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (W - (box[2] - box[0])) // 2 - box[0]
    d.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=(12, 8, 22))

# Top headline, horizontally fitted while retaining a large type size.
headline = "WAITING FOR GTA VI SINCE 2013…"
font = fitted(headline, 1020, 68, 64)
box = d.textbbox((0, 0), headline, font=font, stroke_width=7)
text_img = Image.new("RGBA", (box[2] - box[0] + 8, 100), (0, 0, 0, 0))
ld = ImageDraw.Draw(text_img)
ld.text((4 - box[0], 8 - box[1]), headline, font=font, fill="white", stroke_width=7, stroke_fill=(12, 8, 22))
if text_img.width > 1020:
    text_img = text_img.resize((1020, text_img.height), Image.Resampling.LANCZOS)
img.paste(text_img, ((W - text_img.width) // 2, 26), text_img)
d = ImageDraw.Draw(img)

# Fake 99 percent game loading UI.
label_font = ImageFont.truetype(bold, 50)
outlined_center("GTA VI", 190, label_font, stroke=5)
d.rounded_rectangle((230, 269, 850, 324), radius=20, outline=(255, 255, 255), width=7, fill=(30, 15, 47))
d.rounded_rectangle((239, 278, 239 + int(602 * .99), 315), radius=14, fill=(255, 245, 225))
bar_font = ImageFont.truetype(bold, 30)
outlined_center("99% — since 2013", 330, bar_font, stroke=4)

# Money sack, beside the official ghost mark.
d.ellipse((559, 710, 762, 902), fill=(176, 145, 91), outline=(24, 16, 29), width=8)
d.polygon([(592, 738), (603, 700), (625, 674), (676, 674), (699, 704), (725, 742)], fill=(190, 158, 103), outline=(24, 16, 29))
d.line((608, 704, 686, 704), fill=(24, 16, 29), width=8)
d.line((627, 676, 642, 694, 663, 675), fill=(24, 16, 29), width=7)
sack_font = ImageFont.truetype(bold, 91)
sbox = d.textbbox((0, 0), "$", font=sack_font, stroke_width=1)
d.text((660 - (sbox[2] - sbox[0]) // 2, 754), "$", font=sack_font, fill=(24, 16, 29))

# Official make.fun ghost mark. Its circular badge is part of the supplied mark.
mark = Image.open("assets/mark-1024.png").convert("RGBA")
mark = mark.resize((430, 430), Image.Resampling.LANCZOS)
img = img.convert("RGBA")
img.alpha_composite(mark, (618, 414))
img = img.convert("RGB")
d = ImageDraw.Draw(img)

# Two prominent, outlined bottom caption lines.
for text, y in [("THE GHOST GOT PAID", 879), ("ON make.fun INSTEAD", 967)]:
    font = fitted(text, 1030, 76, 72)
    outlined_center(text, y, font, stroke=7)

img.save("meme.png", quality=95)
img.resize((480, 480), Image.Resampling.LANCZOS).save("preview-480.png")
