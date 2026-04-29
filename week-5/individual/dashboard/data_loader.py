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

def fetch_earliest_sale_date():
    """
    Leiab andmebaasist kõige varasema müügikuupäeva.

    Returns:
        pd.Timestamp: Kõige varasem kuupäev. 
        Tagastab None, kui tabel on tühi.
    """
    query = sa.text("SELECT min(sale_date) AS earliest_sale FROM sales;")
    df = pd.read_sql(query, supabase)
    
    # Võtame esimese rea väärtuse. Kui tabel on tühi, tagastame None.
    val = df['earliest_sale'].iloc[0]
    return pd.to_datetime(val) if pd.notnull(val) else None

def fetch_latest_sale_date():
    """
    Leiab andmebaasist kõige hilisema müügikuupäeva.

    Returns:
        pd.Timestamp: Kõige hilisem kuupäev. 
        Tagastab None, kui tabel on tühi.
    """
    query = sa.text("SELECT max(sale_date) AS latest_sale FROM sales;")
    df = pd.read_sql(query, supabase)
    
    val = df['latest_sale'].iloc[0]
    return pd.to_datetime(val) if pd.notnull(val) else None

def _load_query_template(filename):
    """
    SQL päringu malli laadimine etteantud failist.
    """
    current_dir = Path(__file__).resolve().parent
    file_path = current_dir / "sql" / filename
    with open(file_path, "r") as f:
        return f.read()