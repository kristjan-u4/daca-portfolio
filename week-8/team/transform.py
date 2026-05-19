# Nädal 8 grupitöö alaülesanne Roll B
# Roll B: Data Processing
# Ülesanne: puhastan andmed, arvutan nädalased koondnäitajad ja KPI-d,
# ning liidan müügiandmed kliendiandmetega.

import pandas as pd
import logging


# Seadistan logimise, et oleks näha, mida iga transformatsioon teeb
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def clean_data(df):
    """
    Puhastab müügiandmed:
    - eemaldab duplikaadid
    - käsitleb NULL väärtuseid
    - teisendab sale_date veeru datetime formaati
    - kontrollib andmete kvaliteeti
    """
    logger.info("Alustan andmete puhastamist")

    df_clean = df.copy()

    # Kontrollin, kas vajalikud veerud on olemas
    required_columns = ["sale_date", "customer_id", "total_price"]

    for col in required_columns:
        if col not in df_clean.columns:
            logger.error(f"Puuduv vajalik veerg: {col}")
            raise ValueError(f"Puuduv vajalik veerg: {col}")

    # Eemaldan duplikaadid
    before = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    after = len(df_clean)

    logger.info(f"Eemaldatud duplikaate: {before - after}")

    # Teisendan kuupäeva datetime formaati
    df_clean["sale_date"] = pd.to_datetime(df_clean["sale_date"], errors="coerce")

    # Eemaldan read, kus kuupäev puudub või oli vigane
    missing_dates = df_clean["sale_date"].isna().sum()

    if missing_dates > 0:
        logger.warning(f"Leiti {missing_dates} vigase või puuduva kuupäevaga rida")

    df_clean = df_clean.dropna(subset=["sale_date"])

    # Teisendan total_price numbriliseks
    df_clean["total_price"] = pd.to_numeric(df_clean["total_price"], errors="coerce")

    # Kui total_price puudub, asendan 0-ga
    missing_prices = df_clean["total_price"].isna().sum()

    if missing_prices > 0:
        logger.warning(f"Leiti {missing_prices} puuduva hinnaga rida, asendan 0-ga")

    df_clean["total_price"] = df_clean["total_price"].fillna(0)

    # Kontrollin negatiivseid hindu
    negative_prices = df_clean[df_clean["total_price"] < 0]

    if len(negative_prices) > 0:
        logger.warning(f"Leiti {len(negative_prices)} negatiivse hinnaga rida")

    # Kui customer_id puudub, siis ei saa müüki kliendiga siduda
    missing_customers = df_clean["customer_id"].isna().sum()

    if missing_customers > 0:
        logger.warning(f"Leiti {missing_customers} puuduva customer_id-ga rida")

    df_clean = df_clean.dropna(subset=["customer_id"])

    logger.info(f"Puhastatud andmestikus on {len(df_clean)} rida")
    return df_clean


def calculate_weekly_aggregates(df):
    """
    Arvutab nädalapõhised koondnäitajad:
    - kogutulu
    - tellimuste arv
    - keskmine tellimuse väärtus
    """
    logger.info("Arvutan nädalased koondnäitajad")

    df_weekly = df.copy()

    # Kontrollin, kas andmestik on tühi
    if df_weekly.empty:
        logger.warning("Andmestik on tühi, nädalasi koondnäitajaid ei saa arvutada")
        return pd.DataFrame()

    # Kontrollin vajalikke veerge
    required_columns = ["sale_date", "total_price"]

    for col in required_columns:
        if col not in df_weekly.columns:
            logger.error(f"Puuduv vajalik veerg nädalaste koondite jaoks: {col}")
            raise ValueError(f"Puuduv vajalik veerg: {col}")

    # Kui sale_id puudub, kasutan tellimuste arvuks ridade arvu
    if "sale_id" in df_weekly.columns:
        order_column = "sale_id"
    else:
        order_column = "total_price"
        logger.warning("Veerg 'sale_id' puudub, kasutan tellimuste arvuks ridade arvu")

    df_weekly["sale_date"] = pd.to_datetime(df_weekly["sale_date"], errors="coerce")
    df_weekly["total_price"] = pd.to_numeric(df_weekly["total_price"], errors="coerce").fillna(0)

    df_weekly = df_weekly.dropna(subset=["sale_date"])

    weekly = df_weekly.resample("W", on="sale_date").agg(
        total_revenue=("total_price", "sum"),
        orders_count=(order_column, "count"),
        avg_order_value=("total_price", "mean")
    ).reset_index()

    weekly["total_revenue"] = weekly["total_revenue"].round(2)
    weekly["avg_order_value"] = weekly["avg_order_value"].round(2)

    logger.info(f"Nädalasi ridu arvutatud: {len(weekly)}")
    return weekly


def calculate_kpis(df):
    """
    Arvutab peamised KPI-d ja tagastab need dict kujul:
    - total_revenue
    - unique_customers
    - avg_order_value
    - total_orders
    """
    logger.info("Arvutan KPI-d")

    df_kpi = df.copy()

    if df_kpi.empty:
        logger.warning("Andmestik on tühi, KPI-d tagastatakse nullväärtustega")
        return {
            "total_revenue": 0.0,
            "unique_customers": 0,
            "avg_order_value": 0.0,
            "total_orders": 0
        }

    required_columns = ["total_price", "customer_id"]

    for col in required_columns:
        if col not in df_kpi.columns:
            logger.error(f"Puuduv vajalik veerg KPI-de jaoks: {col}")
            raise ValueError(f"Puuduv vajalik veerg: {col}")

    df_kpi["total_price"] = pd.to_numeric(df_kpi["total_price"], errors="coerce").fillna(0)

    kpis = {
        "total_revenue": float(round(df_kpi["total_price"].sum(), 2)),
        "unique_customers": int(df_kpi["customer_id"].nunique()),
        "avg_order_value": float(round(df_kpi["total_price"].mean(), 2)),
        "total_orders": int(len(df_kpi))
    }

    logger.info(f"KPI-d arvutatud: {kpis}")
    return kpis


def merge_datasets(df_sales, df_customers):
    """
    Liidab müügiandmed kliendiandmetega customer_id järgi.
    Kasutan left join'i, et kõik müügiread jääksid alles.
    """
    logger.info("Liidan müügiandmed ja kliendiandmed")

    if "customer_id" not in df_sales.columns:
        logger.error("Müügiandmetes puudub customer_id")
        raise ValueError("Müügiandmetes puudub customer_id")

    if "customer_id" not in df_customers.columns:
        logger.error("Kliendiandmetes puudub customer_id")
        raise ValueError("Kliendiandmetes puudub customer_id")

    merged = pd.merge(
        df_sales,
        df_customers,
        on="customer_id",
        how="left"
    )

    missing_customer_info = merged.isna().sum().sum()

    if missing_customer_info > 0:
        logger.warning(f"Liidetud andmestikus on {missing_customer_info} puuduvat väärtust")

    logger.info(f"Liidetud andmestikus on {len(merged)} rida ja {len(merged.columns)} veergu")
    return merged


# See osa on ainult Roll B faili eraldi testimiseks.
# Kui pipeline.py impordib selle faili, siis see osa automaatselt ei käivitu.
if __name__ == "__main__":

    # Näidisandmed testimiseks
    df_sales = pd.DataFrame({
        "sale_id": [1, 2, 3, 3],
        "sale_date": ["2024-01-01", "2024-01-08", "2024-01-15", "2024-01-15"],
        "customer_id": [101, 102, 101, 101],
        "total_price": [100, 200, 150, 150]
    })

    df_customers = pd.DataFrame({
        "customer_id": [101, 102],
        "first_name": ["Mari", "Jaan"],
        "city": ["Tallinn", "Tartu"]
    })

    # Testin clean_data() funktsiooni
    df_sales_clean = clean_data(df_sales)

    # Testin nädalaste koondnäitajate arvutamist
    weekly = calculate_weekly_aggregates(df_sales_clean)
    print(weekly.head())

    # Testin KPI-de arvutamist
    kpis = calculate_kpis(df_sales_clean)
    print(kpis)

    # Testin müügi- ja kliendiandmete ühendamist
    merged = merge_datasets(df_sales_clean, df_customers)
    print(merged.head())