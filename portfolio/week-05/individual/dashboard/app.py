"""
UrbanStyle CEO Dashboard
===============================
An interactive dashboard for the UrbanStyle CEO using Plotly + Streamlit.
DACA Program, Week 5: Visualization Design, Track B.
"""

import streamlit as st
import charts
import datetime

import data_loader
import utils

def main():
    """
    Main function to run the UrbanStyle CEO Dashboard application.
    Orchestrates page setup, filter preparation, data loading, and UI rendering.
    """
    setup_page()
    header_section, kpis_section, main_chart_section = prepare_placeholders()
    default_filter_settings = build_default_filter_settings()
    filters = prepare_filters(default_filter_settings)
    fill_header_section(header_section, filters)
    params = compose_sql_params(filters, default_filter_settings)
    data = get_data(params)
    fill_kpis_section(kpis_section, filters)
    fill_main_chart_section(main_chart_section, data)
    render_footer(data)

def setup_page():
    """
    Sets up the Streamlit page configuration.
    """
    st.set_page_config(
        page_title="UrbanStyle Dashboard", # browser tab title
        page_icon="📊", # browser tab icon
        layout="wide" # use full width
    )

def prepare_placeholders():
    """
    Prepares Streamlit empty containers for different sections of the dashboard.

    Returns:
        tuple: A tuple containing the header, KPIs, and main chart section containers.
    """
    header_section = st.empty()
    st.divider()

    kpis_section = st.empty()
    st.divider()

    main_chart_section = st.empty()
    st.divider()

    return header_section, kpis_section, main_chart_section

def build_default_filter_settings():
    """
    Builds the default filter settings for the dashboard,
    including the min/max sale dates.

    Returns:
        dict: A dictionary containing default filter settings.
    """
    min_date, max_date = get_sale_date_boundaries()
    return {
        "min_date": min_date,
        "max_date": max_date,
        "interval": "month"
    }

def prepare_filters(default_filter_settings):
    """
    Prepares and renders the filter section of the dashboard.

    Args:
        default_filter_settings (dict): Default settings for the filters.

    Returns:
        dict: A dictionary containing the selected filter values.
    """
    st.header("Filters")
    col1, _, _, _ = st.columns(4)
    filters = {}
    add_date_range_filter(filters, col1, default_filter_settings)
    st.divider()
    return filters

def add_date_range_filter(filters, container, default_filter_settings):
    """
    Adds a date range filter to the specified container.

    Args:
        filters (dict): The dictionary to store the selected filter values.
        container (streamlit.delta_generator.DeltaGenerator): The Streamlit container
                                                            to render the date input.
        default_filter_settings (dict): Default settings including min_date and max_date.
    """
    min_date = default_filter_settings["min_date"]
    max_date = default_filter_settings["max_date"]

    date_range = container.date_input(
        "Date Range",
        format="YYYY-MM-DD", # Streamlit's date input format, not display format
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        help="Select start and end dates"
    )
    if len(date_range) < 2:
        st.info("Please also select an end date in the calendar.")
        st.stop() # execution is stopped

    # Use default values if for some reason values are missing
    date_from = date_range[0] or default_filter_settings["min_date"]
    date_to = date_range[1] or default_filter_settings["max_date"]

    filters["date_range"] = (date_from, date_to)
    # Define an open-ended date range for SQL queries
    filters["open_date_range"] = (date_from, date_to + datetime.timedelta(days=1))

def compose_sql_params(filters, default_filter_settings):
    """
    Composes SQL query parameters based on active filters and default settings.

    Args:
        filters (dict): Dictionary containing active filter values.
        default_filter_settings (dict): Default filter settings.

    Returns:
        dict: A dictionary of SQL parameters.
    """
    params = {}
    add_date_range_sql_params(params, filters, default_filter_settings)
    add_interval_sql_params(params, default_filter_settings)
    return params

def add_date_range_sql_params(params, filters, default_filter_settings):
    """
    Adds date range parameters to the SQL parameters dictionary.

    Args:
        params (dict): The dictionary to store SQL parameters.
        filters (dict): Dictionary containing active filter values.
        default_filter_settings (dict): Default filter settings.
    """
    date_range = filters["open_date_range"]
    params["time_from"] = date_range[0]
    params["time_to"] = date_range[1]

def add_interval_sql_params(params, default_filter_settings):
    """
    Adds the aggregation interval parameter to the SQL parameters dictionary.

    Args:
        params (dict): The dictionary to store SQL parameters.
        default_filter_settings (dict): Default filter settings.
    """
    delta = params["time_to"] - params["time_from"]
    if delta.days < 60:
        params["interval"] = "day"
    else:
        params["interval"] = default_filter_settings["interval"]

def get_data(params):
    """
    Fetches all necessary data for the dashboard based on SQL parameters.

    Args:
        params (dict): SQL query parameters.

    Returns:
        dict: A dictionary containing aggregated sales data and total customer count.
    """
    return {
        "aggregated_sales": load_aggregated_sales_data(params),
        "total_customers": count_total_customers(params)
    }

def fill_header_section(header_section, filters):
    """
    Fills the header section of the dashboard with a title and descriptive text.

    Args:
        header_section (streamlit.delta_generator.DeltaGenerator): The Streamlit container
                                                                  for the header.
        filters (dict): Dictionary containing active filter values.
    """
    with header_section.container():
        st.title("CEO Dashboard")
        st.markdown(
            f"*Revenue, customer count, and growth trend for the period "
            f"{utils.format_date(filters['date_range'][0])} - {utils.format_date(filters['date_range'][1])}*"
        )

def fill_kpis_section(kpis_section, filters):
    """
    Fills the KPI section of the dashboard with key performance indicators.

    Args:
        kpis_section (streamlit.delta_generator.DeltaGenerator): The Streamlit container
                                                                for the KPIs.
        filters (dict): Dictionary containing active filter values.
    """
    with kpis_section.container():
        # KPI Cards
        col1, col2, col3 = st.columns(3)

        # Calculate total revenue with delta compared to the previous period.
        total_revenue_with_delta = calculate_total_revenue_with_delta(filters["open_date_range"])
        total_revenue = total_revenue_with_delta[0]
        total_revenue_delta = total_revenue_with_delta[1]

        col1.metric(
            label="Revenue",
            value=utils.format_eur_amount(total_revenue, 0),
            delta=utils.format_metric_delta_as_percentage(total_revenue_delta),
            help="Total revenue for the selected period"
        )

        # Calculate customer count with delta compared to the previous period.
        total_customers_with_delta = calculate_total_customers_with_delta(filters["open_date_range"])
        total_customers = total_customers_with_delta[0]
        total_customers_delta = total_customers_with_delta[1]

        col2.metric(
            label="Customer Count",
            value=utils.format_number(total_customers, 0),
            delta=utils.format_metric_delta_as_percentage(total_customers_delta),
            help="Number of unique customers in the selected period"
        )

        kpi3_year = 2024
        kpi3_comparison_year = kpi3_year - 1
        kpi3_date_range = (datetime.date(kpi3_year, 1, 1), datetime.date(kpi3_year + 1, 1, 1))
        kpi3_total_revenue_with_change = calculate_total_revenue_with_delta(kpi3_date_range)
        kpi3_total_revenue_delta = kpi3_total_revenue_with_change[1]

        if kpi3_total_revenue_delta:
            value_text = utils.format_as_percentage(kpi3_total_revenue_delta, 0)
            col3.metric(
                label=f"Revenue change {kpi3_year} vs {kpi3_comparison_year}",
                value=value_text,
                help=f"Comparison of {kpi3_year} with {kpi3_comparison_year}"
            )

def fill_main_chart_section(main_chart_section, data):
    """
    Fills the main chart section with the revenue trend chart.

    Args:
        main_chart_section (streamlit.delta_generator.DeltaGenerator): The Streamlit container
                                                                      for the main chart.
        data (dict): Dictionary containing all fetched data.
    """
    with main_chart_section.container():
        df = data["aggregated_sales"]
        st.header("Sales Trends")
        fig_trend = charts.create_revenue_trend(df)
        st.plotly_chart(fig_trend, use_container_width=True)

def render_footer(data):
    """
    Renders the footer section of the dashboard.

    Args:
        data (dict): Dictionary containing all fetched data.
    """
    orders_text = utils.format_number(data["aggregated_sales"]["orders"].sum(), 0)
    st.caption(
        "UrbanStyle.ltd — CEO Dashboard | "
        "DACA Program, Week 5 | "
        f"Data rows: {orders_text}"
    )

def calculate_total_revenue_with_delta(date_range):
    """
    Calculates the total revenue for a given date range and its percentage change
    compared to the previous equivalent period.

    Args:
        date_range (tuple): A tuple containing the start and end dates (datetime.date)
                            of the current period.

    Returns:
        tuple: A tuple containing the current total revenue and its percentage delta.
    """
    comparison_date_range = utils.calculate_previous_open_date_range(date_range)
    total_revenue_current = calculate_total_revenue({ "time_from": date_range[0], "time_to": date_range[1] })
    total_revenue_previous = calculate_total_revenue({ "time_from": comparison_date_range[0], "time_to": comparison_date_range[1] })
    delta = utils.calculate_delta_in_percents(total_revenue_current, total_revenue_previous)
    return (total_revenue_current, delta)

def calculate_total_customers_with_delta(date_range):
    """
    Calculates the total number of unique customers for a given date range and its percentage change
    compared to the previous equivalent period.

    Args:
        date_range (tuple): A tuple containing the start and end dates (datetime.date)
                            of the current period.

    Returns:
        tuple: A tuple containing the current total customer count and its percentage delta.
    """
    comparison_date_range = utils.calculate_previous_open_date_range(date_range)
    total_customers_current = count_total_customers({ "time_from": date_range[0], "time_to": date_range[1] })
    total_customers_previous = count_total_customers({ "time_from": comparison_date_range[0], "time_to": comparison_date_range[1] })
    delta = utils.calculate_delta_in_percents(total_customers_current, total_customers_previous)
    return (total_customers_current, delta)

# ============================================================
# DATA LOADING and CACHING
# ============================================================

@st.cache_data(ttl=300)
def get_sale_date_boundaries():
    """
    Fetches the minimum and maximum sale dates from the database for default date range filters.
    Results are cached for 5 minutes (300 seconds).

    Returns:
        tuple: A tuple containing the minimum and maximum sale dates (datetime.date).
    """
    return data_loader.fetch_min_and_max_sale_date()

@st.cache_data(ttl=300)
def load_aggregated_sales_data(params):
    """
    Loads aggregated sales data from Supabase based on provided parameters.
    Results are cached for 5 minutes (300 seconds).

    Args:
        params (dict): Parameters for filtering and aggregating sales data.

    Returns:
        pd.DataFrame: A DataFrame containing the aggregated sales data.
    """
    return data_loader.aggregate_sales_by_interval(params)

@st.cache_data(ttl=300)
def count_total_customers(params):
    """
    Counts unique customers based on provided parameters.
    Results are cached for 5 minutes (300 seconds).

    Args:
        params (dict): Parameters for counting unique customers.

    Returns:
        int: The total count of unique customers.
    """
    return data_loader.count_unique_customers(params)

@st.cache_data(ttl=300)
def calculate_total_revenue(params):
    """
    Calculates total revenue based on provided parameters.
    Results are cached for 5 minutes (300 seconds).

    Args:
        params (dict): Parameters for calculating total revenue.

    Returns:
        float: The total revenue.
    """
    return data_loader.calculate_total_revenue(params)

if __name__ == "__main__":
    main()
