import json
from pathlib import Path

import pandas as pd
import streamlit as st

import ui

st.header("Database")
st.caption("Analyzed filings, organized by filing type, company and sector.")

recs = [json.loads(p.read_text()) for p in sorted(Path("database").glob("*.json"))]
if not recs:
    st.info("No filings have been added yet.")
    st.stop()

df = pd.DataFrame([{
    "Company": r["company"], "Ticker": r["ticker"], "Sector": r["sector"], "Filing type": r["filing_type"],
    "Period": r["period"], "Neg. position": ui.pct(r["summary"].get("mean_pos_negative")),
    "Placement asym.": ui.pct(r["summary"].get("placement_asymmetry")),
    "Framing ratio": ui.pct(r["summary"].get("framing_ratio")), "_i": i} for i, r in enumerate(recs)])

c1, c2, c3 = st.columns(3)
types = c1.multiselect("Filing type", sorted(df["Filing type"].unique()))
sectors = c2.multiselect("Sector", sorted(df["Sector"].unique()))
q = c3.text_input("Search company or ticker")
if types: df = df[df["Filing type"].isin(types)]
if sectors: df = df[df["Sector"].isin(sectors)]
if q: df = df[df["Company"].str.contains(q, case=False) | df["Ticker"].str.contains(q, case=False)]

st.dataframe(df.drop(columns="_i"), hide_index=True, width="stretch")
if df.empty:
    st.stop()

st.header("Filing analysis")
pick = st.selectbox("Open a filing", df["_i"], format_func=lambda i:
                    f'{recs[i]["company"]} ({recs[i]["ticker"]}) · {recs[i]["filing_type"]} · {recs[i]["period"]}')
r = recs[pick]
if r.get("demo"):
    st.markdown('<span class="badge">Illustrative: fictional company</span>', unsafe_allow_html=True)
if r.get("source_url"):
    st.markdown(f"[Source document]({r['source_url']})")
ui.profile(r["summary"])
st.subheader("Where the information sits")
ui.strip([x["d"] for x in r["sentences"]], [x["m"] for x in r["sentences"]])
