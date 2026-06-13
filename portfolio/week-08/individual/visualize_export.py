import logging
import os
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Plotly to use a default template that respects the desired font/color
pio.templates.default = "plotly_white" # Use a white background template as a base

def create_weekly_chart(df_weekly):
    """
    Creates a Plotly line chart of total revenue per week, formatted for English locale.

    Args:
        df_weekly (pd.DataFrame): DataFrame from transform.calculate_weekly_aggregates
                                  with "week_start_date" and "total_revenue".

    Returns:
        go.Figure: A Plotly graph object.
    """
    if df_weekly.empty:
        logger.warning("df_weekly is empty, returning an empty Plotly figure.")
        fig = go.Figure()
        fig.update_layout(title_text="Weekly Revenue (no data)", title_x=0.5)
        return fig

    df_plot = df_weekly.copy()
    df_plot["week_label"] = df_plot["week"].apply(
        lambda p: f"Week {p.week}: {p.start_time.strftime('%Y-%m-%d')} - {p.end_time.strftime('%Y-%m-%d')}"
    )

    fig = px.line(
        df_plot,
        x="week_label",
        y="total_revenue",
        title="Total Revenue by Week",
        line_shape="linear",
        color_discrete_sequence=["#009B8D"]
    )

    fig.update_traces(
        mode="lines+markers",
        marker=dict(size=6, color="#009B8D"),
        hovertemplate=(
            "<b>%{x}</b><br>" +
            "<b>Total Revenue:</b> €%{y:,.0f}<extra></extra>"
        )
    )

    fig.update_layout(
        title_x=0.5,
        title_font=dict(size=16),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="sans-serif", color="#1A1A2E"),
        separators=".,",
        xaxis=dict(
            title="Week",
            showgrid=False,
            tickangle=45
        ),
        yaxis=dict(
            title="Total Revenue (€)",
            showgrid=False,
            tickformat=",.0f",
            tickprefix="€"
        )
    )
    logger.info("Created weekly revenue chart using Plotly Express.")
    return fig

def create_kpi_summary(kpis):
    """
    Creates a Plotly figure to display Key Performance Indicators (KPIs) using indicators.

    Args:
        kpis (dict): Dictionary from transform.calculate_kpis containing:
                     'total_revenue', 'unique_customers', 'avg_order_value'.

    Returns:
        go.Figure: A Plotly graph object (figure with indicators).
    """
    if not kpis:
        logger.warning("KPIs dictionary is empty, returning an empty Plotly figure.")
        fig = go.Figure()
        fig.update_layout(title_text="KPI Summary (no data)", title_x=0.5)
        return fig
        
    fig = make_subplots(
        rows=1, 
        cols=3, 
        specs=[[{"type":"domain"}, {"type":"domain"}, {"type":"domain"}]],
        subplot_titles=("Total Revenue", "Unique Customers", "Average Order Value")
    )

    # Total Revenue
    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis.get("total_revenue", 0.0),
        number={
            "valueformat": ",.0f",
            "prefix": "€",
            "font": {"size": 36, "color": "#009B8D"}
        },
        domain={"x": [0, 1], "y": [0, 1]}
    ), row=1, col=1)

    # Unique Customers
    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis.get("unique_customers", 0),
        number={
            "valueformat": ",.0f",
            "font": {"size": 36, "color": "#009B8D"}
        },
        domain={"x": [0, 1], "y": [0, 1]}
    ), row=1, col=2)

    # Average Order Value
    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis.get("avg_order_value", 0.0),
        number={
            "valueformat": ",.0f",
            "prefix": "€",
            "font": {"size": 36, "color": "#009B8D"}
        },
        domain={"x": [0, 1], "y": [0, 1]}
    ), row=1, col=3)

    fig.update_layout(
        title_text="Sales KPI Summary",
        title_x=0.5,
        title_font=dict(size=16),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="sans-serif", color="#1A1A2E"),
        margin=dict(l=20, r=20, t=80, b=20),
        height=250,
        separators=".,"
    )
    # Update subplot titles font
    for i in range(1, 4):
        fig.layout.annotations[i-1].update(font=dict(size=16, color="#1A1A2E"))

    logger.info("Created KPI summary chart using indicators.")
    return fig

def export_results(df: pd.DataFrame, output_dir: str, charts: dict):
    """
    Exports a DataFrame to CSV and Plotly charts to HTML files.

    Args:
        df (pd.DataFrame): The merged DataFrame to export.
        output_dir (str): The directory to save the files.
        charts (dict): A dictionary where keys are prefixes for filenames
                       and values are Plotly figure objects.

    Returns:
        dict: A dictionary of saved file paths, with keys corresponding to chart names
              and 'CSV' for the DataFrame.
    """
    os.makedirs(output_dir, exist_ok=True)
    current_time = datetime.now().strftime("%Y%m%d%H%M")
    saved_files = {}

    # Export charts
    for chart_name, fig in charts.items():
        filename = f"{chart_name}_{current_time}.html"
        filepath = os.path.join(output_dir, filename)
        fig.write_html(filepath)
        saved_files[chart_name] = filepath
        logger.info(f"Exported chart '{chart_name}' to {filepath}")

    # Export DataFrame
    df_filename = f"results_{current_time}.csv"
    df_filepath = os.path.join(output_dir, df_filename)
    df.to_csv(df_filepath, index=False)
    saved_files["CSV"] = df_filepath
    logger.info(f"Exported DataFrame to {df_filepath}")

    return saved_files

def send_success_notification(kpis: dict, saved_files: dict):
    """
    Logs the calculated KPIs and the list of saved files as a success notification.

    Args:
        kpis (dict): The dictionary of calculated KPIs.
        saved_files (dict): The dictionary of exported file paths.
    """
    logger.info("Calculated KPIs:")
    for kpi_name, kpi_value in kpis.items():
        if "revenue" in kpi_name or "value" in kpi_name:
            logger.info(f"  {kpi_name}: {_format_eur_amount_str(kpi_value)}")
        elif "customers" in kpi_name:
            logger.info(f"  {kpi_name}: {_format_number_str(kpi_value)}")
        else:
            logger.info(f"  {kpi_name}: {kpi_value}")

    logger.info("Exported files:")
    for file_type, filepath in saved_files.items():
        logger.info(f"  {file_type}: {filepath}")

def _format_eur_amount_str(value, precision=0):
    """Formats a float as an EUR amount string (e.g., '€1,234')."""
    if pd.isna(value):
        return "€-"
    return f"€{value:,.{precision}f}"

def _format_number_str(value):
    """Formats an integer with comma as thousands separator (e.g., '1,234')."""
    if pd.isna(value):
        return "-"
    return f"{int(value):,}"
