import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Program Insights – DOST SETUP 4.0 iFund",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #f7f7f3; }
header, footer, [data-testid="stDecoration"], #MainMenu { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 4rem 2rem; max-width: 1440px; }

.page-title { font-size: 30px; font-weight: 700; color: #111; margin-bottom: 4px; }
.page-sub   { font-size: 16px; color: #999; margin-bottom: 28px; }

.section-title {
    font-size: 14px; font-weight: 700; color: #888;
    text-transform: uppercase; letter-spacing: .1em;
    margin: 36px 0 16px 0;
    padding-bottom: 8px;
    border-bottom: 1.5px solid #e5e7eb;
}

.kpi-row { display: flex; gap: 14px; margin-bottom: 10px; flex-wrap: wrap; }
.kpi { flex:1; min-width:150px; background:#fff; border-radius:12px; border:1.5px solid #ececec; padding:18px 20px; }
.kpi-label { font-size:12px; color:#aaa; font-weight:600; text-transform:uppercase; letter-spacing:.06em; margin-bottom:6px; }
.kpi-value { font-size:32px; font-weight:700; line-height:1; margin-bottom:4px; }
.kpi-sub   { font-size:13px; color:#aaa; }
.c-blue   { color:#2563eb; }
.c-green  { color:#16a34a; }
.c-orange { color:#d97706; }
.c-red    { color:#dc2626; }
.c-purple { color:#7c3aed; }
.c-gray   { color:#374151; }

.insight-box {
    background:#fff; border-radius:12px; border:1.5px solid #e5e7eb;
    padding:18px 20px; margin-bottom:12px;
}
.insight-box h4 { font-size:16px; font-weight:700; color:#111; margin:0 0 5px 0; }
.insight-box p  { font-size:14px; color:#666; margin:0; line-height:1.6; }

.flag-card {
    background:#fff3f3; border:1.5px solid #fca5a5;
    border-radius:12px; padding:18px 20px; margin-bottom:12px;
}
.flag-card h4 { font-size:16px; font-weight:700; color:#b91c1c; margin:0 0 5px 0; }
.flag-card p  { font-size:14px; color:#666; margin:0; line-height:1.6; }

.badge { display:inline-block; font-size:12px; font-weight:700; padding:3px 10px; border-radius:20px; margin-left:8px; }
.badge-high     { background:#fee2e2; color:#b91c1c; }
.badge-medium   { background:#fef9c3; color:#a16207; }
.badge-low      { background:#dcfce7; color:#15803d; }
.badge-critical { background:#4c1d95; color:#fff; }
.badge-acc      { background:#dcfce7; color:#15803d; }
.badge-part     { background:#fef9c3; color:#a16207; }
.badge-not      { background:#fee2e2; color:#b91c1c; }

.divider { border:none; border-top:1.5px solid #f0f0f0; margin:28px 0; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════════

msmes = pd.DataFrame([
    {"name":"Han Jim Marketing Corporation", "province":"Iloilo",  "sector":"Manufacturing","org_type":"Corporation",          "msme_type":"Small",  "education":"College Graduate","year_est":2007,"assistance":1843245,"sales_s1_2024":4536000, "sales_s2_2024":4900500, "emp_latest":19, "lat":10.6866,       "lon":122.5151,      "refund_total":1843245,"refund_paid":230405.63},
    {"name":"SJL Corporation",               "province":"Iloilo",  "sector":"Services",    "org_type":"Corporation",          "msme_type":"Medium", "education":"College Graduate","year_est":2019,"assistance":4881600,"sales_s1_2024":1625000, "sales_s2_2024":2080000, "emp_latest":36, "lat":10.6932,       "lon":122.5467,      "refund_total":4881600,"refund_paid":610200},
    {"name":"Filbake Food Corporation",      "province":"Aklan",   "sector":"Manufacturing","org_type":"Corporation",          "msme_type":"Medium", "education":"College Graduate","year_est":1986,"assistance":1253933,"sales_s1_2024":32400000,"sales_s2_2024":34500000,"emp_latest":200,"lat":11.67844349,    "lon":122.3604815,   "refund_total":1253933,"refund_paid":156741.63},
    {"name":"Honore Cafe",                   "province":"Aklan",   "sector":"Manufacturing","org_type":"Single Proprietorship","msme_type":"Micro",  "education":"N/A",            "year_est":2010,"assistance":517000, "sales_s1_2024":3207600, "sales_s2_2024":3384500, "emp_latest":3,  "lat":11.69602189,   "lon":122.3705478,   "refund_total":517000, "refund_paid":459552},
    {"name":"Queen's Bakeshop",              "province":"Antique", "sector":"Manufacturing","org_type":"Single Proprietorship","msme_type":"Micro",  "education":"N/A",            "year_est":2005,"assistance":315000, "sales_s1_2024":324000,  "sales_s2_2024":366500,  "emp_latest":7,  "lat":10.786694529808,"lon":122.017570565924,"refund_total":315000, "refund_paid":39375},
])

# Refund metrics
msmes["refund_balance"] = msmes["refund_total"] - msmes["refund_paid"]
msmes["refund_pct"]     = (msmes["refund_paid"] / msmes["refund_total"] * 100).round(1)

# Sales growth
msmes["sales_growth_pct"] = ((msmes["sales_s2_2024"] - msmes["sales_s1_2024"]) / msmes["sales_s1_2024"] * 100).round(1)
msmes["sales_latest"]     = msmes["sales_s2_2024"]

# Delinquency scoring
def score(row):
    s = 0
    if row["refund_pct"] < 15:  s += 4
    elif row["refund_pct"] < 40: s += 2
    else:                         s += 1
    if row["msme_type"] == "Micro":  s += 3
    elif row["msme_type"] == "Small": s += 1
    if row["sales_latest"] < 500000:   s += 3
    elif row["sales_latest"] < 3000000: s += 1
    return s

msmes["d_score"] = msmes.apply(score, axis=1)
def risk_label(s):
    if s >= 7: return "Critical"
    if s >= 5: return "High"
    if s >= 3: return "Medium"
    return "Low"
msmes["risk"] = msmes["d_score"].apply(risk_label)

# Program track classification (Surge Up / Scale Up / Step Up)
# PLACEHOLDER — replace these with each MSME's actual program-track tier.
msmes["program_track"] = ["Step Up", "Scale Up", "Surge Up", "Step Up", "Scale Up"]

# Impact assessment data (quantifiable verdicts per MSME per semester)
impact = pd.DataFrame([
    # Honore Cafe S2 2021
    {"msme":"Honore Cafe","semester":"S2 2021","verdict":"Accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2021","verdict":"Accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2021","verdict":"Not accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2021","verdict":"Not accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2021","verdict":"Not accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2021","verdict":"Partially accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2021","verdict":"Accomplished"},
    # Honore Cafe S1 2024
    {"msme":"Honore Cafe","semester":"S1 2024","verdict":"Accomplished"},
    {"msme":"Honore Cafe","semester":"S1 2024","verdict":"Accomplished"},
    {"msme":"Honore Cafe","semester":"S1 2024","verdict":"Not accomplished"},
    {"msme":"Honore Cafe","semester":"S1 2024","verdict":"Partially accomplished"},
    {"msme":"Honore Cafe","semester":"S1 2024","verdict":"Partially accomplished"},
    {"msme":"Honore Cafe","semester":"S1 2024","verdict":"Accomplished"},
    {"msme":"Honore Cafe","semester":"S1 2024","verdict":"Accomplished"},
    # Honore Cafe S2 2024
    {"msme":"Honore Cafe","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2024","verdict":"Not accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2024","verdict":"Partially accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2024","verdict":"Partially accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2024","verdict":"Accomplished"},
    # Han Jim S1 2024
    {"msme":"Han Jim Marketing Corporation","semester":"S1 2024","verdict":"Accomplished"},
    {"msme":"Han Jim Marketing Corporation","semester":"S1 2024","verdict":"Partially accomplished"},
    {"msme":"Han Jim Marketing Corporation","semester":"S1 2024","verdict":"Accomplished"},
    {"msme":"Han Jim Marketing Corporation","semester":"S1 2024","verdict":"Partially accomplished"},
    {"msme":"Han Jim Marketing Corporation","semester":"S1 2024","verdict":"Partially accomplished"},
    # Han Jim S2 2024
    {"msme":"Han Jim Marketing Corporation","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Han Jim Marketing Corporation","semester":"S2 2024","verdict":"Partially accomplished"},
    {"msme":"Han Jim Marketing Corporation","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Han Jim Marketing Corporation","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Han Jim Marketing Corporation","semester":"S2 2024","verdict":"Accomplished"},
    # SJL S1 2024
    {"msme":"SJL Corporation","semester":"S1 2024","verdict":"Accomplished"},
    {"msme":"SJL Corporation","semester":"S1 2024","verdict":"Accomplished"},
    {"msme":"SJL Corporation","semester":"S1 2024","verdict":"Partially accomplished"},
    {"msme":"SJL Corporation","semester":"S1 2024","verdict":"Accomplished"},
    {"msme":"SJL Corporation","semester":"S1 2024","verdict":"Accomplished"},
    # SJL S2 2024
    {"msme":"SJL Corporation","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"SJL Corporation","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"SJL Corporation","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"SJL Corporation","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"SJL Corporation","semester":"S2 2024","verdict":"Accomplished"},
    # Filbake S1 2023
    {"msme":"Filbake Food Corporation","semester":"S1 2023","verdict":"Partially accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S1 2023","verdict":"Partially accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S1 2023","verdict":"Partially accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S1 2023","verdict":"Partially accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S1 2023","verdict":"Accomplished"},
    # Filbake S2 2023
    {"msme":"Filbake Food Corporation","semester":"S2 2023","verdict":"Accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S2 2023","verdict":"Partially accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S2 2023","verdict":"Partially accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S2 2023","verdict":"Accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S2 2023","verdict":"Accomplished"},
    # Filbake S1 2024
    {"msme":"Filbake Food Corporation","semester":"S1 2024","verdict":"Partially accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S1 2024","verdict":"Partially accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S1 2024","verdict":"Partially accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S1 2024","verdict":"Accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S1 2024","verdict":"Accomplished"},
    # Filbake S2 2024
    {"msme":"Filbake Food Corporation","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S2 2024","verdict":"Accomplished"},
    # Queen's S1 2024
    {"msme":"Queen's Bakeshop","semester":"S1 2024","verdict":"Accomplished"},
    {"msme":"Queen's Bakeshop","semester":"S1 2024","verdict":"Partially accomplished"},
    {"msme":"Queen's Bakeshop","semester":"S1 2024","verdict":"Accomplished"},
    {"msme":"Queen's Bakeshop","semester":"S1 2024","verdict":"Partially accomplished"},
    {"msme":"Queen's Bakeshop","semester":"S1 2024","verdict":"Accomplished"},
    # Queen's S2 2024
    {"msme":"Queen's Bakeshop","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Queen's Bakeshop","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Queen's Bakeshop","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Queen's Bakeshop","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Queen's Bakeshop","semester":"S2 2024","verdict":"Accomplished"},
])

# Merge risk into impact
impact = impact.merge(msmes[["name","province","sector","org_type","msme_type","risk"]], left_on="msme", right_on="name", how="left").drop(columns="name")

# Semester order for charts
SEM_ORDER = ["S2 2021","S1 2023","S2 2023","S1 2024","S2 2024"]

# ══════════════════════════════════════════════════════════════════════════════
# COMPUTED METRICS
# ══════════════════════════════════════════════════════════════════════════════

total_msmes   = len(msmes)
total_outputs = len(impact)
acc_count     = (impact["verdict"] == "Accomplished").sum()
part_count    = (impact["verdict"] == "Partially accomplished").sum()
not_count     = (impact["verdict"] == "Not accomplished").sum()
acc_pct       = round(acc_count / total_outputs * 100, 1)
at_risk       = msmes[msmes["risk"].isin(["High","Critical"])]["name"].tolist()
compliant     = msmes[~msmes["risk"].isin(["High","Critical"])]["name"].tolist()

# MSMEs underperforming in impact AND flagged high risk
msme_acc_rate = impact.groupby("msme").apply(lambda x: (x["verdict"]=="Accomplished").sum()/len(x)*100).reset_index()
msme_acc_rate.columns = ["msme","acc_rate"]
msme_acc_rate = msme_acc_rate.merge(msmes[["name","risk","sector","province","org_type"]], left_on="msme", right_on="name", how="left")
dual_flag = msme_acc_rate[(msme_acc_rate["acc_rate"] < 60) & (msme_acc_rate["risk"].isin(["High","Critical"]))]

# Semester trend
sem_trend = impact.groupby("semester").apply(lambda x: round((x["verdict"]=="Accomplished").sum()/len(x)*100,1)).reset_index()
sem_trend.columns = ["semester","acc_pct"]
sem_trend["semester"] = pd.Categorical(sem_trend["semester"], categories=SEM_ORDER, ordered=True)
sem_trend = sem_trend.sort_values("semester")

# Province avg risk score
prov_risk = msmes.groupby("province").agg(avg_score=("d_score","mean"), count=("name","count")).reset_index()

# Sector comparison
sector_impact = impact.groupby("sector").apply(lambda x: round((x["verdict"]=="Accomplished").sum()/len(x)*100,1)).reset_index()
sector_impact.columns = ["sector","acc_rate"]
sector_risk = msmes.groupby("sector")["d_score"].mean().reset_index()
sector_risk.columns = ["sector","avg_risk_score"]
sector_combined = sector_impact.merge(sector_risk, on="sector")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="page-title">Program Insights</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">DOST SETUP 4.0 iFund Program — Region VI &nbsp;·&nbsp; Aggregate view across all enrolled MSMEs</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — PROGRAM SNAPSHOT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Program Snapshot</div>', unsafe_allow_html=True)

risk_counts = msmes["risk"].value_counts()
high_ct     = risk_counts.get("High", 0) + risk_counts.get("Critical", 0)
low_ct      = risk_counts.get("Low", 0) + risk_counts.get("Medium", 0)

st.markdown(f"""
<div class="kpi-row">
  <div class="kpi">
    <div class="kpi-label">MSMEs Assessed</div>
    <div class="kpi-value c-blue">{total_msmes}</div>
    <div class="kpi-sub">3 provinces · Region VI</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Total Outputs Evaluated</div>
    <div class="kpi-value c-gray">{total_outputs}</div>
    <div class="kpi-sub">Across all semesters</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Overall Accomplishment Rate</div>
    <div class="kpi-value c-green">{acc_pct}%</div>
    <div class="kpi-sub">{acc_count} of {total_outputs} outputs</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Partially Accomplished</div>
    <div class="kpi-value c-orange">{round(part_count/total_outputs*100,1)}%</div>
    <div class="kpi-sub">{part_count} outputs</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Not Accomplished</div>
    <div class="kpi-value c-red">{round(not_count/total_outputs*100,1)}%</div>
    <div class="kpi-sub">{not_count} outputs</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">At-Risk MSMEs</div>
    <div class="kpi-value c-red">{high_ct}</div>
    <div class="kpi-sub">High or Critical risk of not completing the project</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Compliant MSMEs</div>
    <div class="kpi-value c-green">{low_ct}</div>
    <div class="kpi-sub">Low or Medium risk</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — PROGRAM TRACK DISTRIBUTION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Program Track Distribution</div>', unsafe_allow_html=True)

track_order = ["Surge Up", "Scale Up", "Step Up"]
track_counts = msmes["program_track"].value_counts().reindex(track_order).fillna(0).astype(int).reset_index()
track_counts.columns = ["Program Track", "Count"]

fig_track = px.bar(
    track_counts, x="Program Track", y="Count",
    color="Program Track",
    color_discrete_map={"Surge Up": "#6366f1", "Scale Up": "#0ea5e9", "Step Up": "#22c55e"},
    text="Count", title="MSMEs by Program Track",
)
fig_track.update_layout(
    showlegend=False, height=380, title_font_size=16, font=dict(size=14),
    margin=dict(t=44, b=10, l=0, r=0),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fafafa",
    xaxis_title="", yaxis_title="Count",
)
fig_track.update_traces(textposition="outside", textfont_size=16)
st.plotly_chart(fig_track, use_container_width=True)
st.caption("Placeholder tiers — update the `program_track` column in the data section with each MSME's actual Surge Up / Scale Up / Step Up classification.")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — DELINQUENCY RISK
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">At Risk of Not Completing the Project — Breakdown</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1.2, 1.5, 1.3])

with col1:
    risk_df = msmes["risk"].value_counts().reset_index()
    risk_df.columns = ["Risk Tier", "Count"]
    risk_order = ["Critical","High","Medium","Low"]
    risk_df["Risk Tier"] = pd.Categorical(risk_df["Risk Tier"], categories=risk_order, ordered=True)
    risk_df = risk_df.sort_values("Risk Tier")
    fig_r = px.bar(
        risk_df, x="Risk Tier", y="Count",
        color="Risk Tier",
        color_discrete_map={"Critical":"#4c1d95","High":"#ef4444","Medium":"#f59e0b","Low":"#22c55e"},
        text="Count", title="MSMEs by Risk Tier",
    )
    fig_r.update_layout(
        showlegend=False, height=380, title_font_size=16, font=dict(size=14),
        margin=dict(t=44,b=10,l=0,r=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fafafa",
        xaxis_title="", yaxis_title="",
    )
    fig_r.update_traces(textposition="outside", textfont_size=14)
    st.plotly_chart(fig_r, use_container_width=True)

with col2:
    prov_risk_full = msmes.groupby("province").agg(
        avg_score=("d_score","mean"),
        msme_count=("name","count"),
        high_risk=("risk", lambda x: (x.isin(["High","Critical"])).sum())
    ).reset_index()
    fig_prov = px.bar(
        prov_risk_full.sort_values("avg_score", ascending=True),
        x="avg_score", y="province", orientation="h",
        color="avg_score",
        color_continuous_scale=["#22c55e","#f59e0b","#ef4444"],
        text="avg_score", title="Avg 'At Risk' Score by Province",
        labels={"avg_score":"Avg Risk Score","province":""},
    )
    fig_prov.update_coloraxes(showscale=False)
    fig_prov.update_layout(
        height=380, title_font_size=16, font=dict(size=14),
        margin=dict(t=44,b=10,l=0,r=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fafafa",
    )
    fig_prov.update_traces(texttemplate="%{text:.1f}", textposition="outside", textfont_size=14)
    st.plotly_chart(fig_prov, use_container_width=True)

with col3:
    org_risk = msmes.groupby("org_type")["d_score"].mean().reset_index()
    msme_size_risk = msmes.groupby("msme_type")["d_score"].mean().reset_index()
    fig_org = px.bar(
        org_risk.sort_values("d_score", ascending=True),
        x="d_score", y="org_type", orientation="h",
        color="d_score",
        color_continuous_scale=["#22c55e","#f59e0b","#ef4444"],
        text="d_score", title="Avg Risk Score by Org Type",
        labels={"d_score":"Avg Risk Score","org_type":""},
    )
    fig_org.update_coloraxes(showscale=False)
    fig_org.update_layout(
        height=380, title_font_size=16, font=dict(size=14),
        margin=dict(t=44,b=10,l=0,r=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fafafa",
    )
    fig_org.update_traces(texttemplate="%{text:.1f}", textposition="outside", textfont_size=14)
    st.plotly_chart(fig_org, use_container_width=True)

# Refund progress bars
st.markdown("**Refund Completion Rate per MSME**")
ref_sorted = msmes.sort_values("refund_pct")
fig_ref = go.Figure()
for _, row in ref_sorted.iterrows():
    c = {"Critical":"#4c1d95","High":"#ef4444","Medium":"#f59e0b","Low":"#22c55e"}.get(row["risk"],"#888")
    fig_ref.add_trace(go.Bar(
        x=[row["refund_pct"]], y=[row["name"]], orientation="h",
        marker_color=c, text=f'{row["refund_pct"]:.1f}%  ({row["risk"]} Risk)',
        textposition="outside", showlegend=False,
    ))
fig_ref.add_vline(x=100, line_dash="dash", line_color="#aaa", annotation_text="100% target")
fig_ref.update_layout(
    height=320, margin=dict(t=10,b=10,l=0,r=90),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fafafa",
    xaxis=dict(range=[0,130], ticksuffix="%"),
    yaxis_title="",
    font=dict(size=14),
)
st.plotly_chart(fig_ref, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — IMPACT ASSESSMENT INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Impact Assessment Insights</div>', unsafe_allow_html=True)

col4, col5 = st.columns(2)

with col4:
    # Accomplishment rate per MSME
    msme_rates = impact.groupby("msme")["verdict"].value_counts(normalize=True).mul(100).round(1).unstack(fill_value=0).reset_index()
    for col in ["Accomplished","Partially accomplished","Not accomplished"]:
        if col not in msme_rates.columns:
            msme_rates[col] = 0
    msme_rates = msme_rates.sort_values("Accomplished", ascending=True)

    fig_acc = go.Figure()
    fig_acc.add_trace(go.Bar(name="Accomplished",          y=msme_rates["msme"], x=msme_rates["Accomplished"],          orientation="h", marker_color="#22c55e"))
    fig_acc.add_trace(go.Bar(name="Partially accomplished",y=msme_rates["msme"], x=msme_rates["Partially accomplished"],orientation="h", marker_color="#f59e0b"))
    fig_acc.add_trace(go.Bar(name="Not accomplished",      y=msme_rates["msme"], x=msme_rates["Not accomplished"],      orientation="h", marker_color="#ef4444"))
    fig_acc.update_layout(
        barmode="stack", title="Accomplishment Rate per MSME (%)",
        title_font_size=16, height=400, font=dict(size=14),
        margin=dict(t=44,b=10,l=0,r=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fafafa",
        xaxis=dict(ticksuffix="%", range=[0,100]),
        yaxis_title="",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font_size=13),
    )
    st.plotly_chart(fig_acc, use_container_width=True)

with col5:
    # Semester trend
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=sem_trend["semester"], y=sem_trend["acc_pct"],
        mode="lines+markers+text",
        line=dict(color="#6366f1", width=2.5),
        marker=dict(size=8, color="#6366f1"),
        text=sem_trend["acc_pct"].astype(str) + "%",
        textposition="top center",
        name="Accomplishment Rate",
    ))
    fig_trend.update_layout(
        title="Semester Trend: Accomplishment Rate (%)",
        title_font_size=16, height=400, font=dict(size=14),
        margin=dict(t=44,b=10,l=0,r=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fafafa",
        xaxis_title="", yaxis=dict(range=[0,110], ticksuffix="%"),
        showlegend=False,
    )
    fig_trend.add_hrect(y0=0, y1=60, fillcolor="#fee2e2", opacity=0.15, line_width=0, annotation_text="Below target zone", annotation_position="top left", annotation_font_size=12)
    st.plotly_chart(fig_trend, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — SECTOR & EDUCATION ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">What\'s Booming — Sector, Province & Education</div>', unsafe_allow_html=True)

col6, col7, col8 = st.columns(3)

with col6:
    sect_sales = msmes.groupby("sector").agg(
        total_sales=("sales_latest","sum"),
        growth=("sales_growth_pct","mean"),
    ).reset_index().sort_values("total_sales", ascending=True)
    fig_sec = px.bar(
        sect_sales, x="total_sales", y="sector", orientation="h",
        color="growth",
        color_continuous_scale=["#f59e0b","#22c55e"],
        text_auto=".2s",
        title="Sector: Total Sales (color = avg growth %)",
        labels={"total_sales":"Total Sales (PHP)","sector":"","growth":"Growth %"},
    )
    fig_sec.update_layout(
        height=360, title_font_size=15, font=dict(size=13),
        margin=dict(t=40,b=10,l=0,r=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fafafa",
        coloraxis_colorbar=dict(title="Growth %", ticksuffix="%", len=0.6),
    )
    st.plotly_chart(fig_sec, use_container_width=True)

with col7:
    prov_sales = msmes.groupby("province").agg(
        total_sales=("sales_latest","sum"),
        growth=("sales_growth_pct","mean"),
    ).reset_index().sort_values("total_sales", ascending=True)
    fig_prsales = px.bar(
        prov_sales, x="total_sales", y="province", orientation="h",
        color="growth",
        color_continuous_scale=["#f59e0b","#22c55e"],
        text_auto=".2s",
        title="Province: Total Sales (color = avg growth %)",
        labels={"total_sales":"Total Sales (PHP)","province":"","growth":"Growth %"},
    )
    fig_prsales.update_layout(
        height=360, title_font_size=15, font=dict(size=13),
        margin=dict(t=40,b=10,l=0,r=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fafafa",
        coloraxis_colorbar=dict(title="Growth %", ticksuffix="%", len=0.6),
    )
    st.plotly_chart(fig_prsales, use_container_width=True)

with col8:
    edu_df = msmes.groupby("education").agg(
        total_sales=("sales_latest","sum"),
        avg_growth=("sales_growth_pct","mean"),
        count=("name","count"),
    ).reset_index()
    edu_df["education"] = edu_df["education"].replace("N/A","Not Specified")
    fig_edu = px.bar(
        edu_df.sort_values("total_sales", ascending=True),
        x="total_sales", y="education", orientation="h",
        color="avg_growth",
        color_continuous_scale=["#f59e0b","#22c55e"],
        text_auto=".2s",
        title="Owner Education vs. Total Sales",
        labels={"total_sales":"Total Sales (PHP)","education":"Education Level","avg_growth":"Avg Growth %"},
    )
    fig_edu.update_layout(
        height=360, title_font_size=15, font=dict(size=13),
        margin=dict(t=40,b=10,l=0,r=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fafafa",
        coloraxis_colorbar=dict(title="Growth %", ticksuffix="%", len=0.6),
    )
    st.plotly_chart(fig_edu, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — SECTOR: OUTPUT COMPLETION vs RISK OF NOT COMPLETING
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Sector Comparison: Output Completion vs Risk of Not Completing the Project</div>', unsafe_allow_html=True)

fig_quad = px.scatter(
    sector_combined,
    x="acc_rate", y="avg_risk_score",
    text="sector", size=[30,30],
    color="sector",
    color_discrete_sequence=["#6366f1","#f59e0b"],
    labels={"acc_rate":"Output Accomplishment Rate (%)","avg_risk_score":"Avg 'At Risk' Score","sector":"Sector"},
)
fig_quad.add_hline(y=sector_combined["avg_risk_score"].mean(), line_dash="dot", line_color="#aaa", annotation_text="Avg risk")
fig_quad.add_vline(x=sector_combined["acc_rate"].mean(), line_dash="dot", line_color="#aaa", annotation_text="Avg accomplishment")
fig_quad.update_traces(textposition="top center", marker=dict(size=20, opacity=0.85), textfont_size=14)
fig_quad.update_layout(
    height=420, font=dict(size=14),
    margin=dict(t=20,b=20,l=0,r=0),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fafafa",
    xaxis=dict(ticksuffix="%", range=[0,110]),
    showlegend=False,
)
st.plotly_chart(fig_quad, use_container_width=True)
st.caption("Upper-left quadrant = completes outputs but still at risk. Lower-right = low output completion but low financial risk.")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 7 — PRIORITY FLAGS & INTERVENTION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Priority Flags for Intervention</div>', unsafe_allow_html=True)

# Dual flag: underperforming + high risk
if len(dual_flag) > 0:
    for _, row in dual_flag.iterrows():
        st.markdown(f"""
<div class="flag-card">
  <h4>🚨 {row['msme']} <span class="badge badge-critical">Dual Flag</span></h4>
  <p>This MSME is <strong>underperforming in outputs</strong> ({row['acc_rate']:.1f}% accomplishment rate) 
  <strong>AND flagged as {row['risk']} risk of not completing the project</strong>. 
  Province: {row['province']} · Sector: {row['sector']} · Org Type: {row['org_type']}.
  <strong>Recommended for immediate intervention.</strong></p>
</div>
""", unsafe_allow_html=True)
else:
    st.markdown("""
<div class="insight-box">
  <h4>✅ No dual-flagged MSMEs at this time</h4>
  <p>No MSME is simultaneously underperforming in outputs and classified as High/Critical risk of not completing the project.</p>
</div>
""", unsafe_allow_html=True)

# Early termination flags (low acc rate consistently)
low_acc = msme_acc_rate[msme_acc_rate["acc_rate"] < 55]
if len(low_acc) > 0:
    for _, row in low_acc.iterrows():
        risk_badge = f'<span class="badge badge-{row["risk"].lower()}">{row["risk"]} Risk</span>'
        st.markdown(f"""
<div class="insight-box">
  <h4>⚠️ {row['msme']} — Consistently Low Accomplishment {risk_badge}</h4>
  <p>Overall accomplishment rate of <strong>{row['acc_rate']:.1f}%</strong> across all assessed semesters. 
  Consider reviewing project milestones and scheduling a field visit. 
  Province: {row['province']} · Sector: {row['sector']}.</p>
</div>
""", unsafe_allow_html=True)

# High performing MSMEs
high_acc = msme_acc_rate[msme_acc_rate["acc_rate"] >= 80].sort_values("acc_rate", ascending=False)
if len(high_acc) > 0:
    st.markdown("**🌟 Booming MSMEs — High Accomplishment Rate**")
    for _, row in high_acc.iterrows():
        risk_badge = f'<span class="badge badge-{row["risk"].lower()}">{row["risk"]} Risk</span>'
        st.markdown(f"""
<div class="insight-box">
  <h4>🌟 {row['msme']} — {row['acc_rate']:.1f}% Accomplishment Rate {risk_badge}</h4>
  <p>Consistently meeting or exceeding targets. 
  Province: {row['province']} · Sector: {row['sector']} · Org: {row['org_type']}. 
  A strong candidate for success story documentation and replication.</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 8 — PROVINCIAL RISK MAP (STATIC)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Provincial Risk Map — Region VI</div>', unsafe_allow_html=True)

st.image(
    "assets/region_vi_risk_map.png",
    caption="Province fill = average 'at risk of not completing the project' score of enrolled MSMEs (darker red = higher risk).",
    use_container_width=True,
)

st.markdown('<hr class="divider">', unsafe_allow_html=True)
