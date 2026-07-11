"""One-off script to generate icon.png. Not part of the workflow itself."""

from PIL import Image, ImageDraw

SIZE = 512
img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

BADGE = (100, 24, 40, 255)      # deep burgundy
PAGE = (245, 238, 222, 255)     # cream
SPINE = (70, 16, 28, 255)       # darker burgundy
RIBBON = (196, 158, 62, 255)    # gold
LINE = (210, 198, 172, 255)     # faint text-line gray

margin = 20
draw.rounded_rectangle(
    [margin, margin, SIZE - margin, SIZE - margin],
    radius=96,
    fill=BADGE,
)

cx = SIZE // 2

# ribbon bookmark, drawn behind the book so only the tips show
draw.rectangle([cx - 9, 118, cx + 9, 430], fill=RIBBON)
draw.polygon([(cx - 9, 430), (cx + 9, 430), (cx, 452)], fill=RIBBON)

spine_top = (cx, 190)
spine_bottom = (cx, 398)

left_page = [spine_top, (128, 148), (108, 372), spine_bottom]
right_page = [spine_top, (SIZE - 128, 148), (SIZE - 108, 372), spine_bottom]
draw.polygon(left_page, fill=PAGE)
draw.polygon(right_page, fill=PAGE)

# faint text lines on each page
for i, y in enumerate((210, 240, 270, 300, 330)):
    inset = i * 2
    draw.line([(150 + inset, y), (238, y - (i * 6))], fill=LINE, width=4)
    draw.line([(274, y - (i * 6)), (362 - inset, y)], fill=LINE, width=4)

draw.line([spine_top, spine_bottom], fill=SPINE, width=6)

img.save("icon.png")
print("wrote icon.png", img.size)
