# Running this script: streamlit run week-5/individual/dashboard/app.py

"""
UrbanStyle CEO Dashboard
===============================
Interaktiivne dashboard UrbanStyle CEO jaoks — Plotly + Streamlit.
DACA Programm, Nädal 5: Visualiseerimise Disain, Track B.
"""
 
import streamlit as st
import charts
import datetime

import data_loader
import utils

def main():
    setup_page()
    header_section, kpis_section, main_chart_section = prepare_placeholders()
    default_filter_settings = build_default_filter_settings()
    filters = prepare_filters(default_filter_settings)
    fill_header_section(header_section, filters)
    data = get_data(filters)
    fill_kpis_section(kpis_section, filters)
    fill_main_chart_section(main_chart_section, data)
    render_footer(data)

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
    return {
        "date_range": (datetime.date(2024, 1, 1), datetime.date(2024, 12, 31)),
        "interval": "month",
        "store_location": ("Tartu")
    }

def prepare_filters(default_filter_settings):
    st.header("Filtrid")
    col1, col2, _, _ = st.columns(4)
    filters = {}
    add_date_range_filter(filters, col1, default_filter_settings)
    add_store_location_filter(filters, col2, default_filter_settings)
    add_derived_filters(filters, default_filter_settings)
    st.divider()
    return filters

def add_date_range_filter(filters, container, default_filter_settings):
    min_date, max_date = get_sale_date_boundaries()
    
    date_range = container.date_input(
        "Ajavahemik",
        format="DD.MM.YYYY",
        value=default_filter_settings["date_range"],
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

    filters["date_range"] = (date_from, date_to)

def add_store_location_filter(filters, container, default_filter_settings):
    all_store_locations = fetch_store_locations()
    default_store_locations = tuple(
        x for x in all_store_locations
        if x in default_filter_settings["store_location"]
    )
    store_location = container.multiselect(
        "Kaupluste asukohad",
        options=all_store_locations,
        default=default_store_locations,
        help="Vali kaupluste asukohad, mille andmeid soovid näha"
    )
    filters["store_location"] = store_location


# Add secondary date-related settings, derived from user input.
def add_derived_filters(filters, default_filter_settings):
    date_from, date_to = filters["date_range"]
    filters["open_date_range"] = (date_from, date_to + datetime.timedelta(days=1))
    add_interval_setting(filters, default_filter_settings)

def add_interval_setting(filters, default_filter_settings):
    date_from, date_to = filters["open_date_range"]
    delta = date_to - date_from
    if delta.days < 60:
        filters["interval"] = "day"
    else:
        filters["interval"] = default_filter_settings["interval"]

def get_data(filters):
    return {
        "aggregated_sales": load_aggregated_sales_data(filters),
        "total_customers": count_total_customers(filters)
    }

def fill_header_section(header_section, filters):
    with header_section.container():
        st.title("CEO Dashboard")
        st.markdown(
            f"*Müügitulu, klientide arv ja kasvutrend ajavahemikus "
            f"{utils.format_date(filters['date_range'][0])} - {utils.format_date(filters['date_range'][1])}*"
        )

def fill_kpis_section(kpis_section, filters):
    with kpis_section.container():
        # KPI kaardid
        col1, col2, col3 = st.columns(3)
        
        # Arvuta müügikäive koos muutusega eelneva perioodiga võrreldes.
        total_revenue_with_delta = calculate_total_revenue_with_delta(filters)
        total_revenue = total_revenue_with_delta[0]
        total_revenue_delta = total_revenue_with_delta[1]

        col1.metric(
            label="Müügitulu",
            value=f"€{total_revenue:,.0f}".replace(",", " "),
            delta=utils.format_metric_delta_as_percentage(total_revenue_delta),
            help="Valitud perioodi kogu müügitulu"
        )

        # Arvuta klientide arv koos muutusega eelneva perioodiga võrreldes.
        total_customers_with_delta = calculate_total_customers_with_delta(filters)
        total_customers = total_customers_with_delta[0]
        total_customers_delta = total_customers_with_delta[1]
        
        col2.metric(
            label="Klientide arv",
            value=f"{total_customers:,}".replace(",", " "),
            delta=utils.format_metric_delta_as_percentage(total_customers_delta),
            help="Erinevate klientide arv valitud perioodil"
        )

def fill_main_chart_section(main_chart_section, data):
    with main_chart_section.container():
        df = data["aggregated_sales"]
        st.header("Müügitrendid")
        fig_trend = charts.create_revenue_trend(df)
        st.plotly_chart(fig_trend, use_container_width=True)

def render_footer(data):
    orders_text = f"{data['aggregated_sales']['orders'].sum():,}".replace(",", " ")
    st.caption(
        "UrbanStyle.ltd — CEO Dashboard | "
        "DACA Programm, Nädal 5 | "
        f"Andmeid: {orders_text} rida"
    )

def calculate_total_revenue_with_delta(filters):
    comparison_filters = filters_with_comparison_date_range(filters)
    total_revenue_current = calculate_total_revenue(filters)
    total_revenue_previous = calculate_total_revenue(comparison_filters)
    delta = utils.calculate_delta_in_percents(total_revenue_current, total_revenue_previous)
    return (total_revenue_current, delta)

def calculate_total_customers_with_delta(filters):
    comparison_filters = filters_with_comparison_date_range(filters)
    total_customers_current = count_total_customers(filters)
    total_customers_previous = count_total_customers(comparison_filters)
    delta = utils.calculate_delta_in_percents(total_customers_current, total_customers_previous)
    return (total_customers_current, delta)

def filters_with_comparison_date_range(filters):
    comparison_filters = dict(filters) # make a copy
    comparison_date_range = utils.calculate_previous_open_date_range(filters["open_date_range"])
    comparison_filters["open_date_range"] = comparison_date_range
    comparison_filters["date_range"] = (
        comparison_date_range[0],
        comparison_date_range[1] - datetime.timedelta(days=1)
    )
    return comparison_filters

# ============================================================
# ANDMETE LAADIMINE ja mälus puhverdamine (cache)
# ============================================================

# First and last sale date as default date range filters.
@st.cache_data(ttl=300)  # Cache 5 minutiks (300 sekundit)
def get_sale_date_boundaries():
    return data_loader.fetch_min_and_max_sale_date()

@st.cache_data(ttl=300)
def fetch_store_locations():
    return data_loader.fetch_store_locations()
 
@st.cache_data(ttl=300)
def load_aggregated_sales_data(filters):
    """Laadi agregeeritud müügiandmed Supabase'ist."""
    return data_loader.aggregate_sales_by_interval(filters)

@st.cache_data(ttl=300)
def count_total_customers(filters):
    return data_loader.count_unique_customers(filters)

@st.cache_data(ttl=300)
def calculate_total_revenue(filters):
    return data_loader.calculate_total_revenue(filters)

if __name__ == "__main__":
    main()