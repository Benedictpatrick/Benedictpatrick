"""Generates the profile README artwork: ternary pixels, dark and light variants.

Run: python make_assets.py   (writes into ./assets)
Needs Pillow for the logo icons (sources in ./src).
"""
import math
import random
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent
OUT = ROOT / "assets"
CARDS = OUT / "cards"
OUT.mkdir(exist_ok=True)
CARDS.mkdir(exist_ok=True)

THEMES = {
    "dark": dict(bg="#0f1110", card="#141716", ink="#e8e9e4", muted="#9a9f9a", line="#2a2d2b", signal="#ff6533", dot="#262927"),
    "light": dict(bg="#eaebe7", card="#f1f2ee", ink="#121413", muted="#5a5f5b", line="#cfd1cc", signal="#ef4f1a", dot="#d3d5d0"),
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
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "-": ["00000", "00000", "00000", "01110", "00000", "00000", "00000"],
    " ": ["00000"] * 7,
}

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("'", "&#39;")


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


def rect(x, y, s, fill, extra=""):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{s:.1f}" height="{s:.1f}" fill="{fill}"{extra}/>'


def svg(w, h, t, body, title, bg=None):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(title)}">\n'
        f"<title>{esc(title)}</title>\n"
        f'<rect width="{w}" height="{h}" fill="{bg or t["bg"]}"/>\n{body}\n</svg>\n'
    )


# ---------------------------------------------------------------- fields

def field(t, x0, y0, cols, rows, cell, seed, animate=0.0, density=(0.16, 0.12)):
    """A ternary pixel field; a share of the cells flip on and off on their own."""
    s = cell - 2
    rnd = random.Random(seed)
    arnd = random.Random(seed + 7)
    parts = []
    for j in range(rows):
        for i in range(cols):
            r = rnd.random()
            v = 1 if r < density[0] else -1 if r < density[0] + density[1] else 0
            x, y = x0 + i * cell, y0 + j * cell
            if v == 0:
                parts.append(f'<rect x="{x + s / 2 - 1:.1f}" y="{y + s / 2 - 1:.1f}" width="2" height="2" fill="{t["dot"]}"/>')
                continue
            color = t["signal"] if v > 0 else t["ink"]
            if arnd.random() < animate:
                dur = 2.4 + arnd.random() * 3.6
                begin = 1.4 + arnd.random() * 4
                parts.append(
                    f'<rect x="{x:.1f}" y="{y:.1f}" width="{s:.1f}" height="{s:.1f}" fill="{color}">'
                    f'<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.45;0.5;0.95;1" dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/></rect>'
                )
            else:
                parts.append(rect(x, y, s, color))
    return "\n".join(parts)


def reveal(begin, dur=0.2):
    """Opacity animation that holds 0 from load until `begin`, then fades in. The element itself
    stays opacity 1, so renderers without SVG animation still show the finished picture."""
    total = begin + dur
    k = begin / total
    return f'<animate attributeName="opacity" values="0;0;1" keyTimes="0;{k:.3f};1" dur="{total:.2f}s" fill="freeze"/>'


def assemble(x, y, s, color, begin):
    """A pixel that drops into place from a little above."""
    total = begin + 0.32
    k = begin / total
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{s:.1f}" height="{s:.1f}" fill="{color}">'
        + reveal(begin, 0.18)
        + f'<animateTransform attributeName="transform" type="translate" values="0 -14;0 -14;0 0" keyTimes="0;{k:.3f};1" dur="{total:.2f}s" fill="freeze"/>'
        "</rect>"
    )


# ---------------------------------------------------------------- header

def header(name):
    t = THEMES[name]
    W, H = 1280, 470
    cell, s = 16, 14
    rnd = random.Random(5)
    body = []
    for y in (40, 196, 352):
        body.append(f'<line x1="0" x2="{W}" y1="{y}" y2="{y}" stroke="{t["line"]}" stroke-width="1"/>')
    body.append(f'<line x1="40" x2="40" y1="0" y2="{H}" stroke="{t["line"]}"/>')
    body.append(f'<line x1="{W - 40}" x2="{W - 40}" y1="0" y2="{H}" stroke="{t["line"]}"/>')

    # BENEDICT assembles column by column, then PATRICK
    b, bw = word_cells("BENEDICT")
    bx, by = 64, 64
    for c, r in b:
        body.append(assemble(bx + c * cell, by + r * cell, s, t["ink"], 0.15 + c * 0.012 + rnd.random() * 0.12))
    fx = bx + (bw + 2) * cell
    fcols = (W - 40 - fx) // cell
    body.append(field(t, fx, 44, fcols, 9, cell, 11, animate=0.35))
    body.append(f'<line x1="{fx - cell}" x2="{fx - cell}" y1="40" y2="196" stroke="{t["line"]}"/>')

    p, pw = word_cells("PATRICK")
    px = W - 64 - pw * cell
    py = 220
    pcols = (px - cell - 40) // cell
    body.append(field(t, 40, 200, pcols, 9, cell, 23, animate=0.35))
    body.append(f'<line x1="{40 + pcols * cell + 6}" x2="{40 + pcols * cell + 6}" y1="196" y2="352" stroke="{t["line"]}"/>')
    for c, r in p:
        body.append(assemble(px + c * cell, py + r * cell, s, t["ink"], 0.75 + c * 0.012 + rnd.random() * 0.12))
    body.append(assemble(px + (pw + 1) * cell, py + 6 * cell, s, t["signal"], 1.45))

    body.append(
        f'<text x="64" y="402" font-family="{SANS}" font-size="27" font-weight="600" fill="{t["ink"]}" letter-spacing="-0.4">'
        f'From the weights to the chip.{reveal(1.3, 0.6)}</text>'
    )
    body.append(
        f'<text x="64" y="440" font-family="{SANS}" font-size="20" fill="{t["muted"]}">'
        f'I train my own models, write the engines that run them, and ship the tools around them.{reveal(1.5, 0.6)}</text>'
    )
    return svg(W, H, t, "\n".join(body), "Benedict Patrick. From the weights to the chip.")


# ---------------------------------------------------------------- banners

def banner(name, word, note, seed):
    t = THEMES[name]
    W, H = 1280, 132
    cell, s = 10, 8
    body = [
        f'<line x1="0" x2="{W}" y1="1" y2="1" stroke="{t["line"]}"/>',
        f'<line x1="0" x2="{W}" y1="{H - 1}" y2="{H - 1}" stroke="{t["line"]}"/>',
    ]
    cells, _ = word_cells(word)
    x0, y0 = 40, 30
    for c, r in cells:
        body.append(rect(x0 + c * cell, y0 + r * cell, s, t["ink"]))
    sx = W - 40 - 24 * 12
    body.append(field(t, sx, 34, 24, 2, 12, seed, animate=0.5))
    body.append(f'<text x="{W - 40}" y="{y0 + 66}" text-anchor="end" font-family="{MONO}" font-size="16" fill="{t["muted"]}">{esc(note)}</text>')
    return svg(W, H, t, "\n".join(body), word.title())


def footer(name):
    t = THEMES[name]
    W, H = 1280, 120
    body = [f'<line x1="0" x2="{W}" y1="1" y2="1" stroke="{t["line"]}"/>']
    body.append(field(t, 40, 24, 74, 4, 16, 99, animate=0.3))
    return svg(W, H, t, "\n".join(body), "")


# ---------------------------------------------------------------- pixel icons (N x N ternary grids)

N = 14


def icon_from_image(path, crop=None, invert_dark_bg=False):
    """Sample a logo into an N x N ternary grid: background empty, colourful +1, the rest -1."""
    im = Image.open(path).convert("RGBA")
    if crop:
        w, h = im.size
        im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    bg = im.getpixel((0, 0))

    def is_bg(px, tol):
        return px[3] < 110 or (bg[3] >= 110 and math.dist(px[:3], bg[:3]) < tol)

    # trim to content
    small = im.copy()
    small.thumbnail((240, 240))
    sx = im.size[0] / small.size[0]
    xs, ys = [], []
    for y in range(small.size[1]):
        for x in range(small.size[0]):
            if not is_bg(small.getpixel((x, y)), 40):
                xs.append(x)
                ys.append(y)
    if xs:
        im = im.crop((int(min(xs) * sx), int(min(ys) * sx), int((max(xs) + 1) * sx), int((max(ys) + 1) * sx)))
    side = max(im.size)
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.paste(im, ((side - im.size[0]) // 2, (side - im.size[1]) // 2))
    g = sq.resize((N, N), Image.BOX)
    grid = []
    for j in range(N):
        row = []
        for i in range(N):
            px = g.getpixel((i, j))
            if is_bg(px, 30):
                row.append(0)
                continue
            mx, mn = max(px[:3]), min(px[:3])
            sat = (mx - mn) / mx if mx else 0
            row.append(1 if sat > 0.4 and mx > 90 else -1)
        grid.append(row)
    return grid


def icon_pattern(kind, seed=1):
    rnd = random.Random(seed)
    c = (N - 1) / 2
    grid = [[0] * N for _ in range(N)]
    for j in range(N):
        for i in range(N):
            dx, dy = i - c, j - c
            d = math.hypot(dx, dy)
            v = 0
            if kind == "kernel":  # Core-1: a ternary weight matrix
                r = rnd.random()
                v = 1 if r < 0.34 else -1 if r < 0.66 else 0
                if i in (0, N - 1) or j in (0, N - 1):
                    v = 0
            elif kind == "hybrid":  # Phobos: state space bands with attention columns
                v = -1 if j % 3 != 2 else 0
                if i in (3, 4, 9, 10) and j % 3 != 2:
                    v = 1
                if i in (0, N - 1):
                    v = 0
            elif kind == "lock":
                if 1 <= dy <= 6 and abs(dx) <= 4.5:
                    v = 0 if (abs(dx) < 1 and 2 <= dy <= 4) else 1
                elif -5 <= dy <= 0 and 2 <= math.hypot(dx, dy + 0.5) * 1.0 <= 3.6 and dy <= 0:
                    v = -1
            elif kind == "phone":
                if abs(dx) <= 4 and abs(dy) <= 6.5:
                    edge = abs(dx) > 3 or abs(dy) > 5.5
                    v = -1 if edge else (1 if rnd.random() < 0.45 else 0)
            elif kind == "json":
                if j % 2 == 0 and 1 <= j <= N - 2:
                    length = 4 + int(rnd.random() * 8)
                    indent = 1 if (j // 2) % 3 == 0 else 3
                    if indent <= i <= indent + length:
                        v = -1 if i < indent + 3 else 1
            elif kind == "shield":
                half = 5.5 if dy < 0 else 5.5 * (1 - (dy) / 7)
                if -6 <= dy <= 6.5 and abs(dx) <= half:
                    v = 1
                    if abs(dx) > half - 1 or dy <= -5.5:
                        v = -1
            elif kind == "wave":
                amp = (0.5 + 0.5 * math.sin(i * 0.9)) * (0.4 + 0.6 * abs(math.sin(i * 0.35 + 0.6))) * 6
                if abs(dy) < amp * 0.55:
                    v = 1
                elif abs(dy) < amp:
                    v = -1
            elif kind == "ripple":
                ring = d % 3.2
                if d < 1:
                    v = 1
                elif ring < 1 and d < 7.2:
                    v = 1 if d < 3.5 else -1
            grid[j][i] = v
    return grid


# ---------------------------------------------------------------- project cards

def wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) > width:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    if cur:
        lines.append(cur)
    return lines


def card(name, theme, grid, title, status, desc, foot, seed):
    t = THEMES[theme]
    W, H = 900, 330
    body = [f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" fill="{t["card"]}" stroke="{t["line"]}"/>']

    # icon panel with a faint empty grid, pixels pop in once on load
    ic = 15
    ix, iy = 36, 50
    body.append(f'<line x1="{ix + N * ic + 34}" x2="{ix + N * ic + 34}" y1="0" y2="{H}" stroke="{t["line"]}"/>')
    rnd = random.Random(seed)
    for j in range(N):
        for i in range(N):
            x, y = ix + i * ic, iy + j * ic
            v = grid[j][i]
            if v == 0:
                body.append(f'<rect x="{x + 5.5:.1f}" y="{y + 5.5:.1f}" width="2" height="2" fill="{t["dot"]}"/>')
            else:
                color = t["signal"] if v > 0 else t["ink"]
                begin = 0.1 + (i + j) * 0.025 + rnd.random() * 0.15
                body.append(
                    f'<rect x="{x:.1f}" y="{y:.1f}" width="13" height="13" fill="{color}">{reveal(begin)}</rect>'
                )

    # name in the pixel font
    tx = ix + N * ic + 68
    cells, ww = word_cells(title.upper())
    pc = 5
    scale = min(1.0, (W - tx - 40) / (ww * pc))
    cpx = pc * scale
    for c, r in cells:
        body.append(rect(tx + c * cpx, 52 + r * cpx, cpx - 1, t["ink"]))

    # status chip
    chip_w = 16 + len(status) * 9.6
    body.append(f'<rect x="{tx + 0.5}" y="104.5" width="{chip_w:.1f}" height="30" fill="none" stroke="{t["line"]}"/>')
    body.append(f'<rect x="{tx + 10}" y="116" width="7" height="7" fill="{t["signal"]}"/>')
    body.append(f'<text x="{tx + 24}" y="124.5" font-family="{MONO}" font-size="16" fill="{t["muted"]}">{esc(status)}</text>')

    # description
    for k, line in enumerate(wrap(desc, 40)[:4]):
        body.append(f'<text x="{tx}" y="{180 + k * 34}" font-family="{SANS}" font-size="25" fill="{t["ink"]}">{esc(line)}</text>')

    # footer line
    body.append(f'<line x1="{tx}" x2="{W - 36}" y1="{H - 44}" y2="{H - 44}" stroke="{t["line"]}"/>')
    body.append(f'<text x="{tx}" y="{H - 16}" font-family="{MONO}" font-size="16" fill="{t["muted"]}">{esc(foot)}</text>')
    return svg(W, H, t, "\n".join(body), f"{title}: {desc}", bg=t["bg"])


SRC = ROOT / "src"
PROJECTS = [
    ("core1", icon_pattern("kernel", 3), "Core-1", "proof of concept",
     "My own language model for ordinary CPUs. Ternary weights, 16x smaller than fp32, adds instead of multiplies.", "ternary weights + state space"),
    ("phobos", icon_pattern("hybrid"), "Phobos", "research",
     "Mamba-2 layers interleaved with sliding window attention, measured against a matched Transformer.", "hybrid architecture"),
    ("cipheron", icon_pattern("lock"), "Cipheron", "released",
     "A 0.5B coding model trained for secure code review. Flags vulnerabilities, suggests safer code, offline.", "huggingface.co/bencodez/Cipheron"),
    ("spark", icon_from_image(SRC / "spark-logo.jpg", crop=(0.2, 0.1, 0.8, 0.72)), "Spark", "in training",
     "Plain language in, tool calls out. A 3.6M parameter model running fully offline on a $5 ESP32.", "2.2 MB on the chip"),
    ("quanta", icon_pattern("phone", 5), "Quanta Engine", "phone next",
     "An LLM inference engine written from scratch in C++ for the budget phones people actually own.", "no llama.cpp underneath"),
    ("thermollm", icon_pattern("json", 9), "thermollm", "in progress",
     "A tool calling model under 100 MB. Grammar constrained decoding, so every call it emits parses.", "under 100 MB"),
    ("securevibe", icon_pattern("shield"), "securevibe", "on npm",
     "A security scanner for code written fast. Finds the holes, proposes fixes, rescans to prove them.", "npm i -g securevibe"),
    ("smartgrep", icon_from_image(SRC / "smartgrep.png", crop=(0.05, 0.3, 0.32, 0.72)), "smartgrep", "on npm",
     "Ask a codebase questions in plain English. Semantic search with citations, entirely local.", "npm i -g smartgrep"),
    ("navo", icon_from_image(SRC / "navo-mascot.png"), "Navo", "live",
     "A chat model that runs inside your browser tab on WebGPU. Nothing you type leaves your device.", "navoai.space"),
    ("pyphone", icon_from_image(SRC / "pyphone-icon.png"), "PyPhone Studio", "live",
     "A real Python interpreter on your phone, compiled to WebAssembly. Notebooks, pandas, matplotlib.", "pyphone-studio.vercel.app"),
    ("parq", icon_pattern("wave"), "PARQ", "manuscript",
     "Detecting Parkinson's disease from voice with a multitask, dual branch model.", "with Sai Dharshan A. and Dr Ashwini"),
    ("cognitive", icon_pattern("ripple"), "Cognitive Matter", "simulation",
     "A spiking neural fabric simulated live in the browser that learns where you touch it.", "4,096 neurons, 5.1 ms per frame"),
]

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
    for n, (pid, grid, title, status, desc, foot) in enumerate(PROJECTS):
        (CARDS / f"{pid}-{theme}.svg").write_text(card(pid, theme, grid, title, status, desc, foot, n), encoding="utf8")

print("ok:", len(list(OUT.glob("*.svg"))), "banners,", len(list(CARDS.glob("*.svg"))), "cards")
