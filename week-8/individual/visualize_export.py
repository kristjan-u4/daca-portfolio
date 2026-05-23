import logging
import os
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Plotly to use a default template that respects the desired font/color
pio.templates.default = "plotly_white" # Use a white background template as a base

def _format_eur_amount_str(value, precision=0): # Changed default precision to 0
    """Formats a float as an EUR amount string (e.g., '€ 1 234').""" # Updated docstring
    if pd.isna(value):
        return '€ -'
    return f"€ {value:,.{precision}f}".replace(",", " ").replace(".", ",")

def _format_number_str(value):
    """Formats an integer with space as thousands separator (e.g., '1 234')."""
    if pd.isna(value):
        return '-'
    return f"{int(value):,}".replace(",", " ")

def create_weekly_chart(df_weekly):
    """
    Creates a Plotly line chart of total revenue per week, formatted for Estonian locale.

    Args:
        df_weekly (pd.DataFrame): DataFrame from transform.calculate_weekly_aggregates
                                  with 'week_start_date' and 'total_revenue'.

    Returns:
        go.Figure: A Plotly graph object.
    """
    if df_weekly.empty:
        logger.warning("df_weekly is empty, returning an empty Plotly figure.")
        fig = go.Figure()
        fig.update_layout(title_text="Nädala tulu (andmed puuduvad)", title_x=0.5)
        return fig

    df_plot = df_weekly.copy()
    # Create the week label for the x-axis
    df_plot['week_label'] = df_plot.apply(
        lambda row: f"Nädal {row['week_start_date'].isocalendar()[1]}: {row['week_start_date'].strftime('%d.%m.%Y')} - {(row['week_start_date'] + timedelta(days=6)).strftime('%d.%m.%Y')}",
        axis=1
    )

    fig = px.line(
        df_plot,
        x="week_label",
        y="total_revenue",
        title="Kogutulu nädala kaupa",
        line_shape='linear', # Default, but explicitly set for clarity
        color_discrete_sequence=['#009B8D'] # Set line color
    )

    fig.update_traces(
        mode='lines+markers', # Show points on the line
        marker=dict(size=6, color='#009B8D'),
        hovertemplate=(
            '<b>%{x}</b><br>' + # Week label
            '<b>Kogutulu:</b> %{y:,.0f} €<extra></extra>' # Rounded to 0 decimal places
        )
    )

    fig.update_layout(
        title_x=0.5,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="sans-serif", color="#1A1A2E"),
        separators=' .', # Space for thousands, period for decimals
        xaxis=dict(
            title="Nädal", # X-axis title
            showgrid=False,
            tickangle=45 # 45-degree angle
        ),
        yaxis=dict(
            title="Kogutulu (€)",
            showgrid=False,
            tickformat='.0f', # Round to 0 decimal places
            tickprefix='€ '
        )
    )
    logger.info("Created weekly revenue chart using Plotly Express.")
    return fig

def create_kpi_summary(kpis):
    """
    Creates a Plotly table figure to display Key Performance Indicators (KPIs).

    Args:
        kpis (dict): Dictionary from transform.calculate_kpis containing:
                     'total_revenue', 'unique_customers', 'avg_order_value'.

    Returns:
        go.Figure: A Plotly graph object (table).
    """
    if not kpis:
        logger.warning("KPIs dictionary is empty, returning an empty Plotly figure.")
        fig = go.Figure()
        fig.update_layout(title_text="KPI kokkuvõte (andmed puuduvad)", title_x=0.5)
        return fig
        
    kpi_names = ["Kogutulu", "Unikaalsed kliendid", "Keskmine tellimuse väärtus"]
    
    # Format values according to requirements
    formatted_total_revenue = _format_eur_amount_str(kpis.get("total_revenue", 0.0))
    formatted_unique_customers = _format_number_str(kpis.get("unique_customers", 0))
    formatted_avg_order_value = _format_eur_amount_str(kpis.get("avg_order_value", 0.0))

    kpi_values = [formatted_total_revenue, formatted_unique_customers, formatted_avg_order_value]

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=[f"<b>{name}</b>" for name in kpi_names],
            fill_color='#009B8D',
            align='center',
            font=dict(color='white', size=12, family="sans-serif"),
            height=30
        ),
        cells=dict(
            values=[kpi_values],
            fill_color='white',
            align='center',
            font=dict(color='#1A1A2E', size=14, family="sans-serif"),
            height=30
        )
    )])

    fig.update_layout(
        title_text="Müügi KPI kokkuvõte",
        title_x=0.5,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="sans-serif", color="#1A1A2E")
    )
    logger.info("Created KPI summary chart.")
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
    logger.info("------------------------------------------")
