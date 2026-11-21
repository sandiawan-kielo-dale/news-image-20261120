"""Draw the 20 November 2026 front page as a 1024x1024 PNG.

Stdlib only: os, struct, sys, zlib. No external assets, no network.
A tiny 5x7 bitmap font (uppercase only, to keep every glyph unambiguous)
plus a small PNG encoder (zlib + struct, correct CRCs).
"""
import os
import struct
import sys
import zlib

W = 1024
H = 1024

# 5x7 bitmap font: each glyph is 7 rows of 5 bits ("1" = ink).
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "+": ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    ":": ("00000", "01100", "00000", "00000", "01100", "00000", "00000"),
    ";": ("00000", "01100", "00000", "01100", "00100", "01000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
}

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
DARK = (40, 40, 40)
GREY = (120, 120, 120)
LIGHT = (238, 238, 238)
GOLD = (200, 160, 40)

# Six stories: (tag, colour, headline, body lines)
PANELS = [
    ("WAR - EUROPE", (178, 34, 34), "KYIV HIT AGAIN OVERNIGHT",
     ["MISSILES AND DRONES HIT KYIV BEFORE DAWN.",
      "BLASTS SHOOK THE CAPITAL. CREWS SEARCHED WRECKAGE."]),
    ("DISASTER - ASIA", (0, 128, 128), "CYCLONE AKVAN HITS ODISHA",
     ["CYCLONE AKVAN LANDED NEAR GOPALPUR ON FRIDAY.",
      "WINDS 70 TO 80 KM/H, GUSTS TO 90. OVER 300,000 EVACUATED."]),
    ("DIPLOMACY - EUROPE", (30, 80, 180), "EU AND UK SEAL RESET DEAL",
     ["SECOND POST-BREXIT SUMMIT IN BRUSSELS.",
      "FARM CHECKS EASED. CARBON MARKETS LINKED. YOUTH TRAVEL FOR 100,000."]),
    ("CLIMATE", (34, 139, 34), "COP31 DRAFT DROPS FOSSIL PHASE-OUT",
     ["NEGOTIATORS IN ANTALYA CUT ANY CALL TO END FOSSIL FUELS.",
      "THE SLIM DRAFT SHRANK AS FINAL TALKS FALTERED."]),
    ("ECONOMY", (180, 100, 0), "MARKETS SLIDE AGAIN",
     ["NIKKEI FELL 4.8%. THE S&P 500 DROPPED 2% FOR A SIXTH DAY.",
      "DOW FELL 1,101 POINTS. ANTHROPIC SLID TOO."]),
    ("MIDDLE EAST", (110, 60, 160), "SAUDI INTERCEPTS MISSILE AND DRONES",
     ["DEFENCES STOPPED A MISSILE AND FIVE DRONES OVER RIYADH.",
      "A DAY AFTER A STRIKE DAMAGED THE PIF TOWER."]),
]


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = color

    def fill_rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = color

    def text_width(self, text, scale):
        return len(text) * 6 * scale - scale

    def draw_text(self, text, x, y, scale, color):
        for ci, ch in enumerate(text):
            glyph = FONT.get(ch, FONT[" "])
            cx = x + ci * 6 * scale
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == "1":
                        self.fill_rect(cx + col * scale, y + row * scale,
                                       scale, scale, color)

    def draw_text_centered(self, text, cx, y, scale, color):
        self.draw_text(text, cx - self.text_width(text, scale) // 2,
                       y, scale, color)

    def wrap(self, text, max_width, scale):
        """Greedy word wrap; returns a list of lines fitting max_width."""
        lines = []
        for raw in text.split("\n"):
            words = raw.split(" ")
            cur = ""
            for word in words:
                trial = word if not cur else cur + " " + word
                if self.text_width(trial, scale) <= max_width:
                    cur = trial
                else:
                    if cur:
                        lines.append(cur)
                    cur = word
            if cur:
                lines.append(cur)
        return lines


def draw_panel(cv, x, y, w, h, tag, color, headline, body):
    cv.fill_rect(x, y, w, h, WHITE)
    # border
    cv.fill_rect(x, y, w, 3, BLACK)
    cv.fill_rect(x, y + h - 3, w, 3, BLACK)
    cv.fill_rect(x, y, 3, h, BLACK)
    cv.fill_rect(x + w - 3, y, 3, h, BLACK)
    # colour bar
    cv.fill_rect(x + 3, y + 3, w - 6, 10, color)
    # tag
    cv.draw_text(tag, x + 16, y + 24, 2, color)
    # headline, up to two lines
    inner = w - 32
    hl = cv.wrap(headline, inner, 4)
    hy = y + 48
    for line in hl[:2]:
        cv.draw_text(line, x + 16, hy, 4, BLACK)
        hy += 32
    # divider
    cv.fill_rect(x + 16, y + 118, w - 32, 2, LIGHT)
    # body
    by = y + 132
    for para in body:
        for line in cv.wrap(para, inner, 3):
            cv.draw_text(line, x + 16, by, 3, DARK)
            by += 23
        by += 4


def build():
    cv = Canvas(W, H, WHITE)
    # Masthead: black bar with title and date.
    cv.fill_rect(0, 0, W, 140, BLACK)
    cv.draw_text_centered("THE WORLD ON FRIDAY", W // 2, 20, 6, WHITE)
    cv.draw_text_centered("20 NOVEMBER 2026", W // 2, 76, 5, GOLD)
    cv.fill_rect(0, 140, W, 6, GOLD)
    # Kicker strip.
    cv.draw_text_centered("SIX STORIES FROM AROUND THE WORLD",
                          W // 2, 158, 2, DARK)
    # Six panels: 2 columns x 3 rows.
    pw, ph = 488, 258
    xs = (16, 520)
    ys = (184, 454, 724)
    for i, (tag, color, headline, body) in enumerate(PANELS):
        draw_panel(cv, xs[i % 2], ys[i // 2], pw, ph,
                   tag, color, headline, body)
    # Footer: black bar with sources.
    cv.fill_rect(0, 992, W, 32, BLACK)
    cv.draw_text_centered(
        "SOURCES: AP - REUTERS - IMD - EURONEWS - CONSILIUM - BLOOMBERG",
        W // 2, 1001, 2, WHITE)
    return cv


def chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(cv, path):
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    raw = bytearray()
    stride = W * 3
    for yy in range(H):
        raw.append(0)
        raw += cv.px[yy * stride:(yy + 1) * stride]
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(png)
    return len(png)


def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(here)
    out = argv[1] if len(argv) > 1 else os.path.join(repo, "entry.png")
    cv = build()
    size = write_png(cv, out)
    print("wrote %s (%d bytes, %dx%d)" % (out, size, W, H))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
