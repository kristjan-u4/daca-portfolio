"""
Role B — Executive Summary - Tartu Store 2024
=============================================
Loading data from the database.
"""
 
import os
import sqlalchemy as sa
import pandas as pd
from pathlib import Path

from sql_filter_builder import SqlFilterBuilder

CACHE_TTL = 300

try:
    import streamlit as st
    # Streamlit Cloud environment - no .env file available, uses secrets instead.
    supabase_connection_string = st.secrets["supabase"]["connection_string"]
except Exception:
    # Local environment - using .env file.
    from dotenv import load_dotenv
    load_dotenv(override=True)
    supabase_connection_string = os.getenv("SUPABASE_CONNECTION_STRING")
 
# Create Supabase client for SQL queries:
supabase = sa.create_engine(supabase_connection_string)

@st.cache_data(ttl=CACHE_TTL)
def aggregate_sales_by_interval(filters):
    """
    Fetch and aggregate sales data by the specified interval.

    Args:
        filters (dict): Active filter settings.

    Returns:
        pd.DataFrame: Aggregated sales data.
    """
    return _fetch_filtered_data("aggregated_sales_by_interval.sql", filters)

@st.cache_data(ttl=CACHE_TTL)
def aggregate_sales_by_customer_city(filters):
    """
    Fetch and aggregate sales data by customer city.

    Args:
        filters (dict): Active filter settings.

    Returns:
        pd.DataFrame: Aggregated sales data by city.
    """
    return _fetch_filtered_data("aggregated_sales_by_customer_city.sql", filters)

@st.cache_data(ttl=CACHE_TTL)
def fetch_aggregated_sales_summary(filters):
    """
    Fetch a summary of aggregated sales.

    Args:
        filters (dict): Active filter settings.

    Returns:
        dict: A dictionary containing summary metrics.
    """
    df = _fetch_filtered_data("aggregated_sales_summary.sql", filters)
    return df.to_dict(orient="records")[0]

@st.cache_data(ttl=CACHE_TTL)
def fetch_top_products(filters):
    """
    Fetch top selling products based on filters.

    Args:
        filters (dict): Active filter settings.

    Returns:
        pd.DataFrame: Top products data.
    """
    return _fetch_filtered_data("top_products.sql", filters)

@st.cache_data(ttl=CACHE_TTL)
def get_sale_date_boundaries():
    """
    Get the minimum and maximum sale dates available in the database.

    Returns:
        tuple: A tuple containing (min_date, max_date).
    """
    query = sa.text("SELECT min(sale_date) AS min_date, max(sale_date) AS max_date FROM sales;")
    df = pd.read_sql(query, supabase)
    return df["min_date"].iloc[0], df["max_date"].iloc[0]

@st.cache_data(ttl=CACHE_TTL)
def fetch_store_locations():
    """
    Fetch all unique store locations.

    Returns:
        pd.Series: Unique store locations.
    """
    query = sa.text(_load_query_template("store_locations.sql"))
    df = pd.read_sql(query, supabase)
    return df["store_location"]

def _fetch_filtered_data(template_file_name, filters):
    """
    Helper function to fetch filtered data using a SQL template.

    Args:
        template_file_name (str): The name of the SQL template file.
        filters (dict): Active filter settings.

    Returns:
        pd.DataFrame: The query results.
    """
    # Initialize the builder
    builder = SqlFilterBuilder(filters)
    
    # Generate SQL snippet and params
    where_clause, sql_params = builder.build()
    sql_params["interval"] = filters["interval"]
    
    # Load your SQL template
    sql_template = _load_query_template(template_file_name)
    
    # Inject the generated WHERE clause into the template
    query = sa.text(
        sql_template.replace("{{filters_section}}", where_clause)
    )
    
    # Execute query using your database utility
    return pd.read_sql(query, supabase, params=sql_params)

def _load_query_template(filename):
    """
    Load a SQL query template from the specified file.

    Args:
        filename (str): The name of the SQL file.

    Returns:
        str: The SQL query template content.
    """
    current_dir = Path(__file__).resolve().parent
    file_path = current_dir / "sql" / filename
    with open(file_path, "r") as f:
        return f.read()
