"""
UrbanStyle Dashboard — Diagrammide Loomine
============================================
Kolm põhidiagrammi: müügitrend, top tooted, müük linnade kaupa.
"""

import pandas as pd
import plotly.express as px
import data_loader as db

def prepare_filters():
    """Valmista ette vaikefiltrid"""
    return {
        "time_from": db.fetch_earliest_sale_date(),
        "time_to": db.fetch_latest_sale_date(),
        "interval": "month"
    }

def prepare_data(filters):
    """Laadi ja ettevalmista andmed diagrammide jaoks."""

    return {
        "aggregated_sales": db.aggregate_sales_by_period(filters),
        "total_customers": db.count_unique_customers(filters)
    }

def create_revenue_trend(df):
    """
    Joondiagramm: igakuine müügitulu.
    Näitab UrbanStyle müügitrendi ajas.
    """
 
    # Samm 1: Loo joondiagramm
    fig = px.line(
        df, # agregeeritud andmed
        x="perioodi_algus",                    # x-telg: kuupäev
        y="käive",                             # y-telg: müügitulu
        title="UrbanStyle müügitulu trend" # diagrammi pealkiri
    )

    # X-telje seaded.
    fig.update_xaxes(
        title_text=None,
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
    avg_revenue = df["käive"].mean()
    fig.add_hline(
        y=avg_revenue,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Keskmine: €{avg_revenue:,.0f}".replace(",", " "),
        annotation_position="top right"
    )
 
    return fig