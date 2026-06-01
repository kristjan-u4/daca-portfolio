# Week 6: Visualization Data

## Project Overview

This week, the focus was on data refinement and Data Storytelling. I concentrated on the tasks of **Role B (Tartu Store)** in the group work, aiming to analyze the sales dynamics of the Tartu store, uncover the reasons behind trends, and provide strategic recommendations to management.

**Key Finding:** Although the initial hypothesis pointed to a possible general downward trend, my analysis revealed a **13% revenue growth** in 2024 compared to 2023. However, during the analysis, critical seasonal anomalies emerged, such as an unexpected 36% decline in September, and a surprising customer profile – the largest proportion of Tartu store customers are actually shoppers from Tallinn.

**Technical Enhancements (Track B):**
*   **Interactivity:** I enhanced the **Streamlit** dashboard with a store location filter (`store_location`), setting its default value to Tartu. I also set the date range filter's default value to 2024, while maintaining full dashboard interactivity for viewing other periods and locations.
*   **Visualization:** I added annotations and a reference line to the line chart characterizing sales trends, which help explain movements in the data (e.g., Christmas sales peak and September decline) and transform raw numbers into a manageable narrative.
*   **Data Aggregation:** I added a bar chart to visualize the sales of the most popular products and a pie chart to represent the geographical distribution of customers, which support the specific data story of the Tartu store.

## Dashboard
Location: https://daca-portfolio-3hkfvtlw9ikvnhidkd5cw3.streamlit.app/

Preview:

![Tartu store dashboard](./individual/week6_tartu_dashboard_screenshot.png)
*Note: The dashboard includes interactive filters.*

## Use of AI

### Google Gemini

* I asked for help in dynamically constructing the `sales.store_location` SQL filter in Python code according to user-defined filters.
* AI explained how to unify number formats on the Streamlit dashboard and where to make the necessary changes.
* I asked how to add annotations to the line chart at the minimum and maximum points and used the code examples provided in the answer.
* I asked how to find the month with the largest percentage drop from the line chart data to display it as an annotation, and AI provided code examples.
* When I deployed my Streamlit application to the **Streamlit Community Cloud** environment, I encountered issues getting the Supabase database connection to work. AI advised me to use a Transaction Pooler URL and guided me on how to find it in the Supabase user interface. After following AI's instructions, the errors disappeared.

### NotebookLM

* By providing my group work role (Role B - Tartu), a description of the data to be displayed on the dashboard, and my own recommendations for drawing conclusions from the sharp decline in September 2024, I asked AI to compile an executive summary and data story in markdown format.
* AI guided me on where to place the executive summary and data story on the dashboard.

## Technical Implementation

*   **Data Source:** PostgreSQL (Supabase) – data filtering occurred on the server side (`sales.store_location = 'Tartu'`).
*   **Tools:** Python, Pandas, Plotly Express, Streamlit, SQLAlchemy.
*   **Design:** Applied **Knaflic's "Storytelling with Data"** principles: added annotations (`fig.add_annotation`) and a reference line (`fig.add_hline`).

## How to Run the Application (Ubuntu Linux example)

1.  Ensure Python is installed.
2.  Navigate to the root directory of this repository and create a Python virtual environment: `python -m venv .venv` (if `python` doesn't work, try `python3`).
3.  Activate the Python virtual environment: `source .venv/bin/activate`.
4.  Required libraries are listed in the **requirements.txt** file. Install them: `pip install -r requirements.txt`.
5.  Set up the database connection. Create a `.env` file and add: `SUPABASE_CONNECTION_STRING=[direct_connection_string_of_your_database_in_supabase]`. You can find the appropriate value in your Supabase database settings.
6.  Run the application from the terminal: `streamlit run portfolio/week-06/individual/dashboard/app.py`.

## Links
*   **Local Streamlit Application:** [app.py](./individual/dashboard/app.py)
*   **Streamlit Application deployed to Streamlit Community Cloud:** https://daca-portfolio-3hkfvtlw9ikvnhidkd5cw3.streamlit.app/
*   **Executive Summary**: see [week6_executive_summary.md](./individual/week6_executive_summary.md)
*   **Data Story**: see [week6_tartu_narrative.md](./individual/week6_tartu_narrative.md)
*   **Team Consolidated View:** [week6_team_combined_view.md](./team/week6_team_combined_view.md)
