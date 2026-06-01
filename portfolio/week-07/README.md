# Week 7: Python Pandas — RFM Customer Segmentation

## My Role

### Role C: Analysis — RFM Customer Segmentation

*   I analyzed sales data cleaned by Role B up to the **reference date of 28.02.2025**.
*   Using Pandas' `qcut()` method, I calculated 3 metrics for each customer, with a value of **a score on a scale of 1-5**:
    *   **Recency (R)** characterizes the time elapsed since the most recent purchase.
        *   Underlying metric: the difference between the reference date and the last purchase date.
        *   The shorter the time, the higher the score.
    *   **Frequency (F)** characterizes the frequency of purchases.
        *   Underlying metric: the number of orders per customer.
        *   The higher the number of purchases, the higher the score.
    *   **Monetary (M)** characterizes the monetary value of purchases.
        *   Underlying metric: the total amount of purchases in euros per customer.
        *   The higher the total amount, the higher the score.
*   I summed the R, F, and M metrics and thereby found the **RFM score** for each customer, based on which I divided customers into segments:
    *   **VIP Champions:** score 13-15, total **453** customers
    *   **Loyal:** score 10-12, total **677** customers
    *   **Potential:** score 7-9, total **768** customers
    *   **At Risk:** score 4-6, total **525** customers
    *   **Lost:** score 3, total **117** customers
*   I passed the customer RFM scores and segments as input to Role D for data visualization.

## Key Findings

*   The most numerous segment is potential customers - 768 clients. This is UrbanStyle's most important growth engine and "raw material".
*   There are more loyal customers (677 clients) than at-risk customers (525 clients). This indicates that UrbanStyle's customer base is currently healthy and the brand's focus is correct.
*   There are more at-risk customers than VIP customers (453 clients). This is a warning sign, indicating that we are losing valuable customers faster than we can grow them to the top (VIP status).

## Use of AI

### Google Gemini

*   The learning guide showed how R, F, and M source data are grouped separately by customer and finally merged, but I hypothesized that all this could be done with a single method (agg).
    I asked the AI if my methodology yielded the same result as that presented in the learning material. The AI responded that it did and that my method was also more readable and faster in terms of performance.
*   It taught how to dynamically generate a list of scores for F and M metrics when `q=5` in the `qcut()` parameter, and how to generate a reversed list for the R metric from the generated list.
*   I encountered an error when calculating the F-score: `ValueError: Bin edges must be unique: Index([1.0, 2.0, 2.0, 3.0, 5.0, 77.0], dtype='float64', name='total_purchases')`. I asked the AI what caused this and how to solve the problem.
    The AI replied that this error occurs when there are **too many duplicate values** in the data and recommended using `.rank(method='first')`. The AI's suggested code enhancement removed the error.

### NotebookLM

*   Assisted in formulating business interpretations by comparing the main given customer segments based on my observations.

## Technical Implementation

*   **Data Source:** PostgreSQL (Supabase).
*   **Tools:** Python, Pandas, SQLAlchemy, Supabase, Plotly Express, Jupyter Lab.
*   **Methods:** `groupby`, `agg`, `qcut`, `rank`.

## How to Run the .ipynb Notebook (Ubuntu Linux example)

1.  Ensure Python is installed.
2.  Navigate to the root directory of this repository and create a Python virtual environment: `python -m venv .venv` (if `python` doesn't work, try `python3`).
3.  Activate the Python virtual environment: `source .venv/bin/activate`.
4.  Required libraries are listed in the **requirements.txt** file. Install them: `pip install -r requirements.txt`.
5.  Set up the database connection using the `.env` file. If a Supabase connection error occurs in step 7, revisit this point.
6.  Launch **Jupyter Lab** from the terminal: `jupyter lab`. Jupyter Lab is a more modern evolution of Jupyter Notebook.
7.  In the Jupyter Lab environment, select the desired .ipynb file from the week-07 subdirectories of the project and click **Restart the kernel and run all cells**.

## Links

*   **Team .ipynb notebook:** [week7_rfm_complete.ipynb](./team/week7_rfm_complete.ipynb)
*   **Individual .ipynb notebook**, where I also simulated other roles, which allowed me to work on my subtask simultaneously with other team members: [individual/week7_rfm_role_c.ipynb](./individual/week7_rfm_role_c.ipynb)
