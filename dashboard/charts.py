"""
UrbanStyle Dashboard — Diagrammide Loomine
============================================
Kolm põhidiagrammi: müügitrend, top tooted, müük linnade kaupa.
"""

import pandas as pd
import plotly.express as px
import utils

def create_revenue_trend(df):
    """
    Joondiagramm: igakuine müügitulu.
    Näitab UrbanStyle müügitrendi ajas.
    """
 
    # Samm 1: Loo joondiagramm
    fig = px.line(
        df, # agregeeritud andmed
        x="interval_start", # x-telg: Kuu
        y="total_revenue", # y-telg: müügitulu
        title="UrbanStyle müügitulu trend", # diagrammi pealkiri
        labels={ # telgede sildid
            "interval_start": "Kuu",
            "total_revenue": "Müügitulu (EUR)"
        }
    )

    # X-telje seaded.
    fig.update_xaxes(
        title_text=None,
        tickformat="%b %Y",
        dtick=None, # punktide intervall (nt."M1" tähendab 1 kuu)
        tickfont_size=12,
        tickfont_color="#1A1A2E"
    )

    # Y-telje seaded.
    fig.update_yaxes(
        title_text=None,
        tickfont_size=12,
        tickfont_color="#1A1A2E"
    )

    if not df.empty:
        max_row = df.loc[df['total_revenue'].idxmax()]

        # Annotation for month with maximum total revenue.
        fig.add_annotation(
            x=max_row["interval_start"],
            y=max_row["total_revenue"],
            text=f"MAX: {utils.format_eur_amount(max_row['total_revenue'])} ({utils.format_date_as_text(max_row["interval_start"])})",
            showarrow=True,
            arrowhead=2,
            ax=0, # Arrow rotation
            ay=-40, # Text is above the arrow
            bgcolor="#009B8D",
            font=dict(color="white")
        )

        min_row = df.loc[df['total_revenue'].idxmin()]

        # Annotation for month with minimum total revenue.
        fig.add_annotation(
            x=min_row["interval_start"],
            y=min_row["total_revenue"],
            text=f"MIN: {utils.format_eur_amount(min_row['total_revenue'])} ({utils.format_date_as_text(min_row["interval_start"])})",
            showarrow=True,
            arrowhead=2,
            ax=0, # Arrow rotation
            ay=40, # Text is below the arrow
            bgcolor="#009B8D",
            font=dict(color="white")
        )
 
    # Samm 2: Kohanda välimust
    fig.update_layout(
        font_family="Arial",         # font
        title_font_size=16,          # pealkirja suurus
        title_font_color="#1A1A2E", # pealkirja värv
        hovermode="x unified",       # hover näitab kõiki punkte samal x-väärtusel
        yaxis_tickformat=",.0f",     # y-telg: tuhandete eraldaja, 0 kohta peale koma
        yaxis_tickprefix="€",        # y-telg: euro sümbol ette
        separators=", "              # Kümnendkohad eraldatud komaga, tuhandelised tühikuga
    )

    # Samm 3: Muudame joone värvi ja  paksust
    fig.update_traces(line_color="#009B8D", line_width=3)
 
    # Samm 4: Lisa joon, mis näitab keskmist
    avg_revenue = df["total_revenue"].mean()
    fig.add_hline(
        y=avg_revenue,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Keskmine: {utils.format_eur_amount(avg_revenue)}",
        annotation_position="top right"
    )
 
    return fig

def create_top_products(df, top_n=5):
    """
    Horizontal bar chart - TOP N products.
    """
 
    product_revenue = df.head(top_n)
 
    # Create chart.
    fig = px.bar(
        product_revenue,
        x="total_revenue",
        y="product_name",
        orientation="h",
        title=f"Top {top_n} toodet",
        labels={
            "total_revenue": "Käive (€)",
            "product_name": "Toode"
        },
        color="total_revenue",
        color_continuous_scale="Teal"
    )
 
    # Adjust appearance.
    fig.update_layout(
        font_family="Arial",
        title_font_size=16,
        showlegend=False,
        xaxis_tickformat=",.0f",
        xaxis_tickprefix="€",
        coloraxis_showscale=False,
        separators=", "
    )
 
    return fig

def create_sales_by_customer_city(df):
    """
    Pie chart of total revenue by customer city.
    """

    # First n cities will be displayed separately:
    main_cities = _compress_cites_data_for_pie_chart(df, 5)
 
    # Samm 3: Loo sektordiagramm
    fig = px.pie(
        main_cities,
        values="total_revenue",
        names="city",
        title="Käibe jaotus klientide päritolulinnade kaupa",
        color_discrete_sequence=px.colors.sequential.Teal_r  # värviskeem
    )
 
    # Samm 4: Kohanda välimust
    fig.update_traces(
        textposition="inside",                         # tekst sektori sees
        textinfo="percent+label",                      # näita protsenti ja nime
        hovertemplate="<b>%{label}</b><br>"
                      "Käive: €%{value:,.0f}<br>"
                      "Osakaal: %{percent}<extra></extra>"
    )
 
    fig.update_layout(
        font_family="Arial",
        title_font_size=16,
        separators=", "
    )
 
    return fig

def _compress_cites_data_for_pie_chart(df, number_of_sectors):
    if len(df) <= number_of_sectors:
        return df
    
    n = number_of_sectors - 1

    # First n cities will be displayed separately:
    result = df.iloc[:n]

    # Remaining cities will be grouped together and represented as others:
    other_cities = df.iloc[n:]
    other_total = other_cities["total_revenue"].sum()

    other_row = pd.DataFrame({
        "city": ["Muud linnad"],
        "total_revenue": [other_total]
    })
    result = pd.concat([result, other_row], ignore_index=True)

    return result