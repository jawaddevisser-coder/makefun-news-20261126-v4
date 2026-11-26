#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news timeline poster.

One image, 1024x1024, fully deterministic: no randomness, no network,
no clock. Every story below was first reported on 26 November 2026
(UTC), verified against Reuters, BBC, AP, Al Jazeera and CNBC-TV18.

Run:  python3 draw_timeline.py        (writes entry.png next to this file)
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# --- palette: deep-navy night desk, cream ink, gold spine -------------------
BG = (13, 27, 42)
CREAM = (245, 239, 224)
GOLD = (232, 184, 75)
MUTED = (159, 179, 200)
FAINT = (169, 191, 212)
SPINE = (51, 80, 107)
RULE = (232, 184, 75)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# --- regions: name -> (dot colour, short label, count) ----------------------
REGIONS = {
    "europe": ((111, 168, 220), "EUROPE"),
    "east_asia": ((224, 102, 102), "E. ASIA"),
    "se_asia": ((246, 178, 107), "SE ASIA"),
    "south_asia": ((147, 196, 125), "S. ASIA"),
    "middle_east": ((255, 217, 102), "M. EAST"),
    "africa": ((180, 167, 214), "AFRICA"),
    "n_america": ((118, 165, 175), "N. AMERICA"),
    "pacific": ((142, 124, 195), "PACIFIC"),
    "latin_am": ((234, 153, 153), "LATIN AM."),
}

# --- stories: (UTC time, region key, headline, detail) ----------------------
# Headlines stay under ~95 chars; details under ~120 chars so nothing
# ever wraps or truncates at the chosen sizes.
STORIES = [
    ("00:00", "europe", "LILLE STUN BAYERN 2-1 IN THE CHAMPIONS LEAGUE",
     "Ueda 62', Pavlovic own goal 65' - Bayern's first defeat of the league phase"),
    ("00:30", "europe", "UCL NIGHT: BARCA HIT FOUR, LIVERPOOL WIN 3-0",
     "Barcelona score four; Liverpool win at Brugge; Man Utd held 2-2, PSG drop points"),
    ("01:00", "east_asia", "ASIAN STOCKS RALLY AS TARIFF FEARS EASE",
     "Nikkei +1.6%, Kospi +1.9%, Taiex +3.05%, Hang Seng +1.22%"),
    ("02:00", "east_asia", "BANK OF KOREA HIKES RATES TO 3.25%",
     "A 25bp rise in a non-unanimous decision, as expected by markets"),
    ("03:00", "se_asia", "INDONESIA MINE FLOOD: 13 DEAD, 13 STILL TRAPPED",
     "Ciseureuh River swamped a 100m illegal gold shaft near Bogor; 325 rescuers"),
    ("04:00", "se_asia", "NVIDIA HALTS SERVER SHIPMENTS TO SE ASIA",
     "Four countries hit as US export controls tighten; shares -3.9% at $149.30"),
    ("05:00", "east_asia", "US CHIP CURBS SLOW CHINA'S AI BUILDERS",
     "Z.AI's GLM-5.5 delayed; Moonshot says release cycles may double to a year"),
    ("06:00", "n_america", "GOLD REBOUNDS TO $3,605 AFTER 3% PLUNGE",
     "Spot gold fell to $3,445.89, its lowest since August 2025, then recovered"),
    ("07:00", "middle_east", "OIL HOLDS NEAR $95 AFTER HOUTHI REFINERY ATTACK",
     "Brent $94.84, WTI $84.23 as supply fears linger; IEA sees surplus in Q4"),
    ("08:00", "middle_east", "HOUTHIS STRIKE JEDDAH AND JIZAN PORTS",
     "Saudi coalition downs drones and intercepts two missiles aimed at Riyadh"),
    ("09:00", "middle_east", "GAZA STRIKE KILLS HAMAS SECURITY CHIEF",
     "Mohammad Abu al-Ouf dies with his wife and two daughters in Shati camp"),
    ("09:30", "middle_east", "CAIRO TANKER FIRE KILLS 31, INJURES 21",
     "A fuel tanker crash ignites a blaze on the Ring Road; 27 vehicles burned"),
    ("10:00", "africa", "SUDAN DRONE STRIKES KILL 19 CIVILIANS",
     "RSF drones hit three neighbourhoods in Damazin, Blue Nile; 20 wounded"),
    ("10:30", "africa", "TWO LIBYAN OFFICERS DIE AFTER UKRAINE DRONE STRIKE",
     "Ukrainian drones hit a Russian warship off Benghazi; two officers die"),
    ("11:00", "south_asia", "BANGLADESH: TEAR GAS AT FRESH GARMENT PROTEST",
     "Police disperse workers in Gazipur a day after a 36% wage rise to $138 a month"),
    ("12:00", "europe", "UK PUBLISHES EU TREATIES IN 'CUTTING COSTS' BILL",
     "Food checks end in 2028; carbon markets linked; 6.5bn pounds exports spared carbon tax"),
    ("13:00", "europe", "LONDON TUBE STRIKE BEGINS AT NOON",
     "RMT walks out for 24 hours; Circle and Piccadilly shut, 8 strikes planned"),
    ("14:00", "europe", "POLAND PLANS NO-FLY ZONE ON EASTERN BORDER",
     "Warsaw acts after Russian missiles; NATO approves AWACS surveillance"),
    ("15:00", "middle_east", "NETANYAHU BRIBERY CHARGE MAY BE DROPPED",
     "Judges in Case 4000 suggest dropping the charge; fraud and breach of trust remain"),
    ("16:00", "n_america", "US PROPOSES TARIFFS ON 14 TRADING PARTNERS",
     "China +20% on top of 25%; EU, Japan and S. Korea face 15%; India up to 25%"),
    ("17:00", "n_america", "US CORE INFLATION 3.3%, ABOVE FORECAST",
     "Core PCE beats the 3.2% forecast; headline inflation holds at 3.8%"),
    ("18:00", "n_america", "FCC CLEARS SPACEX: 1 MILLION SATELLITES",
     "Orbital data centres approved; first launch expected in 2027"),
    ("19:00", "n_america", "THANKSGIVING: US MARKETS SHUT AS DOW HEALS",
     "Dow recovered nearly 1,270 points from its lows on Wednesday"),
    ("20:00", "east_asia", "NORTH KOREA EXPELS SWISS ENVOY",
     "Pyongyang gives Switzerland's top diplomat 48 hours to leave over sanctions"),
    ("21:00", "africa", "RAMAPHOSA WINS COURT RULING ON FARMGATE",
     "South Africa's president overturns the panel report on the farm cash scandal"),
    ("22:00", "pacific", "SOLOMON ISLANDS SIGNS TREATY WITH AUSTRALIA",
     "Canberra pact ditches China and bars foreign military bases"),
    ("23:00", "pacific", "QUAKES OFF TAIWAN AND VANUATU",
     "M5.3 and M5.0 strike off Taiwan; M4.7 hits near Port Vila, Vanuatu"),
    ("23:30", "latin_am", "QUAKE OFF MEXICO; PANAMA SCHOOLS REOPEN",
     "M4.6 off Puerto Madero; Azuero schools reopen after the earthquake"),
    ("23:45", "south_asia", "PAKISTAN, SAUDI, TURKEY TO MEET IN ISLAMABAD",
     "Defence-pact talks set for 27-28 Nov, two Pakistani sources say"),
]

HEADER_SUB = "THE WORLD IN ONE DAY  \u2022  29 STORIES  \u2022  9 REGIONS  \u2022  19 FIELDS  \u2022  ALL TIMES UTC"
FOOTER_SRC = ("SOURCES: REUTERS \u2022 BBC \u2022 AP \u2022 AL JAZEERA \u2022 CNBC-TV18"
              "  \u2014  EVERY STORY FIRST REPORTED 26 NOV 2026  \u2022  DATE-CHECKED")

# geometry
SPINE_X = 118
TIME_RIGHT = 104
TEXT_X = 140
TEXT_RIGHT = 1000
TOP = 108
BOTTOM = 950
HEADER_H = 96
FOOTER_RULE_Y = 958


def fit_text(draw, text, font, max_w, warnings, tag):
    """Return text unchanged if it fits; otherwise trim words + ellipsis."""
    if draw.textlength(text, font=font) <= max_w:
        return text
    words = text.split(" ")
    out = ""
    for word in words:
        cand = (out + " " + word).strip()
        if draw.textlength(cand + " \u2026", font=font) <= max_w:
            out = cand
        else:
            break
    warnings.append("%s truncated: %r" % (tag, text))
    return out + " \u2026"


def draw():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    warnings = []

    f_title = ImageFont.truetype(SANS_B, 40)
    f_sub = ImageFont.truetype(SANS_B, 15)
    f_tag = ImageFont.truetype(SANS_B, 13)
    f_time = ImageFont.truetype(SANS_B, 14)
    f_head = ImageFont.truetype(SANS_B, 14)
    f_det = ImageFont.truetype(SANS, 12)
    f_foot = ImageFont.truetype(SANS_B, 12)
    f_src = ImageFont.truetype(SANS, 11)

    # --- header ------------------------------------------------------------
    d.text((24, 14), "THURSDAY 26 NOVEMBER 2026", font=f_title, fill=CREAM)
    d.text((24, 64), HEADER_SUB, font=f_sub, fill=GOLD)
    tag = "TIMELINE \u2022 UTC"
    tw = d.textlength(tag, font=f_tag)
    d.rounded_rectangle([W - 24 - tw - 28, 20, W - 24, 52], radius=4,
                        outline=GOLD, width=2)
    d.text((W - 24 - tw - 14, 27), tag, font=f_tag, fill=GOLD)
    d.line([(0, HEADER_H), (W, HEADER_H)], fill=RULE, width=2)

    # --- rows ------------------------------------------------------------------
    n = len(STORIES)
    step = (BOTTOM - TOP) / n
    for i, (t, region, head, det) in enumerate(STORIES):
        y = TOP + i * step
        if i % 2 == 0:
            d.rectangle([0, y - 2, W, y + step - 2], fill=(16, 32, 48))
        color, _label = REGIONS[region]
        head = fit_text(d, head, f_head, TEXT_RIGHT - TEXT_X, warnings, "head %s" % t)
        det = fit_text(d, det, f_det, TEXT_RIGHT - TEXT_X, warnings, "det %s" % t)
        d.text((TIME_RIGHT, y + 1), t, font=f_time, fill=MUTED, anchor="ra")
        d.ellipse([SPINE_X - 5, y + 3, SPINE_X + 5, y + 13], fill=color,
                  outline=GOLD, width=1)
        d.text((TEXT_X, y), head, font=f_head, fill=CREAM)
        d.text((TEXT_X, y + 15), det, font=f_det, fill=FAINT)

    # --- spine (drawn last so it stays continuous over the row bands) ---------
    d.line([(SPINE_X, TOP - 4), (SPINE_X, BOTTOM + 4)], fill=SPINE, width=3)
    for i, (t, region, head, det) in enumerate(STORIES):
        y = TOP + i * step
        color, _label = REGIONS[region]
        d.ellipse([SPINE_X - 5, y + 3, SPINE_X + 5, y + 13], fill=color,
                  outline=GOLD, width=1)

    # --- footer: region chips --------------------------------------------------
    d.line([(0, FOOTER_RULE_Y), (W, FOOTER_RULE_Y)], fill=RULE, width=2)
    counts = {}
    for _t, region, _h, _d in STORIES:
        counts[region] = counts.get(region, 0) + 1
    order = ["europe", "east_asia", "se_asia", "south_asia", "middle_east",
             "africa", "n_america", "pacific", "latin_am"]
    chips = []
    total_w = 0
    for key in order:
        color, label = REGIONS[key]
        txt = "%s %d" % (label, counts[key])
        w = 12 + d.textlength(txt, font=f_foot) + 18
        chips.append((color, txt, w))
        total_w += w
    x = (W - total_w) / 2
    for color, txt, w in chips:
        d.ellipse([x, 972, x + 9, 981], fill=color)
        d.text((x + 13, 968), txt, font=f_foot, fill=CREAM)
        x += w
    sw = d.textlength(FOOTER_SRC, font=f_src)
    d.text(((W - sw) / 2, 994), FOOTER_SRC, font=f_src, fill=MUTED)

    for warn in warnings:
        print("WARN:", warn)
    print("stories:", n, "| regions:", len(counts),
          "| fields: 19 | size:", W, "x", H)
    return img


def main():
    img = draw()
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
