"""
UrbanStyle CEO Dashboard
===================================================
Data loading from the database.
"""

import os
from dotenv import load_dotenv
import sqlalchemy as sa
import pandas as pd
from pathlib import Path

# Load environment variables from .env file
load_dotenv(override=True)

# Create Supabase client for SQL queries
supabase = sa.create_engine(os.getenv("SUPABASE_CONNECTION_STRING"))

def aggregate_sales_by_interval(filter):
    """
    Aggregates sales data by a specified interval (e.g., day, month) based on provided filters.

    Args:
        filter (dict): A dictionary containing filter parameters for the SQL query.

    Returns:
        pd.DataFrame: A DataFrame with aggregated sales data.
    """
    query = sa.text(_load_query_template("aggregated_sales_by_interval.sql"))
    return pd.read_sql(query, supabase, params=filter)

def count_unique_customers(filter):
    """
    Counts the number of unique customers based on provided filters.

    Args:
        filter (dict): A dictionary containing filter parameters for the SQL query.

    Returns:
        int: The number of unique customers.
    """
    query = sa.text(_load_query_template("unique_customers_count.sql"))
    df = pd.read_sql(query, supabase, params=filter)
    return df["unique_customers"].iloc[0]

def calculate_total_revenue(filter):
    """
    Calculates the total revenue based on provided filters.

    Args:
        filter (dict): A dictionary containing filter parameters for the SQL query.

    Returns:
        float: The total revenue.
    """
    query = sa.text(_load_query_template("total_revenue.sql"))
    df = pd.read_sql(query, supabase, params=filter)
    return df["total_revenue"].iloc[0]

def fetch_min_and_max_sale_date():
    """
    Fetches the minimum and maximum sale dates from the sales table.

    Returns:
        tuple: A tuple containing the minimum and maximum sale dates (datetime.date).
    """
    query = sa.text("SELECT min(sale_date) AS min_date, max(sale_date) AS max_date FROM sales;")
    df = pd.read_sql(query, supabase)
    return df["min_date"].iloc[0], df["max_date"].iloc[0]

def _load_query_template(filename):
    """
    Loads an SQL query template from a specified file.

    Args:
        filename (str): The name of the SQL file to load.

    Returns:
        str: The content of the SQL query file.
    """
    current_dir = Path(__file__).resolve().parent
    file_path = current_dir / "sql" / filename
    with open(file_path, "r") as f:
        return f.read()
