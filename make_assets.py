"""Generates the profile README artwork: ternary pixels, dark and light variants.

Run: python make_assets.py   (writes into ./assets)
"""
import random
from pathlib import Path

OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)

THEMES = {
    "dark": dict(bg="#0f1110", ink="#e8e9e4", muted="#9a9f9a", line="#2a2d2b", signal="#ff6533", dot="#262927"),
    "light": dict(bg="#eaebe7", ink="#121413", muted="#5a5f5b", line="#cfd1cc", signal="#ef4f1a", dot="#d3d5d0"),
}

FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "G": ["01111", "10000", "10000", "10011", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    " ": ["00000"] * 7,
}

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"


def word_cells(text, bold=True):
    """(col, row) cells of a word in the 5x7 font. Bold widens every stroke one pixel to the right."""
    adv = 7 if bold else 6
    cells = set()
    for g, ch in enumerate(text):
        for y, line in enumerate(FONT[ch]):
            for x, bit in enumerate(line):
                if bit == "1":
                    cells.add((g * adv + x, y))
                    if bold:
                        cells.add((g * adv + x + 1, y))
    return sorted(cells), len(text) * adv - 1


def ternary(seed, w, h, density=(0.16, 0.12)):
    rnd = random.Random(seed)
    out = []
    for j in range(h):
        for i in range(w):
            r = rnd.random()
            v = 1 if r < density[0] else -1 if r < density[0] + density[1] else 0
            out.append((i, j, v, rnd.random()))
    return out


def rect(x, y, s, fill, extra=""):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{s:.1f}" height="{s:.1f}" fill="{fill}"{extra}/>'


def field(t, x0, y0, cols, rows, cell, seed, animate=0.0):
    """A ternary pixel field; a share of the cells flip on and off on their own."""
    s = cell - 2
    parts = []
    rnd = random.Random(seed + 7)
    for i, j, v, r in ternary(seed, cols, rows):
        x = x0 + i * cell
        y = y0 + j * cell
        if v == 0:
            parts.append(f'<rect x="{x + s / 2 - 1:.1f}" y="{y + s / 2 - 1:.1f}" width="2" height="2" fill="{t["dot"]}"/>')
            continue
        color = t["signal"] if v > 0 else t["ink"]
        anim = ""
        if r < animate:
            dur = 2.4 + rnd.random() * 3.6
            begin = rnd.random() * 4
            anim = f'><animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.45;0.5;0.95;1" dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/></rect'
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{s:.1f}" height="{s:.1f}" fill="{color}"{anim}>')
        else:
            parts.append(rect(x, y, s, color))
    return "\n".join(parts)


def svg(w, h, t, body, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{title}">\n'
        f"<title>{title}</title>\n"
        f'<rect width="{w}" height="{h}" fill="{t["bg"]}"/>\n{body}\n</svg>\n'
    )


def header(name):
    t = THEMES[name]
    W, H = 1280, 470
    cell = 16
    s = cell - 2
    body = []
    # hairline frame rows, like the site
    for y in (40, 196, 352):
        body.append(f'<line x1="0" x2="{W}" y1="{y}" y2="{y}" stroke="{t["line"]}" stroke-width="1"/>')
    body.append(f'<line x1="40" x2="40" y1="0" y2="{H}" stroke="{t["line"]}"/>')
    body.append(f'<line x1="{W - 40}" x2="{W - 40}" y1="0" y2="{H}" stroke="{t["line"]}"/>')

    # BENEDICT, top left
    b, bw = word_cells("BENEDICT")
    bx, by = 64, 64
    for c, r in b:
        body.append(rect(bx + c * cell, by + r * cell, s, t["ink"]))
    # field to the right of BENEDICT
    fx = bx + (bw + 2) * cell
    fcols = (W - 40 - fx) // cell
    body.append(field(t, fx, 44, fcols, 9, cell, 11, animate=0.35))
    body.append(f'<line x1="{fx - cell}" x2="{fx - cell}" y1="40" y2="196" stroke="{t["line"]}"/>')

    # PATRICK, right aligned on the second row, field to its left
    p, pw = word_cells("PATRICK")
    px = W - 64 - pw * cell
    py = 220
    pcols = (px - cell - 40) // cell
    body.append(field(t, 40, 200, pcols, 9, cell, 23, animate=0.35))
    body.append(f'<line x1="{40 + pcols * cell + 6}" x2="{40 + pcols * cell + 6}" y1="196" y2="352" stroke="{t["line"]}"/>')
    for c, r in p:
        body.append(rect(px + c * cell, py + r * cell, s, t["ink"]))
    # one vermilion pixel: the +1
    body.append(rect(px + (pw + 1) * cell, py + 6 * cell, s, t["signal"]))

    # statement
    body.append(
        f'<text x="64" y="402" font-family="{SANS}" font-size="27" font-weight="600" fill="{t["ink"]}" letter-spacing="-0.4">'
        "From the weights to the chip.</text>"
    )
    body.append(
        f'<text x="64" y="440" font-family="{SANS}" font-size="20" fill="{t["muted"]}">'
        "I train my own models, write the engines that run them, and ship the tools around them.</text>"
    )
    return svg(W, H, t, "\n".join(body), "Benedict Patrick. From the weights to the chip.")


def banner(name, word, note, seed):
    t = THEMES[name]
    W, H = 1280, 132
    cell = 10
    s = cell - 2
    body = [
        f'<line x1="0" x2="{W}" y1="1" y2="1" stroke="{t["line"]}"/>',
        f'<line x1="0" x2="{W}" y1="{H - 1}" y2="{H - 1}" stroke="{t["line"]}"/>',
    ]
    cells, ww = word_cells(word)
    x0, y0 = 40, 30
    for c, r in cells:
        body.append(rect(x0 + c * cell, y0 + r * cell, s, t["ink"]))
    # a short ternary strip and a mono note on the right
    sx = W - 40 - 24 * 12
    body.append(field(t, sx, 34, 24, 2, 12, seed, animate=0.5))
    body.append(
        f'<text x="{W - 40}" y="{y0 + 66}" text-anchor="end" font-family="{MONO}" font-size="16" fill="{t["muted"]}">{note}</text>'
    )
    return svg(W, H, t, "\n".join(body), word.title())


def footer(name):
    t = THEMES[name]
    W, H = 1280, 120
    body = [f'<line x1="0" x2="{W}" y1="1" y2="1" stroke="{t["line"]}"/>']
    body.append(field(t, 40, 24, 74, 4, 16, 99, animate=0.3))
    return svg(W, H, t, "\n".join(body), "")


for theme in THEMES:
    (OUT / f"header-{theme}.svg").write_text(header(theme), encoding="utf8")
    for word, note, seed in [
        ("MODELS", "Core-1, Phobos, Cipheron", 31),
        ("EDGE", "Spark, Quanta Engine, thermollm", 37),
        ("SHIPPED", "securevibe, smartgrep, Navo, PyPhone", 41),
        ("RESEARCH", "PARQ, Cognitive Matter", 43),
        ("CONTACT", "say hello", 47),
    ]:
        (OUT / f"{word.lower()}-{theme}.svg").write_text(banner(theme, word, note, seed), encoding="utf8")
    (OUT / f"footer-{theme}.svg").write_text(footer(theme), encoding="utf8")

print("wrote", sorted(p.name for p in OUT.iterdir()))
