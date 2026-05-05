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
    header_section, kpis_section, main_chart_section, helper_charts_section = prepare_placeholders()
    default_filter_settings = build_default_filter_settings()
    filters = prepare_filters(default_filter_settings)
    fill_header_section(header_section, filters)
    data = get_data(filters, default_filter_settings)
    fill_kpis_section(kpis_section, data)
    fill_main_chart_section(main_chart_section, data)
    fill_helper_charts_section(helper_charts_section, data)
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

    helper_charts_section = st.empty()
    st.divider()

    return header_section, kpis_section, main_chart_section, helper_charts_section

def build_default_filter_settings():
    return {
        "date_range": (datetime.date(2024, 1, 1), datetime.date(2024, 12, 31)),
        "interval": "month",
        "store_location": ("Tartu",),
        "comparison_store_location": ("Tallinn",),
        "top_products_limit": 5
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
    min_date, max_date = data_loader.get_sale_date_boundaries()
    
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
    all_store_locations = data_loader.fetch_store_locations()
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
    filters["top_products_limit"] = default_filter_settings["top_products_limit"]

def add_interval_setting(filters, default_filter_settings):
    date_from, date_to = filters["open_date_range"]
    delta = date_to - date_from
    if delta.days < 60:
        filters["interval"] = "day"
    else:
        filters["interval"] = default_filter_settings["interval"]

def get_data(filters, default_filter_settings):
    comparison_filters = filters_with_comparison_date_range(filters)
    return {
        "aggregated_sales": data_loader.aggregate_sales_by_interval(filters),
        "top_products": data_loader.fetch_top_products(filters),
        "aggregated_sales_by_customer_city": data_loader.aggregate_sales_by_customer_city(filters),
        "summary": data_loader.fetch_aggregated_sales_summary(filters),
        "comparison_summary": data_loader.fetch_aggregated_sales_summary(comparison_filters),
        "comparison_store_location_aggregated_sales": data_loader.aggregate_sales_by_interval(
            filters_with_comparison_store_location(filters, default_filter_settings)
        )
    }

def fill_header_section(header_section, filters):
    with header_section.container():
        st.title("Tartu kauplus")
        st.markdown(
            f"*Müügitulu, klientide arv ja kasvutrend ajavahemikus "
            f"{utils.format_date(filters['date_range'][0])} - {utils.format_date(filters['date_range'][1])}*"
        )

def fill_kpis_section(kpis_section, data):
    with kpis_section.container():
        # KPI kaardid
        col1, col2, col3 = kpis_section.columns(3)
        
        # Arvuta müügikäive koos muutusega eelneva perioodiga võrreldes.
        value, value_delta = compose_kpi_data(data, "total_revenue")

        col1.metric(
            label="Kogukäive",
            value=utils.format_eur_amount(value),
            delta=utils.format_metric_delta_as_percentage(value_delta),
            help="Valitud perioodi kogukäive võrreldes eelmisega"
        )

        # Number of orders compared to previous period.
        value, value_delta = compose_kpi_data(data, "orders")
        
        col2.metric(
            label="Tellimuste arv",
            value=utils.format_number(value),
            delta=utils.format_metric_delta_as_percentage(value_delta),
            help="Tellimuste arv valitud perioodil võrreldes eelmisega"
        )

        # Number of orders compared to previous period.
        value, value_delta = compose_kpi_data(data, "average_order")
        
        col3.metric(
            label="Keskmine tellimus",
            value=utils.format_eur_amount(value),
            delta=utils.format_metric_delta_as_percentage(value_delta),
            help="Keskmine tellimus valitud perioodil võrreldes eelmisega"
        )

def fill_main_chart_section(main_chart_section, data):
    with main_chart_section.container():
        st.header("Müügitrendid")
        fig_trend = charts.create_revenue_trend(data)
        st.plotly_chart(fig_trend, use_container_width=True)

def fill_helper_charts_section(helper_charts_section, data):
    with helper_charts_section.container():
        df = data["top_products"]
        col1, col2 = st.columns(2)

        col1.header("Suurima kogumüügiga tooted")
        top_products = charts.create_top_products(data["top_products"])
        col1.plotly_chart(top_products, use_container_width=True)

        col2.header("Klientide päritolu")
        cities = charts.create_sales_by_customer_city(data["aggregated_sales_by_customer_city"])
        col2.plotly_chart(cities, use_container_width=True)


def render_footer(data):
    orders = data['summary']['orders']
    st.caption(
        "UrbanStyle.ltd — CEO Dashboard | "
        "DACA Programm, Nädal 6 | "
        f"Andmeid: {utils.format_number(orders)} rida"
    )

def compose_kpi_data(data, metric_name):
    metric_current = data["summary"][metric_name]
    metric_previous = data["comparison_summary"][metric_name]
    delta = utils.calculate_delta_in_percents(metric_current, metric_previous)
    return (metric_current, delta)

def filters_with_comparison_date_range(filters):
    comparison_filters = dict(filters) # make a copy
    comparison_date_range = utils.calculate_previous_open_date_range(filters["open_date_range"])
    comparison_filters["open_date_range"] = comparison_date_range
    comparison_filters["date_range"] = (
        comparison_date_range[0],
        comparison_date_range[1] - datetime.timedelta(days=1)
    )
    return comparison_filters

def filters_with_comparison_store_location(filters, default_filter_settings):
    comparison_filters = dict(filters)
    comparison_filters["store_location"] = default_filter_settings["comparison_store_location"]
    return comparison_filters

if __name__ == "__main__":
    main()