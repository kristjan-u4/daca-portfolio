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

def aggregate_sales_by_period(filter):
    """
    Laeb agregeeritud müügiandmed Supabase'ist.

    Kasutab SQL malli 'aggregated_sales_by_period.sql', et pärida agregeeritud müügiandmed valitud ajaperioodil.

    Args:
        filter_params (dict): Sõnastik SQL parameetritega. 
            Oodatavad võtmed:
            - 'time_from': Alguskuupäev (datetime.date).
            - 'time_to': Lõpukuupäev (datetime.date).
            - 'interval': Grupeerimise alus ('day', 'week', 'month', 'quarter').

    Returns:
        pd.DataFrame: Andmetabel veergudega ['perioodi_algus', 'käive', 'tellimusi', 'kliente'].
        
    Raises:
        SQLAlchemyError: Kui andmebaasipäring ebaõnnestub.
    """
    query = sa.text(_load_query_template("aggregated_sales_by_period.sql"))
    return pd.read_sql(query, supabase, params=filter)

def count_unique_customers(filter):
    query = sa.text(_load_query_template("unique_customers_count.sql"))
    df = pd.read_sql(query, supabase, params=filter)
    return df["unique_customers"].iloc[0]

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