#!/usr/bin/env python3
"""Build launch media for the Shark Tank skill: seat cards, a verdict card,
terminal stills, and a demo video. Needs rsvg-convert and ffmpeg.

Run: python3 marketing/build_media.py
Output: marketing/media/
"""
import json
import subprocess
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "marketing" / "media"
FRAMES = OUT / "_frames"
ROSTER = json.loads((ROOT / "skills/shark-tank/roster.json").read_text())

SERIF = "Georgia, 'Times New Roman', serif"
SANS = "Helvetica Neue, Helvetica, Arial, sans-serif"
MONO = "Menlo, 'Courier New', monospace"
DISCLAIMER = "AI simulation built from a public persona. Not the real person. Not endorsed."
INSTALL1 = "/plugin marketplace add sidrat2612/shark-tank-skill"
INSTALL2 = "/plugin install shark-tank@shark-tank-skill"


def png(svg: str, path: Path, w: int, h: int) -> None:
    tmp = path.with_suffix(".svg")
    tmp.write_text(svg)
    subprocess.run(["rsvg-convert", "-w", str(w), "-h", str(h), "-o", str(path), str(tmp)], check=True)
    tmp.unlink()


def lines(x, y, text, width, size, fill, family, gap=1.3, weight="400"):
    out = []
    for i, ln in enumerate(textwrap.wrap(text, width)):
        out.append(
            f'<text x="{x}" y="{y + i * size * gap:.0f}" font-family="{family}" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(ln)}</text>'
        )
    return "\n".join(out)


def seat_card(seat) -> str:
    c = seat["color"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b2540"/><stop offset="1" stop-color="#05121f"/></linearGradient></defs>
<rect width="1080" height="1080" fill="url(#g)"/>
<rect x="0" y="0" width="1080" height="14" fill="{c}"/>
<text x="80" y="120" font-family="{SANS}" font-size="30" letter-spacing="4" fill="#c9d6e3">SHARK TANK FOR CLAUDE CODE</text>
<circle cx="200" cy="330" r="110" fill="{c}"/>
<text x="200" y="365" text-anchor="middle" font-family="{SERIF}" font-size="96" font-weight="700" fill="#f4f1ea">{escape(seat['initials'])}</text>
<text x="360" y="320" font-family="{SERIF}" font-size="68" font-weight="700" fill="#f4f1ea">{escape(seat['name'])}</text>
<text x="360" y="375" font-family="{SANS}" font-size="30" fill="{c}">The {escape(seat['short'])} seat</text>
<text x="80" y="540" font-family="{SANS}" font-size="28" letter-spacing="3" fill="#8aa3b8">THE SEAT COVERS</text>
{lines(80, 600, seat['pillar'], 34, 44, '#f4f1ea', SERIF, weight='700')}
<text x="80" y="760" font-family="{SANS}" font-size="28" letter-spacing="3" fill="#8aa3b8">THE QUESTION IT ASKS YOU</text>
{lines(80, 815, seat['question'], 48, 34, '#e8e3d6', SERIF)}
<rect x="80" y="960" width="920" height="2" fill="#27465f"/>
<text x="80" y="1005" font-family="{MONO}" font-size="24" fill="#e8a33d">{escape(INSTALL2)}</text>
<text x="80" y="1045" font-family="{SANS}" font-size="20" fill="#7d93a6">{escape(DISCLAIMER)}</text>
</svg>"""


def verdict_card() -> str:
    rows = [("Mr. Wonderful", "OUT", "2/10"), ("Lori", "OUT", "3/10"), ("Cuban", "OUT", "2/10"),
            ("Barbara", "OUT", "3/10"), ("Daymond", "OUT", "2/10")]
    body = []
    for i, (n, d, s) in enumerate(rows):
        y = 300 + i * 62
        body.append(f'<text x="80" y="{y}" font-family="{SANS}" font-size="34" fill="#f4f1ea">{n}</text>')
        body.append(f'<text x="520" y="{y}" font-family="{SANS}" font-size="34" font-weight="700" fill="#e86a5e">{d}</text>')
        body.append(f'<text x="680" y="{y}" font-family="{MONO}" font-size="32" fill="#c9d6e3">{s}</text>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" viewBox="0 0 1200 675">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b2540"/><stop offset="1" stop-color="#05121f"/></linearGradient></defs>
<rect width="1200" height="675" fill="url(#g)"/>
<rect width="1200" height="10" fill="#e8a33d"/>
<text x="80" y="95" font-family="{SANS}" font-size="24" letter-spacing="4" fill="#8aa3b8">EXAMPLE VERDICT: SMART LUNCHBOX</text>
<text x="80" y="170" font-family="{SERIF}" font-size="64" font-weight="700" fill="#f4f1ea">No deal.</text>
<text x="80" y="220" font-family="{SANS}" font-size="28" fill="#c9d6e3">The ask: 250,000 for 10%. Implied valuation 2,500,000.</text>
{''.join(body)}
<rect x="820" y="240" width="300" height="250" rx="16" fill="#102f4d"/>
<text x="970" y="320" text-anchor="middle" font-family="{SANS}" font-size="24" fill="#8aa3b8">PANEL SCORE</text>
<text x="970" y="420" text-anchor="middle" font-family="{SERIF}" font-size="104" font-weight="700" fill="#e8a33d">2.5</text>
<text x="970" y="465" text-anchor="middle" font-family="{SANS}" font-size="26" fill="#c9d6e3">out of 10</text>
<text x="80" y="600" font-family="{SANS}" font-size="26" fill="#e8e3d6">The fix list: landed cost under 25, know the app cost per unit, commit the team.</text>
<text x="80" y="640" font-family="{SANS}" font-size="20" fill="#7d93a6">{escape(DISCLAIMER)}</text>
</svg>"""


# ---- terminal scenes ------------------------------------------------------
W, H = 1280, 720
LH, FS = 30, 20
MAXLINES = 19

WHITE, DIM, GOLD, BLUE, RED, GREEN = "#e8e3d6", "#7d93a6", "#e8a33d", "#6fb3ff", "#e86a5e", "#6fd3a0"

# Each step: (seconds on screen, [(text, color), ...] appended)
STEPS = [
    (1.6, [("> /shark-tank", GREEN)]),
    (2.4, [("Pitch: a smart lunchbox with a food temperature sensor.", WHITE),
           ("Ask: 250,000 for 10%.", WHITE)]),
    (2.6, [("", WHITE),
           ("HOST  Panel set: Mr. Wonderful, Lori, Cuban, Barbara, Daymond.", GOLD),
           ("HOST  Implied valuation: 250,000 / 0.10 = 2,500,000.", GOLD)]),
    (3.0, [("", WHITE),
           ("ROUND 1  Five Sharks read the pitch in parallel.", BLUE),
           ("Lori, Daymond, Mr. Wonderful all ask:", WHITE),
           ("  What does it really cost to land one unit, all in?", WHITE)]),
    (3.2, [("", WHITE),
           ("ROUND 2  Offer or out.", BLUE),
           ("MR. WONDERFUL  OUT. 18 times revenue on a box bought once a year.", RED),
           ("LORI  OUT. At 41 wholesale nobody in the chain makes money.", RED)]),
    (3.0, [("CUBAN  OUT. A patent on a latch is not a moat.", RED),
           ("BARBARA  OUT. Half a team will not carry this ask.", RED),
           ("DAYMOND  OUT. Every new retailer loses you money.", RED)]),
    (3.4, [("", WHITE),
           ("VERDICT  No deal. Panel score 2.5 out of 10.", GOLD),
           ("Fix 1  Landed cost under 25, with a signed factory quote.", WHITE),
           ("Fix 2  Know the app and sensor cost per unit.", WHITE),
           ("Fix 3  Commit the team. File the trademark.", WHITE)]),
]


def terminal_frame(buf, title="shark-tank") -> str:
    shown = buf[-MAXLINES:]
    body = []
    for i, (t, col) in enumerate(shown):
        body.append(f'<text x="48" y="{110 + i * LH}" font-family="{MONO}" font-size="{FS}" fill="{col}">{escape(t)}</text>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" fill="#05121f"/>
<rect width="{W}" height="56" fill="#0b2540"/>
<circle cx="32" cy="28" r="8" fill="#e86a5e"/><circle cx="58" cy="28" r="8" fill="#e8a33d"/><circle cx="84" cy="28" r="8" fill="#6fd3a0"/>
<text x="640" y="35" text-anchor="middle" font-family="{SANS}" font-size="18" fill="#8aa3b8">claude code: {escape(title)}</text>
{''.join(body)}
<rect x="0" y="{H - 44}" width="{W}" height="44" fill="#0b2540"/>
<text x="48" y="{H - 16}" font-family="{SANS}" font-size="16" fill="#7d93a6">{escape(DISCLAIMER)}</text>
</svg>"""


def title_frame(head, sub, mono_lines) -> str:
    mono = "".join(
        f'<text x="640" y="{470 + i * 44}" text-anchor="middle" font-family="{MONO}" font-size="26" fill="#e8a33d">{escape(m)}</text>'
        for i, m in enumerate(mono_lines)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b2540"/><stop offset="1" stop-color="#05121f"/></linearGradient></defs>
<rect width="{W}" height="{H}" fill="url(#g)"/>
<text x="640" y="270" text-anchor="middle" font-family="{SERIF}" font-size="92" font-weight="700" fill="#f4f1ea">{escape(head)}</text>
<text x="640" y="340" text-anchor="middle" font-family="{SANS}" font-size="34" fill="#c9d6e3">{escape(sub)}</text>
{mono}
<text x="640" y="{H - 40}" text-anchor="middle" font-family="{SANS}" font-size="18" fill="#7d93a6">{escape(DISCLAIMER)}</text>
</svg>"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    FRAMES.mkdir(exist_ok=True)

    for seat in ROSTER["seats"]:
        png(seat_card(seat), OUT / f"seat-{seat['key']}.png", 1080, 1080)
    png(verdict_card(), OUT / "verdict-card.png", 1200, 675)

    # Video frames
    seq = [(3.0, title_frame("Shark Tank", "for Claude Code", ["Pitch it. Get grilled. Get an offer, or hear why not."]))]
    buf = []
    for dur, new in STEPS:
        buf += new
        seq.append((dur, terminal_frame(buf)))
    seq.append((4.5, title_frame("Try it", "Free and open source", [INSTALL1, INSTALL2])))

    concat = []
    for i, (dur, svg) in enumerate(seq):
        p = FRAMES / f"f{i:02d}.png"
        png(svg, p, W, H)
        concat.append(f"file '{p}'\nduration {dur}")
        if i >= 1 and i < len(seq) - 1:
            png(svg, OUT / f"terminal-{i:02d}.png", W, H)
    concat.append(f"file '{FRAMES / f'f{len(seq) - 1:02d}.png'}'")
    (FRAMES / "list.txt").write_text("\n".join(concat) + "\n")

    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(FRAMES / "list.txt"),
         "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "20", "-movflags", "+faststart",
         str(OUT / "shark-tank-demo.mp4")],
        check=True,
    )
    for f in FRAMES.glob("*"):
        f.unlink()
    FRAMES.rmdir()
    print("done:", OUT)


if __name__ == "__main__":
    main()
