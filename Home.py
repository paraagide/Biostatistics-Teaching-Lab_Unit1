import streamlit as st

st.set_page_config(page_title="Biostatistics Teaching Lab", page_icon="📊", layout="wide")

st.title("📊 Biostatistics Teaching Laboratory")
st.subheader("Unit 1 — Descriptive Statistics")
st.markdown("""
Welcome to the interactive laboratory for **Applied Biostatistics and Data Analytics for Pharmaceutical Sciences**.

Use the navigation menu to explore:
- **Descriptive Statistics Lab:** inspect the dataset, calculate central tendency and dispersion, and examine skewness.
- **Frequency Distributions:** build frequency tables for categorical and numerical variables, including student-defined class intervals.
- **Central Tendency:** predict and check mean, median and mode; explore distributions and the effect of an extreme value.
- **Measures of Dispersion Practice Lab:** explore range, IQR, variance, standard deviation, coefficient of variation, and sample-to-population estimation error.
- **Unit 1 Study Material: Questions and Answers:** progressive Q&A notes, pharmaceutical examples, worked frequency-distribution and central-tendency problems, dispersion formulas, and a quick self-check quiz.

### Learning sequence
**Raw data → classify variables → frequency distribution → histogram → mean/median/mode → range/IQR/variance/SD → skewness → interpretation**

### Dataset
The bundled teaching file contains 10,000 records. You can use it as provided or upload another Excel/CSV file in either lab page.
""")
st.info("Teaching note: the included dataset is for statistical practice. Do not interpret its summaries as clinical advice or as representative of a real patient population unless its provenance and sampling design are independently established.")

st.markdown("### Suggested activities")
st.markdown("""
1. Select **Age** and compare its mean and median.
2. Select **Health_Quality_Score** and inspect the left-skewed distribution.
3. Select **HbA1c** and compare the histogram with its skewness value.
4. Change the variance method between population (`n`) and sample (`n − 1`).
5. Create grouped frequency distributions and compare frequency with relative and cumulative frequency.
6. In the Central Tendency lab, predict mean, median and mode before revealing the calculated values.
7. Add a hypothetical extreme value and compare how the mean and median respond.
8. In the Central Tendency lab, compare sample estimates with parameters calculated from all 10,000 records and explore how estimates vary with sample size.
9. In the Measures of Dispersion lab, compare sample SD with population σ and use repeated sampling to explore how estimation error changes with sample size.
10. Use **Unit 1 Study Material: Questions and Answers** to revise the concepts in sequence and complete the quick self-check.
""")
