"""
UrbanStyle Dashboard — Chart Creation
=====================================
Three main charts: revenue trend, top products, sales by customer city.
"""

import pandas as pd
import plotly.express as px
import utils

INTERVAL_CONFIGS = {
    "day": {
        "label": "Date",
        "tickformat": "%d %b %Y",
        "format_fn": utils.format_date
    },
    "week": {
        "label": "Week Starting",
        "tickformat": "%d %b %Y",
        "format_fn": utils.format_date
    },
    "month": {
        "label": "Month",
        "tickformat": "%b %Y",
        "format_fn": utils.format_date_as_text
    }
}

def create_revenue_trend(data, filters):
    """
    Create a line chart showing revenue trend based on the selected interval.

    Args:
        data (dict): Dictionary containing aggregated sales data.
        filters (dict): Active filter settings containing the interval.

    Returns:
        plotly.graph_objects.Figure: The generated line chart figure.
    """
    df = data["aggregated_sales"]
    store_location_comparison_df = data["comparison_store_location_aggregated_sales"]
    df["total_revenue_delta"] = df["total_revenue"].pct_change()
 
    interval = filters["interval"]
    config = INTERVAL_CONFIGS[interval]

    # Step 1: Create line chart
    fig = px.line(
        df,
        x="interval_start",
        y="total_revenue",
        title="Total Revenue Trend",
        labels={
            "interval_start": config["label"],
            "total_revenue": "Revenue (EUR)"
        }
    )

    # X-axis settings
    fig.update_xaxes(
        title_text=None,
        tickformat=config["tickformat"],
        dtick=None,
        tickfont_size=12,
        tickfont_color="#1A1A2E"
    )

    # Y-axis settings
    fig.update_yaxes(
        title_text=None,
        tickfont_size=12,
        tickfont_color="#1A1A2E"
    )

    if not df.empty:
        max_row = df.loc[df["total_revenue"].idxmax()]
        format_fn = config["format_fn"]

        # Annotation for month with maximum total revenue.
        fig.add_annotation(
            x=max_row["interval_start"],
            y=max_row["total_revenue"],
            text=f"Max: {utils.format_eur_amount(max_row['total_revenue'])} ({format_fn(max_row['interval_start'])})",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-40,
            bgcolor="#009B8D",
            font=dict(color="white")
        )

        min_row = df.loc[df["total_revenue"].idxmin()]

        # Annotation for month with minimum total revenue.
        fig.add_annotation(
            x=min_row["interval_start"],
            y=min_row["total_revenue"],
            text=f"Min: {utils.format_eur_amount(min_row['total_revenue'])} ({format_fn(min_row['interval_start'])})",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=40,
            bgcolor="#009B8D",
            font=dict(color="white")
        )

        biggest_drop_row = df.loc[df["total_revenue_delta"].idxmin()]

        # Annotation for month with biggest drop in revenue.
        fig.add_annotation(
            x=biggest_drop_row["interval_start"],
            y=biggest_drop_row["total_revenue"],
            text=f"Biggest Drop: {utils.format_as_percentage(biggest_drop_row['total_revenue_delta'])} ({format_fn(biggest_drop_row['interval_start'])})",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=40,
            bgcolor="#009B8D",
            font=dict(color="white")
        )
 
    # Step 2: Customize appearance
    fig.update_layout(
        font_family="Arial",
        title_font_size=16,
        title_font_color="#1A1A2E",
        hovermode="x unified",
        yaxis_tickformat=",.0f",
        yaxis_tickprefix="€",
        separators=".,"
    )

    # Step 3: Change line color and width
    fig.update_traces(line_color="#009B8D", line_width=3)
 
    # Step 4: Add horizontal line for average revenue
    avg_revenue = df["total_revenue"].mean()
    fig.add_hline(
        y=avg_revenue,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Average: {utils.format_eur_amount(avg_revenue)}",
        annotation_position="top right"
    )
 
    return fig

def create_top_products(df, top_n=5):
    """
    Create a horizontal bar chart showing the top N products.

    Args:
        df (pd.DataFrame): DataFrame containing product sales data.
        top_n (int, optional): Number of top products to display. Defaults to 5.

    Returns:
        plotly.graph_objects.Figure: The generated bar chart figure.
    """
    product_revenue = df.head(top_n)
 
    # Create chart
    fig = px.bar(
        product_revenue,
        x="total_revenue",
        y="product_name",
        orientation="h",
        title=f"Top {top_n} Products",
        text="total_revenue",
        labels={
            "total_revenue": "Total Sales (€)",
            "product_name": "Product"
        },
        color="total_revenue",
        color_continuous_scale="Teal"
    )

    # Step 1: Configure text formatting on bars
    fig.update_traces(
        texttemplate="€%{text:,.0f}",
        textposition="inside",
        hovertemplate="<b>%{y}</b><br>Total Sales: €%{x:,.0f}<extra></extra>"
    )
 
    # Adjust appearance
    fig.update_layout(
        font_family="Arial",
        title_font_size=16,
        showlegend=False,
        xaxis_tickformat=",.0f",
        xaxis_tickprefix="€",
        coloraxis_showscale=False,
        separators=".,",
        yaxis={"categoryorder": "total ascending"}
    )
 
    return fig

def create_sales_by_customer_city(df):
    """
    Create a pie chart of total revenue by customer city.

    Args:
        df (pd.DataFrame): DataFrame containing sales data by city.

    Returns:
        plotly.graph_objects.Figure: The generated pie chart figure.
    """
    # First n cities will be displayed separately
    main_cities = _compress_cites_data_for_pie_chart(df, 5)
 
    # Step 3: Create pie chart
    fig = px.pie(
        main_cities,
        values="total_revenue",
        names="city",
        title="Revenue Distribution by Customer City",
        color_discrete_sequence=px.colors.sequential.Teal_r
    )
 
    # Step 4: Customize appearance
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>"
                      "Revenue: €%{value:,.0f}<br>"
                      "Share: %{percent}<extra></extra>"
    )
 
    fig.update_layout(
        font_family="Arial",
        title_font_size=16,
        separators=".,"
    )
 
    return fig

def _compress_cites_data_for_pie_chart(df, number_of_sectors):
    """
    Compress city sales data to group smaller cities into an 'Other cities' category.

    Args:
        df (pd.DataFrame): DataFrame containing sales data by city.
        number_of_sectors (int): Maximum number of sectors to display.

    Returns:
        pd.DataFrame: Compressed DataFrame.
    """
    if len(df) <= number_of_sectors:
        return df
    
    n = number_of_sectors - 1

    # First n cities will be displayed separately
    result = df.iloc[:n]

    # Remaining cities will be grouped together and represented as others
    other_cities = df.iloc[n:]
    other_total = other_cities["total_revenue"].sum()

    other_row = pd.DataFrame({
        "city": ["Other cities"],
        "total_revenue": [other_total]
    })
    result = pd.concat([result, other_row], ignore_index=True)

    return result
