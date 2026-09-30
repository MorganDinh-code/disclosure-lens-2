"""Shared look-and-feel: black / deep navy / gold, serif type."""
import streamlit as st

GOLD, GREEN, RED, GREY, MUTED = "#C9A24B", "#4C9F70", "#C8534F", "#5B6577", "#8C93A3"
FACT = {1: GREEN, -1: RED, 0: GREY}


def tone_color(t):
    return GREEN if t > 0.05 else RED if t < -0.05 else GREY


def pct(x):
    return "n/a" if x is None else f"{x * 100:.0f}%"


def apply_theme():
    st.markdown(f"""<style>
    h1,h2,h3 {{ font-weight:600; letter-spacing:.01em; }}
    h2 {{ border-bottom:1px solid {GOLD}55; padding-bottom:.35rem; margin-top:2rem; }}
    .eyebrow {{ color:{GOLD}; text-transform:uppercase; letter-spacing:.18em; font-size:.72rem; font-weight:600; }}
    .tagline {{ font-size:2.1rem; font-weight:600; margin:.2rem 0 .3rem; }}
    .lede {{ color:{MUTED}; font-size:1.02rem; max-width:52rem; line-height:1.55; }}
    div[data-testid="stMetricLabel"] p {{ color:{MUTED}; text-transform:uppercase; letter-spacing:.08em; font-size:.7rem; }}
    div[data-testid="stMetricValue"] {{ font-variant-numeric:tabular-nums; }}
    .card {{ border:1px solid #1E2C48; border-top:2px solid {GOLD}; background:#0E1A30; padding:1rem 1.2rem; border-radius:2px; height:100%; }}
    .card b {{ color:{GOLD}; text-transform:uppercase; letter-spacing:.1em; font-size:.7rem; }}
    .badge {{ background:{GOLD}22; color:{GOLD}; padding:1px 8px; font-size:.7rem; letter-spacing:.06em; text-transform:uppercase; }}
    </style>""", unsafe_allow_html=True)


def header():
    st.markdown('<div class="eyebrow">Disclosure Lens</div>'
                '<div class="tagline">Position. Hedging. Tone.</div>'
                '<div class="lede">An open research tool that maps the structure of corporate disclosures: '
                'where information appears, how it is qualified, and how it is framed.</div>',
                unsafe_allow_html=True)


def strip(dirs, mats):
    """Position strip: one block per sentence, coloured by financial direction."""
    b = "".join(f'<div title="Sentence {i + 1}" style="flex:1;height:26px;background:{FACT[d]};'
                f'border-right:1px solid #070B14;{"outline:2px solid #E9E6DC;outline-offset:-2px;" if m else ""}"></div>'
                for i, (d, m) in enumerate(zip(dirs, mats)))
    st.markdown(f'<div style="display:flex;width:100%">{b}</div>'
                f'<div style="display:flex;justify-content:space-between;font-size:.75rem;color:{MUTED}">'
                f'<span>Start of document</span><span>End of document</span></div>', unsafe_allow_html=True)
    st.caption("One block per sentence: green = positive fact, red = negative fact, grey = neutral. "
               "White outline = material negative.")


def profile(s):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<span class="eyebrow">Information order</span>', unsafe_allow_html=True)
        st.metric("Avg position, negatives", pct(s.get("mean_pos_negative")))
        st.metric("Avg position, positives", pct(s.get("mean_pos_positive")))
        st.metric("Placement asymmetry", pct(s.get("placement_asymmetry")),
                  help="Positive = bad news appears later than good news.")
        d = s.get("distance_from_headline")
        st.metric("Distance from headline", "n/a" if d is None else f"{d} sentences")
    with c2:
        st.markdown('<span class="eyebrow">Hedging</span>', unsafe_allow_html=True)
        st.metric("Hedge density near negatives", pct(s.get("hedge_near_negative")))
        st.metric("Hedge density near positives", pct(s.get("hedge_near_positive")))
        ha = s.get("hedging_asymmetry")
        st.metric("Hedging asymmetry", f"{ha:.1f}x" if ha is not None else
                  ("undefined" if s.get("hedge_near_negative") else "n/a"),
                  help="Undefined = no hedging near positives at all.")
    with c3:
        st.markdown('<span class="eyebrow">Tone vs. facts</span>', unsafe_allow_html=True)
        st.metric("Negative facts in positive language", pct(s.get("framing_ratio")))
        g = s.get("mean_tone_gap_on_negatives")
        st.metric("Mean tone gap on negatives", "n/a" if g is None else f"{g:.2f}",
                  help="Higher = more positive wording around negative facts.")


def guidelines():
    """What Disclosure Lens is (and is not) built for."""
    c1, c2 = st.columns(2)
    c1.markdown('<div class="card"><b>Built for</b><ul style="margin:.5rem 0 0 1rem;padding:0">'
                '<li><strong>Earnings press releases</strong> (best starting point)</li>'
                '<li>Earnings call transcripts, prepared remarks</li>'
                '<li>MD&amp;A sections of 10-Q and 10-K filings</li>'
                '<li>Shareholder letters and other management commentary</li></ul></div>',
                unsafe_allow_html=True)
    c2.markdown('<div class="card"><b>Not built for</b><ul style="margin:.5rem 0 0 1rem;padding:0">'
                '<li>Financial statement tables (cash flow, balance sheet, income statement)</li>'
                '<li>PDFs and scanned images (copy the text out first)</li>'
                '<li>Complete 10-Ks (too long and mostly boilerplate)</li>'
                '<li>Text in languages other than English</li></ul></div>', unsafe_allow_html=True)
    st.markdown("""
**How to prepare a document**
1. **Find it.** Company websites list press releases under *Investors* or *Investor Relations*. The free official source is
   [SEC EDGAR](https://www.sec.gov/edgar): search the company, open an **8-K** filing, then **Exhibit 99.1**.
2. **Copy the written text only.** Skip the tables of numbers at the end.
3. **Paste it or save it as a `.txt` file,** with a blank line between paragraphs.
4. The tool removes the legal *forward-looking statements* disclaimer for you if it finds one, since it is almost entirely hedging.
""")
