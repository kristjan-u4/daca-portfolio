import plotly.express as px
import pandas as pd


def main():
    """
    Generates and displays a bar chart showing monthly sales revenue for the first half-year.
    """
    data = {
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Sales (€)": [18500, 17200, 20100, 22300, 21800, 24500]
    }

    df = pd.DataFrame(data)

    fig = px.bar(
        df,
        x="Month",
        y="Sales (€)",
        title="Sales Revenue by Month (First Half-Year)",
        text_auto=".s",
        color="Sales (€)",
        color_continuous_scale="Viridis"
    )

    fig.show()


if __name__ == "__main__":
    main()
