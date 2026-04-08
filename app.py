import streamlit as st
import pandas as pd
import plotly.express as px
import warnings
import os
import numpy as np

# Suppress warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# 1. PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Toronto Island Ferry",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# 2. GLOBAL CSS (Dark Mode Tech Theme)
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

  html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: var(--bg) !important;
    color: var(--text);
    font-family: 'Plus Jakarta Sans', sans-serif;
  }

  [data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
  }

  /* KPI Card Styling */
  .kpi-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px 16px;
    position: relative;
    transition: transform .2s;
  }
  .kpi-card::before {
    content: "";
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: var(--top-color, var(--accent));
    border-radius: 14px 14px 0 0;
  }
  .kpi-label { font-family:'DM Mono',monospace; font-size:.62rem; text-transform:uppercase; color:var(--muted); }
  .kpi-value { font-family:'Unbounded',sans-serif; font-size:1.3rem; font-weight:900; color:#fff; }

  .sec-title {
    font-family: 'Unbounded', sans-serif;
    font-size: .82rem;
    color: var(--accent);
    border-bottom: 1px solid var(--border);
    margin: 25px 0 15px 0;
    padding-bottom: 5px;
  }

  .hero-title { font-family: 'Unbounded', sans-serif; font-size: 1.8rem; font-weight: 900; color: #fff; line-height: 1.2; }
  .hero-sub { font-family: 'DM Mono', monospace; font-size: 0.75rem; color: var(--muted); margin-top: 5px; letter-spacing: 1px; }
  .live-dot { display: inline-block; width: 8px; height: 8px; background: var(--green); border-radius: 50%; margin-right: 8px; animation: pulse 1.6s infinite; }

  @keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:.3; } }

  .alert-box {
      padding: 15px;
      border-radius: 10px;
      margin: 10px 0;
      border: 1px solid transparent;
  }
  .alert-critical { background: rgba(255, 77, 109, 0.1); border-color: var(--rose); color: #ff8fa3; }
  .alert-nominal  { background: rgba(0, 255, 163, 0.1); border-color: var(--green); color: #8affd3; }
</style>
""", unsafe_allow_html=True)

LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="100" viewBox="0 0 48.66 14.83"><path fill="#00e5ff" d="M16.76 6.42c0-1.29 1.17-1.77 2.47-1.77s2.46.48 2.46 1.77v6.48c0 1.3-1.17 1.77-2.46 1.77s-2.47-.48-2.47-1.77zm2.84.25c0-.27 0-.64-.37-.64s-.37.37-.37.64v5.92c0 .27 0 .64.37.64s.37-.37.37-.64zM22.48 14.48v-9.64h2.47c1.29 0 2.47.48 2.47 2v.76a1.5 1.5 0 0 1-1.62 1.58c1.32.07 1.62.53 1.62 1.64v1.92a4.48 4.48 0 0 0 .31 1.72h-2.13a2.32 2.32 0 0 1-.28-1.25v-2.21c0-.6 0-1.08-.74-1.08v4.54zm2.06-5.66h.25c.34 0 .49-.15.49-.61v-1.43c0-.46-.15-.61-.49-.61h-.25zM28.13 6.42c0-1.29 1.17-1.77 2.47-1.77s2.46.48 2.46 1.77v6.48c0 1.3-1.17 1.77-2.46 1.77s-2.47-.48-2.47-1.77zm2.87.25c0-.27 0-.64-.37-.64s-.37.37-.37.64v5.92c0 .27 0 .64.37.64s.37-.37.37-.64zM33.83 14.48v-9.64h2.77l.95 6.14.01.23h.03v-6.37h1.67v9.64h-2.59l-1.14-7.36-.01-.27h-.02v7.63h-1.67zM43.72 6.42c0-1.29 1.17-1.77 2.47-1.77s2.46.48 2.46 1.77v6.48c0 1.3-1.17 1.77-2.46 1.77s-2.47-.48-2.47-1.77zm2.84.25c0-.27 0-.64-.37-.64s-.37.37-.37.64v5.92c0 .27 0 .64.37.64s.37-.37.37-.64zM43.37 4.84h-3.7v1.45h.8v8.19h2.1v-8.19h.8v-1.45zM17.58 2.48h-5.25v1.55h1.55v10.45h2.14v-10.45h1.56v-1.55zM12.17 14.83v-.06a9.59 9.59 0 0 0-4.39-.77h-7.78v.53h10.5a6.47 6.47 0 0 1 1.67.34M9.07.29l-.31-.29a.37.37 0 0 0-.29 0l-.47.26v2.29a3.72 3.72 0 0 1-1.49 1.37.35.35 0 0 0-.21.36v8.53c-.31 0-.81.07-.81.07v-7.22c0-.27-.12-.35-.37-.41a14.42 14.42 0 0 1-2.72-.92v-1.48l-.4-.2a.52.52 0 0 0-.34 0 3.8 3.8 0 0 0-.49.28 2.32 2.32 0 0 0-1.17 1.92v8.82h.79v-8.82a1.48 1.48 0 0 1 .75-1.32h.06v10.14h.78v-8.5c.62.23 1 .39 1.67.6 l.64.17v7.06a9.5 9.5 0 0 0-2.19.68h1.5a9.23 9.23 0 0 1 3.77-.8l-.72-.06v-8.32h.08a4.11 4.11 0 0 0 .87-.71v9.88h.81v-12.47a3.8 3.8 0 0 1 .77 2.23v10.32c.24 0 .54.06.79.13v-10.47a4.71 4.71 0 0 0-1.3-3.12"/></svg>"""

# ─────────────────────────────────────────────
# 3. HELPER FUNCTIONS
# ─────────────────────────────────────────────
SEASON_COLORS = {"Peak Season": "#ffb347", "Shoulder": "#00ffa3", "Off-Season": "#00e5ff"}


def safe_resample_alias(label: str) -> str:
    """Return a resample frequency string compatible with both old and new pandas."""
    alias_map = {"15min": "15min", "D": "D", "ME": "ME", "YE": "YE"}
    pd_version = tuple(int(x) for x in pd.__version__.split(".")[:2])
    if pd_version < (2, 2):
        alias_map["ME"] = "M"
        alias_map["YE"] = "Y"
    return alias_map.get(label, label)


def apply_base(fig, height=360):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(12,31,53,0.3)",
        font=dict(family="DM Mono, monospace", color="#dce9f5", size=10),
        height=height,
        margin=dict(t=30, b=20, l=14, r=14),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#dce9f5")),
        xaxis=dict(gridcolor="#163352", zeroline=False),
        yaxis=dict(gridcolor="#163352", zeroline=False)
    )
    return fig


@st.cache_data
def load_processed_data():
    path = r"C:/Users/vincy/Desktop/Unified Mentor Internship/Project 2/Processed_Ferry_Tickets.csv.gz"

    # Check if file exists; if not, create dummy data for demonstration
    if not os.path.exists(path):
        st.info("CSV not found at specified path. Generating synthetic data for preview.")
        rng = np.random.default_rng(42)
        date_rng = pd.date_range(start='2025-05-01', end='2025-12-31', freq='15min')
        n = len(date_rng)
        df = pd.DataFrame({
            'Timestamp': date_rng,
            'OLI': rng.uniform(0.2, 0.9, size=n),
            'Season': rng.choice(["Peak Season", "Shoulder", "Off-Season"], size=n),
            'Redemption_Pressure_Ratio': rng.uniform(0.5, 2.5, size=n),
            'Total_Activity_Load': rng.integers(50, 500, size=n),
            'Idle_Capacity_Indicator': rng.choice([True, False], size=n),
        })
    else:
        df = pd.read_csv(path, compression='gzip')
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    if 'OLI' in df.columns:
        df['Utilization'] = df['OLI'] * 100

    # Filter: May to December
    df = df[df['Timestamp'].dt.month.isin(range(5, 13))].copy()

    # Feature Engineering
    days = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
            4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    df['Day'] = df['Timestamp'].dt.dayofweek.map(days)
    return df


# ─────────────────────────────────────────────
# 4. DASHBOARD LOGIC
# ─────────────────────────────────────────────
df = load_processed_data()

if not df.empty:
    FREQ_MAP = {
        "15-Minutes": "15min",
        "Daily":      "D",
        "Monthly":    "ME",
        "Yearly":     "YE"
    }

    with st.sidebar:
        st.markdown(f'<div style="text-align:center; padding:10px;">{LOGO_SVG}</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### ⚓ Control Center")

        min_d, max_d = df["Timestamp"].min().date(), df["Timestamp"].max().date()
        date_range = st.date_input("Analysis Window", value=(min_d, max_d), min_value=min_d, max_value=max_d)

        seasons = sorted(df['Season'].unique().tolist())
        sel_seasons = st.multiselect("Filter Seasons", seasons, default=seasons)

        freq_label = st.selectbox("Time Resolution", list(FREQ_MAP.keys()), index=0)
        threshold  = st.slider("Congestion Limit (%)", 10, 100, 75)

    # Filter Logic
    start_d = date_range[0] if isinstance(date_range, (list, tuple)) and len(date_range) >= 1 else min_d
    end_d   = date_range[1] if isinstance(date_range, (list, tuple)) and len(date_range) == 2 else max_d

    fdf = df.loc[
        (df["Timestamp"].dt.date >= start_d) &
        (df["Timestamp"].dt.date <= end_d) &
        (df["Season"].isin(sel_seasons))
    ].copy()

    # Header Section
    st.markdown("""
    <div style="margin-bottom: 30px;">
      <div class="hero-title">Ferry Capacity Utilization &amp; Efficiency Analytics</div>
      <div class="hero-sub"><span class="live-dot"></span>SYSTEM STATUS: ACTIVE · TORONTO ISLAND DATASTREAM</div>
    </div>
    """, unsafe_allow_html=True)

    if fdf.empty:
        st.warning("No data found for the selected filters.")
        st.stop()

    # 5. KPI CALCULATIONS
    avg_util       = fdf["Utilization"].mean()
    pressure       = fdf["Redemption_Pressure_Ratio"].mean() if "Redemption_Pressure_Ratio" in fdf.columns else 0.0
    total_activity = fdf["Total_Activity_Load"].sum()        if "Total_Activity_Load"        in fdf.columns else 0
    stability      = 100 - fdf["Utilization"].std()          if len(fdf) > 1                                else 100.0
    idle_pct       = (fdf["Idle_Capacity_Indicator"] == True).mean() * 100 \
                     if "Idle_Capacity_Indicator" in fdf.columns else 0.0


    def kpi_card(icon, label, value, sub, color):
        return f'''<div class="kpi-card" style="--top-color:{color}">
                    <div style="font-size:1rem; margin-bottom:5px;">{icon}</div>
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{value}</div>
                    <div style="font-size:0.6rem; color:var(--muted)">{sub}</div>
                  </div>'''


    cols = st.columns(5)
    with cols[0]:
        st.markdown(kpi_card("⚖️", "Avg Utilization", f"{avg_util:.1f}%",         "EFFICIENCY",  "#00e5ff"), unsafe_allow_html=True)
    with cols[1]:
        st.markdown(kpi_card("🔺", "Pressure Index",  f"{pressure:.2f}",           "DEMAND",      "#ff4d6d"), unsafe_allow_html=True)
    with cols[2]:
        st.markdown(kpi_card("💤", "Idle Capacity",   f"{idle_pct:.1f}%",          "WASTE RATIO", "#ffb347"), unsafe_allow_html=True)
    with cols[3]:
        st.markdown(kpi_card("⏱️", "Total Load",      f"{int(total_activity):,}",  "VOLUME",      "#c084fc"), unsafe_allow_html=True)
    with cols[4]:
        st.markdown(kpi_card("📐", "Stability",       f"{max(0.0, stability):.1f}", "CONSISTENCY", "#00ffa3"), unsafe_allow_html=True)

    # 6. VISUALIZATIONS
    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown(f'<div class="sec-title">📈 {freq_label.upper()} UTILIZATION TREND</div>', unsafe_allow_html=True)
        resample_freq = safe_resample_alias(FREQ_MAP[freq_label])
        ts_data = (
            fdf.set_index("Timestamp")
               .resample(resample_freq)
               .agg({"Utilization": "mean"})
               .reset_index()
        )
        fig_line = px.line(ts_data, x="Timestamp", y="Utilization", color_discrete_sequence=["#00e5ff"])
        fig_line.add_hline(y=threshold, line_dash="dot", line_color="#ff4d6d", annotation_text="Limit")
        apply_base(fig_line)
        st.plotly_chart(fig_line, use_container_width=True)

    with c2:
        st.markdown('<div class="sec-title">🎻 SEASONAL DISTRIBUTION</div>', unsafe_allow_html=True)
        fig_vio = px.violin(fdf, y="Utilization", x="Season", color="Season",
                            color_discrete_map=SEASON_COLORS, box=True)
        apply_base(fig_vio)
        st.plotly_chart(fig_vio, use_container_width=True)

    # Heatmap
    st.markdown('<div class="sec-title">🗺️ WEEKLY CONGESTION HEATMAP (15-MIN BLOCKS)</div>', unsafe_allow_html=True)
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    fdf["Bucket"] = fdf["Timestamp"].dt.floor(pd.Timedelta(minutes=15)).dt.strftime("%H:%M")
    hm_data = (
        fdf.groupby(["Day", "Bucket"])["Utilization"]
           .mean()
           .unstack()
           .reindex(day_order)
           .fillna(0)
    )
    hm_data = hm_data.reindex(sorted(hm_data.columns), axis=1)

    fig_hm = px.imshow(hm_data, color_continuous_scale="Viridis", aspect="auto", labels=dict(color="Util %"))
    apply_base(fig_hm, height=400)
    st.plotly_chart(fig_hm, use_container_width=True)

    # 7. ALERTS
    st.markdown('<div class="sec-title">⚠️ OPERATIONAL ADVISORY</div>', unsafe_allow_html=True)
    cong_pct = (fdf["Utilization"] > threshold).mean() * 100

    if cong_pct > 20:
        st.markdown(
            f'<div class="alert-box alert-critical">'
            f'<b>CRITICAL:</b> High congestion ({cong_pct:.1f}%) detected in the selected period. '
            f'Review fleet deployment for summer peaks.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="alert-box alert-nominal">'
            '<b>NOMINAL:</b> Ferry utilization is within acceptable bounds for the selected dates.</div>',
            unsafe_allow_html=True,
        )