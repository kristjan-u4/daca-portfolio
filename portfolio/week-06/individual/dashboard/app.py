"""
UrbanStyle CEO Dashboard
===============================
Interactive Executive Summary Dashboard - Tartu Store 2024 — Plotly + Streamlit.
DACA Program, Week 6: Visualization Data, Track B.
"""

import streamlit as st
import charts
import datetime

import data_loader
import utils

def main():
    """
    Main entry point for the UrbanStyle CEO Dashboard.

    Initializes the page layout, prepares placeholders, builds and applies
    filters, fetches the required data, and renders all dashboard sections.
    """
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
    """
    Configure the Streamlit page settings.

    Sets the browser tab title, icon, and wide layout.
    """
    st.set_page_config(
        page_title="UrbanStyle Dashboard",
        page_icon="📊",
        layout="wide"
    )

def prepare_placeholders():
    """
    Create empty Streamlit containers to act as layout placeholders.

    Returns:
        tuple: A tuple containing the header, KPIs, main chart, and helper charts section placeholders.
    """
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
    """
    Define the default filter settings for the dashboard.

    Returns:
        dict: A dictionary containing default values for date range, interval, store locations, and limits.
    """
    return {
        "date_range": (datetime.date(2024, 1, 1), datetime.date(2024, 12, 31)),
        "interval": "month",
        "store_location": ("Tartu",),
        "comparison_store_location": ("Tallinn",),
        "top_products_limit": 5
    }

def prepare_filters(default_filter_settings):
    """
    Render the filter UI controls and collect user selections.

    Args:
        default_filter_settings (dict): The default filter values.

    Returns:
        dict: The active filters selected by the user.
    """
    st.header("Filters")
    col1, col2, _, _ = st.columns(4)
    filters = {}
    add_date_range_filter(filters, col1, default_filter_settings)
    add_store_location_filter(filters, col2, default_filter_settings)
    add_derived_filters(filters, default_filter_settings)
    st.divider()
    return filters

def add_date_range_filter(filters, container, default_filter_settings):
    """
    Add a date range input control to the specified container.

    Args:
        filters (dict): The dictionary to store the selected date range.
        container (DeltaGenerator): The Streamlit container to render the input in.
        default_filter_settings (dict): The default filter values.
    """
    min_date, max_date = data_loader.get_sale_date_boundaries()
    
    date_range = container.date_input(
        "Date Range",
        format="DD.MM.YYYY",
        value=default_filter_settings["date_range"],
        min_value=min_date,
        max_value=max_date,
        help="Select start and end dates"
    )
    if len(date_range) < 2:
        st.info("Please also select an end date in the calendar.")
        st.stop()

    date_from = date_range[0] or default_filter_settings["min_date"]
    date_to = date_range[1] or default_filter_settings["max_date"]

    filters["date_range"] = (date_from, date_to)

def add_store_location_filter(filters, container, default_filter_settings):
    """
    Add a multi-select store location filter to the specified container.

    Args:
        filters (dict): The dictionary to store the selected store locations.
        container (DeltaGenerator): The Streamlit container to render the input in.
        default_filter_settings (dict): The default filter values.
    """
    all_store_locations = data_loader.fetch_store_locations()
    default_store_locations = tuple(
        x for x in all_store_locations
        if x in default_filter_settings["store_location"]
    )
    store_location = container.multiselect(
        "Store Locations",
        options=all_store_locations,
        default=default_store_locations,
        help="Select store locations to display data for"
    )
    filters["store_location"] = store_location

def add_derived_filters(filters, default_filter_settings):
    """
    Calculate and add secondary date-related settings derived from user input.

    Args:
        filters (dict): The active filters dictionary.
        default_filter_settings (dict): The default filter values.
    """
    date_from, date_to = filters["date_range"]
    filters["open_date_range"] = (date_from, date_to + datetime.timedelta(days=1))
    add_interval_setting(filters, default_filter_settings)
    filters["top_products_limit"] = default_filter_settings["top_products_limit"]

def add_interval_setting(filters, default_filter_settings):
    """
    Determine the aggregation interval based on the selected date range.

    Args:
        filters (dict): The active filters dictionary.
        default_filter_settings (dict): The default filter values.
    """
    date_from, date_to = filters["open_date_range"]
    delta = date_to - date_from
    if delta.days < 60:
        filters["interval"] = "day"
    else:
        filters["interval"] = default_filter_settings["interval"]

def get_data(filters, default_filter_settings):
    """
    Fetch all required datasets for the dashboard based on active filters.

    Args:
        filters (dict): The active filters dictionary.
        default_filter_settings (dict): The default filter values.

    Returns:
        dict: A dictionary containing the fetched datasets.
    """
    comparison_filters = _filters_with_comparison_date_range(filters)
    return {
        "aggregated_sales": data_loader.aggregate_sales_by_interval(filters),
        "top_products": data_loader.fetch_top_products(filters),
        "aggregated_sales_by_customer_city": data_loader.aggregate_sales_by_customer_city(filters),
        "summary": data_loader.fetch_aggregated_sales_summary(filters),
        "comparison_summary": data_loader.fetch_aggregated_sales_summary(comparison_filters),
        "comparison_store_location_aggregated_sales": data_loader.aggregate_sales_by_interval(
            _filters_with_comparison_store_location(filters, default_filter_settings)
        )
    }

def fill_header_section(header_section, filters):
    """
    Render the header section containing the title and executive summary narrative.

    Args:
        header_section (DeltaGenerator): The Streamlit placeholder for the header.
        filters (dict): The active filters dictionary.
    """
    with header_section.container():
        st.title("Executive Summary - Tartu Store 2024")
        st.markdown("""
            * ✅ **Sustainable Growth:** Tartu revenue has grown **13%** YoY, confirming the brand's regional viability.
            * ⚠️ **September Paradox:** A **36%** drop during the arrival of students suggests a lack of targeted marketing or product assortment mismatch with student budgets.
            * 🎓 **Student Segment:** The high share of customers from Tallinn and other cities points to students; this segment is currently an underutilized potential for UrbanStyle.
            * 🎯 **Recommendation for Anna Mets:** Launch a student-targeted discount campaign and test a more affordable "Campus-look" product line.
            * 🔍 **Recommendation for Liis Koppel:** Conduct a price sensitivity audit for the Tartu store to clarify the relationship between the September drop and product pricing.
        """)

        st.markdown("""
            UrbanStyle's rapid expansion has brought data chaos, but the Tartu store's **13%** annual
            revenue growth confirms our brand's strengthening outside the capital.
            Deep analysis revealed a paradox: although Tartu is a university town and the largest share of sales
            there is generated by customers registered elsewhere (including Tallinn), a critical **36%**
            drop occurred in September during the return of students. This points to a potential gap between
            our premium products (e.g., the best-selling **Luksuslikud villased pahkluu saapad**) and student purchasing
            power, or the lack of a targeted "Back-to-University" campaign. We recommend auditing the
            Tartu store's pricing strategy and launching a student-targeted segment campaign to secure the
            half-million euro growth story promised to investors.
        """)

def fill_kpis_section(kpis_section, data):
    """
    Render the KPI cards section with comparison metrics.

    Args:
        kpis_section (DeltaGenerator): The Streamlit placeholder for the KPIs.
        data (dict): The fetched dashboard data.
    """
    with kpis_section.container():
        col1, col2, col3 = kpis_section.columns(3)
        
        value, value_delta = _compose_kpi_data(data, "total_revenue")

        col1.metric(
            label="Total Revenue",
            value=utils.format_eur_amount(value),
            delta=utils.format_metric_delta_as_percentage(value_delta),
            help="Total revenue for the selected period compared to the previous period"
        )

        value, value_delta = _compose_kpi_data(data, "orders")
        
        col2.metric(
            label="Number of Orders",
            value=utils.format_number(value),
            delta=utils.format_metric_delta_as_percentage(value_delta),
            help="Number of orders in the selected period compared to the previous period"
        )

        value, value_delta = _compose_kpi_data(data, "average_order")
        
        col3.metric(
            label="Average Order Value",
            value=utils.format_eur_amount(value),
            delta=utils.format_metric_delta_as_percentage(value_delta),
            help="Average order value in the selected period compared to the previous period"
        )

def fill_main_chart_section(main_chart_section, data):
    """
    Render the main sales trend chart.

    Args:
        main_chart_section (DeltaGenerator): The Streamlit placeholder for the main chart.
        data (dict): The fetched dashboard data.
    """
    with main_chart_section.container():
        st.header("Sales Trends")
        fig_trend = charts.create_revenue_trend(data)
        st.plotly_chart(fig_trend, use_container_width=True)

def fill_helper_charts_section(helper_charts_section, data):
    """
    Render the secondary charts (top products and customer origin).

    Args:
        helper_charts_section (DeltaGenerator): The Streamlit placeholder for helper charts.
        data (dict): The fetched dashboard data.
    """
    with helper_charts_section.container():
        col1, col2 = st.columns(2)

        col1.header("Top Selling Products")
        top_products = charts.create_top_products(data["top_products"])
        col1.plotly_chart(top_products, use_container_width=True)

        col2.header("Customer Origin")
        cities = charts.create_sales_by_customer_city(data["aggregated_sales_by_customer_city"])
        col2.plotly_chart(cities, use_container_width=True)

def render_footer(data):
    """
    Render the dashboard footer with metadata.

    Args:
        data (dict): The fetched dashboard data.
    """
    orders = data["summary"]["orders"]
    st.caption(
        "UrbanStyle Ltd. — Executive Summary (Role B) | "
        "DACA Program, Week 6 | "
        f"Data: {utils.format_number(orders)} rows"
    )

def _compose_kpi_data(data, metric_name):
    """
    Calculate the current value and percentage delta for a specific metric.

    Args:
        data (dict): The fetched dashboard data.
        metric_name (str): The name of the metric to calculate.

    Returns:
        tuple: A tuple containing the current metric value and its percentage delta.
    """
    metric_current = data["summary"][metric_name]
    metric_previous = data["comparison_summary"][metric_name]
    delta = utils.calculate_delta_in_percents(metric_current, metric_previous)
    return (metric_current, delta)

def _filters_with_comparison_date_range(filters):
    """
    Generate a copy of the filters with the date range shifted to the comparison period.

    Args:
        filters (dict): The active filters dictionary.

    Returns:
        dict: A new filters dictionary with the comparison date range.
    """
    comparison_filters = dict(filters)
    comparison_date_range = utils.calculate_previous_open_date_range(filters["open_date_range"])
    comparison_filters["open_date_range"] = comparison_date_range
    comparison_filters["date_range"] = (
        comparison_date_range[0],
        comparison_date_range[1] - datetime.timedelta(days=1)
    )
    return comparison_filters

def _filters_with_comparison_store_location(filters, default_filter_settings):
    """
    Generate a copy of the filters with the store location set to the comparison store.

    Args:
        filters (dict): The active filters dictionary.
        default_filter_settings (dict): The default filter values.

    Returns:
        dict: A new filters dictionary with the comparison store location.
    """
    comparison_filters = dict(filters)
    comparison_filters["store_location"] = default_filter_settings["comparison_store_location"]
    return comparison_filters

if __name__ == "__main__":
    main()
