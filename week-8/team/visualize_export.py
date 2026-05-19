# ROLL C - Visualization + Saving / Visualiseerimine ja salvestamine
#
# ÜLESANNE:
# Luua Plotly diagrammid töödeldud andmetest ja eksportida tulemused failidesse.
#
# SISEND:
# Roll B töödeldud andmed:
# - weekly_df ehk nädalased koondnäitajad
# - kpis ehk KPI-de dict
# - merged_df ehk ühendatud müügi- ja kliendiandmed
#
# VÄLJUND:
# visualize_export.py fail, kus on:
# 1. create_weekly_chart(weekly_df)
# 2. create_kpi_summary(kpis)
# 3. export_results(df, output_dir)
# 4. send_success_notification(kpis)

import os
import logging
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Seadistan loggingu, et näha terminalis, millal graafikud ja failid luuakse.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# 1. FUNKTSIOON: create_weekly_chart(weekly_df)
#
# ÜLESANNE:
# - luua Plotly joondiagramm nädalastest tululiikumistest
#
# SISEND:
# weekly_df DataFrame Roll B-st, kus on vähemalt veerud:
# - sale_date
# - weekly_revenue
#
# VÄLJUND:
# Plotly figure objekt, mida saab hiljem HTML-failina salvestada

def create_weekly_chart(weekly_df: pd.DataFrame):
    """
    Loob Plotly joondiagrammi nädalase tulu muutuse kohta.
    Funktsioon arvestab erinevate võimalike veerunimedega,
    sest Roll B weekly aggregate väljund võib olla nimetatud erinevalt.
    """
    try:
        logger.info("Alustan nädalase tulu joondiagrammi loomist.")

        if weekly_df.empty:
            logger.warning("weekly_df on tühi. Graafikut ei loodud.")
            return None

        possible_date_columns = ["sale_date", "week", "date"]
        possible_revenue_columns = ["weekly_revenue", "revenue", "total_revenue", "total_price"]

        x_column = None
        y_column = None

        for column in possible_date_columns:
            if column in weekly_df.columns:
                x_column = column
                break

        for column in possible_revenue_columns:
            if column in weekly_df.columns:
                y_column = column
                break

        if x_column is None:
            logger.error(
                f"Nädalase graafiku loomiseks puudub kuupäeva/nädala veerg. "
                f"Olemasolevad veerud: {list(weekly_df.columns)}"
            )
            return None

        if y_column is None:
            logger.error(
                f"Nädalase graafiku loomiseks puudub tulu veerg. "
                f"Olemasolevad veerud: {list(weekly_df.columns)}"
            )
            return None

        fig = px.line(
            weekly_df,
            x=x_column,
            y=y_column,
            title="Nädalane tulu",
            markers=True
        )

        fig.update_layout(
            xaxis_title="Nädal",
            yaxis_title="Tulu",
            template="plotly_white"
        )

        logger.info(
            f"Nädalase tulu joondiagramm loodud. "
            f"Kasutatud x-veerg: {x_column}, y-veerg: {y_column}."
        )

        return fig

    except Exception as error:
        logger.error(f"Viga nädalase tulu graafiku loomisel: {error}")
        return None
    
# 2. FUNKTSIOON: create_kpi_summary(kpis)
#
# ÜLESANNE:
# - luua Plotly KPI kokkuvõte
# - näidata peamisi mõõdikuid:
#   total_revenue, unique_customers, avg_order_value
#
# SISEND:
# kpis dict Roll B-st, näiteks:
# {
#     "total_revenue"
#     "unique_customers"
#     "avg_order_value"
# }
#
# VÄLJUND:
# Plotly figure objekt, mida saab hiljem HTML-failina salvestada

def create_kpi_summary(kpis: dict):
    """
    Loob Plotly indicator-kaardid KPI-de kuvamiseks.
    """
    try:
        logger.info("Alustan KPI kokkuvõtte loomist.")

        required_keys = ["total_revenue", "unique_customers", "avg_order_value"]

        missing_keys = [
            key for key in required_keys
            if key not in kpis
        ]

        if missing_keys:
            logger.error(
                f"KPI kokkuvõtte loomiseks puuduvad võtmed: {missing_keys}"
            )
            return None

        fig = make_subplots(
            rows=1,
            cols=3,
            specs=[
                [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]
            ],
            horizontal_spacing=0.12
        )

        fig.add_trace(
            go.Indicator(
                mode="number",
                value=kpis["total_revenue"],
                number={
                    "prefix": "€",
                    "valueformat": ",.2f",
                    "font": {"size": 46}
                },
                title={
                    "text": "<b>Kogutulu</b>",
                    "font": {"size": 18}
                }
            ),
            row=1,
            col=1
        )

        fig.add_trace(
            go.Indicator(
                mode="number",
                value=kpis["unique_customers"],
                number={
                    "valueformat": ",.0f",
                    "font": {"size": 46}
                },
                title={
                    "text": "<b>Unikaalsed kliendid</b>",
                    "font": {"size": 18}
                }
            ),
            row=1,
            col=2
        )

        fig.add_trace(
            go.Indicator(
                mode="number",
                value=kpis["avg_order_value"],
                number={
                    "prefix": "€",
                    "valueformat": ",.2f",
                    "font": {"size": 46}
                },
                title={
                    "text": "<b>Keskmine tellimuse väärtus</b>",
                    "font": {"size": 18}
                }
            ),
            row=1,
            col=3
        )

        fig.update_layout(
            title={
                "text": "<b>UrbanStyle KPI kokkuvõte</b>",
                "x": 0.5,
                "xanchor": "center",
                "font": {"size": 26}
            },
            height=320,
            margin={
                "l": 40,
                "r": 40,
                "t": 80,
                "b": 30
            },
            template="plotly_white",
            paper_bgcolor="white"
        )

        logger.info("KPI kokkuvõtte graafik loodud.")

        return fig

    except Exception as error:
        logger.error(f"Viga KPI kokkuvõtte loomisel: {error}")
        return None
    
# 3. FUNKTSIOON: export_results(df, output_dir, charts=None)
#
# ÜLESANNE:
# - salvestada DataFrame CSV-failina
# - lisada failinimele ajatempel
# - salvestada Plotly diagrammid HTML-failidena
# - luua output kaust, kui seda veel ei ole
#
# SISEND:
# df: DataFrame, mida soovin CSV-failina salvestada
# output_dir: kausta nimi, kuhu tulemused salvestatakse
# charts: sõnastik Plotly figuuridega, näiteks:
# {
#     "weekly_revenue": weekly_fig,
#     "kpi_summary": kpi_fig
# }
#
# VÄLJUND:
# dict salvestatud failide asukohtadega

def export_results(df: pd.DataFrame, output_dir: str = "output", charts: dict = None) -> dict:
    """
    Salvestab DataFrame'i CSV-failina ja Plotly diagrammid HTML-failidena.
    Failinimed sisaldavad ajatemplina kuupäeva ja kellaaega.
    """
    try:
        logger.info("Alustan tulemuste eksportimist.")

        # Loob output kausta, kui seda veel ei ole.
        os.makedirs(output_dir, exist_ok=True)

        # Ajatempel failinimede jaoks, näiteks 20260519_143012.
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")

        saved_files = {}

        # Salvestab DataFrame'i CSV-failina.
        csv_path = os.path.join(output_dir, f"results_{date_str}.csv")
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")

        saved_files["csv"] = csv_path

        logger.info(f"CSV fail salvestatud: {csv_path}")

        # Kui diagrammid on kaasa antud, salvestab need HTML-failidena.
        if charts:
            for chart_name, fig in charts.items():
                if fig is None:
                    logger.warning(
                        f"Graafikut '{chart_name}' ei salvestatud, sest figuur puudub."
                    )
                    continue

                html_path = os.path.join(output_dir, f"{chart_name}_{date_str}.html")
                fig.write_html(html_path)

                saved_files[chart_name] = html_path

                logger.info(f"HTML diagramm salvestatud: {html_path}")

        logger.info("Tulemuste eksportimine lõpetatud.")

        return saved_files

    except Exception as error:
        logger.error(f"Viga tulemuste eksportimisel: {error}")
        return {}

# 4. FUNKTSIOON: send_success_notification(kpis, saved_files=None)
#
# ÜLESANDE LISANÕUE:
# - lisada teavitusfunktsioon, mis saadab pipeline'i õnnestumise teatise
#   koos kokkuvõtvate numbritega
#
# TEAVITUSVERSIOON:
# - selles versioonis logitakse teade terminali hiljem saab vajadusel lisada päris emaili või Google Workspace Chat webhooki
#
# SISEND:
# kpis: Roll B-st saadud KPI dict
# saved_files: export_results() funktsiooni tagastatud failiteede dict
#
# VÄLJUND:
# notification_message tekstina

def send_success_notification(kpis: dict, saved_files: dict = None) -> str:
    """
    Koostab ja logib pipeline'i õnnestumise teatise.
    Teavitus logitakse terminali; vajadusel saab hiljem lisada emaili või webhooki.
    """
    try:
        logger.info("Koostan pipeline'i õnnestumise teavituse.")

        total_revenue = kpis.get("total_revenue", 0)
        unique_customers = kpis.get("unique_customers", 0)
        avg_order_value = kpis.get("avg_order_value", 0)

        notification_message = (
            "UrbanStyle pipeline lõpetas edukalt.\n"
            f"Kogutulu: €{total_revenue:,.2f}\n"
            f"Unikaalseid kliente: {unique_customers}\n"
            f"Keskmine tellimuse väärtus: €{avg_order_value:,.2f}\n"
        )

        if saved_files:
            notification_message += "\nSalvestatud failid:\n"

            for file_type, file_path in saved_files.items():
                notification_message += f"- {file_type}: {file_path}\n"

        logger.info("\n" + notification_message)

        return notification_message

    except Exception as error:
        logger.error(f"Viga teavituse koostamisel: {error}")
        return ""
    
# TESTIPLOKK:
#
# See osa käivitub ainult siis, kui visualize_export.py faili käivitatakse otse.
# Test kasutab versioone:
# - data_fetcher.py
# - transform.py
#
# Testi eesmärk:
# - pärida Roll A andmed
# - töödelda need Roll B funktsioonidega
# - luua Roll C graafikud
# - salvestada CSV ja HTML failid output/ kausta
# - logida pipeline'i õnnestumise teavitus

if __name__ == "__main__":
    from data_fetcher import fetch_sales, fetch_customers
    from transform import (
        clean_data,
        calculate_weekly_aggregates,
        calculate_kpis,
        merge_datasets
    )

    logger.info("Alustan Roll C faili testimist.")

    sales_df = fetch_sales("2000-01-01", "2100-12-31")
    customers_df = fetch_customers()

    # Roll B ametlik clean_data() eeldab sale_date veergu,seega kasutame seda ainult sales_df puhastamiseks.
    sales_clean = clean_data(sales_df)

    # Customers tabelis sale_date veergu ei ole,seega ei kutsu siin clean_data(customers_df).
    # merge_datasets() kasutab customers_df-i customer_id järgi liitmiseks.
    merged_df = merge_datasets(sales_clean, customers_df)

    weekly_df = calculate_weekly_aggregates(sales_clean)
    kpis = calculate_kpis(sales_clean)

    weekly_fig = create_weekly_chart(weekly_df)
    kpi_fig = create_kpi_summary(kpis)

    saved_files = export_results(
        df=merged_df,
        output_dir="output",
        charts={
            "weekly_revenue": weekly_fig,
            "kpi_summary": kpi_fig
        }
    )

    notification_message = send_success_notification(kpis, saved_files)

    print("\n--- KPI-d ---")
    print(kpis)

    print("\n--- Salvestatud failid ---")
    print(saved_files)

    print("\n--- Teavitus ---")
    print(notification_message)

# AI kasutamine:
# AI abil koostasin Plotly visualiseerimise ja tulemuste eksportimise funktsioonid.
# Lisasin nädalase tulu joondiagrammi, KPI indicator-kaardid,
# CSV ekspordi ajatempliga failinimega ning HTML diagrammide salvestamise.
# Lisaks lisasin teavitusfunktsiooni, mis logib pipeline'i õnnestumise koos kokkuvõtvate KPI numbrite ja salvestatud failide asukohtadega.
#
# Plotly KPI indicator kaardid:
# KPI-de kuvamiseks kasutatakse Plotly go.Indicator komponente.
# Loodi kolm KPI kaarti: kogutulu, unikaalsed kliendid ja keskmine tellimuse väärtus.
# Need väärtused tulevad Roll B calculate_kpis() funktsiooni dict-väljundist.
#
# KOKKUVÕTE:
# Lõin faili visualize_export.py, mis sisaldab Roll C põhifunktsioone:
# create_weekly_chart(weekly_df), create_kpi_summary(kpis),
# export_results(df, output_dir, charts) ja send_success_notification(kpis, saved_files).
#
# create_weekly_chart() loob Plotly joondiagrammi nädalase tulu muutuse kohta.
# Funktsioon kontrollib, millised kuupäeva- ja tulude veerud weekly_df andmestikus olemas on, ning kasutab graafiku loomiseks sobivaid veerge.
#
# create_kpi_summary() loob KPI kokkuvõtte indicator-kaartidena.
# KPI kaartidel kuvatakse kogutulu, unikaalsete klientide arv ja keskmine tellimuse väärtus.
#
# export_results() loob output/ kausta, kui seda ei eksisteeri, salvestab DataFrame'i CSV-failina ajatempliga failinimega ning salvestab Plotly diagrammid HTML-failidena.
#
# send_success_notification() koostab pipeline'i õnnestumise teavituse koos KPI-de ja salvestatud failide asukohtadega. Selles versioonis logitakse teavitus terminali.
#
# Testimisel loodi output/ kausta järgmised väljundid:
# - results_YYYYMMDD_HHMMSS.csv
# - weekly_revenue_YYYYMMDD_HHMMSS.html
# - kpi_summary_YYYYMMDD_HHMMSS.html
#
# CSV fail avanes VS Code'is ja sisaldas ühendatud müügi- ning kliendiandmeid.
# weekly_revenue HTML diagramm avanes brauseris ja näitas nädalast tulu.
# kpi_summary HTML diagramm avanes brauseris ja näitas KPI väärtuseid.
#
# Testimisel kasutati grupi Roll A ja Roll B faile:
# - data_fetcher.py
# - transform.py
#
# Testi tulemus:
# weekly_df sisaldas 183 nädalast rida.
# Arvutatud KPI-d olid:
# total_revenue = 2607691.53,
# unique_customers = 2549,
# avg_order_value = 287.57,
# total_orders = 9068
#
# Roll C kvaliteedikontroll:
# [x] Diagrammid avanevad brauseris ja näitavad õigeid andmeid
# [x] CSV fail sisaldab ühendatud müügi- ja kliendiandmeid
# [x] Failinimed sisaldavad kuupäeva ja kellaaega
# [x] output/ kaust luuakse automaatselt os.makedirs abil
# [x] Teavitusfunktsioon logib pipeline'i õnnestumise kokkuvõtte
