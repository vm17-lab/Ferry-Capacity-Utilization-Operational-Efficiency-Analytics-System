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

  [data-testid="stSidebar"] label,
  [data-testid="stSidebar"] .nav-label,
  [data-testid="stSidebar"] h2,
  [data-testid="stSidebar"] p {
    color: #13EAC9 !important;
  }

  /* ── Input Styling (Selectbox & Date) ── */
  /* Force Date Input and Selectbox to have black text for readability */
  [data-testid="stSidebar"] input, 
  [data-testid="stSidebar"] [data-baseweb="select"] div {
    color: #000 !important;
  }

  /* ── CALENDAR POPUP STYLING ── */
  /* This ensures the calendar floating menu is legible */
  div[data-baseweb="datepicker"], div[role="listbox"] {
    background-color: #ffffff !important;
  }
  div[data-baseweb="calendar"] button {
    color: #000 !important;
  }
  div[data-baseweb="calendar"] [aria-selected="true"] {
    background-color: var(--accent) !important;
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
  .kpi-value { font-family:'Unbounded',sans-serif; font-size: 1.5rem; font-weight:900;
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
  .hero-title { font-family: 'Unbounded', sans-serif; font-size: 1.8rem; font-weight: 900; color: #fff; line-height: 1.1; }
  .hero-sub   { font-family: 'DM Mono', monospace; font-size: .7rem; letter-spacing: .2em; color: var(--muted); margin-top: 6px; }
  .live-dot   { display: inline-block; width: 8px; height: 8px; background: var(--green); border-radius: 50%; margin-right: 6px; animation: pulse 1.6s ease-in-out infinite; }
  @keyframes pulse { 0%,100% { opacity:1; transform:scale(1); } 50% { opacity:.5; transform:scale(1.5); } }

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
  
  /* Hide standard Streamlit elements */
  #MainMenu, [data-testid="stHeader"], footer { display:none; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 3. LOGO & UTILS
# ─────────────────────────────────────────────
LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="48.66" height="14.83" viewBox="0 0 48.66 14.83">
<path fill="#fff" d="M16.76 6.42c0-1.29 1.17-1.77 2.47-1.77s2.46.48 2.46 1.77v6.48c0 1.3-1.17 1.77-2.46 1.77s-2.47-.48-2.47-1.77zm2.84.25c0-.27 0-.64-.37-.64s-.37.37-.37.64v5.92c0 .27 0 .64.37.64s.37-.37.37-.64zM22.48 14.48v-9.64h2.47c1.29 0 2.47.48 2.47 2v.76a1.5 1.5 0 0 1-1.62 1.58c1.32.07 1.62.53 1.62 1.64v1.92a4.48 4.48 0 0 0 .31 1.72h-2.13a2.32 2.32 0 0 1-.28-1.25v-2.21c0-.6 0-1.08-.74-1.08v4.54zm2.06-5.66h.25c.34 0 .49-.15.49-.61v-1.43c0-.46-.15-.61-.49-.61h-.25zM28.13 6.42c0-1.29 1.17-1.77 2.47-1.77s2.46.48 2.46 1.77v6.48c0 1.3-1.17 1.77-2.46 1.77s-2.47-.48-2.47-1.77zm2.87.25c0-.27 0-.64-.37-.64s-.37.37-.37.64v5.92c0 .27 0 .64.37.64s.37-.37.37-.64zM33.83 14.48v-9.64h2.77l.95 6.14.01.23h.03v-6.37h1.67v9.64h-2.59l-1.14-7.36-.01-.27h-.02v7.63h-1.67zM43.72 6.42c0-1.29 1.17-1.77 2.47-1.77s2.46.48 2.46 1.77v6.48c0 1.3-1.17 1.77-2.46 1.77s-2.47-.48-2.47-1.77zm2.84.25c0-.27 0-.64-.37-.64s-.37.37-.37.64v5.92c0 .27 0 .64.37.64s.37-.37.37-.64zM43.37 4.84h-3.7v1.45h.8v8.19h2.1v-8.19h.8v-1.45zM17.58 2.48h-5.25v1.55h1.55v10.45h2.14v-10.45h1.56v-1.55zM12.17 14.83v-.06a9.59 9.59 0 0 0-4.39-.77h-7.78v.53h10.5a6.47 6.47 0 0 1 1.67.34M9.07.29l-.31-.29a.37.37 0 0 0-.29 0l-.47.26v2.29a3.72 3.72 0 0 1-1.49 1.37.35.35 0 0 0-.21.36v8.53c-.31 0-.81.07-.81.07v-7.22c0-.27-.12-.35-.37-.41a14.42 14.42 0 0 1-2.72-.92v-1.48l-.4-.2a.52.52 0 0 0-.34 0 3.8 3.8 0 0 0-.49.28 2.32 2.32 0 0 0-1.17 1.92v8.82h.79v-8.82a1.48 1.48 0 0 1 .75-1.32h.06v10.14h.78v-8.5c.62.23 1 .39 1.67.6l.64.17v7.06a9.5 9.5 0 0 0-2.19.68h1.5a9.23 9.23 0 0 1 3.77-.8l-.72-.06v-8.32h.08a4.11 4.11 0 0 0 .87-.71v9.88h.81v-12.47a3.8 3.8 0 0 1 .77 2.23v10.32c.24 0 .54.06.79.13v-10.47a4.71 4.71 0 0 0-1.3-3.12"/></svg>"""

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
# 4. DATA GENERATOR
# ─────────────────────────────────────────────
@st.cache_data
def generate_long_term_data() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    start_date = datetime(2015, 1, 1)
    end_date = datetime(2025, 12, 31)
    total_intervals = int((end_date - start_date).total_seconds() / 900)
    ts = [start_date + timedelta(minutes=15 * i) for i in range(total_intervals)]
    df = pd.DataFrame({"Timestamp": ts})
    df["Hour"] = df["Timestamp"].dt.hour
    df["Month"] = df["Timestamp"].dt.month
    df["Year"] = df["Timestamp"].dt.year
    df["Day"] = df["Timestamp"].dt.day_name()
    df["DayOfWeek"] = df["Timestamp"].dt.dayofweek
    month_factor = {1:.4, 2:.42, 3:.52, 4:.62, 5:.74, 6:.88, 7:.97, 8:.94, 9:.75, 10:.6, 11:.45, 12:.38}
    hour_curve = np.array([.1, .08, .07, .07, .09, .14, .25, .45, .65, .75, .78, .8, .82, .84, .82, .8, .78, .76, .72, .65, .55, .4, .28, .15])
    df["Utilization"] = (df["Month"].map(month_factor) * df["Hour"].map(lambda h: hour_curve[h]) * df["DayOfWeek"].apply(lambda d: 1.25 if d >= 5 else 1.0) * 100 + rng.normal(0, 5, len(df))).clip(5, 99)
    df["Season"] = df["Month"].map(lambda m: "Summer" if m in (6,7,8) else ("Spring" if m in (3,4,5) else ("Fall" if m in (9,10,11) else "Winter")))
    return df

# ─────────────────────────────────────────────
# 5. DATA LOADING & SIDEBAR
# ─────────────────────────────────────────────
df = generate_long_term_data()
FREQ_MAP = {"15-min": "15min", "Hourly": "h", "Daily": "D", "Monthly": "ME", "Yearly": "YE"}

with st.sidebar:
    st.markdown(f'<div class="sidebar-logo">{LOGO_SVG}</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="font-family:Unbounded;font-size:1.1rem;color:#fff;">⚓ Navigation</h2>', unsafe_allow_html=True)

    st.markdown('<div class="nav-label">① Date Range (2015-2025)</div>', unsafe_allow_html=True)
    min_d, max_d = df["Timestamp"].min().date(), df["Timestamp"].max().date()
    # Updated st.date_input with label_visibility="collapsed"
    date_range = st.date_input(
        "Range Selector", 
        value=(datetime(2024, 1, 1).date(), max_d), 
        min_value=min_d, 
        max_value=max_d,
        label_visibility="collapsed"
    )

    st.markdown('<div class="nav-label">② Seasonality</div>', unsafe_allow_html=True)
    sel_seasons = st.multiselect("Filter Seasons", ["Spring", "Summer", "Fall", "Winter"], default=["Spring", "Summer", "Fall", "Winter"])

    st.markdown('<div class="nav-label">③ Aggregation</div>', unsafe_allow_html=True)
    freq_label = st.selectbox("Frequency", list(FREQ_MAP.keys()), index=3)

    st.markdown('<div class="nav-label">④ Threshold</div>', unsafe_allow_html=True)
    threshold = st.slider("Congestion Limit %", 10, 100, 75)

# ─────────────────────────────────────────────
# 6. FILTERING & HEADER
# ─────────────────────────────────────────────
start_d = date_range[0] if len(date_range) >= 1 else min_d
end_d = date_range[1] if len(date_range) == 2 else max_d
fdf = df.loc[(df["Timestamp"].dt.date >= start_d) & (df["Timestamp"].dt.date <= end_d) & (df["Season"].isin(sel_seasons))].copy()

st.markdown(f"""
<div class="hero-wrap">
  <div class="hero-logo">{LOGO_SVG}</div>
  <div>
    <div class="hero-title">Ferry Capacity Utilization Analytics</div>
    <div class="hero-sub"><span class="live-dot"></span>LIVE · TORONTO ISLAND FERRY INTELLIGENCE PLATFORM</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 7. KPIs & CHARTS
# ─────────────────────────────────────────────
avg_util = fdf["Utilization"].mean()
idle_pct = (fdf["Utilization"] < 30).mean() * 100
congest_pct = (fdf["Utilization"] > threshold).mean() * 100

def kpi_card(icon, label, value, sub, color):
    return f'<div class="kpi-card" style="--top-color:{color}"><div class="kpi-icon">{icon}</div><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-sub">{sub}</div></div>'

st.markdown('<div class="kpi-grid">' + 
    kpi_card("⚖️", "Utilization Ratio", f"{(avg_util/100):.2f}", "ferry efficiency", "#00e5ff") +
    kpi_card("🔺", "Pressure Index", f"{congest_pct:.1f}", "congestion factor", "#ff4d6d") +
    kpi_card("💤", "Idle Rate", f"{idle_pct:.1f}%", "under-utilization", "#ffb347") +
    kpi_card("⏱️", "Peak Strain", f"{((congest_pct*24)/100):.1f}h", "est. daily peak", "#c084fc") +
    kpi_card("📐", "Stability", f"{max(0, 100-(fdf['Utilization'].std()*2)):.1f}", "ops score", "#00ffa3") +
    '</div>', unsafe_allow_html=True)

c1, c2 = st.columns([2, 1])
with c1:
    st.markdown('<div class="sec-title">📈 HISTORICAL UTILIZATION TREND</div>', unsafe_allow_html=True)
    ts_data = fdf.set_index("Timestamp").resample(FREQ_MAP[freq_label]).agg({"Utilization": "mean"}).reset_index()
    fig_line = px.line(ts_data, x="Timestamp", y="Utilization", color_discrete_sequence=["#00e5ff"])
    fig_line.add_hline(y=threshold, line_dash="dot", line_color="#ff4d6d")
    st.plotly_chart(apply_base(fig_line), use_container_width=True)

with c2:
    st.markdown('<div class="sec-title">🎻 DENSITY BY SEASON</div>', unsafe_allow_html=True)
    fig_vio = px.violin(fdf, y="Utilization", x="Season", color="Season", color_discrete_map=SEASON_COLORS, box=True)
    st.plotly_chart(apply_base(fig_vio), use_container_width=True)

st.markdown('<div class="sec-title">🗺️ WEEKLY CONGESTION HEATMAP</div>', unsafe_allow_html=True)
hm_data = fdf.groupby(["Day", "Hour"])["Utilization"].mean().unstack().reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
fig_hm = px.imshow(hm_data, color_continuous_scale="Viridis", aspect="auto")
st.plotly_chart(apply_base(fig_hm, height=300), use_container_width=True)
