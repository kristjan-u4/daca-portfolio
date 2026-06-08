"""
UrbanStyle Dashboard — Chart Creation
"""

import plotly.express as px

def create_revenue_trend(df):
    """
    Creates a line chart displaying the monthly revenue trend for UrbanStyle.

    Args:
        df (pd.DataFrame): Aggregated data containing "interval_start" (month)
                           and "total_revenue" columns.

    Returns:
        plotly.graph_objects.Figure: A Plotly line chart figure.
    """
    fig = px.line(
        df,
        x="interval_start",
        y="total_revenue",
        title="UrbanStyle Revenue Trend",
        labels={
            "interval_start": "Month",
            "total_revenue": "Revenue (EUR)"
        }
    )

    fig.update_xaxes(
        title_text=None,
        tickformat="%b %Y",
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
        separators=", "
    )

    fig.update_traces(line_color="#009B8D", line_width=3)

    avg_revenue = df["total_revenue"].mean()
    fig.add_hline(
        y=avg_revenue,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Average: €{avg_revenue:,.0f}".replace(",", " "),
        annotation_position="top right"
    )

    return fig
