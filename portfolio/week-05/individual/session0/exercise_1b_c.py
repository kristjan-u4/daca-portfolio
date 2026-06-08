import pandas as pd
import plotly.express as px


def main():
    """
    Generates and displays a pie chart showing sales distribution by location.
    """
    data = {
        "Location": ["Tallinn", "Online", "Tartu", "Pärnu"],
        "Share (%)": [42, 28, 18, 12]
    }

    df = pd.DataFrame(data)

    fig = px.pie(
        df,
        values="Share (%)",
        names="Location",
        title="Sales by Location",
        color_discrete_sequence=px.colors.sequential.RdBu,
        hole=0.3
    )

    fig.update_traces(textinfo="percent+label")
    fig.show()


if __name__ == "__main__":
    main()
