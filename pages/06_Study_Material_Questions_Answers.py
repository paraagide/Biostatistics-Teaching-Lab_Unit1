import streamlit as st
import random

st.set_page_config(page_title="Unit 1 Study Material", page_icon="📘", layout="wide")
st.title("📘 Unit 1 Study Material: Questions and Answers")
st.caption("Applied Biostatistics and Data Analytics for Pharmaceutical Sciences")
st.markdown("Use these questions in sequence. Try answering each question before expanding the answer. Worked examples use illustrative teaching data, not clinical recommendations.")

sections = [
("1. Meaning, scope and importance of statistics and biostatistics", [
("What is statistics?", "Statistics is the science of collecting, organizing, summarizing, analysing and interpreting data to describe phenomena and support decisions under uncertainty."),
("What is biostatistics?", "Biostatistics is the application of statistical principles and methods to biology, medicine, pharmacy, public health and other life sciences."),
("What is the difference between statistics and biostatistics?", "Statistics is the general discipline; biostatistics applies statistical methods to biological, health and pharmaceutical questions. The underlying principles overlap."),
("Why is biostatistics important in pharmaceutical sciences?", "It helps design studies, summarize laboratory and clinical data, quantify uncertainty, compare treatments or processes, assess safety and efficacy, monitor quality, and make evidence-informed decisions."),
("Give four pharmaceutical examples where biostatistics is useful.", "Examples include analysing adverse-event reports in pharmacovigilance; comparing treatment groups in clinical trials; monitoring tablet weight or assay results in quality control; and analysing concentration–time data in pharmacokinetics and bioavailability studies."),
("Does statistical significance automatically mean clinical importance?", "No. Statistical significance concerns compatibility with a statistical null model under specified assumptions. Clinical or practical importance also depends on effect size, uncertainty, safety, costs and context."),
]),
("2. Variables and their types", [
("What is a variable?", "A variable is a characteristic recorded for each unit or observation that can take different values, such as age, dosage, blood group or dissolution percentage."),
("What is a qualitative (categorical) variable? Give examples.", "A qualitative variable places observations into categories. Examples include blood group, adverse-event type, dosage form and treatment arm."),
("What is a quantitative (numerical) variable? Give examples.", "A quantitative variable represents a count or measurement. Examples include number of adverse events, tablet weight, plasma drug concentration and patient age."),
("What is a discrete variable?", "A discrete variable takes separate countable values, often whole numbers. Examples include number of tablets rejected, number of hospital visits or number of adverse events reported."),
("What is a continuous variable?", "A continuous variable can theoretically take any value within an interval, subject to measurement precision. Examples include body weight, blood pressure, dissolution time and plasma concentration."),
("How do nominal and ordinal variables differ?", "Nominal categories have no inherent order (e.g., blood group). Ordinal categories have a meaningful order, but the gaps between levels are not necessarily equal (e.g., mild, moderate and severe adverse-event intensity)."),
("Is an identification number a quantitative variable?", "Usually not for statistical arithmetic. A patient ID or batch number is an identifier: its digits label records rather than measure quantity. It is generally treated as nominal/identifier data."),
]),
("3. Measurement scales", [
("What are the four common measurement scales?", "Nominal, ordinal, interval and ratio."),
("What is the nominal scale?", "It classifies observations into distinct categories without order. Examples: blood group, formulation type, adverse-event category and treatment group. Counts, proportions and mode are meaningful summaries."),
("What is the ordinal scale?", "It has ordered categories, but distances between categories are not known to be equal. Examples: pain severity categories, Likert responses and severity grades. Frequencies, medians and percentiles are often useful."),
("What is the interval scale?", "Differences are meaningful and equal intervals are assumed, but zero is arbitrary rather than an absence of the measured quantity. Temperature in degrees Celsius is a standard example."),
("What is the ratio scale?", "It has equal intervals and a meaningful zero, so ratios are meaningful. Examples include mass, length, time, dose, concentration and number of tablets."),
("Why does the measurement scale matter?", "It influences which summaries, graphs and statistical methods are appropriate. For example, calculating a mean of blood-group codes such as A=1, B=2, AB=3 and O=4 is meaningless because the numbers are labels."),
]),
("4. Data: meaning, types and sources", [
("What is data?", "Data are recorded observations, measurements, counts, categories or responses collected for a purpose. A single recorded value is often called an observation; a collection of observations forms a dataset."),
("What is primary data?", "Data collected directly for the current study or question, such as measurements collected in a new dissolution experiment or responses collected in a survey."),
("What is secondary data?", "Data originally collected by someone else or for another purpose and then reused, such as published trial datasets, electronic health records, registries or historical manufacturing records."),
("What are common sources of pharmaceutical and health data?", "Laboratory experiments, clinical trials, electronic health records, disease registries, pharmacy records, spontaneous adverse-event reports, manufacturing records, stability studies, bioanalytical assays and published research."),
("Give examples of data used in pharmacovigilance.", "Suspected adverse-event reports may contain event type, onset date, seriousness, suspected medicine, dose, concomitant medicines, outcome and reporter information. Spontaneous reports can generate safety signals but usually cannot by themselves establish incidence or causality."),
("Give examples of data used in clinical trials.", "Treatment assignment, baseline characteristics, efficacy outcomes, adverse events, laboratory measurements, adherence, withdrawals and follow-up time. Study design and a prespecified analysis plan guide valid comparisons."),
("Give examples of data used in pharmaceutical quality control.", "Assay percentage, tablet weight, hardness, friability, dissolution at a specified time, impurity levels, pH, moisture content and batch acceptance outcomes."),
("Give examples of pharmacokinetic and bioavailability data.", "Drug concentration measured at time points after administration. Derived parameters may include Cmax, Tmax, AUC and elimination half-life. Bioavailability studies often compare exposure after different formulations or routes."),
("What should be checked before analysing a dataset?", "Check provenance, definitions, units, coding, missing values, duplicate records, outliers, measurement methods, data quality, sampling/design and privacy requirements. Never assume a dataset is clinically representative merely because it contains health-related variables."),
]),
("5. Descriptive and inferential statistics", [
("What is descriptive statistics?", "Descriptive statistics organizes and summarizes the data actually observed using tables, graphs and numerical summaries such as mean, median, standard deviation and proportions."),
("What is inferential statistics?", "Inferential statistics uses sample data and probability models to draw conclusions about a wider population, while accounting for uncertainty. Examples include confidence intervals, hypothesis tests and model-based estimates."),
("What is the difference between a population and a sample?", "A population is the complete set of units relevant to the question. A sample is a subset observed from that population. A population parameter describes the population; a sample statistic summarizes the sample."),
("What are the main types of descriptive summaries?", "Frequency summaries; measures of central tendency (mean, median, mode); measures of dispersion (range, IQR, variance, SD); position measures (quartiles and percentiles); and distribution-shape measures such as skewness. Tables and graphs are also descriptive tools."),
("Why does a sample estimate vary from sample to sample?", "Different random samples generally contain different observations. This sampling variability means their statistics differ, even when they are drawn from the same population."),
("As sample size increases, will every estimate move closer to the population parameter?", "Not at every step. A larger sample generally reduces sampling variability under suitable sampling assumptions, so estimates tend to be more stable and typical error often decreases. A particular estimate can still move farther from the true value when the sample grows."),
]),
("6. Frequency distributions and graphical displays", [
("What is a frequency distribution?", "A frequency distribution summarizes how often each category or value, or each interval of values, occurs in a dataset."),
("What are frequency, relative frequency, percentage and cumulative frequency?", "Frequency is the count in a category/class. Relative frequency is frequency divided by the total. Percentage is relative frequency multiplied by 100. Cumulative frequency is the running total of frequencies in ordered categories or classes."),
("How do you calculate relative frequency and percentage?", "For a category/class with frequency f and total n: relative frequency = f/n; percentage = (f/n) × 100%. Across all categories/classes, relative frequencies should sum to 1 and percentages to 100%, subject to rounding."),
("When should an ungrouped frequency distribution be used?", "Use it when there are relatively few distinct values or categories and showing each value separately remains readable. Examples include blood group categories or a small set of tablet-defect types."),
("When should a grouped frequency distribution be used?", "Use class intervals when a numerical variable has many distinct values or is measured continuously and a compact overview is useful. Examples include age, tablet weight, dissolution time or plasma concentration."),
("What makes good class intervals?", "They should cover the full data range, avoid gaps and overlaps, use clear boundary conventions, and preferably have equal widths for a basic histogram unless unequal widths are deliberately justified. State how values on boundaries are assigned."),
("What is the difference between a bar graph and a histogram?", "A bar graph displays categories or discrete groups with separated bars. A histogram displays a quantitative variable grouped into ordered numerical intervals, with bars touching. For unequal-width bins, histogram heights should represent frequency density if area is to be proportional to frequency."),
("Which graph is suitable for blood group, age and a time series?", "Blood group: bar graph. Age: histogram (or a box plot for a compact spread summary). Measurements over time: line graph is often useful. The best graph depends on the variable and question."),
("Practice: A sample has blood groups A=8, B=5, AB=2 and O=5. What are the total and percentages?", "Total = 8+5+2+5 = 20. A: 40%; B: 25%; AB: 10%; O: 25%. The bar graph should show four category bars with these frequencies or percentages."),
("Practice: The numbers of rejected tablets in five batches are 2, 0, 3, 2, 1. Construct an ungrouped frequency table.", "Value 0: frequency 1; value 1: frequency 1; value 2: frequency 2; value 3: frequency 1. Total frequency = 5. A bar graph can display the four count values."),
("Practice: Times (minutes) for 10 dissolution observations are 5, 6, 7, 7, 8, 8, 8, 9, 10, 12. Give one possible grouped distribution using intervals [5,7), [7,9), [9,11), [11,13].", "[5,7): 2 values (5,6); [7,9): 5 values (7,7,8,8,8); [9,11): 2 values (9,10); [11,13]: 1 value (12). Total = 10. This is one valid grouping; different valid boundaries can produce a different-looking histogram."),
("Why can changing class boundaries change the histogram?", "Grouping combines individual observations into bins. Changing the bin width or starting boundary changes which observations are combined, so the visible shape may change even though the raw data do not."),
]),
("7. Measures of central tendency", [
("What is central tendency?", "It describes the centre or typical value of a distribution. The main measures are arithmetic mean, median and mode."),
("What is the arithmetic mean for ungrouped data?", "For observations x₁, x₂, …, xₙ, the arithmetic mean is x̄ = (Σxᵢ)/n. Add all observations and divide by the number of observations."),
("How is the mean calculated from a frequency table?", "For distinct values xᵢ with frequencies fᵢ, mean = Σ(fᵢxᵢ)/Σfᵢ. For grouped continuous data, use each class midpoint mᵢ as an approximation: grouped mean ≈ Σ(fᵢmᵢ)/N."),
("What is the median for ungrouped data?", "Sort the observations. If n is odd, the median is the observation at position (n+1)/2. If n is even, it is the average of the observations at positions n/2 and n/2+1."),
("What is the grouped-data median formula?", "For a grouped continuous frequency distribution, median ≈ L + [(N/2 − cfb)/f] × h, where L is the lower boundary of the median class, N is total frequency, cfb is cumulative frequency before the median class, f is the median-class frequency and h is class width. It assumes observations are distributed sufficiently smoothly within the class."),
("What is the mode?", "The mode is the most frequent value or category. A dataset can have one mode, more than one mode, or no unique mode. For grouped continuous data, an approximate mode is L + [d₁/(d₁+d₂)] × h, where d₁ = frequency of modal class − preceding-class frequency and d₂ = frequency of modal class − following-class frequency. This is an interpolation estimate, not an exact raw-data mode."),
("When is the mean most useful?", "For numerical data on an interval or ratio scale when arithmetic averaging is meaningful and extreme values do not unduly distort the summary. It uses every value but is sensitive to outliers and skewness."),
("When is the median most useful?", "For ordered or numerical data when the distribution is skewed or has extreme values. It is resistant to outliers and is appropriate for ordinal data with a meaningful order."),
("When is the mode most useful?", "For nominal categorical data, such as blood group or most common adverse-event category, and for identifying the most frequent value or class. It may not be unique and may not summarize the centre well for all numerical distributions."),
("How does skewness affect mean and median?", "In a typical right-skewed distribution, the mean is pulled toward the long right tail and is often greater than the median. In a typical left-skewed distribution, the mean is pulled toward the long left tail and is often less than the median. These are patterns, not universal laws."),
("Practice: Find the mean and median of 2, 3, 3, 4, 8.", "Mean = (2+3+3+4+8)/5 = 20/5 = 4. The sorted middle value is 3, so median = 3. Mode = 3."),
("Practice: Five assay results (%) are 98, 99, 99, 100, 124. Which measure better represents a typical result, and why?", "The mean is 104, while the median is 99 and mode is 99. The unusually high value 124 pulls the mean upward. If it is a valid observation, the median may better represent the typical result, but the cause and validity of the extreme value should be investigated rather than automatically removed."),
("Can the mode be calculated meaningfully for coded nominal categories?", "Yes, by identifying the most frequent category, but not by averaging the category codes. For example, the mode of blood group is the most common blood-group category."),
]),
("8. Measures of dispersion", [
("What is dispersion and why measure it?", "Dispersion describes how spread out observations are. Two datasets can have the same mean but different variability; spread is important for consistency, precision, risk and process monitoring."),
("What is the range?", "Range = maximum − minimum. It is easy to calculate but uses only the two extreme observations and is sensitive to outliers."),
("What are quartiles and the interquartile range?", "Quartiles divide ordered data into four parts. Q1 is the lower quartile (25th percentile) and Q3 the upper quartile (75th percentile). IQR = Q3 − Q1; it describes the spread of the middle 50% and is less sensitive to extremes than the range."),
("What is population variance?", "For a complete population of N values with population mean μ, population variance σ² = Σ(xᵢ−μ)²/N. It is the mean squared deviation from the population mean."),
("What is sample variance?", "For a sample of n observations with sample mean x̄, the usual sample variance is s² = Σ(xᵢ−x̄)²/(n−1). The n−1 denominator is Bessel's correction and makes s² unbiased for population variance under standard independent random-sampling assumptions with finite variance."),
("What is standard deviation?", "Standard deviation is the square root of variance. Population SD: σ = √[Σ(xᵢ−μ)²/N]. Sample SD: s = √[Σ(xᵢ−x̄)²/(n−1)]. It is expressed in the original units of the variable."),
("Why is SD often easier to interpret than variance?", "Variance is expressed in squared units (e.g., mg²), whereas SD is expressed in the original units (e.g., mg), making its scale easier to compare with the observations."),
("What is the coefficient of variation (CV)?", "For a positive-scale ratio variable with a meaningful non-zero mean, CV = (SD/mean) × 100%. It expresses SD relative to the mean. Avoid using it when the mean is zero or near zero, or when the scale lacks a meaningful ratio zero."),
("How should dispersion be paired with central tendency?", "For roughly symmetric numerical data without influential outliers, mean and SD are often reported together. For skewed numerical data or data with outliers, median and IQR are often more informative. For categorical data, frequencies/percentages and mode are generally appropriate."),
("Practice: For 2, 4, 6, 8, 10, calculate range and IQR using the median-of-halves convention.", "Range = 10−2 = 8. Lower half is 2,4,6, so Q1=4. Upper half is 8,10 plus the middle? Under the median-of-halves convention for an odd-sized dataset, exclude the overall median 6: upper half 8,10 has median 9, so Q3=9. Thus IQR=9−4=5. Quartile algorithms can differ, so state the convention used."),
("Practice: For 2, 4, 6, calculate population variance and population SD.", "Mean μ = 4. Squared deviations are 4, 0, 4, sum = 8. Population variance = 8/3 ≈ 2.667. Population SD = √(8/3) ≈ 1.633."),
("Practice: For 2, 4, 6, calculate sample variance and sample SD.", "Sample mean = 4; squared-deviation sum = 8. Sample variance = 8/(3−1) = 4. Sample SD = √4 = 2."),
("Why might two batches have the same mean assay but different SDs?", "Their average assay can be identical while individual results are more tightly clustered in one batch and more spread out in the other. SD helps quantify batch consistency, alongside specification limits and other quality requirements."),
]),
("9. Integrated pharmaceutical examples", [
("A pharmacovigilance team wants the most frequently reported adverse-event category. Which summary is suitable?", "A frequency table and bar graph for the categorical event type, with the mode identifying the most frequently reported category. Spontaneous reports alone generally cannot estimate event incidence because reporting is selective and exposure denominators may be unavailable."),
("A clinical trial endpoint is highly right-skewed. Which summaries might be useful?", "The median and IQR may describe the typical value and spread robustly. Depending on the endpoint and analysis objective, a transformation or suitable statistical model may also be considered. The choice should follow the protocol and analysis plan."),
("A QC team compares tablet weights from a production run. Which summaries are useful?", "Mean and SD can describe centre and spread when the data are reasonably symmetric; median, IQR, histogram and control charts may add insight. Specification limits and process-control rules are distinct from descriptive summaries."),
("A pharmacokinetic study measures plasma concentration at multiple times. Which graph and summaries are useful?", "A concentration–time plot is central. Parameters such as Cmax, Tmax and AUC summarize different aspects of exposure. Concentration data may be skewed, and pharmacokinetic analyses should follow appropriate methods and the study protocol."),
("A bioavailability study compares exposure between formulations. Is comparing sample means alone always sufficient?", "No. The design, paired or crossover structure, log transformation where appropriate, variability, confidence intervals and prespecified bioavailability criteria matter. Descriptive summaries are useful but do not replace the planned inferential analysis."),
]),
("10. Mixed practice and answer key", [
("Question: A dataset has 12 observations. What is the cumulative frequency at the final class if every observation is included?", "12. The final cumulative frequency should equal the total number of observations."),
("Question: Which is more suitable for blood group: mean, median or mode?", "Mode, together with a frequency table or bar graph, because blood group is nominal categorical data."),
("Question: A sample has mean 50 and population mean 48. What is the absolute estimation error?", "|50−48| = 2 units. Absolute error measures distance from the population parameter; it does not indicate whether the estimate is above or below it."),
("Question: If sample size increases, must the sample mean move monotonically toward the population mean?", "No. Each added observation can move the sample mean either toward or away from the population mean. Across repeated samples, estimates typically become less variable as sample size grows under suitable assumptions."),
("Question: A frequency table of a numerical variable has class widths 5, 5, 10 and 10. Can bar heights simply be frequencies in a histogram?", "If class widths differ and histogram area is intended to represent frequency, use frequency density (frequency divided by class width) for bar height. Otherwise wider bins could appear more prominent simply because they are wider."),
("Question: State one key difference between variance and SD.", "SD is the square root of variance and is in the original units; variance is in squared units."),
])
]

search = st.text_input("Search questions and answers", placeholder="Try: pharmacovigilance, IQR, grouped median, measurement scale...")
if search:
    qlow = search.lower()
    found = 0
    for section_title, items in sections:
        matches = [(q, a) for q, a in items if qlow in q.lower() or qlow in a.lower() or qlow in section_title.lower()]
        if matches:
            st.subheader(section_title)
            for q, a in matches:
                with st.expander(q):
                    st.write(a)
            found += len(matches)
    if not found:
        st.warning("No matching questions. Try a broader keyword.")
else:
    for section_title, items in sections:
        with st.expander(section_title, expanded=False):
            for idx, (q, a) in enumerate(items, start=1):
                st.markdown(f"**Q{idx}. {q}**")
                st.markdown(f"**Answer:** {a}")
                st.divider()

st.markdown("---")
st.subheader("Quick self-check")
quiz = [
    {"q":"Which scale applies to blood group?", "opts":["Nominal", "Ordinal", "Interval", "Ratio"], "ans":"Nominal", "why":"Blood groups are categories without an inherent order."},
    {"q":"Which graph is normally used for a continuous numerical distribution grouped into intervals?", "opts":["Pie chart", "Histogram", "Line graph only", "Pictogram"], "ans":"Histogram", "why":"A histogram displays frequencies across ordered numerical intervals, with touching bars."},
    {"q":"Which measure is generally less affected by a single extreme value?", "opts":["Mean", "Median", "Range", "Variance"], "ans":"Median", "why":"The median depends on the middle position(s) in sorted data rather than the magnitude of every observation."},
    {"q":"What is IQR?", "opts":["Q3 − Q1", "Maximum − minimum", "Mean divided by SD", "Sum divided by n"], "ans":"Q3 − Q1", "why":"The interquartile range is the difference between the upper and lower quartiles."},
    {"q":"In spontaneous pharmacovigilance reports, can the count of reports alone usually estimate incidence?", "opts":["Yes, always", "No, usually not without suitable exposure and ascertainment information", "Only if the count is large", "Only for serious events"], "ans":"No, usually not without suitable exposure and ascertainment information", "why":"Spontaneous reports are subject to under-reporting, stimulated reporting and lack of a reliable exposed-population denominator."},
]
with st.form("qa_quick_check"):
    responses = {}
    for i, item in enumerate(quiz):
        responses[i] = st.radio(f"{i+1}. {item['q']}", item["opts"], key=f"qa_quiz_{i}")
    submitted = st.form_submit_button("Check answers")
if submitted:
    score = 0
    for i, item in enumerate(quiz):
        correct = responses[i] == item["ans"]
        score += int(correct)
        st.markdown(f"**{i+1}. {'Correct' if correct else 'Review this answer'}** — {item['why']}")
    st.success(f"Your score: {score}/{len(quiz)}")

st.info("Teaching note: examples and formulas are for learning. For real clinical, pharmacovigilance, clinical-trial or quality decisions, use the applicable protocol, validated methods, regulatory requirements and subject-matter review.")
