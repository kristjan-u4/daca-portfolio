"""
Roll A — UrbanStyle CEO Dashboard
===================================================
Andmete laadimine andmebaasist.
"""
 
import os
from dotenv import load_dotenv
import sqlalchemy as sa
import pandas as pd
from pathlib import Path

from sql_filter_builder import SqlFilterBuilder
 
# Laadi keskkonna muutujad .env failist
load_dotenv(override=True)
 
# Loo Supabase klient SQL päringute tegemiseks:
supabase = sa.create_engine(os.getenv("SUPABASE_CONNECTION_STRING"))

def aggregate_sales_by_interval(filters):
    return _fetch_filtered_data("aggregated_sales_by_interval.sql", filters)

def count_unique_customers(filters):
    df = _fetch_filtered_data("unique_customers_count.sql", filters)
    return df["unique_customers"].iloc[0]

def calculate_total_revenue(filters):
    df = _fetch_filtered_data("total_revenue.sql", filters)
    return df["total_revenue"].iloc[0]

def fetch_min_and_max_sale_date():
    query = sa.text("SELECT min(sale_date) AS min_date, max(sale_date) AS max_date FROM sales;")
    df = pd.read_sql(query, supabase)
    return df["min_date"].iloc[0], df["max_date"].iloc[0]

def fetch_store_locations():
    query = sa.text(_load_query_template("store_locations.sql"))
    df = pd.read_sql(query, supabase)
    return df["store_location"]

# In your main Streamlit file or controller
def _fetch_filtered_data(template_file_name, filters):
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
    SQL päringu malli laadimine etteantud failist.
    """
    current_dir = Path(__file__).resolve().parent
    file_path = current_dir / "sql" / filename
    with open(file_path, "r") as f:
        return f.read()