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
import math

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
    col1, _, _, _ = st.columns(4)
    date_range = prepare_date_range_filter(col1, default_filter_settings)
    st.divider()
    return {
        "date_range": date_range
    }

def prepare_date_range_filter(container, default_filter_settings):
    min_date = default_filter_settings["min_date"]
    max_date = default_filter_settings["max_date"]
    
    date_range = container.date_input(
        "Ajavahemik",
        format="DD.MM.YYYY",
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
        total_revenue = df["total_revenue"].sum()
        total_customers = data["total_customers"]
        
        # KPI kaardid
        col1, col2, col3 = st.columns(3)
        
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

        kpi3_year = 2024
        kpi3_comparison_year = kpi3_year - 1
        total_revenue_delta = calculate_yearly_total_revenue_change_percentage(kpi3_year)

        # Kas muutuse jaoks eraldi KPI kaart on ikka õige? Alternatiiv oleks kuvada muutus delta= parameetrina esimesel KPI-l.
        # Praegune eraldi KPI, kus on võrdlus fikseeritud aastate vahel, on vaid grupitöö jaoks.
        if total_revenue_delta and not math.isnan(total_revenue_delta) and not math.isinf(total_revenue_delta):
            value_text = f"{total_revenue_delta:,.0f} %".replace(",", " ")
            col3.metric(
                label=f"Müügitulu muutus {kpi3_year} vs {kpi3_comparison_year}",
                value=value_text,
                help=f"{kpi3_year} võrdluses {kpi3_comparison_year}. aastaga"
            )

def fill_main_chart_section(main_chart_section, data):
    with main_chart_section.container():
        df = data["aggregated_sales"]
        st.header("📈 Müügitrendid")
        fig_trend = charts.create_revenue_trend(df)
        st.plotly_chart(fig_trend, use_container_width=True)

def render_footer(data):
    orders_text = f"{data['aggregated_sales']['orders'].sum():,}".replace(",", " ")
    st.caption(
        "UrbanStyle.ltd — Investor Dashboard | "
        "DACA Programm, Nädal 5 | "
        f"Andmeid: {orders_text} rida"
    )

def calculate_yearly_total_revenue_change_percentage(year):
    try:
        period_start = datetime.date(year, 1, 1)
        period_end = datetime.date(year + 1, 1, 1)
        previous_period_start = datetime.date(year - 1, 1, 1)
        total_revenue_current = calculate_total_revenue({ "time_from": period_start, "time_to": period_end })
        total_revenue_previous = calculate_total_revenue({ "time_from": previous_period_start, "time_to": period_start })
        return (total_revenue_current - total_revenue_previous) * 100 / total_revenue_previous
    except ZeroDivisionError:
        return None

# Eesti formaat kuupäevadele.
def format_date(date):
    return date.strftime('%d.%m.%Y')

# ============================================================
# ANDMETE LAADIMINE ja mälus puhverdamine (cache)
# ============================================================

# First and last sale date as default date range filters.
@st.cache_data(ttl=300)  # Cache 5 minutiks (300 sekundit)
def get_sale_date_boundaries():
    return data_loader.fetch_min_and_max_sale_date()
 
@st.cache_data(ttl=300)
def load_aggregated_sales_data(params):
    """Laadi agregeeritud müügiandmed Supabase'ist ja cache'i need."""
    return data_loader.aggregate_sales_by_interval(params)

@st.cache_data(ttl=300)
def count_total_customers(params):
    return data_loader.count_unique_customers(params)

@st.cache_data(ttl=300)
def calculate_total_revenue(params):
    return data_loader.calculate_total_revenue(params)

if __name__ == "__main__":
    main()