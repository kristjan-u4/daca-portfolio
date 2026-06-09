"""
UrbanStyle Dashboard — Chart Creation
"""

import plotly.express as px
import utils

INTERVAL_CONFIGS = {
    "day": {
        "label": "Day",
        "tickformat": "%d %b %Y",
        "hoverformat": "%d %b %Y"
    },
    "week": {
        "label": "Week Starting",
        "tickformat": "Week %W, %Y",
        "hoverformat": "%d %b %Y"
    },
    "month": {
        "label": "Month",
        "tickformat": "%b %Y",
        "hoverformat": "%b %Y"
    }
}

def create_revenue_trend(df, filters):
    """
    Creates a line chart displaying the revenue trend for UrbanStyle.

    Args:
        df (pd.DataFrame): Aggregated data containing "interval_start"
                           and "total_revenue" columns.
        filters (dict): Dictionary containing active filter values.

    Returns:
        plotly.graph_objects.Figure: A Plotly line chart figure.
    """
    interval = filters["interval"]
    config = INTERVAL_CONFIGS[interval]
    interval_label = config["label"]
    tick_format = config["tickformat"]

    fig = px.line(
        df,
        x="interval_start",
        y="total_revenue",
        title="UrbanStyle Revenue Trend",
        markers=True, # Visualize data points as bold dots on the chart.
        labels={
            "interval_start": interval_label,
            "total_revenue": "Revenue (EUR)"
        }
    )

    fig.update_xaxes(
        title_text=None,
        tickformat=tick_format,
        hoverformat=config["hoverformat"],
        dtick=None,
        tickfont_size=12,
        tickfont_color="#1A1A2E"
    )

    fig.update_yaxes(
        title_text=None,
        tickfont_size=12,
        tickfont_color="#1A1A2E"
    )

    fig.update_layout(
        font_family="Arial",
        title_font_size=16,
        title_font_color="#1A1A2E",
        hovermode="x unified",
        yaxis_tickformat=",.0f",
        yaxis_tickprefix="€",
        separators=".," # Thousands separator is comma, decimal separator is dot
    )

    fig.update_traces(
        line_color="#009B8D",
        line_width=3,
        xhoverformat=config["tickformat"],
        hovertemplate=f"{config['label']}=%{{x|{config['hoverformat']}}}<br>Revenue (EUR) = €%{{y:,.0f}}<extra></extra>"
    )

    avg_revenue = df["total_revenue"].mean()
    fig.add_hline(
        y=avg_revenue,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Average: {utils.format_eur_amount(avg_revenue, 0)}",
        annotation_position="top right"
    )

    return fig
