import os
from dotenv import load_dotenv
import pandas as pd
from supabase import create_client

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

BATCH_SIZE = 1000  # Supabase API restriction on number of rows returned in API response

def fetch_sales(start_date=None, end_date=None):
    """
    Fetch sales data filtered by an optional date range in batches.
    
    Args:
        start_date (datetime.date, optional): The earliest sale date to include. Defaults to None.
        end_date (datetime.date, optional): The latest sale date to include. Defaults to None.
    
    Returns:
        pd.DataFrame: A DataFrame containing the fetched sales data.
    """
    def api_call_factory():
        query = supabase.table("sales").select("*")
        if start_date:
            query = query.gte("sale_date", start_date)
        if end_date:
            query = query.lte("sale_date", end_date)
        return query

    return _fetch_data_in_batches(api_call_factory)

def fetch_customers():
    """Fetch all customers data in batches."""
    api_call_factory = lambda: supabase.table("customers").select("*")
    return _fetch_data_in_batches(api_call_factory, order_column="customer_id")

def fetch_products():
    """Fetch all products data in batches."""
    api_call_factory = lambda: supabase.table("products").select("*")
    return _fetch_data_in_batches(api_call_factory, order_column="product_id")

def _fetch_data_in_batches(api_call_factory, order_column="id"):
    """
    Generic helper to fetch data in batches using a factory lambda 
    to avoid Supabase query object mutation bugs.
    """
    all_rows = []
    start = 0
    step = BATCH_SIZE
    
    while True:
        # Generate a fresh, unmutated query object on every iteration
        api_call = api_call_factory().order(order_column)
        
        # Apply inclusive range restriction
        api_call = api_call.range(start, start + step - 1)
        
        response = api_call.execute()
        batch = response.data
        all_rows.extend(batch)

        # Break the loop if we hit the final incomplete batch
        if len(batch) < step:
            break
        
        start += step

    return pd.DataFrame(all_rows)
