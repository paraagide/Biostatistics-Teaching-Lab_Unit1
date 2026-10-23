# Biostatistics Teaching Laboratory — Unit 1

A beginner-friendly Streamlit application for teaching descriptive statistics using the supplied 10,000-record Excel dataset.

## Features
- Load the bundled Excel dataset or upload Excel/CSV.
- Preview records, column types and missing values.
- Select a numerical variable and calculate mean, median, mode, min, max, range, quartiles, IQR, variance, SD and skewness.
- Switch between sample variance/SD (n−1) and population variance/SD (n).
- Plot histograms and show mean/median reference lines.
- Create grouped or ungrouped frequency tables with frequency, relative frequency, percentage and cumulative frequency.
- Download the current summary or frequency table as CSV.

## Run locally on Windows

1. Install Python (a currently supported version recommended for Streamlit and its dependencies).
2. Extract the ZIP file to a folder, for example `D:\Biostatistics_Teaching_Lab_Unit1`.
3. Open Command Prompt or PowerShell in that folder.
4. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt:
   ```bat
   .venv\Scripts\activate.bat
   ```

5. Install packages:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. Start the application:

   ```powershell
   streamlit run Home.py
   ```

Streamlit will display a local address, usually `http://localhost:8501`.

## Publish for students using Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload `Home.py`, the `pages` folder, `data` folder and `requirements.txt`.
3. Keep the dataset only if you have permission to share it and it contains no identifiable or confidential information.
4. In Streamlit Community Cloud, create an app from the repository and choose `Home.py` as the entry point.
5. Test the deployed app with students before sharing the link.

## Important notes
- This is an educational tool, not a clinical decision-support system.
- The included data's provenance and representativeness have not been independently verified.
- Pandas' quartile interpolation and skewness conventions are used. Other textbooks/software may use slightly different definitions.
- The exact mode for continuous measurements can be affected by rounding and may be less informative than a grouped modal interval.
- If you deploy publicly, consider removing the bundled dataset and requiring students to upload approved teaching data instead.


## Central Tendency module

The `03_Central_Tendency.py` page lets students choose a numeric variable, predict and check mean/median/mode, visualize mean and median on a histogram, examine the effect of adding one hypothetical extreme value, answer measure-selection questions, and download a summary CSV. The added value is hypothetical and does not modify the source data.


## Central Tendency Practice Lab

The `04_Central_Tendency_Lab.py` page provides a guided student workflow: choose a sample size from the bundled 10,000-record dataset, select a variable, classify the variable, generate a categorical or student-bounded numerical frequency distribution, select the suggested measure of central tendency, choose the corresponding equation, calculate an answer, and compare it with the app's grouped-data/categorical answer. Numerical grouped-data practice currently requires equal-width classes so the median and mode equations use a consistent class width. The suggested mean-versus-median rule is an instructional heuristic, not a universal statistical rule.


### Latest Central Tendency Practice Lab updates

- Students can enter any whole-number sample size from 1 to the number of non-missing records for their selected variable; there is no preset minimum of 25. Samples are drawn without replacement from rows where the selected variable is present.
- The frequency distribution is visualised before the student selects a central-tendency measure: numerical grouped distributions use a histogram, and categorical distributions use a bar graph.
- If a student changes the variable or sample size after generating a sample, the page asks them to regenerate the sample before continuing, preventing stale settings from being used.

## Measures of Dispersion Practice Lab

The `05_Measures_of_Dispersion.py` page allows students to choose a numeric variable and any sample size from 1 to the number of non-missing observations, then explore range, quartiles, IQR, mean absolute deviation, variance, standard deviation and coefficient of variation. It includes a histogram, answer-checking for range/IQR/sample SD, a hypothetical added-value activity, and a comparison of sample SD with population σ. A repeated-sampling experiment plots mean absolute estimation error across increasing sample sizes; it does not compare alternative variance denominators.


## Population parameter comparisons
The Central Tendency Practice Lab compares raw-sample mean/median/mode with parameters calculated from all usable records in the bundled dataset and plots mean/median estimates over increasing sample sizes. The Measures of Dispersion Lab compares sample SD with population σ and uses repeated random samples at progressively larger sample sizes to show how the typical absolute estimation error changes. These are teaching demonstrations: a single estimate need not get closer at every increase in sample size, but larger samples generally provide more stable estimates and lower typical sampling error.


## Unit 1 Study Material: Questions and Answers

The page `06_Study_Material_Questions_Answers.py` provides progressive Q&A study material covering statistics and biostatistics, variables and measurement scales, data types and sources, pharmaceutical/health data examples, descriptive and inferential statistics, frequency distributions and graphs, grouped versus ungrouped data, central tendency, dispersion, worked examples, and a short self-check quiz.
