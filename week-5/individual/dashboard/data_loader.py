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
 
# Laadi keskkonna muutujad .env failist
load_dotenv(override=True)
 
# Loo Supabase klient SQL päringute tegemiseks:
supabase = sa.create_engine(os.getenv("SUPABASE_CONNECTION_STRING"))

def aggregate_sales_by_interval(filter):
    query = sa.text(_load_query_template("aggregated_sales_by_interval.sql"))
    return pd.read_sql(query, supabase, params=filter)

def count_unique_customers(filter):
    query = sa.text(_load_query_template("unique_customers_count.sql"))
    df = pd.read_sql(query, supabase, params=filter)
    return df["unique_customers"].iloc[0]

def calculate_total_revenue(filter):
    query = sa.text(_load_query_template("total_revenue.sql"))
    df = pd.read_sql(query, supabase, params=filter)
    return df["total_revenue"].iloc[0]

def fetch_min_and_max_sale_date():
    query = sa.text("SELECT min(sale_date) AS min_date, max(sale_date) AS max_date FROM sales;")
    df = pd.read_sql(query, supabase)
    return df["min_date"].iloc[0], df["max_date"].iloc[0]

def _load_query_template(filename):
    """
    SQL päringu malli laadimine etteantud failist.
    """
    current_dir = Path(__file__).resolve().parent
    file_path = current_dir / "sql" / filename
    with open(file_path, "r") as f:
        return f.read()