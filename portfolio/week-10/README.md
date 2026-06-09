# Week 10: Portfolio Defense

## My Role

During the final week of the DACA program, our team's task was to prepare a 7-minute presentation for the UrbanStyle board meeting. My responsibility was to present the **automation achieved through the ETL pipeline** that the team built using Python in [Week 8](../week-08/README.md).

In my presentation, I described how manual data processing and the lack of real-time insights were key business problems for UrbanStyle, which drove the team to build an automated ETL pipeline. I highlighted that while manual data processing previously consumed 4 hours of valuable time from the UrbanStyle team every week, the automated ETL pipeline now **saves the company 200 hours of manual labor per year**. As my biggest takeaway, I noted that the ETL pipeline can accept dynamic arguments, such as specific sales date ranges.

## AI Usage

In addition to the presentation, I worked on polishing the individual components of this portfolio. The most extensive task was translating the portfolio into English.

### Aider

This week I discovered that there's a lot newer Gemini model that can be used with Aider: **Gemini 3.5 Flash**. Using a wider choice of models also helped me to work around rate-limit issues, since each Gemini model appears to have its own capacity. By using `.env`, I can easily switch between Gemini models by commenting out those that I'm not currently using:

```bash
#DEVELOPMENT_AI_MODEL=gemini/gemini-2.5-flash
DEVELOPMENT_AI_MODEL=gemini/gemini-3.5-flash
```
After the changes in `.env` I would only have to restart Aider.

Aider helped me with the following:

* Translating Python comments.
* Making Python style corrections based on the [provided global instructions](../../config/development/ai_global_instructions.md).
* Fixing a few bugs in Streamlit dashboards:
  * Store location filter in Week 6 Dashboard will no longer reset when changing date filter.
  * Week 6 Dashboard no longer crashes when selecting only 1-day-long date range.
* Adding **Dynamic Aggregation** to Total Revenue Trend chart: sales data is aggregated using either daily, weekly or monthly precision, depending on the selected date range.

### Google Gemini Chatbot

Due to Aider's AI model rate and context limits, I also utilized the Gemini chatbot interface to assist with translating markdown files, SQL scripts, and Jupyter notebook content. Gemini Chatbot also explained the differences between Aider's **/editor** and **/architect** modes and which one to choose for a particular task.
