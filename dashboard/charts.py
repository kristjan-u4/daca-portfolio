"""
UrbanStyle Dashboard — Diagrammide Loomine
============================================
Kolm põhidiagrammi: müügitrend, top tooted, müük linnade kaupa.
"""

import pandas as pd
import plotly.express as px

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
        annotation_text=f"Keskmine: €{avg_revenue:,.0f}".replace(",", " "),
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
        title=f"Top {top_n} toodet müügitulu järgi",
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
        title_font_size=20,
        showlegend=False,
        xaxis_tickformat=",.0f",
        xaxis_tickprefix="€",
        coloraxis_showscale=False
    )
 
    return fig