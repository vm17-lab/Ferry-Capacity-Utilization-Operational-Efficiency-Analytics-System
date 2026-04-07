import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# 1. PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Toronto Island Ferry · Intelligence",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# 2. GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Unbounded:wght@700;900&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap');

  :root {
    --bg:      #030c18;
    --surface: #071524;
    --card:    #0c1f35;
    --border:  #163352;
    --accent:  #00e5ff;
    --amber:   #ffb347;
    --rose:    #ff4d6d;
    --green:   #00ffa3;
    --text:    #dce9f5;
    --muted:   #5a7fa0;
  }

  html, body,
  [data-testid="stAppViewContainer"],
  [data-testid="stMain"] {
    background: var(--bg) !important;
    color: var(--text);
    font-family: 'Plus Jakarta Sans', sans-serif;
  }

  [data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed; inset: 0; pointer-events: none;
    background:
      radial-gradient(ellipse 900px 600px at 15% 0%,  rgba(0,229,255,.06) 0%, transparent 70%),
      radial-gradient(ellipse 700px 500px at 85% 100%, rgba(255,179,71,.05) 0%, transparent 70%);
  }

  /* ── Sidebar base ── */
  [data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
  }

  /* Sidebar labels, headings, nav-labels, slider text */
  [data-testid="stSidebar"] label,
  [data-testid="stSidebar"] .nav-label,
  [data-testid="stSidebar"] h2,
  [data-testid="stSidebar"] p,
  [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
  [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
  [data-testid="stSidebar"] [data-testid="stSlider"] p,
  [data-testid="stSidebar"] [data-testid="stSlider"] span,
  [data-testid="stSidebar"] [data-testid="stSlider"] div[data-testid="stThumbValue"],
  [data-testid="stSidebar"] [data-testid="stSlider"] div[data-testid="stTickBarMin"],
  [data-testid="stSidebar"] [data-testid="stSlider"] div[data-testid="stTickBarMax"] {
    color: #13EAC9 !important;
  }

  /* ── Selectbox (Frequency) — selected value BLACK ── */
  [data-testid="stSidebar"] [data-baseweb="select"] {
    background: var(--card) !important;
    border-color: var(--border) !important;
  }
  [data-testid="stSidebar"] [data-baseweb="select"] [data-baseweb="single-select"] span,
  [data-testid="stSidebar"] [data-baseweb="select"] [data-baseweb="single-select"],
  [data-testid="stSidebar"] [data-baseweb="select"] div[class*="placeholder"],
  [data-baseweb="select"] [data-baseweb="single-select"] span,
  [data-baseweb="select"] [data-baseweb="single-select"] {
    color: #000 !important;
  }

  /* ── Date range inputs — BLACK text ── */
  [data-testid="stSidebar"] input[type="text"],
  [data-testid="stSidebar"] input[type="date"],
  [data-testid="stSidebar"] [data-testid="stDateInput"] input {
    color: #000 !important;
    background: #fff !important;
  }

  /* ── Multiselect selected tags — BLACK text ── */
  [data-testid="stSidebar"] [data-baseweb="tag"] span,
  [data-testid="stSidebar"] [data-baseweb="tag"] [data-testid="stMarkdownContainer"] p,
  [data-testid="stSidebar"] span[data-baseweb="tag"] {
    color: #000 !important;
  }

  /* ── Dropdown portal (selectbox + multiselect) — light bg, BLACK text ── */
  [data-baseweb="menu"],
  [data-baseweb="popover"] ul,
  [role="listbox"],
  ul[data-baseweb="menu"],
  [data-baseweb="popover"] [role="listbox"] {
    background: #f0f4f8 !important;
    border: 1px solid #cdd8e3 !important;
  }
  [role="option"],
  [role="option"] *,
  [data-baseweb="menu"] li,
  [data-baseweb="menu"] li * {
    background: #f0f4f8 !important;
    color: #000 !important;
  }
  [role="option"]:hover,
  [data-baseweb="menu"] li:hover {
    background: #d6eaff !important;
    color: #000 !important;
  }

  /* ── KPI grid ── */
  .kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 14px;
    margin-bottom: 26px;
  }
  .kpi-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px 16px;
    position: relative;
    overflow: hidden;
    transition: transform .2s;
  }
  .kpi-card:hover { transform: translateY(-3px); }
  .kpi-card::before {
    content: "";
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: var(--top-color, var(--accent));
  }
  .kpi-icon  { font-size: 1.3rem; margin-bottom: 8px; opacity: .85; }
  .kpi-label { font-family:'DM Mono',monospace; font-size:.62rem; letter-spacing:.12em;
               text-transform:uppercase; color:var(--muted); margin-bottom:6px; }
  .kpi-value { font-family:'Unbounded',sans-serif; font-size:1.7rem; font-weight:900;
               color:#fff; line-height:1; }
  .kpi-sub   { font-size:.7rem; color:var(--muted); margin-top:5px; font-family:'DM Mono',monospace; }

  /* ── Section titles ── */
  .sec-title {
    font-family: 'Unbounded', sans-serif;
    font-size: .82rem;
    color: var(--accent);
    letter-spacing: .06em;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 14px;
  }

  /* ── Alerts ── */
  .alert-critical { background: rgba(255,77,109,.08); border: 1px solid var(--rose); border-left: 4px solid var(--rose); border-radius: 10px; padding: 14px 18px; color: #ffb3c0; font-size: .88rem; margin-top: 14px; }
  .alert-warn     { background: rgba(255,179,71,.08); border: 1px solid var(--amber); border-left: 4px solid var(--amber); border-radius: 10px; padding: 14px 18px; color: #ffd899; font-size: .88rem; margin-top: 14px; }
  .alert-ok       { background: rgba(0,255,163,.07); border: 1px solid var(--green); border-left: 4px solid var(--green); border-radius: 10px; padding: 14px 18px; color: #99ffe0; font-size: .88rem; margin-top: 14px; }

  /* ── Nav labels ── */
  .nav-label { font-family: 'DM Mono', monospace; font-size: .65rem; letter-spacing: .15em; text-transform: uppercase; color: #13EAC9; margin: 18px 0 6px; font-weight: 700; }

  /* ── Hero ── */
  .hero-wrap {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 28px;
  }
  .hero-logo {
    flex-shrink: 0;
    background: rgba(0,229,255,0.07);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 20px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .hero-logo svg { width: 120px; height: auto; }
  .hero-title { font-family: 'Unbounded', sans-serif; font-size: 2.1rem; font-weight: 900; color: #fff; line-height: 1; }
  .hero-sub   { font-family: 'DM Mono', monospace; font-size: .7rem; letter-spacing: .2em; color: var(--muted); margin-top: 6px; }
  .live-dot   { display: inline-block; width: 8px; height: 8px; background: var(--green); border-radius: 50%; margin-right: 6px; animation: pulse 1.6s ease-in-out infinite; }
  @keyframes pulse { 0%,100% { opacity:1; transform:scale(1); } 50% { opacity:.5; transform:scale(1.5); } }

  /* ── Sidebar logo ── */
  .sidebar-logo {
    background: rgba(0,229,255,0.06);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .sidebar-logo svg { width: 100%; max-width: 140px; height: auto; }

  #MainMenu, [data-testid="stHeader"], footer { display:none; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOGO SVG (inline)
# ─────────────────────────────────────────────
LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="48.66" height="14.83" viewBox="0 0 48.66 14.83">
  <defs><style>.a{fill:#fff;}</style></defs>
  <path class="a" d="M16.76 6.42c0-1.29 1.17-1.77 2.47-1.77s2.46.48 2.46 1.77v6.48c0 1.3-1.17 1.77-2.46 1.77s-2.47-.48-2.47-1.77zm2.84.25c0-.27 0-.64-.37-.64s-.37.37-.37.64v5.92c0 .27 0 .64.37.64s.37-.37.37-.64zM22.48 14.48v-9.64h2.47c1.29 0 2.47.48 2.47 2v.76a1.5 1.5 0 0 1-1.62 1.58c1.32.07 1.62.53 1.62 1.64v1.92a4.48 4.48 0 0 0 .31 1.72h-2.13a2.32 2.32 0 0 1-.28-1.25v-2.21c0-.6 0-1.08-.74-1.08v4.54zm2.06-5.66h.25c.34 0 .49-.15.49-.61v-1.43c0-.46-.15-.61-.49-.61h-.25zM28.13 6.42c0-1.29 1.17-1.77 2.47-1.77s2.46.48 2.46 1.77v6.48c0 1.3-1.17 1.77-2.46 1.77s-2.47-.48-2.47-1.77zm2.87.25c0-.27 0-.64-.37-.64s-.37.37-.37.64v5.92c0 .27 0 .64.37.64s.37-.37.37-.64zM33.83 14.48v-9.64h2.77l.95 6.14.01.23h.03v-6.37h1.67v9.64h-2.59l-1.14-7.36-.01-.27h-.02v7.63h-1.67zM43.72 6.42c0-1.29 1.17-1.77 2.47-1.77s2.46.48 2.46 1.77v6.48c0 1.3-1.17 1.77-2.46 1.77s-2.47-.48-2.47-1.77zm2.84.25c0-.27 0-.64-.37-.64s-.37.37-.37.64v5.92c0 .27 0 .64.37.64s.37-.37.37-.64zM43.37 4.84h-3.7v1.45h.8v8.19h2.1v-8.19h.8v-1.45zM17.58 2.48h-5.25v1.55h1.55v10.45h2.14v-10.45h1.56v-1.55zM12.17 14.83v-.06a9.59 9.59 0 0 0-4.39-.77h-7.78v.53h10.5a6.47 6.47 0 0 1 1.67.34M9.07.29l-.31-.29a.37.37 0 0 0-.29 0l-.47.26v2.29a3.72 3.72 0 0 1-1.49 1.37.35.35 0 0 0-.21.36v8.53c-.31 0-.81.07-.81.07v-7.22c0-.27-.12-.35-.37-.41a14.42 14.42 0 0 1-2.72-.92v-1.48l-.4-.2a.52.52 0 0 0-.34 0 3.8 3.8 0 0 0-.49.28 2.32 2.32 0 0 0-1.17 1.92v8.82h.79v-8.82a1.48 1.48 0 0 1 .75-1.32h.06v10.14h.78v-8.5c.62.23 1 .39 1.67.6l.64.17v7.06a9.5 9.5 0 0 0-2.19.68h1.5a9.23 9.23 0 0 1 3.77-.8l-.72-.06v-8.32h.08a4.11 4.11 0 0 0 .87-.71v9.88h.81v-12.47a3.8 3.8 0 0 1 .77 2.23v10.32c.24 0 .54.06.79.13v-10.47a4.71 4.71 0 0 0-1.3-3.12"/>
</svg>"""

# ─────────────────────────────────────────────
# 3. CHART HELPER
# ─────────────────────────────────────────────
GRID = "#163352"
SEASON_COLORS = {"Summer": "#ffb347", "Spring": "#00ffa3", "Fall": "#ff4d6d", "Winter": "#00e5ff"}


def apply_base(fig, height=360):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(12,31,53,0.45)",
        font=dict(family="DM Mono, monospace", color="#dce9f5", size=11),
        height=height,
        margin=dict(t=28, b=20, l=14, r=14),
        colorway=["#00e5ff", "#ffb347", "#ff4d6d", "#00ffa3"],
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#dce9f5")),
    )
    return fig


# ─────────────────────────────────────────────
# 4. SYNTHETIC DATA GENERATOR (2015 - 2025)
# ─────────────────────────────────────────────
@st.cache_data
def generate_long_term_data() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    start_date = datetime(2015, 1, 1)
    end_date = datetime(2025, 12, 31)

    delta = end_date - start_date
    total_intervals = int(delta.total_seconds() / 900)

    ts = [start_date + timedelta(minutes=15 * i) for i in range(total_intervals)]
    df = pd.DataFrame({"Timestamp": ts})

    df["Hour"] = df["Timestamp"].dt.hour
    df["Month"] = df["Timestamp"].dt.month
    df["Year"] = df["Timestamp"].dt.year
    df["Day"] = df["Timestamp"].dt.day_name()
    df["DayOfWeek"] = df["Timestamp"].dt.dayofweek

    month_factor = {1: .40, 2: .42, 3: .52, 4: .62, 5: .74, 6: .88, 7: .97, 8: .94, 9: .75, 10: .60, 11: .45, 12: .38}
    hour_curve = np.array(
        [.10, .08, .07, .07, .09, .14, .25, .45, .65, .75, .78, .80, .82, .84, .82, .80, .78, .76, .72, .65, .55, .40,
         .28, .15])

    df["SeasonFactor"] = df["Month"].map(month_factor)
    df["HourFactor"] = df["Hour"].map(lambda h: hour_curve[h])
    df["WeekendBoost"] = df["DayOfWeek"].apply(lambda d: 1.25 if d >= 5 else 1.0)
    df["GrowthTrend"] = 1 + (df["Year"] - 2015) * 0.012

    base_u = df["SeasonFactor"] * df["HourFactor"] * df["WeekendBoost"] * df["GrowthTrend"] * 100
    df["Utilization"] = (base_u + rng.normal(0, 5, len(df))).clip(5, 99)
    df["OLI"] = df["Utilization"] / 100

    df["Season"] = df["Month"].map(lambda m:
                                   "Summer" if m in (6, 7, 8) else (
                                       "Spring" if m in (3, 4, 5) else ("Fall" if m in (9, 10, 11) else "Winter")))

    df["Tickets"] = (df["Utilization"] * 4.2 + rng.normal(0, 10, len(df))).clip(0).astype(int)
    return df


# ─────────────────────────────────────────────
# 5. DATA LOADING & SIDEBAR
# ─────────────────────────────────────────────
df = generate_long_term_data()
FREQ_MAP = {"15-min": "15min", "Hourly": "h", "Daily": "D", "Monthly": "ME", "Yearly": "YE"}

with st.sidebar:
    # ── Sidebar Logo ──
    st.markdown(
        f'<div class="sidebar-logo">{LOGO_SVG}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<h2 style="font-family:Unbounded;font-size:1.1rem;color:#fff;">⚓ Navigation</h2>',
                unsafe_allow_html=True)

    st.markdown('<div class="nav-label">① Date Range (2015-2025)</div>', unsafe_allow_html=True)
    min_d, max_d = df["Timestamp"].min().date(), df["Timestamp"].max().date()
    date_range = st.date_input("Range Selection", value=(datetime(2024, 1, 1).date(), max_d), min_value=min_d,
                               max_value=max_d)

    st.markdown('<div class="nav-label">② Seasonality</div>', unsafe_allow_html=True)
    sel_seasons = st.multiselect("Filter Seasons", ["Spring", "Summer", "Fall", "Winter"],
                                 default=["Spring", "Summer", "Fall", "Winter"])

    st.markdown('<div class="nav-label">③ Aggregation</div>', unsafe_allow_html=True)
    freq_label = st.selectbox("Frequency", list(FREQ_MAP.keys()), index=3)

    st.markdown('<div class="nav-label">④ Threshold</div>', unsafe_allow_html=True)
    threshold = st.slider("Congestion Limit %", 10, 100, 75)

# ─────────────────────────────────────────────
# 6. FILTERING
# ─────────────────────────────────────────────
start_d = date_range[0] if len(date_range) >= 1 else min_d
end_d = date_range[1] if len(date_range) == 2 else max_d

fdf = df.loc[
    (df["Timestamp"].dt.date >= start_d) &
    (df["Timestamp"].dt.date <= end_d) &
    (df["Season"].isin(sel_seasons))
    ].copy()

# ─────────────────────────────────────────────
# 7. HEADER WITH LOGO & KPIs
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero-wrap">
  <div class="hero-logo">{LOGO_SVG}</div>
  <div>
    <div class="hero-title">Ferry Capacity Utilization &amp; Operational Efficiency Analytics System</div>
    <div class="hero-sub"><span class="live-dot"></span>LIVE · TORONTO ISLAND FERRY INTELLIGENCE PLATFORM</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI CALCULATIONS
# ─────────────────────────────────────────────

# 1. Capacity Utilization Ratio — measure of ferry load efficiency
# Ratio of average utilization to max possible (99%), expressed as a ratio
avg_util = fdf["Utilization"].mean()
capacity_utilization_ratio = avg_util / 99.0  # normalized 0–1 ratio

# 2. Congestion Pressure Index — identifies over-utilized intervals
# Mean utilization of intervals exceeding the threshold, normalized to 0–100
over_threshold = fdf.loc[fdf["Utilization"] > threshold, "Utilization"]
if len(over_threshold) > 0:
    congestion_pressure_index = (over_threshold.mean() - threshold) / (99 - threshold) * 100
else:
    congestion_pressure_index = 0.0

# 3. Idle Capacity Percentage — measures under-utilization
# % of intervals where utilization is below 30% (low-demand threshold)
idle_threshold = 30
idle_pct = (fdf["Utilization"] < idle_threshold).mean() * 100

# 4. Peak Strain Duration — length of sustained high-pressure periods
# Count of consecutive 15-min intervals where utilization > threshold,
# expressed as average streak length in hours
util_series = (fdf["Utilization"] > threshold).astype(int).values
streak_lengths = []
current_streak = 0
for val in util_series:
    if val == 1:
        current_streak += 1
    else:
        if current_streak > 0:
            streak_lengths.append(current_streak)
        current_streak = 0
if current_streak > 0:
    streak_lengths.append(current_streak)
avg_peak_strain_hours = (np.mean(streak_lengths) * 15 / 60) if streak_lengths else 0.0

# 5. Operational Variability Score — stability of utilization patterns
# Coefficient of variation (std/mean), lower = more stable; invert for a "score"
cv = fdf["Utilization"].std() / fdf["Utilization"].mean() if fdf["Utilization"].mean() > 0 else 0
# Score: 100 = perfectly stable, 0 = highly variable
operational_variability_score = max(0, 100 - cv * 100)


def kpi_card(icon, label, value, sub, color):
    return f'<div class="kpi-card" style="--top-color:{color}"><div class="kpi-icon">{icon}</div><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-sub">{sub}</div></div>'


st.markdown(
    '<div class="kpi-grid">' +
    kpi_card(
        "⚖️",
        "Capacity Utilization Ratio",
        f"{capacity_utilization_ratio:.2f}",
        "ferry load efficiency",
        "#00e5ff"
    ) +
    kpi_card(
        "🔺",
        "Congestion Pressure Index",
        f"{congestion_pressure_index:.1f}",
        "over-utilized intervals",
        "#ff4d6d"
    ) +
    kpi_card(
        "💤",
        "Idle Capacity %",
        f"{idle_pct:.1f}%",
        "under-utilization rate",
        "#ffb347"
    ) +
    kpi_card(
        "⏱️",
        "Peak Strain Duration",
        f"{avg_peak_strain_hours:.1f}h",
        "avg sustained high-load",
        "#c084fc"
    ) +
    kpi_card(
        "📐",
        "Operational Variability",
        f"{operational_variability_score:.1f}",
        "stability score (100=stable)",
        "#00ffa3"
    ) +
    '</div>',
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────
# 8. VISUALIZATIONS
# ─────────────────────────────────────────────
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown('<div class="sec-title">📈 HISTORICAL UTILIZATION TREND</div>', unsafe_allow_html=True)
    ts_data = fdf.set_index("Timestamp").resample(FREQ_MAP[freq_label]).agg({"Utilization": "mean"}).reset_index()
    fig_line = px.line(ts_data, x="Timestamp", y="Utilization", color_discrete_sequence=["#00e5ff"])
    fig_line.add_hline(y=threshold, line_dash="dot", line_color="#ff4d6d", annotation_text="Limit")
    apply_base(fig_line)
    st.plotly_chart(fig_line, use_container_width=True)

with c2:
    st.markdown('<div class="sec-title">🎻 DENSITY BY SEASON</div>', unsafe_allow_html=True)
    fig_vio = px.violin(fdf, y="Utilization", x="Season", color="Season", color_discrete_map=SEASON_COLORS, box=True)
    apply_base(fig_vio)
    st.plotly_chart(fig_vio, use_container_width=True)

# ─────────────────────────────────────────────
# 9. HEATMAP
# ─────────────────────────────────────────────
st.markdown('<div class="sec-title">🗺️ WEEKLY CONGESTION HEATMAP</div>', unsafe_allow_html=True)
hm_data = fdf.groupby(["Day", "Hour"])["Utilization"].mean().unstack().reindex(
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
fig_hm = px.imshow(hm_data, color_continuous_scale="Viridis", aspect="auto")
apply_base(fig_hm, height=300)
st.plotly_chart(fig_hm, use_container_width=True)

# ─────────────────────────────────────────────
# 10. ALERTS
# ─────────────────────────────────────────────
st.markdown('<div class="sec-title">🔔 SYSTEM ALERTS</div>', unsafe_allow_html=True)
cong_pct = (fdf["Utilization"] > threshold).mean() * 100
if cong_pct > 20:
    st.markdown(
        f'<div class="alert-critical"><b>CRITICAL:</b> High congestion ({cong_pct:.1f}%) detected in the selected period. Review fleet deployment for summer peaks.</div>',
        unsafe_allow_html=True)
else:
    st.markdown(
        '<div class="alert-ok"><b>NOMINAL:</b> Ferry utilization is within acceptable bounds for the selected dates.</div>',
        unsafe_allow_html=True)