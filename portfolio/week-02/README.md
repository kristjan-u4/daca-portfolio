# Week 2: SQL Data Cleaning (UrbanStyle.ltd)

## Overview
This week, I focused on cleaning UrbanStyle's database to prepare the data for the upcoming board meeting. My role was **Customer Data Cleaner (Role B)**, where my task was to analyze and organize the `customers` table.

## Work Done
I worked according to Toomas Kask's guidelines using the "Test, Verify, Log, Commit" methodology:
1.  **Test Environment Creation:** I made a copy of the `customers` table, `customers_test`, to ensure safe data processing.
2.  **Diagnostics:** I identified duplicate emails, missing customer names, and inconsistent city names.
3.  **Cleaning (Advanced Level):** I standardized city names (`INITCAP`, `TRIM`), normalized emails, and filled in missing name fields with the value 'Unknown'.

## Key Findings
*   **Most Critical Finding:** Missing emails, as this prevents UrbanStyle from communicating with its customers and sending them campaign offers. Also, for anonymous customers, it is unclear how many of them are the same and how many are different people, leading to a distorted picture of customer count.
*   **Data Condition:** The customer base is largely correct but requires better validation at the input stage, especially for emails and locations.
*   **Recommendation:** Implement mandatory email field completion upon registration to prevent the creation of anonymous entries. When entering city names, use a dropdown menu instead of a text field to prevent different name forms from being saved in the database.

## Files in Portfolio
*   [SQL Cleaning Script](./individual/week2_customers_cleaning.sql)
*   [Individual Cleaning Report](./individual/week2_customers_report.md)
*   [Team Consolidated Report](./team/week2_team_cleaning_report.md)

## Self-Reflection (Shu-Phase)
This week, I precisely followed the given instructions. I learned the importance of using transactions or test copies before modifying data. The biggest challenge was correctly counting duplicates in a normalized form.
