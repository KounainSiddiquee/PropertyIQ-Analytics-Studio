import os
import io
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

try:
    import joblib
except ImportError:
    joblib = None


# ============================================================
# 1. APP CONFIG
# ============================================================
st.set_page_config(
    page_title="PropertyIQ | Predictive Analytics Studio",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# 2. DESIGN SYSTEM
# ============================================================
st.markdown(
    """
    <style>
    /* ========================================================
       PROPERTYIQ — PREMIUM UI POLISH
       Visual-only layer: no data/model/prediction logic changed.
       ======================================================== */
    :root {
        --bg: #F5F2EA;
        --surface: #FFFEFA;
        --surface-soft: #F0ECE2;
        --ink: #18231E;
        --muted: #6F7872;
        --forest: #21483A;
        --forest-deep: #17372D;
        --forest-soft: #356653;
        --sage: #AAB9A7;
        --sage-pale: #E7EDE6;
        --gold: #B4935C;
        --gold-soft: #D8C49F;
        --line: #DDD8CC;
        --shadow: 0 10px 30px rgba(31, 58, 47, .065);
        --shadow-lg: 0 20px 48px rgba(31, 58, 47, .12);
    }

    #MainMenu, footer {visibility: hidden;}
    .stDeployButton {display: none;}
    [data-testid="stToolbar"] {visibility: hidden;}

    html {scroll-behavior: smooth;}

    .stApp {
        background:
            radial-gradient(circle at 88% 2%, rgba(170,185,167,.22), transparent 25rem),
            radial-gradient(circle at 8% 28%, rgba(180,147,92,.06), transparent 20rem),
            var(--bg);
        color: var(--ink);
    }

    .block-container {
        max-width: 1440px;
        padding-top: 1.45rem;
        padding-bottom: 3.5rem;
    }

    /* Header */
    .topbar {
        position: relative;
        overflow: hidden;
        background: rgba(255,254,250,.91);
        border: 1px solid rgba(221,216,204,.9);
        border-radius: 24px;
        padding: 24px 28px;
        box-shadow: var(--shadow);
        margin-bottom: 12px;
        backdrop-filter: blur(10px);
    }

    .topbar::after {
        content: "";
        position: absolute;
        width: 170px;
        height: 170px;
        border-radius: 50%;
        right: -60px;
        top: -95px;
        background: rgba(170,185,167,.16);
        pointer-events: none;
    }

    .eyebrow, .section-kicker {
        color: var(--gold);
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.8px;
        text-transform: uppercase;
    }

    .brand {
        color: var(--ink);
        font-size: 31px;
        line-height: 1.08;
        font-weight: 800;
        letter-spacing: -1.15px;
        margin-top: 5px;
    }

    .brand-sub {
        color: var(--muted);
        font-size: 13px;
        margin-top: 8px;
        line-height: 1.5;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(231,237,230,.9);
        color: var(--forest);
        border: 1px solid #CCD8CE;
        border-radius: 999px;
        padding: 8px 13px;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: .35px;
        box-shadow: 0 5px 15px rgba(33,72,58,.05);
    }

    /* Navigation */
    div[data-testid="stSegmentedControl"] {
        margin: 2px 0 8px 0;
    }

    div[data-testid="stSegmentedControl"] > div {
        background: rgba(255,254,250,.72);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 4px;
        box-shadow: 0 5px 16px rgba(31,58,47,.035);
    }

    div[data-testid="stSegmentedControl"] button {
        min-height: 38px;
        border-radius: 10px !important;
        font-weight: 700 !important;
        transition: all .18s ease;
    }

    div[data-testid="stSegmentedControl"] button:hover {
        background: var(--sage-pale) !important;
        color: var(--forest) !important;
    }

    /* Hero */
    .hero {
        position: relative;
        overflow: hidden;
        background: linear-gradient(120deg, var(--forest-deep) 0%, #285342 56%, #356653 100%);
        border: 1px solid rgba(255,255,255,.08);
        border-radius: 24px;
        padding: 27px 30px;
        margin: 18px 0 24px 0;
        box-shadow: var(--shadow-lg);
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 300px;
        height: 300px;
        border: 1px solid rgba(255,255,255,.09);
        border-radius: 50%;
        right: -90px;
        top: -185px;
    }

    .hero::before {
        content: "";
        position: absolute;
        width: 190px;
        height: 190px;
        background: rgba(180,147,92,.08);
        border-radius: 50%;
        right: 90px;
        bottom: -155px;
    }

    .hero h1, .hero h2, .hero p {color: #FBF9F2 !important;}

    .hero h2 {
        position: relative;
        z-index: 1;
        margin: 0 0 8px 0;
        font-size: 27px;
        font-weight: 760;
        letter-spacing: -.7px;
    }

    .hero p {
        position: relative;
        z-index: 1;
        opacity: .82;
        max-width: 850px;
        margin: 0;
        font-size: 13.5px;
        line-height: 1.65;
    }

    /* Section hierarchy */
    .section-kicker {margin-bottom: 4px;}

    .section-title {
        color: var(--ink);
        font-size: 23px;
        font-weight: 780;
        letter-spacing: -.55px;
        margin-bottom: 15px;
    }

    /* KPI / metric cards */
    div[data-testid="stMetric"] {
        position: relative;
        overflow: hidden;
        background: rgba(255,254,250,.94);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 17px 18px;
        box-shadow: 0 7px 22px rgba(23,32,28,.045);
        min-height: 108px;
        transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: #CBC5B8;
        box-shadow: 0 12px 28px rgba(23,32,28,.075);
    }

    div[data-testid="stMetric"]::before {
        content: "";
        position: absolute;
        left: 0;
        top: 17px;
        bottom: 17px;
        width: 3px;
        border-radius: 0 4px 4px 0;
        background: var(--gold);
        opacity: .72;
    }

    div[data-testid="stMetricLabel"] p {
        color: var(--muted) !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        letter-spacing: .2px;
    }

    div[data-testid="stMetricValue"] {
        color: var(--ink) !important;
        font-weight: 800 !important;
        letter-spacing: -.7px;
    }

    div[data-testid="stMetricDelta"] {color: var(--forest-soft) !important;}

    /* Insight cards */
    .insight-card {
        background: rgba(255,254,250,.94);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 21px;
        min-height: 150px;
        box-shadow: 0 7px 22px rgba(23,32,28,.04);
        transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
    }

    .insight-card:hover {
        transform: translateY(-2px);
        border-color: #CDC7BA;
        box-shadow: 0 12px 30px rgba(23,32,28,.07);
    }

    .insight-card .label {
        color: var(--gold);
        font-size: 9.5px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.35px;
    }

    .insight-card .big {
        color: var(--ink);
        font-size: 20px;
        font-weight: 800;
        letter-spacing: -.3px;
        margin: 9px 0;
    }

    .insight-card .copy {
        color: var(--muted);
        font-size: 12.8px;
        line-height: 1.6;
    }

    /* Prediction focal card */
    .prediction-card {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #142E25 0%, #21483A 58%, #2E5B49 100%);
        border: 1px solid rgba(255,255,255,.08);
        border-radius: 22px;
        padding: 26px;
        box-shadow: 0 17px 38px rgba(33,72,58,.17);
        margin-top: 12px;
    }

    .prediction-card::after {
        content: "";
        position: absolute;
        width: 160px;
        height: 160px;
        right: -60px;
        top: -85px;
        border-radius: 50%;
        background: rgba(180,147,92,.10);
    }

    .prediction-card .small {
        color: #CAD6CE;
        font-size: 10px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.35px;
    }

    .prediction-card .value {
        color: #FFFDF7;
        font-size: 39px;
        font-weight: 820;
        letter-spacing: -1.6px;
        margin: 6px 0 9px 0;
    }

    .prediction-card .note {
        color: #CAD6CE;
        font-size: 12px;
    }

    /* Buttons */
    .stButton > button, .stDownloadButton > button {
        min-height: 42px;
        border-radius: 12px !important;
        border: 1px solid var(--forest) !important;
        background: linear-gradient(135deg, var(--forest) 0%, var(--forest-soft) 100%) !important;
        color: #FFFDF8 !important;
        font-weight: 720 !important;
        box-shadow: 0 6px 15px rgba(33,72,58,.12);
        transition: all .18s ease !important;
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-1px);
        background: linear-gradient(135deg, #193D31 0%, #2D5B49 100%) !important;
        border-color: #193D31 !important;
        box-shadow: 0 9px 20px rgba(33,72,58,.17);
    }

    .stButton > button:disabled {
        background: #D9D8D0 !important;
        color: #858A86 !important;
        border-color: #D0CEC5 !important;
        box-shadow: none;
    }

    /* Inputs */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    [data-testid="stNumberInput"] input {
        background: rgba(255,254,250,.96) !important;
        border-color: var(--line) !important;
        border-radius: 11px !important;
    }

    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="input"] > div:focus-within {
        border-color: var(--sage) !important;
        box-shadow: 0 0 0 1px var(--sage) !important;
    }

    /* Slider: remove the old coral/pink visual accent */
    div[data-testid="stSlider"] [role="slider"] {
        background-color: var(--forest) !important;
        border-color: var(--forest) !important;
        box-shadow: 0 0 0 3px rgba(170,185,167,.22) !important;
    }

    div[data-testid="stSlider"] [data-testid="stTickBar"] {
        color: var(--muted) !important;
    }

    /* Multiselect chips */
    span[data-baseweb="tag"] {
        background-color: var(--sage-pale) !important;
        color: var(--forest) !important;
        border-radius: 8px !important;
    }

    /* Tabs */
    div[data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid var(--line);
    }

    button[data-baseweb="tab"] {
        color: var(--muted) !important;
        font-weight: 700 !important;
        border-radius: 9px 9px 0 0;
        padding-left: 14px !important;
        padding-right: 14px !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: var(--forest) !important;
        background: rgba(231,237,230,.62) !important;
    }

    /* Dataframes */
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 7px 20px rgba(23,32,28,.035);
    }

    /* Alerts */
    div[data-testid="stAlert"] {
        border-radius: 14px;
        border-width: 1px;
        box-shadow: 0 5px 16px rgba(23,32,28,.03);
    }

    /* Expander */
    details[data-testid="stExpander"] {
        background: rgba(255,254,250,.72);
        border: 1px solid var(--line) !important;
        border-radius: 15px !important;
        overflow: hidden;
    }

    /* Plot containers */
    div[data-testid="stPlotlyChart"] {
        background: rgba(255,254,250,.58);
        border: 1px solid rgba(221,216,204,.75);
        border-radius: 18px;
        padding: 6px;
        box-shadow: 0 7px 22px rgba(23,32,28,.03);
    }

    hr {border-color: var(--line) !important;}

    [data-testid="stHeader"] {
        background: rgba(245,242,234,.78);
        backdrop-filter: blur(8px);
    }

    [data-testid="stCaptionContainer"] {
        color: #858C87 !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {width: 9px; height: 9px;}
    ::-webkit-scrollbar-track {background: transparent;}
    ::-webkit-scrollbar-thumb {
        background: #C8C8BE;
        border-radius: 999px;
    }
    ::-webkit-scrollbar-thumb:hover {background: #AEB4AD;}

    @media (max-width: 900px) {
        .block-container {padding-top: .8rem;}
        .brand {font-size: 25px;}
        .topbar {padding: 20px;}
        .hero {padding: 23px;}
        .hero h2 {font-size: 23px;}
        .prediction-card .value {font-size: 32px;}
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
<style>
/* ---------- V2 EDITORIAL / PINTEREST-INSPIRED FINISH ---------- */
.editorial-hero {
    display:grid;
    grid-template-columns: 1.35fr .65fr;
    gap:18px;
    margin:20px 0 24px;
}
.editorial-main {
    min-height:270px;
    border-radius:28px;
    padding:38px 40px;
    background:
        radial-gradient(circle at 88% 18%, rgba(216,196,159,.20), transparent 22%),
        linear-gradient(135deg,#17372D 0%,#285342 65%,#356653 100%);
    box-shadow:0 24px 55px rgba(31,58,47,.16);
    position:relative; overflow:hidden;
    display:flex; flex-direction:column; justify-content:flex-end;
}
.editorial-main:before {
    content:"PROPERTY / INTELLIGENCE";
    position:absolute; top:28px; left:40px;
    font-size:10px; letter-spacing:2.2px; font-weight:800;
    color:rgba(255,255,255,.55);
}
.editorial-main h2 {
    color:#FFFDF7!important; font-size:36px; line-height:1.08;
    max-width:720px; letter-spacing:-1.4px; margin:0 0 12px;
}
.editorial-main p {
    color:rgba(255,253,247,.72)!important; max-width:700px;
    font-size:13.5px; line-height:1.65; margin:0;
}
.editorial-side {
    border-radius:28px; padding:28px;
    background:#FFFEFA; border:1px solid var(--line);
    box-shadow:var(--shadow);
    display:flex; flex-direction:column; justify-content:space-between;
}
.editorial-side .mini-label {
    font-size:9px; letter-spacing:1.7px; font-weight:800;
    color:var(--gold); text-transform:uppercase;
}
.editorial-side .statement {
    font-size:22px; line-height:1.22; font-weight:760;
    letter-spacing:-.6px; color:var(--ink); margin:14px 0 26px;
}
.editorial-side .meta {
    padding-top:18px; border-top:1px solid var(--line);
    color:var(--muted); font-size:12px; line-height:1.55;
}

.kpi-editorial {
    background:#FFFEFA; border:1px solid var(--line);
    border-radius:20px; padding:20px 22px; min-height:118px;
    box-shadow:0 8px 24px rgba(23,32,28,.045);
}
.kpi-editorial .k-label {
    color:var(--muted); font-size:10px; font-weight:750;
    text-transform:uppercase; letter-spacing:1.15px; margin-bottom:11px;
}
.kpi-editorial .k-value {
    color:var(--ink); font-size:28px; font-weight:820;
    letter-spacing:-1px; line-height:1.05;
}
.kpi-editorial .k-note {
    color:#8B918C; font-size:10.5px; margin-top:8px;
}

.overview-grid-title {
    font-size:29px; font-weight:790; letter-spacing:-1px;
    line-height:1.12; color:var(--ink); margin:3px 0 8px;
}
.overview-grid-copy {
    color:var(--muted); font-size:13px; line-height:1.65;
    max-width:520px; margin-bottom:18px;
}
.market-feature {
    background:linear-gradient(145deg,#EEE9DE,#F8F5ED);
    border:1px solid var(--line); border-radius:24px;
    padding:28px; min-height:245px; position:relative; overflow:hidden;
}
.market-feature .mf-label {
    color:var(--gold); font-size:9px; font-weight:800;
    letter-spacing:1.5px; text-transform:uppercase;
}
.market-feature .mf-value {
    color:var(--forest); font-size:43px; font-weight:820;
    letter-spacing:-1.8px; margin:18px 0 8px;
}
.market-feature .mf-copy {
    color:var(--muted); font-size:12.5px; line-height:1.6;
    max-width:360px;
}

/* Make navigation feel like a real premium nav rail */
div[data-testid="stSegmentedControl"] > div {
    width:fit-content!important; padding:5px!important;
    border-radius:999px!important; background:#EAE6DC!important;
    border:1px solid #DCD6C9!important;
}
div[data-testid="stSegmentedControl"] button {
    border-radius:999px!important; padding:0 18px!important;
    min-height:40px!important;
}
div[data-testid="stSegmentedControl"] button[aria-pressed="true"] {
    background:#FFFEFA!important;
    box-shadow:0 5px 15px rgba(31,58,47,.10)!important;
    color:var(--forest)!important;
}

/* Metric labels: force visible and visually distinct everywhere */
div[data-testid="stMetricLabel"] {display:block!important; opacity:1!important;}
div[data-testid="stMetricLabel"] p {
    display:block!important; color:#6F7872!important;
    font-size:11px!important; font-weight:750!important;
    text-transform:uppercase!important; letter-spacing:.65px!important;
    margin-bottom:8px!important;
}

.insight-spotlight {
    border-radius:26px; padding:30px;
    background:#17372D; color:#FFFDF7;
    min-height:230px; box-shadow:0 20px 45px rgba(31,58,47,.14);
}
.insight-spotlight .number {
    color:var(--gold-soft); font-size:10px; font-weight:800;
    letter-spacing:1.8px; text-transform:uppercase;
}
.insight-spotlight .title {
    font-size:27px; font-weight:780; letter-spacing:-.8px;
    margin:30px 0 10px;
}
.insight-spotlight .copy {
    color:rgba(255,253,247,.72); font-size:13px; line-height:1.65;
}

@media(max-width:900px){
    .editorial-hero{grid-template-columns:1fr;}
    .editorial-main{min-height:250px;padding:30px;}
    .editorial-main h2{font-size:30px;}
}
</style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <style>
    /* ========================================================
       FINAL PREMIUM VISIBILITY + SURFACE POLISH
       CSS ONLY — application logic/functionality untouched
       ======================================================== */

    /* Base widget labels: ensure labels such as Color points by are visible */
    .stApp label,
    div[data-testid="stWidgetLabel"] p,
    div[data-testid="stWidgetLabel"] span {
        color: #25352E !important;
        opacity: 1 !important;
        font-weight: 700 !important;
    }

    /* Selectboxes / multiselects: readable cream surfaces and dark text */
    div[data-baseweb="select"] > div {
        background: #FFFEFA !important;
        border: 1px solid #D8D2C6 !important;
        color: #25352E !important;
        box-shadow: 0 4px 14px rgba(31,58,47,.035) !important;
    }

    div[data-baseweb="select"] *,
    div[data-baseweb="popover"] *,
    div[role="listbox"] *,
    div[role="option"] * {
        color: #25352E !important;
        opacity: 1 !important;
    }

    /* Dropdown menus/options — removes invisible white-on-white options */
    div[data-baseweb="popover"] > div,
    div[role="listbox"] {
        background: #FFFEFA !important;
        border: 1px solid #D8D2C6 !important;
        border-radius: 13px !important;
        box-shadow: 0 14px 34px rgba(31,58,47,.12) !important;
    }

    div[role="option"] {
        background: #FFFEFA !important;
        color: #25352E !important;
    }

    div[role="option"]:hover,
    div[role="option"][aria-selected="true"] {
        background: #E7EDE6 !important;
        color: #17372D !important;
    }

    /* Inputs and number controls */
    input, textarea,
    [data-testid="stNumberInput"] input {
        color: #25352E !important;
        background: #FFFEFA !important;
        -webkit-text-fill-color: #25352E !important;
    }

    [data-testid="stNumberInput"] button {
        color: #315E4C !important;
        background: #F0ECE2 !important;
        border-color: #D8D2C6 !important;
    }

    /* Slider/select-slider values and tick labels */
    div[data-testid="stSlider"] *,
    div[data-testid="stSelectSlider"] * {
        color: #394941 !important;
    }

    div[data-testid="stSlider"] [role="slider"],
    div[data-testid="stSelectSlider"] [role="slider"] {
        background: #315E4C !important;
        border-color: #315E4C !important;
    }

    /* Tabs: visible inactive labels and refined active state */
    button[data-baseweb="tab"] p,
    button[data-baseweb="tab"] span {
        color: #69736D !important;
        opacity: 1 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] p,
    button[data-baseweb="tab"][aria-selected="true"] span {
        color: #21483A !important;
        font-weight: 800 !important;
    }

    /* Alerts: force readable text on all info/warning/success surfaces */
    div[data-testid="stAlert"] {
        background: #F2EEE4 !important;
        border: 1px solid #D8CFBC !important;
        color: #3A463F !important;
    }

    div[data-testid="stAlert"] *,
    div[data-testid="stAlert"] p,
    div[data-testid="stAlert"] span {
        color: #3A463F !important;
        opacity: 1 !important;
    }

    /* Disabled button: readable 'No predictions yet' */
    .stButton > button:disabled,
    .stButton > button:disabled *,
    button:disabled {
        background: #E8E5DC !important;
        color: #646D67 !important;
        -webkit-text-fill-color: #646D67 !important;
        opacity: 1 !important;
        border-color: #D3CEC2 !important;
    }

    /* Premium dataframe/table treatment */
    div[data-testid="stDataFrame"] {
        background: #FFFEFA !important;
        border: 1px solid #DCD6CA !important;
        border-radius: 18px !important;
        padding: 4px !important;
        box-shadow: 0 10px 28px rgba(31,58,47,.055) !important;
    }

    div[data-testid="stDataFrame"] canvas {
        border-radius: 14px !important;
    }

    /* Native Streamlit table fallback */
    div[data-testid="stTable"] {
        border: 1px solid #DCD6CA !important;
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 24px rgba(31,58,47,.045) !important;
    }

    div[data-testid="stTable"] table {
        background: #FFFEFA !important;
        color: #25352E !important;
    }

    div[data-testid="stTable"] th {
        background: #E9E7DE !important;
        color: #21483A !important;
        font-weight: 800 !important;
    }

    div[data-testid="stTable"] td {
        background: #FFFEFA !important;
        color: #394941 !important;
        border-color: #E7E2D8 !important;
    }

    /* Plot surfaces: more editorial and premium */
    div[data-testid="stPlotlyChart"] {
        position: relative;
        overflow: hidden;
        background:
            radial-gradient(circle at 96% 0%, rgba(170,185,167,.12), transparent 145px),
            rgba(255,254,250,.88) !important;
        border: 1px solid #DDD8CC !important;
        border-radius: 22px !important;
        padding: 10px 10px 4px !important;
        box-shadow: 0 12px 30px rgba(31,58,47,.055) !important;
    }

    /* Soft decorative surface around expanders */
    details[data-testid="stExpander"] {
        background:
            radial-gradient(circle at 98% 0%, rgba(180,147,92,.07), transparent 120px),
            #FFFEFA !important;
        box-shadow: 0 8px 24px rgba(31,58,47,.04) !important;
    }

    /* Refined download/action buttons */
    .stDownloadButton > button {
        letter-spacing: .1px !important;
        box-shadow: 0 8px 20px rgba(33,72,58,.13) !important;
    }

    /* Add delicate decorative bubbles to major hero surfaces */
    .hero::after {
        box-shadow:
            -90px 130px 0 -45px rgba(255,255,255,.045),
            -205px 35px 0 -70px rgba(216,196,159,.09) !important;
    }

    .editorial-main::after {
        content: "";
        position: absolute;
        width: 210px;
        height: 210px;
        border-radius: 50%;
        right: -75px;
        top: -85px;
        border: 1px solid rgba(255,255,255,.10);
        box-shadow:
            -105px 145px 0 -65px rgba(216,196,159,.10),
            -230px 35px 0 -82px rgba(255,255,255,.055);
        pointer-events: none;
    }

    .editorial-side {
        position: relative;
        overflow: hidden;
    }

    .editorial-side::after {
        content: "";
        position: absolute;
        width: 115px;
        height: 115px;
        border-radius: 50%;
        right: -54px;
        bottom: -54px;
        background: rgba(170,185,167,.11);
        border: 1px solid rgba(170,185,167,.18);
        pointer-events: none;
    }

    .market-feature::after {
        content: "";
        position: absolute;
        width: 145px;
        height: 145px;
        border-radius: 50%;
        right: -65px;
        bottom: -72px;
        border: 1px solid rgba(180,147,92,.18);
        box-shadow: -92px -48px 0 -56px rgba(170,185,167,.13);
        pointer-events: none;
    }

    /* Gentle section separators — premium without bold blocks */
    hr {
        margin-top: 2.1rem !important;
        margin-bottom: 2.1rem !important;
        border: 0 !important;
        height: 1px !important;
        background: linear-gradient(
            90deg,
            transparent 0%,
            #DCD6CA 18%,
            #DCD6CA 82%,
            transparent 100%
        ) !important;
    }

    /* Better focus ring while preserving all functionality */
    button:focus-visible,
    input:focus-visible {
        outline: 2px solid rgba(49,94,76,.28) !important;
        outline-offset: 2px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <style>
    /* ===== FINAL HIGH-SPECIFICITY VISIBILITY FIXES ===== */

    /* TAB LABELS: Scatter Explorer / Distribution / Correlation / Data Table */
    .stTabs [data-baseweb="tab-list"] button,
    .stTabs [data-baseweb="tab-list"] button *,
    .stTabs button[role="tab"],
    .stTabs button[role="tab"] *,
    [data-baseweb="tab-list"] [role="tab"],
    [data-baseweb="tab-list"] [role="tab"] * {
        color: #68736D !important;
        -webkit-text-fill-color: #68736D !important;
        opacity: 1 !important;
        visibility: visible !important;
    }

    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"],
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] *,
    [data-baseweb="tab-list"] [role="tab"][aria-selected="true"],
    [data-baseweb="tab-list"] [role="tab"][aria-selected="true"] * {
        color: #17372D !important;
        -webkit-text-fill-color: #17372D !important;
        font-weight: 800 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: #ECE9E0 !important;
        padding: 5px !important;
        border: 1px solid #DCD6CA !important;
        border-radius: 14px !important;
        gap: 3px !important;
    }

    .stTabs [data-baseweb="tab-list"] button {
        border-radius: 10px !important;
        padding: 8px 15px !important;
    }

    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: #FFFEFA !important;
        box-shadow: 0 4px 12px rgba(31,58,47,.08) !important;
    }

    /* SELECT / SELECT-SLIDER CURRENT VALUES */
    [data-baseweb="select"] div,
    [data-baseweb="select"] span,
    [data-baseweb="select"] input,
    [data-testid="stSelectbox"] div,
    [data-testid="stSelectbox"] span,
    [data-testid="stSelectSlider"] div,
    [data-testid="stSelectSlider"] span,
    [data-testid="stSelectSlider"] p {
        color: #25352E !important;
        -webkit-text-fill-color: #25352E !important;
        opacity: 1 !important;
    }

    /* SELECT SLIDER track labels */
    [data-testid="stSelectSlider"] [data-testid="stTickBar"] *,
    [data-testid="stSelectSlider"] [data-testid="stThumbValue"] {
        color: #3D4B44 !important;
        -webkit-text-fill-color: #3D4B44 !important;
    }

    /* DROPDOWN MENU */
    [data-baseweb="popover"],
    [data-baseweb="popover"] div,
    [data-baseweb="popover"] li,
    [data-baseweb="popover"] span {
        color: #25352E !important;
        -webkit-text-fill-color: #25352E !important;
    }

    /* DATAFRAME / GLIDE GRID: broad theme overrides */
    [data-testid="stDataFrame"],
    [data-testid="stDataFrame"] > div,
    [data-testid="stDataFrame"] iframe {
        background-color: #FFFEFA !important;
        color: #25352E !important;
    }

    [data-testid="stDataFrame"] {
        --gdg-bg-cell: #FFFEFA !important;
        --gdg-bg-cell-medium: #F6F2E9 !important;
        --gdg-bg-header: #E7EDE6 !important;
        --gdg-bg-header-hovered: #DEE7DD !important;
        --gdg-bg-header-has-focus: #D6E1D5 !important;
        --gdg-text-dark: #25352E !important;
        --gdg-text-medium: #536159 !important;
        --gdg-text-light: #78817C !important;
        --gdg-border-color: #DED8CC !important;
        --gdg-accent-color: #315E4C !important;
        --gdg-accent-light: rgba(49,94,76,.12) !important;
    }

    /* Toolbar around dataframe */
    [data-testid="stElementToolbar"] button,
    [data-testid="stElementToolbar"] svg {
        color: #536159 !important;
        fill: #536159 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <style>
    /* Final tab-label visibility override.
       Covers Explore Data and Predict tabs without changing behavior or layout. */
    .stTabs [data-baseweb="tab-list"] button,
    .stTabs [data-baseweb="tab-list"] button *,
    .stTabs button[role="tab"],
    .stTabs button[role="tab"] *,
    div[data-testid="stTabs"] [data-baseweb="tab-list"] button,
    div[data-testid="stTabs"] [data-baseweb="tab-list"] button *,
    div[data-testid="stTabs"] button[role="tab"],
    div[data-testid="stTabs"] button[role="tab"] * {
        color: #4F5E56 !important;
        -webkit-text-fill-color: #4F5E56 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }

    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"],
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] *,
    .stTabs button[role="tab"][aria-selected="true"],
    .stTabs button[role="tab"][aria-selected="true"] *,
    div[data-testid="stTabs"] [data-baseweb="tab-list"] button[aria-selected="true"],
    div[data-testid="stTabs"] [data-baseweb="tab-list"] button[aria-selected="true"] *,
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"],
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] * {
        color: #17372D !important;
        -webkit-text-fill-color: #17372D !important;
        font-weight: 800 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# ============================================================
# 3. HELPERS
# ============================================================
@st.cache_data
def load_dataset():
    candidates = [
        "dataset/cleaned_properties.csv",
        "cleaned_properties.csv",
    ]
    for path in candidates:
        if os.path.exists(path):
            return pd.read_csv(path), path
    return None, None


@st.cache_resource
def load_model():
    if joblib is None:
        return None, None
    candidates = [
        "models/random_forest_model.pkl",
        "random_forest_model.pkl",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return joblib.load(path), path
            except Exception:
                return None, None
    return None, None


def money(value):
    return f"${value:,.0f}"


def section(kicker, title):
    st.markdown(
        f'<div class="section-kicker">{kicker}</div>'
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True,
    )


def style_plot(fig, height=360):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FBFAF6",
        font=dict(color="#33413A"),
        margin=dict(l=20, r=20, t=35, b=20),
        legend_title_text="",
        hoverlabel=dict(bgcolor="#FFFEFA", font_color="#18231E", bordercolor="#DDD8CC"),
    )
    fig.update_xaxes(
        gridcolor="#E7E2D8",
        zerolinecolor="#E7E2D8",
        linecolor="#D8D2C6",
        tickfont=dict(color="#6F7872"),
        title_font=dict(color="#455149"),
    )
    fig.update_yaxes(
        gridcolor="#E7E2D8",
        zerolinecolor="#E7E2D8",
        linecolor="#D8D2C6",
        tickfont=dict(color="#6F7872"),
        title_font=dict(color="#455149"),
    )
    return fig


def build_model_input(sqft, beds, age, location, model):
    # The training script uses pd.get_dummies(..., drop_first=True).
    # Most likely feature order after encoding is:
    # Square_Feet, Bedrooms, Age_Years, Location_Grade_B, Location_Grade_C.
    if model is None:
        return None
    feature_names = getattr(model, "feature_names_in_", None)
    if feature_names is None:
        return pd.DataFrame([{
            "Square_Feet": sqft,
            "Bedrooms": beds,
            "Age_Years": age,
            "Location_Grade_B": 1 if location == "B" else 0,
            "Location_Grade_C": 1 if location == "C" else 0,
        }])
    row = {}
    for feature in feature_names:
        if feature == "Square_Feet":
            row[feature] = sqft
        elif feature == "Bedrooms":
            row[feature] = beds
        elif feature == "Age_Years":
            row[feature] = age
        elif feature == "Location_Grade_B":
            row[feature] = 1 if location == "B" else 0
        elif feature == "Location_Grade_C":
            row[feature] = 1 if location == "C" else 0
        else:
            row[feature] = 0
    return pd.DataFrame([row])


def predict_value(sqft, beds, age, location, model):
    if model is not None:
        try:
            X = build_model_input(sqft, beds, age, location, model)
            return float(model.predict(X)[0]), "Trained Random Forest"
        except Exception:
            pass

    # Transparent fallback when the saved model is unavailable/incompatible.
    value = sqft * 142 + beds * 25000 - age * 1150
    if location == "A":
        value *= 1.22
    elif location == "C":
        value *= 0.88
    return max(float(value), 50000), "Rule-based fallback"


def model_importance_df(model):
    if model is None or not hasattr(model, "feature_importances_"):
        return None
    names = getattr(
        model,
        "feature_names_in_",
        [f"Feature {i+1}" for i in range(len(model.feature_importances_))],
    )
    return pd.DataFrame({
        "Feature": list(names),
        "Importance": model.feature_importances_,
    }).sort_values("Importance", ascending=True)


def percentile_rank(series, value):
    return float((series <= value).mean() * 100)


df, dataset_path = load_dataset()
model, model_path = load_model()

if df is None:
    st.error("Cleaned dataset not found. Run clean_data.py first.")
    st.stop()

required = {"Square_Feet", "Bedrooms", "Age_Years", "Location_Grade", "Price_USD"}
missing = required.difference(df.columns)
if missing:
    st.error(f"Dataset is missing required columns: {', '.join(sorted(missing))}")
    st.stop()

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []


# ============================================================
# 4. HEADER + FUNCTIONAL NAVIGATION
# ============================================================
header_left, header_right = st.columns([8, 2], vertical_alignment="center")

with header_left:
    st.markdown(
        """
        <div class="topbar">
            <div class="eyebrow">Predictive Analytics System</div>
            <div class="brand">PropertyIQ Analytics Studio</div>
            <div class="brand-sub">
                Explore data · Build predictions · Explain model behavior · Generate actionable insights
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_right:
    st.markdown(
        f"""
        <div style="text-align:right;padding:12px 0;">
            <span class="status-pill">● SYSTEM ONLINE</span>
            <div style="margin-top:9px;color:#6D756F;font-size:11px;">
                {datetime.now().strftime("%d %b %Y")}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

page = st.segmented_control(
    "Navigation",
    ["Overview", "Explore Data", "Predict", "Model Lab", "Insights", "Reports"],
    default="Overview",
    label_visibility="collapsed",
)


# ============================================================
# 5. OVERVIEW PAGE
# ============================================================
if page == "Overview":
    avg_price = df["Price_USD"].mean()
    median_price = df["Price_USD"].median()
    avg_area = df["Square_Feet"].mean()
    premium_location = df.groupby("Location_Grade")["Price_USD"].mean().idxmax()
    completeness = (1 - df.isna().sum().sum() / max(df.size, 1)) * 100
    corr_area = df["Square_Feet"].corr(df["Price_USD"])
    price_spread = df["Price_USD"].quantile(.75) - df["Price_USD"].quantile(.25)

    # Editorial opening instead of the same hero + horizontal KPI strip
    st.markdown(
        f"""
        <div class="editorial-hero">
            <div class="editorial-main">
                <h2>Property intelligence,<br>designed for decisions.</h2>
                <p>A refined analytical workspace that turns market records into clear signals,
                comparable segments and decision-ready property intelligence.</p>
            </div>
            <div class="editorial-side">
                <div>
                    <div class="mini-label">Live dataset portrait</div>
                    <div class="statement">A compact view of the market before you explore the details.</div>
                </div>
                <div class="meta">
                    <b>{len(df):,} clean records</b><br>
                    {completeness:.1f}% complete · Grade {premium_location} leads average pricing
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Asymmetric first fold: narrative + only two principal KPIs
    intro, primary_kpis = st.columns([1.05, 1.35], gap="large")
    with intro:
        st.markdown(
            """
            <div class="section-kicker">Market at a glance</div>
            <div class="overview-grid-title">The numbers that frame<br>this property market.</div>
            <div class="overview-grid-copy">
                Start with price and scale. Supporting indicators sit deeper in the page,
                so the dashboard reads like a story rather than a row of disconnected counters.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="market-feature">
                <div class="mf-label">Leading location segment</div>
                <div class="mf-value">Grade {premium_location}</div>
                <div class="mf-copy">
                    This location grade currently carries the highest average property price
                    across the loaded records.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with primary_kpis:
        a, b = st.columns(2)
        with a:
            st.markdown(
                f"""<div class="kpi-editorial">
                <div class="k-label">Average property price</div>
                <div class="k-value">{money(avg_price)}</div>
                <div class="k-note">Mean value across all clean records</div></div>""",
                unsafe_allow_html=True,
            )
        with b:
            st.markdown(
                f"""<div class="kpi-editorial">
                <div class="k-label">Typical property size</div>
                <div class="k-value">{avg_area:,.0f} sq ft</div>
                <div class="k-note">Average floor area in the dataset</div></div>""",
                unsafe_allow_html=True,
            )

        st.write("")
        section("Price portrait", "How values are distributed")
        fig = px.histogram(df, x="Price_USD", nbins=24)
        fig.update_traces(marker_color="#315E4C", opacity=.92)
        fig.update_layout(bargap=.08)
        st.plotly_chart(style_plot(fig, 330), use_container_width=True)

    st.write("")
    st.write("")
    section("Market signals", "Context behind the headline numbers")

    s1, s2, s3 = st.columns([1, 1, 1])
    with s1:
        st.markdown(
            f"""<div class="kpi-editorial">
            <div class="k-label">Median property price</div>
            <div class="k-value">{money(median_price)}</div>
            <div class="k-note">Midpoint of observed property values</div></div>""",
            unsafe_allow_html=True,
        )
    with s2:
        st.markdown(
            f"""<div class="kpi-editorial">
            <div class="k-label">Middle-market price spread</div>
            <div class="k-value">{money(price_spread)}</div>
            <div class="k-note">Interquartile range: 25th to 75th percentile</div></div>""",
            unsafe_allow_html=True,
        )
    with s3:
        st.markdown(
            f"""<div class="kpi-editorial">
            <div class="k-label">Area ↔ price correlation</div>
            <div class="k-value">{corr_area:+.2f}</div>
            <div class="k-note">Strength of the linear relationship</div></div>""",
            unsafe_allow_html=True,
        )

    st.write("")
    chart_text, chart_b = st.columns([.72, 1.28], gap="large")
    with chart_text:
        section("Segment lens", "Where the market sits")
        st.markdown(
            """
            <div class="overview-grid-copy">
                Location segments are shown as a ranked market profile rather than another
                conventional dashboard bar chart. This keeps the overview visually lighter
                while preserving the comparison.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.metric("Clean records", f"{len(df):,}", help="Number of processed property records available for analysis")
        st.metric("Data completeness", f"{completeness:.1f}%", help="Share of dataset cells containing non-null values")

    with chart_b:
        loc = df.groupby("Location_Grade", as_index=False)["Price_USD"].mean().sort_values("Price_USD")
        fig = px.scatter(
            loc, x="Price_USD", y="Location_Grade", size="Price_USD",
            text=loc["Price_USD"].map(lambda x: f"${x/1000:.0f}k"),
        )
        fig.update_traces(marker=dict(color="#B6945D", line=dict(width=2, color="#FFFEFA")), textposition="middle right")
        fig.update_layout(showlegend=False)
        st.plotly_chart(style_plot(fig, 310), use_container_width=True)

    st.write("")
    section("Data health", "Quiet checks, kept out of the spotlight")
    h1, h2, h3 = st.columns(3)
    h1.metric("Rows available", f"{len(df):,}")
    h2.metric("Remaining null values", int(df.isnull().sum().sum()))
    h3.metric("Remaining duplicate rows", int(df.duplicated().sum()))


# ============================================================
# 6. EXPLORE DATA PAGE
# ============================================================
elif page == "Explore Data":
    st.markdown(
        """
        <div class="hero">
            <h2>Explore the market without touching the code.</h2>
            <p>Filter the dataset, inspect distributions, compare segments and export exactly the records you need.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section("Interactive filters", "Build your own analytical slice")
    f1, f2, f3, f4 = st.columns(4)

    min_price = int(df["Price_USD"].min())
    max_price = int(df["Price_USD"].max())
    min_area = int(df["Square_Feet"].min())
    max_area = int(df["Square_Feet"].max())

    with f1:
        price_range = st.slider(
            "Price range",
            min_price,
            max_price,
            (min_price, max_price),
        )
    with f2:
        area_range = st.slider(
            "Area range",
            min_area,
            max_area,
            (min_area, max_area),
        )
    with f3:
        locations = st.multiselect(
            "Location grades",
            sorted(df["Location_Grade"].dropna().unique().tolist()),
            default=sorted(df["Location_Grade"].dropna().unique().tolist()),
        )
    with f4:
        bedrooms = st.multiselect(
            "Bedrooms",
            sorted(df["Bedrooms"].dropna().unique().tolist()),
            default=sorted(df["Bedrooms"].dropna().unique().tolist()),
        )

    filtered = df[
        df["Price_USD"].between(*price_range)
        & df["Square_Feet"].between(*area_range)
        & df["Location_Grade"].isin(locations)
        & df["Bedrooms"].isin(bedrooms)
    ].copy()

    q1, q2, q3, q4 = st.columns(4)
    q1.metric("Matching records", len(filtered))
    q2.metric("Average price", money(filtered["Price_USD"].mean()) if len(filtered) else "—")
    q3.metric("Average area", f"{filtered['Square_Feet'].mean():,.0f} sq ft" if len(filtered) else "—")
    q4.metric("Average age", f"{filtered['Age_Years'].mean():.1f} years" if len(filtered) else "—")

    if filtered.empty:
        st.warning("No records match the selected filters.")
    else:
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Scatter Explorer", "Distribution", "Correlation", "Data Table"]
        )

        with tab1:
            color_by = st.selectbox(
                "Color points by",
                ["Location_Grade", "Bedrooms", "Age_Years"],
            )
            fig = px.scatter(
                filtered,
                x="Square_Feet",
                y="Price_USD",
                color=color_by,
                size="Bedrooms",
                hover_data=["Age_Years", "Location_Grade"],
            )
            st.plotly_chart(style_plot(fig, 440), use_container_width=True)

        with tab2:
            variable = st.selectbox(
                "Analyze distribution of",
                ["Price_USD", "Square_Feet", "Bedrooms", "Age_Years"],
            )

            # Premium distribution view: softer bars + median reference + editorial annotation.
            median_value = filtered[variable].median()
            fig = px.histogram(
                filtered,
                x=variable,
                nbins=22,
                marginal="box",
                opacity=0.88,
            )
            fig.update_traces(
                marker_color="#7F9A88",
                marker_line_color="#FFFEFA",
                marker_line_width=1.2,
            )
            fig.add_vline(
                x=median_value,
                line_width=2,
                line_dash="dot",
                line_color="#B4935C",
                annotation_text="Median",
                annotation_position="top",
            )
            fig.update_layout(
                bargap=0.08,
                showlegend=False,
                xaxis_title=variable.replace("_", " "),
                yaxis_title="Number of properties",
            )
            st.plotly_chart(style_plot(fig, 440), use_container_width=True)

        with tab3:
            corr = filtered.select_dtypes(include="number").corr()
            fig = px.imshow(
                corr,
                text_auto=".2f",
                aspect="auto",
                color_continuous_scale=[
                    [0, "#E7DDD0"],
                    [.5, "#F8F5ED"],
                    [1, "#315E4C"],
                ],
            )
            st.plotly_chart(style_plot(fig, 440), use_container_width=True)

        with tab4:
            st.dataframe(filtered, use_container_width=True, hide_index=True)
            st.download_button(
                "Download filtered data",
                filtered.to_csv(index=False).encode("utf-8"),
                "filtered_properties.csv",
                "text/csv",
            )


# ============================================================
# 7. PREDICT PAGE
# ============================================================
elif page == "Predict":
    st.markdown(
        """
        <div class="hero">
            <h2>Turn property inputs into a decision-ready estimate.</h2>
            <p>
                Run a valuation, compare it with the current dataset, inspect percentile position
                and test alternative scenarios before saving the result.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    input_col, output_col = st.columns([.9, 1.35], gap="large")

    with input_col:
        section("Property profile", "Prediction controls")
        sqft = st.number_input(
            "Square feet",
            min_value=int(df["Square_Feet"].min()),
            max_value=max(int(df["Square_Feet"].max()), 5000),
            value=int(df["Square_Feet"].median()),
            step=50,
        )
        beds = st.select_slider(
            "Bedrooms",
            options=sorted(df["Bedrooms"].unique().tolist()),
            value=int(df["Bedrooms"].median()),
        )
        age = st.slider(
            "Property age (years)",
            0,
            max(30, int(df["Age_Years"].max())),
            int(df["Age_Years"].median()),
        )
        location = st.selectbox(
            "Location grade",
            sorted(df["Location_Grade"].dropna().unique().tolist()),
        )

        run_prediction = st.button(
            "Generate valuation",
            use_container_width=True,
            type="primary",
        )

    predicted, engine = predict_value(sqft, beds, age, location, model)
    percentile = percentile_rank(df["Price_USD"], predicted)

    comparable = df[
        (df["Location_Grade"] == location)
        & (df["Bedrooms"] == beds)
    ].copy()
    if comparable.empty:
        comparable = df.copy()

    comparable["Area_Difference"] = (comparable["Square_Feet"] - sqft).abs()
    comparable = comparable.nsmallest(5, "Area_Difference")

    with output_col:
        section("Valuation", "Prediction result")
        st.markdown(
            f"""
            <div class="prediction-card">
                <div class="small">Estimated property value</div>
                <div class="value">{money(predicted)}</div>
                <div class="note">Engine: {engine} · Market percentile: {percentile:.0f}th</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        r1, r2, r3 = st.columns(3)
        r1.metric("Market percentile", f"{percentile:.0f}th")
        r2.metric("Comparable avg.", money(comparable["Price_USD"].mean()))
        risk = "Lower" if percentile < 75 else "Elevated"
        r3.metric("Price-position risk", risk)

        if run_prediction:
            st.session_state.prediction_history.insert(
                0,
                {
                    "Time": datetime.now().strftime("%H:%M:%S"),
                    "Square_Feet": sqft,
                    "Bedrooms": beds,
                    "Age_Years": age,
                    "Location_Grade": location,
                    "Predicted_Price": round(predicted, 2),
                    "Engine": engine,
                },
            )
            st.session_state.prediction_history = st.session_state.prediction_history[:20]
            st.toast("Valuation added to prediction history.")

    st.write("")
    tab1, tab2, tab3 = st.tabs(
        ["Comparable Properties", "What-if Scenarios", "Prediction History"]
    )

    with tab1:
        st.dataframe(
            comparable.drop(columns=["Area_Difference"]),
            use_container_width=True,
            hide_index=True,
        )

    with tab2:
        scenarios = []
        for delta in [-500, -250, 0, 250, 500]:
            scenario_area = max(100, sqft + delta)
            scenario_value, _ = predict_value(
                scenario_area, beds, age, location, model
            )
            scenarios.append({
                "Square_Feet": scenario_area,
                "Predicted_Price": scenario_value,
            })
        scenario_df = pd.DataFrame(scenarios)
        fig = px.line(
            scenario_df,
            x="Square_Feet",
            y="Predicted_Price",
            markers=True,
        )
        fig.update_traces(line_color="#315E4C", marker_color="#B6945D")
        st.plotly_chart(style_plot(fig, 380), use_container_width=True)

    with tab3:
        if st.session_state.prediction_history:
            history_df = pd.DataFrame(st.session_state.prediction_history)
            st.dataframe(history_df, use_container_width=True, hide_index=True)
            st.download_button(
                "Download prediction history",
                history_df.to_csv(index=False).encode("utf-8"),
                "prediction_history.csv",
                "text/csv",
            )
        else:
            st.info("Generate a valuation to start prediction history.")


# ============================================================
# 8. MODEL LAB PAGE
# ============================================================
elif page == "Model Lab":
    st.markdown(
        """
        <div class="hero">
            <h2>Understand what the predictive system is actually doing.</h2>
            <p>
                Inspect the model source, feature importance and training logic.
                No invented accuracy or confidence metrics are displayed.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section("Model status", "Runtime intelligence")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Primary model", "Random Forest")
    m2.metric("Task", "Regression")
    m3.metric("Split strategy", "80 / 20")
    m4.metric("Saved model", "Loaded" if model is not None else "Not found")

    if model is not None:
        st.success(f"Using trained model: {model_path}")
    else:
        st.warning(
            "Saved Random Forest model was not found or could not be loaded. "
            "The Predict page will clearly use the rule-based fallback."
        )

    section("Explainability", "Feature importance")
    importance = model_importance_df(model)

    if importance is not None:
        fig = px.bar(
            importance,
            x="Importance",
            y="Feature",
            orientation="h",
            text_auto=".3f",
        )
        fig.update_traces(marker_color="#315E4C")
        st.plotly_chart(style_plot(fig, 420), use_container_width=True)
    else:
        st.info(
            "Feature importance becomes available here after models/random_forest_model.pkl "
            "is generated by train_model.py."
        )

    with st.expander("Model logic and training pipeline", expanded=True):
        st.markdown(
            """
            **1. Preprocessing:** The cleaned property dataset is loaded and `Location_Grade`
            is one-hot encoded using `drop_first=True`.

            **2. Target:** `Price_USD` is the regression target.

            **3. Baseline:** Linear Regression is trained to provide a simple reference model.

            **4. Advanced model:** Random Forest Regressor combines multiple decision trees
            and averages their outputs.

            **5. Validation:** The training script uses an 80/20 train-test split and evaluates
            models using R² and Mean Absolute Error (MAE).

            **6. Explainability:** Random Forest exposes feature importance values, allowing
            the dashboard to show which encoded inputs contributed most to the fitted model.
            """
        )

    section("Data-model relationship", "Feature correlations")
    corr = df.select_dtypes(include="number").corr()
    fig = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale=[
            [0, "#E7DDD0"],
            [.5, "#F8F5ED"],
            [1, "#315E4C"],
        ],
    )
    st.plotly_chart(style_plot(fig, 420), use_container_width=True)


# ============================================================
# 9. INSIGHTS PAGE
# ============================================================
elif page == "Insights":
    st.markdown(
        """
        <div class="hero">
            <h2>Signals worth noticing.</h2>
            <p>
                A curated interpretation layer built from the live dataset — designed to read
                more like an executive intelligence brief than a conventional analytics page.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    loc_stats = (
        df.groupby("Location_Grade")["Price_USD"]
        .agg(["mean", "median", "count"])
        .sort_values("mean", ascending=False)
    )
    premium = loc_stats.index[0]
    budget = loc_stats.index[-1]
    area_corr = df["Square_Feet"].corr(df["Price_USD"])
    age_corr = df["Age_Years"].corr(df["Price_USD"])
    bedroom_stats = df.groupby("Bedrooms")["Price_USD"].mean().sort_values(ascending=False)
    best_bedroom = bedroom_stats.index[0]

    section("Executive intelligence", "The story inside the dataset")

    lead, side = st.columns([1.15, .85], gap="large")
    with lead:
        st.markdown(
            f"""
            <div class="insight-spotlight">
                <div class="number">Signal 01 · Location premium</div>
                <div class="title">Grade {premium} is setting the pricing ceiling.</div>
                <div class="copy">
                    Average property value in this segment is {money(loc_stats.loc[premium, 'mean'])},
                    while Grade {budget} sits at {money(loc_stats.loc[budget, 'mean'])}.
                    The gap makes location segmentation one of the clearest commercial lenses in this dataset.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with side:
        st.markdown(
            f"""<div class="kpi-editorial">
            <div class="k-label">Area ↔ price signal</div>
            <div class="k-value">{area_corr:+.2f}</div>
            <div class="k-note">Association only — not evidence of causation</div></div>""",
            unsafe_allow_html=True,
        )
        st.write("")
        st.markdown(
            f"""<div class="kpi-editorial">
            <div class="k-label">Age ↔ price signal</div>
            <div class="k-value">{age_corr:+.2f}</div>
            <div class="k-note">Best interpreted alongside area and location</div></div>""",
            unsafe_allow_html=True,
        )

    st.write("")
    section("Location intelligence", "A premium-to-value market ladder")

    # Replaces the old plain vertical bar chart with a ranked horizontal lollipop-style view.
    loc_display = loc_stats.reset_index().sort_values("mean", ascending=True)
    fig = go.Figure()
    for _, row in loc_display.iterrows():
        fig.add_trace(go.Scatter(
            x=[0, row["mean"]],
            y=[str(row["Location_Grade"]), str(row["Location_Grade"])],
            mode="lines",
            line=dict(color="#D8D2C6", width=4),
            hoverinfo="skip",
            showlegend=False,
        ))
    fig.add_trace(go.Scatter(
        x=loc_display["mean"],
        y=loc_display["Location_Grade"].astype(str),
        mode="markers+text",
        marker=dict(size=24, color="#315E4C", line=dict(width=3, color="#FFFEFA")),
        text=loc_display["mean"].map(lambda x: f"  ${x/1000:.0f}k"),
        textposition="middle right",
        hovertemplate="Grade %{y}<br>Average price: $%{x:,.0f}<extra></extra>",
        showlegend=False,
    ))
    fig.update_xaxes(showgrid=False, tickprefix="$", separatethousands=True)
    fig.update_yaxes(title=None)
    st.plotly_chart(style_plot(fig, 330), use_container_width=True)

    st.write("")
    section("Additional signals", "What else deserves attention")
    i1, i2, i3 = st.columns(3)
    with i1:
        st.markdown(
            f"""<div class="insight-card">
            <div class="label">Bedroom segment</div>
            <div class="big">{best_bedroom} bedroom(s)</div>
            <div class="copy">This bedroom group currently carries the highest average price among the observed bedroom segments.</div>
            </div>""", unsafe_allow_html=True)
    with i2:
        st.markdown(
            f"""<div class="insight-card">
            <div class="label">Observed floor</div>
            <div class="big">{money(df['Price_USD'].min())}</div>
            <div class="copy">The lowest property value represented in the current cleaned dataset.</div>
            </div>""", unsafe_allow_html=True)
    with i3:
        st.markdown(
            f"""<div class="insight-card">
            <div class="label">Observed ceiling</div>
            <div class="big">{money(df['Price_USD'].max())}</div>
            <div class="copy">The highest property value represented in the current cleaned dataset.</div>
            </div>""", unsafe_allow_html=True)


# ============================================================
# 10. REPORTS PAGE
# ============================================================
elif page == "Reports":
    st.markdown(
        """
        <div class="hero">
            <h2>Package the analysis for submission or presentation.</h2>
            <p>
                Export the cleaned dataset, prediction history and generated project report
                from one place.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section("Submission center", "Available exports")
    e1, e2, e3 = st.columns(3)

    with e1:
        st.markdown(
            """
            <div class="insight-card">
                <div class="label">Dataset</div>
                <div class="big">Cleaned CSV</div>
                <div class="copy">The processed dataset currently used by the dashboard.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.download_button(
            "Download cleaned dataset",
            df.to_csv(index=False).encode("utf-8"),
            "cleaned_properties.csv",
            "text/csv",
            use_container_width=True,
        )

    with e2:
        st.markdown(
            """
            <div class="insight-card">
                <div class="label">Predictions</div>
                <div class="big">Session history</div>
                <div class="copy">All valuations generated during the current Streamlit session.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.session_state.prediction_history:
            history_df = pd.DataFrame(st.session_state.prediction_history)
            st.download_button(
                "Download prediction history",
                history_df.to_csv(index=False).encode("utf-8"),
                "prediction_history.csv",
                "text/csv",
                use_container_width=True,
            )
        else:
            st.button(
                "No predictions yet",
                disabled=True,
                use_container_width=True,
            )

    with e3:
        st.markdown(
            """
            <div class="insight-card">
                <div class="label">Final report</div>
                <div class="big">Project PDF</div>
                <div class="copy">Generated by the existing document generation script.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        report_candidates = [
            "ReadyNest_System_Performance_Report.pdf",
            "System_Performance_Report.pdf",
        ]
        report_path = next(
            (p for p in report_candidates if os.path.exists(p)),
            None,
        )
        if report_path:
            with open(report_path, "rb") as report_file:
                st.download_button(
                    "Download project report",
                    report_file.read(),
                    "Predictive_Analytics_Report.pdf",
                    "application/pdf",
                    use_container_width=True,
                )
        else:
            st.button(
                "Generate report first",
                disabled=True,
                use_container_width=True,
            )

    st.write("")
    section("Submission checklist", "Task coverage")
    checklist = pd.DataFrame(
        {
            "Requirement": [
                "Dataset + code",
                "Data cleaning",
                "Visualizations",
                "Prediction model",
                "Model logic explanation",
                "Business insights",
                "Interactive dashboard",
                "Final report",
            ],
            "Status": [
                "Ready",
                "Ready",
                "Ready",
                "Ready / model file dependent",
                "Ready",
                "Ready",
                "Ready",
                "Available after report generation",
            ],
        }
    )
    st.dataframe(checklist, use_container_width=True, hide_index=True)


# ============================================================
# 11. FOOTER
# ============================================================
st.divider()
st.caption(
    "PropertyIQ Predictive Analytics Studio  ·  "
    f"Dataset: {dataset_path or 'not resolved'}  ·  "
    f"Model: {model_path or 'fallback mode'}  ·  "
    "Python · Streamlit · Pandas · Plotly · Scikit-learn"
)

# ============================================================
# FINAL TARGETED TAB VISIBILITY FIX
# Explore Data + Predict only in effect (all Streamlit tabs share this styling)
# ============================================================
st.markdown(
    """
    <style>
    /* Streamlit/BaseWeb tab text can inherit theme colors from nested <p>.
       Force every inactive tab label to a clearly visible dark tone. */
    div[data-baseweb="tab-list"] button[role="tab"],
    div[data-baseweb="tab-list"] button[role="tab"] p,
    div[data-baseweb="tab-list"] button[role="tab"] span,
    button[data-baseweb="tab"],
    button[data-baseweb="tab"] p,
    button[data-baseweb="tab"] span {
        color: #34473E !important;
        -webkit-text-fill-color: #34473E !important;
        opacity: 1 !important;
        visibility: visible !important;
        font-weight: 700 !important;
    }

    /* Active tab: deeper forest green, preserving the existing premium palette. */
    div[data-baseweb="tab-list"] button[role="tab"][aria-selected="true"],
    div[data-baseweb="tab-list"] button[role="tab"][aria-selected="true"] p,
    div[data-baseweb="tab-list"] button[role="tab"][aria-selected="true"] span,
    button[data-baseweb="tab"][aria-selected="true"],
    button[data-baseweb="tab"][aria-selected="true"] p,
    button[data-baseweb="tab"][aria-selected="true"] span {
        color: #17372D !important;
        -webkit-text-fill-color: #17372D !important;
        opacity: 1 !important;
        font-weight: 800 !important;
    }

    /* Hover remains readable instead of turning pale/white. */
    div[data-baseweb="tab-list"] button[role="tab"]:hover,
    div[data-baseweb="tab-list"] button[role="tab"]:hover *,
    button[data-baseweb="tab"]:hover,
    button[data-baseweb="tab"]:hover * {
        color: #21483A !important;
        -webkit-text-fill-color: #21483A !important;
        opacity: 1 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

