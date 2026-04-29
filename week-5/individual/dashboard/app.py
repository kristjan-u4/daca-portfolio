# Running this script: streamlit run dashboard/app.py

"""
UrbanStyle Investor Dashboard
===============================
Interaktiivne dashboard investoritele — Plotly + Streamlit.
DACA Programm, Nädal 5: Visualiseerimise Disain, Track B.
"""
 
import streamlit as st
import pandas as pd
import charts
 
# ============================================================
# 1. LEHE SEADISTAMINE
# ============================================================
 
st.set_page_config(
    page_title="UrbanStyle Dashboard",     # brauseri vahekaardi pealkiri
    page_icon="📊",                         # brauseri vahekaardi ikoon
    layout="wide"                           # kasuta kogu laiust
)
 
# ============================================================
# 2. ANDMETE LAADIMINE (cache'iga)
# ============================================================

filters = charts.prepare_filters()
 
@st.cache_data(ttl=300)  # Cache 5 minutiks (300 sekundit)
def get_data():
    """Laadi andmed Supabase'ist ja cache'i need."""
    return charts.prepare_data(filters)
 
# Laadi andmed
data = get_data()
df = data["aggregated_sales"]
 
# Teisenda kuupäev
df["perioodi_algus"] = pd.to_datetime(df["perioodi_algus"])
 
# ============================================================
# 3. PÄIS JA KPI KAARDID
# ============================================================
 
st.title("📊 CEO Dashboard")
st.markdown("*Müügitulu, klientide arv ja kasvutrend*")
st.divider()
 
# Arvuta KPI-d
total_revenue = df["käive"].sum()
total_customers = data["total_customers"]
 
# KPI kaardid
col1, col2 = st.columns(2)
 
col1.metric(
    label="Müügitulu",
    value=f"€{total_revenue:,.0f}",
    help="Valitud perioodi kogu müügitulu"
)
 
col2.metric(
    label="Klientide arv",
    value=f"{total_customers:,}",
    help="Erinevate klientide arv valitud perioodil"
)
 
st.divider()
 
# ============================================================
# 4. PEADIAGRAMM
# ============================================================
 
# Esimene rida: müügitrend (täislaiuses)
st.header("📈 Müügitrendid")
fig_trend = charts.create_revenue_trend(df)
st.plotly_chart(fig_trend, use_container_width=True)

st.divider()

# ============================================================
# 5. TUGIDIAGRAMMID
# ============================================================

pass

# ============================================================
# 6. FILTRID
# ============================================================
 
st.header("🔍 Filtrid")
 
# Kuupäeva filter
min_date = filters["time_from"].date()
max_date = filters["time_to"].date()
date_range = st.sidebar.date_input(
    "Ajavahemik",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    help="Vali algus- ja lõppkuupäev"
)

# ============================================================
# 7. JALUS
# ============================================================
 
st.divider()
st.caption(
    "UrbanStyle.ltd — Investor Dashboard | "
    "DACA Programm, Nädal 5 | "
    f"Andmeid: {df["tellimusi"].sum():,} rida"
)
