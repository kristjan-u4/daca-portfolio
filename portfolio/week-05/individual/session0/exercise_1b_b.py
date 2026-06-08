import plotly.express as px
import pandas as pd


def main():
    """
    Generates and displays a bar chart showing the top 5 products by revenue.
    """
    data = {
        "Product": [
            "Denim Jacket",
            "Urban Sneakers",
            "Hoodie Classic",
            "Street Tee",
            "Canvas Bag"
        ],
        "Revenue (€)": [45000, 35000, 28000, 21000, 16000]
    }

    df = pd.DataFrame(data)

    fig = px.bar(
        df,
        x="Product",
        y="Revenue (€)",
        title="TOP 5 Products by Revenue",
        text_auto=".s",
        color="Revenue (€)",
        color_continuous_scale="Viridis"
    )

    fig.show()


if __name__ == "__main__":
    main()
