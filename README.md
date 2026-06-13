# DACA Portfolio -- Kristjan

## About This Repository

This repository contains my portfolio, which documents my 11-week journey through **the DACA program** - a **Junior Data Analyst mentorship program** organized by [Ettevõtluskeskus](https://www.ettevotluskeskus.ee/). The program started on March 23rd, and I graduated on June 10th, 2026. **DACA** stands for **D**ata **A**nalyst **C**areer **A**ccelerator. During the program, a fictional company named **UrbanStyle Ltd.** was used as a simulation.

## Why I Enrolled in the DACA Program

As a software developer, I frequently utilized **Object-Relational Mapping (ORM)** frameworks to interact with databases and execute queries from application code, translating **PostgreSQL** tables into **Ruby** or **Java** classes. I was also often tasked with writing SQL queries to generate reports in CSV and Excel formats, so I already had a quite solid foundation in working with data. In fact, I have always genuinely enjoyed working with databases and SQL.

Reflecting on my career as a developer, I've realized that I felt most fulfilled by analytical tasks. I loved delving into application code to troubleshoot problems and tracking down their root causes—sometimes digging into the core Ruby code itself.

Because of my background, the words **"data"** and **"analysis"** strongly resonate with me.

Although I was already quite comfortable with SQL, I knew there was still a lot to learn. Beyond databases, I had almost no experience with **Python**—and "data analysis" as a discipline was completely new territory for me. I decided to enroll in the DACA program to truly understand what data analysis entails, discover how SQL and Python are used in this context, gain hands-on experience with Python, and see how **AI** can be integrated into the data analysis workflow.

## What I Learned

During the program, I advanced my SQL skills by learning how to leverage **SQL (PostgreSQL)** specifically for data cleaning and transformation. To my surprise, despite my prior database experience, I discovered powerful features I hadn't used before, such as **CTEs (Common Table Expressions)** and **window functions**.

I also visualized data using **Plotly charts** on **Streamlit dashboards** built with Python. Additionally, I used Python and the **Pandas** library to perform an **RFM analysis**. To integrate data fetching, cleaning, aggregation, and visualization into a seamless workflow, I built an **automated ETL pipeline**, leveraging Python once again. Most importantly, I gained hands-on experience in drawing **business conclusions** based on transformed and visualized data. Throughout the program, I utilized AI extensively to solve problems more efficiently.

## Portfolio

Each week the program concentrated on a different topic. The work done during each week ended up as a documented weekly **project**. The weekly projects together form a **portfolio** and are located in [portfolio](./portfolio) directory. Here's a brief overview of the projects.

### [Onboarding](./portfolio/week-00)
**Week 0** | 23 Mar 2026 - 29 Mar 2026 | **Completed** ✅

Setting up software (VS Code, Python & packages) and services (GitHub repository, Supabase, NotebookLM) needed for work. Importing data into Supabase, using CSV files.

---

### [SQL Basics](./portfolio/week-01)
**Week 1** | 30 Mar 2026 - 05 Apr 2026 | **Completed** ✅

Reading data (`SELECT`), filtering (`WHERE`, `AND`, `OR`), sorting (`ORDER BY`), limiting the number of rows (`LIMIT`), `NULL` keyword, counting(`count(*)`, `count(column_name)`, `count(DISTINCT column_name)`). Exploring `sales` table (**15,234** rows x **12** columns).

---

### [SQL Cleaning](./portfolio/week-02)
**Week 2** | 06 Apr 2026 - 12 Apr 2026 | **Completed** ✅

Detecting duplicate values using `GROUP BY` + `HAVING` and duplicate rows using `row_number()`. Using `trim()`, `lower()`, `initcap()` to unify different forms of text values (e.g. out of **54** distinct forms in `customers.city` column, it was discovered that there were only **12** unique cities). 

Creating a copy from a table (e.g. `customers_test` based on `customers`) to perform `UPDATE` and `DELETE` safely without modifying original data, since SQL write operations are irreversible. Using `UPDATE` to sanitize data and `DELETE` to remove duplicates. Writing a markdown report about data cleaning process and its results.

---

### [SQL JOINs](./portfolio/week-03)
**Week 3** | 13 Apr 2026 - 19 Apr 2026 | **Completed** ✅

Using `INNER JOIN`, `LEFT JOIN`, and occasionally `RIGHT JOIN` - to combine tables by matching primary and foreign keys. Joining `products` table with `sales` and `inventory` tables using `LEFT JOIN` in order to analyse products - including those without inventory and sales.

Noticed anomalies regarding product quantities in different inventory locations (e.g. a product has **9,850** items in Pärnu which is more than **260** times over reorder point (**37**), while in other cities the number of product items is only slightly above or even below the reorder point).

---

### [SQL Aggregation](./portfolio/week-04)
**Week 4** | 20 Apr 2026 - 26 Apr 2026 | **Completed** ✅

Using `GROUP BY` in conjunction with aggregate functions such as `count()`, `sum()` and `avg()`. Filtering aggregated rows using `HAVING`. Using **CTE**-s (**C**ommon **T**able **E**xpression) to make parts of SQL queries reusable (**DRY** principle - Don't Repeat Yourself) and more readable. Using **window functions** to append comparison values from other rows as separate columns to the result (e.g. `lag(s.total_revenue) OVER (ORDER BY s.month_start ASC) AS previous_month_total_revenue`).

Making use of the newly acquired SQL tools to analyze marketing channels of customers (`web_logs` table with **50,000** rows) to find out that values in `source` column needed unification, just like customer city names in Week 2. After unification, **Facebook Ads** was found to be the most effective marketing channel with **€944** as average revenue per customer.

---

### [Visualization - Design](./portfolio/week-05)
**Week 5** | 27 Apr 2026 - 03 May 2026 | **Completed** ✅

Had to choose a Data Visualization toolkit: **Track A (Power BI)** vs **Track B (Plotly + Streamlit)**. My choice: **Track B**. Reasons: 1) Power BI requires Windows, but I'm Ubuntu Linux user 2) heavily influenced by my software development background 3) eager to get hands-on experience with Python.

Built a **Streamlit dashboard** featuring KPI metrics at the top with total revenue, number of customers and their deltas compared to previous date range - equal in length to the selected date range. Below the KPI cards, a **Plotly Express** line chart visualizing monthly (or weekly or daily, depending on the length of selected date range) trend of total revenue. To the bottom of the dashboard, added the date range selection filter, discussed earlier, making the dashboard **interactive**. Leveraged AI to learn Python and troubleshoot issues.

---

### [Visualization - Data](./portfolio/week-06)
**Week 6** | 04 May 2026 - 10 May 2026 | **Completed** ✅

Built another **Streamlit dashboard** following the layout principles familiar from Week 5 (KPIs at the top below the title, main trendline chart below the KPIs, secondary charts below the trendline and filters at the bottom). Deployed the Streamlit dashboard app to **Streamlit Community Cloud**. The dashboard is accessible [via this link](https://daca-portfolio-3hkfvtlw9ikvnhidkd5cw3.streamlit.app/) (might be in sleep mode due to inactivity, but could be woken up). Annotated months (or weeks or days when shorter date ranges selected) with minimum and maximum revenue and biggest revenue decrease.

By selecting year **2024** as default date range and **Tartu** as default store location, used the **annotations** to support **data storytelling**. Filters at the bottom of the dashboard allow to explore other date ranges and store locations, making the dashboard **interactive**.

---

### [Python - Pandas](./portfolio/week-07)
**Week 7** | 11 May 2026 - 17 May 2026 | **Completed** ✅

In weeks 5–6, I discovered certain technical limitations in the Python **Supabase** library, such as its apparent lack of support for `GROUP BY`. To gain more flexibility, I initially switched to **SQLAlchemy** to query Supabase using pure SQL. However, since this week's objective was to demonstrate data aggregations using Python **Pandas**, I chose to continue using the Supabase library for learning purposes, despite recognizing **potential scalability issues with tables containing tens of millions of rows**.

Used **Pandas** to perform **RFM Analysis** (**R**ecency **F**requency **M**onetary) on aggregated sales data grouped by customer, using **28 Feb 2025** as a **reference date** for the analysis, because later data contained anomalies and was incomplete. Used the reference date to filter out all later purchases from the Pandas DataFrame given as input before starting with analysis. Based on the **RFM scores** as analysis result, distributed customers into **5 segments**, out of which the most valuable segment (RFM score: **13-15**) - **VIP Champions** - contained **453** customers. The revenue generated by the **VIP Champions** was **43%** out of the total revenue generated by all customers until the reference date.

Used **Jupyter Lab** to execute the Python code stored in **IPython Notebook (.ipynb file)**.

---

### [Python - APIs](./portfolio/week-08)
**Week 8** | 18 May 2026 - 24 May 2026 | **Completed** ✅

Built an automated **ETL Pipeline** using Python to orchestrate data extraction (**E**) from data source (Supabase), data transformation (**T**) for data cleaning, aggregations and calculations, and finally, data loading (**L**) to save the transformed Pandas DataFrames as CSV and Plotly charts - visualizations of the transformed Pandas DataFrames - as HTML files. The pipeline logs the beginning and end of each stage and measures the total execution time which it also logs. Various test runs of the pipeline demonstrated that it usually takes **3-4 seconds** to execute the pipeline. According to the DACA program manual, it used to take **4h / week** to manually perform the tasks which are now automated using the ETL Pipeline.

The pipeline receives **start date** and **end date** as arguments. The arguments are used in **E** stage to set filters on `sale_date` when querying Supabase via its API client implementation in Python.

Demonstrated that the ETL Pipeline can be configured to launch automatically and periodically, using Linux `crontab`. For that purpose, wrote a wrapper shell script.

Discovered **Aider** - an AI pair-programming tool with direct access to local codebase. Gave the Python file paths and typed in instructions after which the AI model made the requested changes in the Python files. My task was to validate and make necessary adjustments.

---

### [Career Preparation](./portfolio/week-09)
**Week 9** | 25 May 2026 - 31 May 2026 | **Completed** ✅

Composed a peer review about a teammate, from Hiring Manager perspective. The peer review was written based on the teammate's DACA portfolio in GitHub. **NotebookLM** helped greatly with that task due to its ability to compose a summary based on input documents.

Started reorganizing files in my own DACA portfolio. Used **Aider** to automate that task. Wrote a [shell script](./bin/aider.sh) which can launch Aider with often-used parameters, including path of the file with [global instructions for the AI model](./config/development/ai_global_instructions.md) used with Aider. The model name and API key are assumed to be defined in the `.env` file which is not part of this repository due to security reasons.

---

### [Portfolio Defense](./portfolio/week-10)
**Week 10** | 01 Jun 2026 - 10 Jun 2026 | **Completed** ✅

Talked about **automatization via ETL Pipeline** during team presentation.

Finished reorganizing files in the current repository. Translated all individual markdowns, SQL files and Python scripts into English. Leveraged AI to automate that. With the help of **Aider + Gemini 3.5 Flash**, fixed some bugs and added improvements to my Week 5-6 dashboards.

## After the official end of the program

* Updating this README.
* Built Vercel page with the help of Aider + Gemini 3.5 Flash.
* Translating Week 8 ETL Pipeline outputs.
* Adding/updating screenshots.
