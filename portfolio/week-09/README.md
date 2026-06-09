# Week 9: Career Preparation

## My Role

### Role A: Hiring Manager's Perspective (HR/Hiring Manager)

My task was to evaluate a teammate's (**Role B**) GitHub portfolio, paying attention to the following:

1.  Can the portfolio be converted into a strong CV?
2.  Is the portfolio representative enough to be highlighted on LinkedIn?
3.  Identify 3 strengths and 2 suggestions for improvement.
4.  Provide a hiring recommendation and justify it.

**Output:** [peer_review_hr_view.md](./individual/peer_review_hr_view.md)

## Use of AI

### NotebookLM

*   To better understand what the concepts of **portfolio** and **project** mean in the context of the DACA program and this repository, I addressed the question to the AI, providing the URL of this repository as a source. The answer I received was that the directories containing weekly work (e.g., the current, **week-9**) are projects, which collectively form the portfolio.
*   In addition to the weekly project directories, my repository has acquired a number of helper directories, such as `bin` and `config` in the last week, related to **Aider** setup. To distinguish project directories from helper directories, I see the need to create a `portfolio` directory to consolidate the project directories. AI confirmed that my idea was good and recommended that I carry out the planned activity.
*   To complete my group work task (peer review from an HR perspective), I collected the content of my teammate's week 0-8 project README files and the SQL queries, Python scripts, and Jupyter notebooks referenced therein from GitHub, to consolidate them into a single markdown file. I provided the AI with my teammate's GitHub repository URL and the aforementioned markdown file as sources, based on which the AI generated a peer review document in markdown format for me. It can be said that AI did 95% of the work. My part was to prepare the sources for the AI and perform quality control on the AI's output.

### Aider + Gemini 2.5 Flash

*   I continued familiarizing myself with **Aider**, the AI pair programming tool discovered last week. I used Aider to organize this repository. With Aider's help, I moved the weekly projects into the `portfolio` directory and prefixed the week number with `0` in the project names (e.g., `week-01` instead of `week-1`) to maintain natural chronological sorting when `week-10` arrives. Additionally, with the help of Aider + AI model, I corrected errors in Python code and Shell scripts that arose due to file transfers.
*   I added instructions for the Aider + AI model that apply across the entire repository: [config/development/ai_global_instructions.md](../../config/development/ai_global_instructions.md)
*   I added a Shell script with the necessary context (AI model name, default files to be read, instructions for the AI model) for conveniently launching Aider: [bin/aider.sh](../../bin/aider.sh)

### Google Gemini chatbot

*   When I initially tested using NotebookLM for peer review on my own repository, I provided NotebookLM with the GitHub URLs of the files I deemed necessary, each separately, to which NotebookLM responded with an error message: "_Your notebook's file upload limit is full_". I turned to Gemini, who advised me to consolidate all information into one markdown file, using XML tags to divide individual files into "pages". I followed the recommendation, which resolved the NotebookLM error.
*   Guided in writing the Aider startup script and composing the markdown file needed to instruct its AI model.

## Team Output

From the individual role outputs, the team synthesized a [recruitment guide](https://github.com/sillepragi/urbanstyle-marketing-data/blob/main/week_9/urbanstyle_da_recruitment_guide.md).
