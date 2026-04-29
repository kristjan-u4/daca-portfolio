# Running this script: streamlit run dashboard/app.py

"""
UrbanStyle Investor Dashboard
===============================
Interaktiivne dashboard investoritele — Plotly + Streamlit.
DACA Programm, Nädal 5: Visualiseerimise Disain, Track B.
"""
 
import streamlit as st
import pandas as pd
import data_loader
import charts
import datetime

def main():
    setup_page()
    header_section, kpis_section, main_chart_section = prepare_placeholders()
    default_filter_settings = build_default_filter_settings()
    filters = prepare_filters(default_filter_settings)
    fill_header_section(header_section, filters)
    params = compose_sql_params(filters, default_filter_settings)
    data = get_data(params)
    fill_kpis_section(kpis_section, data)
    fill_main_chart_section(main_chart_section, data)
    render_footer(data)

# ============================================================
# 1. LEHE SEADISTAMINE
# ============================================================
def setup_page():
    st.set_page_config(
        page_title="UrbanStyle Dashboard", # brauseri vahekaardi pealkiri
        page_icon="📊", # brauseri vahekaardi ikoon
        layout="wide" # kasuta kogu laiust
    )

def prepare_placeholders():
    header_section = st.empty()
    st.divider()

    kpis_section = st.empty()
    st.divider()

    main_chart_section = st.empty()
    st.divider()

    return header_section, kpis_section, main_chart_section

def build_default_filter_settings():
    min_date, max_date = get_sale_date_boundaries()
    return {
        "min_date": min_date,
        "max_date": max_date,
        "interval": "month"
    }

def prepare_filters(default_filter_settings):
    st.header("🔍 Filtrid")
    date_range = prepare_date_range_filter(default_filter_settings)
    st.divider()
    return {
        "date_range": date_range
    }

def prepare_date_range_filter(default_filter_settings):
    min_date = default_filter_settings["min_date"]
    max_date = default_filter_settings["max_date"]
    
    date_range = st.date_input(
        "Ajavahemik",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        help="Vali algus- ja lõppkuupäev"
    )
    if len(date_range) < 2:
        st.info("Palun vali kalendris ka lõppkuupäev.")
        st.stop() # programmikoodi täitmine lõpetatakse

   # Kasutame vaikeväärtusi, kui mingil põhjusel väärtused puuduvad:
    date_from = date_range[0] or default_filter_settings["min_date"]
    date_to = date_range[1] or default_filter_settings["max_date"]

    return (date_from, date_to)

def compose_sql_params(filters, default_filter_settings):
    params = {}
    add_date_range_sql_params(params, filters, default_filter_settings)
    add_interval_sql_params(params, default_filter_settings)
    return params

def add_date_range_sql_params(params, filters, default_filter_settings):
    date_range = filters["date_range"]
    params["time_from"] = date_range[0]
    # Lisame ühe päeva juurde, sest SQL päringus on ülemine piir lahtine,
    # kuid kasutaja poolt etteantud filtrina on ajavahemiku ülemine piir kaasa arvatud.
    params["time_to"] = date_range[1] + datetime.timedelta(days=1)

def add_interval_sql_params(params, default_filter_settings):
    delta = params["time_to"] - params["time_from"]
    if delta.days < 60:
        params["interval"] = "day"
    else:
        params["interval"] = default_filter_settings["interval"]

def get_data(params):
    return {
        "aggregated_sales": load_aggregated_sales_data(params),
        "total_customers": count_total_customers(params)
    }

def fill_header_section(header_section, filters):
    with header_section.container():
        st.title("📊 CEO Dashboard")
        st.markdown(
            f"*Müügitulu, klientide arv ja kasvutrend ajavahemikus "
            f"{format_date(filters['date_range'][0])} - {format_date(filters['date_range'][1])}*"
        )

def fill_kpis_section(kpis_section, data):
    with kpis_section.container():
        df = data["aggregated_sales"]
        # Arvuta KPI-d
        total_revenue = df["käive"].sum()
        total_customers = data["total_customers"]
        
        # KPI kaardid
        col1, col2 = st.columns(2)
        
        col1.metric(
            label="Müügitulu",
            value=f"€{total_revenue:,.0f}".replace(",", " "),
            help="Valitud perioodi kogu müügitulu"
        )
        
        col2.metric(
            label="Klientide arv",
            value=f"{total_customers:,}".replace(",", " "),
            help="Erinevate klientide arv valitud perioodil"
        )

def fill_main_chart_section(main_chart_section, data):
    with main_chart_section.container():
        df = data["aggregated_sales"]
        st.header("📈 Müügitrendid")
        fig_trend = charts.create_revenue_trend(df)
        st.plotly_chart(fig_trend, use_container_width=True)

def render_footer(data):
    orders_text = f"{data['aggregated_sales']['tellimusi'].sum():,}".replace(",", " ")
    st.caption(
        "UrbanStyle.ltd — Investor Dashboard | "
        "DACA Programm, Nädal 5 | "
        f"Andmeid: {orders_text} rida"
    )

# Eesti formaat kuupäevadele.
def format_date(date):
    return date.strftime('%d.%m.%Y')

# ============================================================
# 2. ANDMETE LAADIMINE (cache'iga)
# ============================================================

# First and last sale date as default date range filters.
@st.cache_data(ttl=300)  # Cache 5 minutiks (300 sekundit)
def get_sale_date_boundaries():
    return data_loader.fetch_min_and_max_sale_date()
 
@st.cache_data(ttl=300)
def load_aggregated_sales_data(params):
    """Laadi agregeeritud müügiandmed Supabase'ist ja cache'i need."""
    return data_loader.aggregate_sales_by_period(params)

@st.cache_data(ttl=300)
def count_total_customers(params):
    return data_loader.count_unique_customers(params)

if __name__ == "__main__":
    main()