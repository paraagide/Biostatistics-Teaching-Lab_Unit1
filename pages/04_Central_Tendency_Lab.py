import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Central Tendency Practice Lab", page_icon="🧪", layout="wide")
st.title("🧪 Central Tendency Practice Lab")
st.caption("Sample the 10,000-record teaching dataset, classify a variable, build its frequency distribution, choose a suitable measure and equation, then calculate and check your answer.")

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "Advanced_Health_Records_10000_with_Left_Skew.xlsx"

@st.cache_data
def load_data(path):
    return pd.read_excel(path)

def fmt(x, digits=3):
    if x is None or pd.isna(x):
        return "Not available"
    if isinstance(x, (int, np.integer)) or float(x).is_integer():
        return f"{int(x):,}"
    return f"{float(x):,.{digits}f}"

def parse_boundaries(text):
    try:
        vals = [float(v.strip()) for v in text.split(",") if v.strip()]
    except ValueError:
        return None, "Enter numbers separated by commas."
    if len(vals) < 3:
        return None, "Enter at least three boundaries to create two or more classes."
    if any(not np.isfinite(v) for v in vals):
        return None, "Boundaries must be finite numbers."
    if any(vals[i] >= vals[i+1] for i in range(len(vals)-1)):
        return None, "Boundaries must be strictly increasing with no duplicates."
    widths = np.diff(vals)
    if not np.allclose(widths, widths[0], rtol=1e-6, atol=1e-8):
        return None, "For this formula-practice activity, use equal-width classes. You can still explore unequal widths on the Frequency Distributions page."
    return vals, None

# Classification is based on the meaning/recording of fields in this teaching dataset.
CLASSIFICATION = {
    "ID": "Identifier (not a substantive variable)",
    "Gender": "Nominal categorical", "BloodGroup": "Nominal categorical", "Smoking": "Nominal categorical",
    "Exercise_Level": "Ordinal categorical", "Socioeconomic_Class": "Ordinal categorical",
    "Diabetes": "Nominal categorical", "Heart_Disease": "Nominal categorical",
    "Chronic_Kidney_Disease": "Nominal categorical", "Ailment": "Nominal categorical",
    "Diagnostic_Test": "Nominal categorical", "Survival_Status": "Nominal categorical",
    "Age": "Discrete numerical", "Followup_Months": "Discrete numerical",
    "Height_cm": "Continuous numerical", "Weight_kg": "Continuous numerical", "BMI": "Continuous numerical",
    "Systolic_BP": "Continuous numerical", "Diastolic_BP": "Continuous numerical",
    "Total_Cholesterol": "Continuous numerical", "HbA1c": "Continuous numerical",
    "Health_Quality_Score": "Continuous numerical",
}
ORDERS = {
    "Exercise_Level": ["Low", "Moderate", "High"],
    "Socioeconomic_Class": ["Low", "Middle", "High"],
}
CLASS_OPTIONS = ["Nominal categorical", "Ordinal categorical", "Discrete numerical", "Continuous numerical", "Identifier (not a substantive variable)"]

try:
    df = load_data(str(DATA_FILE))
except Exception as exc:
    st.error(f"Could not load the bundled dataset: {exc}")
    st.stop()

st.info(f"Source dataset: **{len(df):,} records** and **{len(df.columns)} columns**. This is a teaching dataset; do not interpret it as verified clinical evidence.")

with st.expander("How this activity works", expanded=False):
    st.markdown("""
    1. Choose a variable and enter any sample size from 1 to the number of usable records for that variable, then generate a random sample without replacement.
    2. Classify the variable and check your classification.
    3. Create a frequency distribution. For numerical variables, you supply equal-width class boundaries. A histogram or bar graph is displayed before the measure-choice step.
    4. Choose the most suitable measure of central tendency and select its equation.
    5. Calculate the result from the frequency table and enter your answer for feedback.

    **Important:** grouped-data answers are estimates based on class midpoints/boundaries and can differ from answers calculated from the ungrouped raw observations. For numerical variables, the suggested mean-versus-median decision is a teaching heuristic based on sample skewness, not a universal rule. Consider the study question and outliers too.
    """)

# Sampling controls: variable-specific usable rows define the maximum sample size.
variable = st.selectbox("Select a variable/column", list(df.columns), index=list(df.columns).index("Age"))
usable_record_count = int(df[variable].notna().sum())
left, right = st.columns([1, 2])
with left:
    sample_size = st.number_input(
        "Enter your sample size",
        min_value=1,
        max_value=max(1, usable_record_count),
        value=min(100, max(1, usable_record_count)),
        step=1,
        help=f"Enter any whole number from 1 to {usable_record_count:,}. No preset minimum of 25 is imposed.",
    )
with right:
    st.caption(f"You can sample any number of usable records from 1 to {usable_record_count:,} for **{variable}**. The sample is drawn without replacement from records where this variable is present.")

if "ctlab_sample" not in st.session_state:
    st.session_state.ctlab_sample = None
if "ctlab_sample_meta" not in st.session_state:
    st.session_state.ctlab_sample_meta = None

if st.button("🎲 Generate / regenerate random sample", type="primary"):
    eligible_rows = df.loc[df[variable].notna()]
    sampled = eligible_rows.sample(n=int(sample_size), replace=False).reset_index(drop=True)
    st.session_state.ctlab_sample = sampled
    st.session_state.ctlab_sample_meta = {"size": int(sample_size), "variable": variable}
    for k in [
        "ctlab_class_checked", "ctlab_class_choice_saved", "ctlab_freq_ready",
        "ctlab_freq_table", "ctlab_freq_edges", "ctlab_freq_variable", "ctlab_freq_sample_size",
        "ctlab_measure_checked", "ctlab_measure_choice_saved", "ctlab_formula_checked",
        "ctlab_equation_saved", "ctlab_answer_checked", "ctlab_grouped_answers",
        "ctlab_category_counts", "ctlab_class_choice", "ctlab_measure_choice",
        "ctlab_equation_choice", "ctlab_numeric_answer", "ctlab_category_answer",
        "ctlab_boundaries",
    ]:
        st.session_state.pop(k, None)

sampled_df = st.session_state.ctlab_sample
if sampled_df is None:
    st.warning("Choose a sample size and variable, then click **Generate / regenerate random sample** to begin.")
    st.stop()

meta = st.session_state.ctlab_sample_meta or {}
if meta.get("size") != int(sample_size) or meta.get("variable") != variable:
    st.warning("Your selected variable or sample size has changed. Click **Generate / regenerate random sample** to apply the new settings before continuing.")
    st.stop()

series = sampled_df[variable].dropna().reset_index(drop=True)
if series.empty:
    st.error("The selected variable has no non-missing values in this sample. Generate a new sample or choose another variable.")
    st.stop()

m1, m2, m3 = st.columns(3)
m1.metric("Sample records", f"{len(sampled_df):,}")
m2.metric("Valid values for selected variable", f"{len(series):,}")
m3.metric("Distinct observed values", f"{series.nunique(dropna=True):,}")
with st.expander("Preview sampled records"):
    st.dataframe(sampled_df.head(20), use_container_width=True)

# 1. Classification
st.markdown("## Step 1 — Classify the variable")
expected_class = CLASSIFICATION.get(variable)
if expected_class is None:
    if pd.api.types.is_numeric_dtype(df[variable]):
        expected_class = "Continuous numerical" if df[variable].nunique() > 20 else "Discrete numerical"
    else:
        expected_class = "Nominal categorical"
with st.form("ctlab_classification_form"):
    class_choice = st.radio("What type of variable is this?", CLASS_OPTIONS, index=None, key="ctlab_class_choice")
    class_submit = st.form_submit_button("Check variable classification")
if class_submit:
    st.session_state.ctlab_class_checked = True
    st.session_state.ctlab_class_choice_saved = class_choice
if st.session_state.get("ctlab_class_checked", False):
    if st.session_state.get("ctlab_class_choice_saved") == expected_class:
        st.success(f"Correct classification: **{expected_class}**.")
    else:
        st.warning(f"Review this choice. Expected classification for this dataset column: **{expected_class}**.")
    if expected_class == "Identifier (not a substantive variable)":
        st.info("An ID labels records. Its numerical appearance does not make its mean or median substantively meaningful. Choose another variable for central-tendency calculations.")

if expected_class == "Identifier (not a substantive variable)":
    st.stop()

# 2. Frequency distribution
st.markdown("## Step 2 — Generate the frequency distribution")
numeric_variable = expected_class in ["Discrete numerical", "Continuous numerical"]
if numeric_variable:
    numeric_values = pd.to_numeric(series, errors="coerce").dropna()
    vmin, vmax = float(numeric_values.min()), float(numeric_values.max())
    st.write(f"Sample minimum = **{fmt(vmin)}**; sample maximum = **{fmt(vmax)}**; range = **{fmt(vmax-vmin)}**.")
    st.write("Decide on class intervals. Enter equal-width class boundaries that cover the sample minimum and maximum. The first interval includes its lower endpoint; later intervals are interpreted as (lower, upper], with the first endpoint included as well.")
    boundary_text = st.text_input("Your class boundaries (comma-separated)", placeholder="For example: 18, 30, 42, 54, 66, 78, 90", key="ctlab_boundaries")
    if st.button("Generate frequency distribution", key="ctlab_generate_freq"):
        edges, err = parse_boundaries(boundary_text)
        if err:
            st.session_state.ctlab_freq_ready = False
            st.error(err)
        elif edges[0] > vmin or edges[-1] < vmax:
            st.session_state.ctlab_freq_ready = False
            st.error(f"Boundaries must cover the complete sample range: start at or below {fmt(vmin)} and end at or above {fmt(vmax)}.")
        else:
            cats = pd.cut(numeric_values, bins=edges, right=True, include_lowest=True, ordered=True)
            freq = cats.value_counts(sort=False).sort_index()
            intervals = list(freq.index)
            table = pd.DataFrame({"Class interval": [str(x) for x in intervals], "Lower boundary": [float(edges[i]) for i in range(len(edges)-1)], "Upper boundary": [float(edges[i+1]) for i in range(len(edges)-1)], "Midpoint (m)": [(edges[i]+edges[i+1])/2 for i in range(len(edges)-1)], "Frequency (f)": freq.to_numpy()})
            table["Relative frequency"] = table["Frequency (f)"] / table["Frequency (f)"].sum()
            table["Percentage"] = 100 * table["Relative frequency"]
            table["Cumulative frequency"] = table["Frequency (f)"].cumsum()
            st.session_state.ctlab_freq_table = table
            st.session_state.ctlab_freq_edges = edges
            st.session_state.ctlab_freq_ready = True
            st.session_state.ctlab_freq_variable = variable
            st.session_state.ctlab_freq_sample_size = len(series)
    freq_ready = st.session_state.get("ctlab_freq_ready", False) and st.session_state.get("ctlab_freq_variable") == variable and st.session_state.get("ctlab_freq_sample_size") == len(series)
    if freq_ready:
        freq_table = st.session_state.ctlab_freq_table.copy()
        st.dataframe(freq_table, use_container_width=True, hide_index=True)
        st.metric("Frequency total", f"{int(freq_table['Frequency (f)'].sum()):,}")
        st.download_button("Download frequency distribution CSV", freq_table.to_csv(index=False).encode("utf-8"), file_name=f"{variable}_sample_frequency.csv", mime="text/csv")
        # Show the distribution graph before asking students to choose a measure.
        st.markdown("### Visualise the frequency distribution before choosing a measure")
        edges = np.asarray(st.session_state.ctlab_freq_edges, dtype=float)
        plot_freq = freq_table["Frequency (f)"].to_numpy(dtype=float)
        plot_widths = np.diff(edges)
        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.bar(edges[:-1], plot_freq, width=plot_widths, align="edge", edgecolor="black", alpha=0.8)
        ax.set_xlabel(variable + " (class intervals)")
        ax.set_ylabel("Frequency")
        ax.set_title(f"Histogram of {variable} (sample n={len(series):,})")
        ax.set_xticks(edges)
        ax.tick_params(axis="x", labelrotation=45)
        ax.grid(axis="y", alpha=0.25)
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        f = freq_table["Frequency (f)"].to_numpy(dtype=float)
        mid = freq_table["Midpoint (m)"].to_numpy(dtype=float)
        grouped_mean = float(np.sum(f*mid)/np.sum(f))
        cum = np.cumsum(f)
        med_idx = int(np.searchsorted(cum, np.sum(f)/2, side="left"))
        med_idx = min(med_idx, len(f)-1)
        cf_before = float(cum[med_idx-1]) if med_idx > 0 else 0.0
        h_med = float(edges[med_idx+1]-edges[med_idx])
        grouped_median = float(edges[med_idx] + ((np.sum(f)/2-cf_before)/f[med_idx])*h_med) if f[med_idx] else float("nan")
        maxfreq = np.max(f)
        modal_indices = np.where(f == maxfreq)[0]
        grouped_mode = None
        mode_explanation = ""
        if len(modal_indices) == 1:
            j = int(modal_indices[0])
            f1 = f[j]
            f0 = f[j-1] if j > 0 else 0.0
            f2 = f[j+1] if j < len(f)-1 else 0.0
            denom = 2*f1-f0-f2
            if denom != 0:
                h_mode = float(edges[j+1]-edges[j])
                grouped_mode = float(edges[j] + ((f1-f0)/denom)*h_mode)
        else:
            mode_explanation = "The highest frequency is tied across multiple classes, so a single grouped modal estimate is not identified."
        st.session_state.ctlab_grouped_answers = {"Mean": grouped_mean, "Median": grouped_median, "Mode": grouped_mode}
        st.caption("For grouped numerical data, the mean uses class midpoints; the median and mode use grouped-data estimation formulae. These estimates may differ from raw-data statistics.")
    else:
        st.info("Generate a valid frequency table to continue to the measure and equation steps.")
        st.stop()
else:
    # categorical variable distribution
    counts = series.astype(str).value_counts(dropna=False)
    table = counts.rename_axis("Category").reset_index(name="Frequency")
    table["Relative frequency"] = table["Frequency"] / table["Frequency"].sum()
    table["Percentage"] = 100 * table["Relative frequency"]
    table["Cumulative frequency"] = table["Frequency"].cumsum()
    st.dataframe(table, use_container_width=True, hide_index=True)
    st.metric("Frequency total", f"{int(table['Frequency'].sum()):,}")
    st.download_button("Download frequency distribution CSV", table.to_csv(index=False).encode("utf-8"), file_name=f"{variable}_sample_frequency.csv", mime="text/csv")
    # Display categorical bar chart before the measure-choice step.
    st.markdown("### Visualise the frequency distribution before choosing a measure")
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar(table["Category"].astype(str), table["Frequency"], edgecolor="black", alpha=0.8)
    ax.set_xlabel(variable + " (categories)")
    ax.set_ylabel("Frequency")
    ax.set_title(f"Bar graph of {variable} (sample n={len(series):,})")
    ax.tick_params(axis="x", labelrotation=35)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    category_counts = series.astype(str).value_counts()
    mode_candidates = category_counts[category_counts == category_counts.max()].index.tolist()
    mode_cat = mode_candidates[0] if len(mode_candidates) == 1 else " / ".join(map(str, mode_candidates))
    ordered = ORDERS.get(variable)
    if expected_class == "Ordinal categorical" and ordered:
        order_values = [x for x in series.astype(str).tolist() if x in ordered]
        sorted_ordered = sorted(order_values, key=ordered.index)
        n = len(sorted_ordered)
        if n % 2:
            median_cat = sorted_ordered[n//2]
        else:
            median_cat = f"{sorted_ordered[n//2-1]} / {sorted_ordered[n//2]}"
    else:
        median_cat = None
    st.session_state.ctlab_grouped_answers = {"Mean": None, "Median": median_cat, "Mode": mode_cat}
    st.session_state.ctlab_category_counts = category_counts.to_dict()

# 3. Select the best measure
st.markdown("## Step 3 — Choose the most suitable measure")
if numeric_variable:
    skew = float(pd.to_numeric(series, errors="coerce").skew())
    st.write(f"Sample skewness (calculated from the raw sampled values) = **{skew:.3f}**.")
    if abs(skew) >= 1:
        expected_measure = "Median"
        why = "The absolute skewness is at least 1, so the median is the suggested robust summary for this teaching activity. Inspect the histogram and outliers too."
    else:
        expected_measure = "Mean"
        why = "The absolute skewness is below 1, so the mean is the suggested summary for this teaching activity. Inspect the histogram and study question too."
    measure_options = ["Mean", "Median", "Mode"]
else:
    expected_measure = "Median" if expected_class == "Ordinal categorical" else "Mode"
    why = "For nominal categories, the mode is appropriate. For ordered categories, the median can use the order of categories; the mode is also a valid descriptive summary."
    measure_options = ["Mode", "Median"] if expected_class == "Ordinal categorical" else ["Mode"]
with st.form("ctlab_measure_form"):
    measure_choice = st.radio("Which measure would you use?", measure_options, index=None, key="ctlab_measure_choice", horizontal=True)
    measure_submit = st.form_submit_button("Check my measure choice")
if measure_submit:
    st.session_state.ctlab_measure_checked = True
    st.session_state.ctlab_measure_choice_saved = measure_choice
if st.session_state.get("ctlab_measure_checked", False):
    if st.session_state.get("ctlab_measure_choice_saved") == expected_measure:
        st.success(f"Good choice: **{expected_measure}**. {why}")
    else:
        st.warning(f"For this activity, the suggested choice is **{expected_measure}**. {why}")

# 4. Equation selection
st.markdown("## Step 4 — Select the equation")
if numeric_variable:
    equation_options = {
        "Grouped arithmetic mean: x̄ = Σ(fm) / N": "Mean",
        "Grouped median: Median = L + [(N/2 − CF_before) / f_m] × h": "Median",
        "Grouped mode: Mode = L + [(f₁ − f₀) / (2f₁ − f₀ − f₂)] × h": "Mode",
    }
else:
    equation_options = {
        "Mode = category with the highest frequency": "Mode",
    }
    if expected_class == "Ordinal categorical":
        equation_options["Median = middle ordered category (or the two middle categories) after sorting"] = "Median"
with st.form("ctlab_equation_form"):
    equation_choice = st.selectbox("Choose the equation that matches your selected measure", ["Select an equation..."] + list(equation_options.keys()), key="ctlab_equation_choice")
    equation_submit = st.form_submit_button("Check equation")
if equation_submit:
    st.session_state.ctlab_formula_checked = True
    st.session_state.ctlab_equation_saved = equation_choice
expected_equation = next((label for label, measure in equation_options.items() if measure == st.session_state.get("ctlab_measure_choice_saved")), None)
if st.session_state.get("ctlab_formula_checked", False):
    if st.session_state.get("ctlab_equation_saved") == expected_equation and expected_equation is not None:
        st.success("Correct equation for the measure you selected.")
    else:
        st.warning("Choose the equation corresponding to the measure you selected. Check the symbols and the type of data first.")

# 5. Calculate and compare
st.markdown("## Step 5 — Calculate and compare your answer")
selected_measure = st.session_state.get("ctlab_measure_choice_saved")
answers = st.session_state.get("ctlab_grouped_answers", {})
if selected_measure not in measure_options:
    st.info("Complete Step 3 first. Then choose the measure and equation before entering your answer.")
else:
    correct_answer = answers.get(selected_measure)
    if correct_answer is None or (isinstance(correct_answer, float) and not np.isfinite(correct_answer)):
        st.warning("A unique answer cannot be calculated for this measure from the current frequency distribution (for example, tied modal classes). Choose another suitable measure or review your class intervals.")
    else:
        if numeric_variable:
            entered = st.number_input("Your calculated value", value=0.0, format="%.6f", key="ctlab_numeric_answer")
            if st.button("Compare my answer with the calculated answer", key="ctlab_compare_numeric"):
                tolerance = max(0.05, abs(float(correct_answer))*0.01)
                ok = abs(float(entered)-float(correct_answer)) <= tolerance
                if ok:
                    st.success(f"Correct within the accepted rounding tolerance. Grouped-data answer = **{fmt(correct_answer, 4)}**.")
                else:
                    st.warning(f"Not quite. The grouped-data answer is **{fmt(correct_answer, 4)}**. Check your frequency, midpoint, cumulative frequency, median class, modal class and class width.")
                st.session_state.ctlab_answer_checked = True
        elif selected_measure == "Median" and expected_class == "Ordinal categorical":
            entered_cat = st.text_input("Your calculated median category (for two middle categories, separate them with /)", key="ctlab_category_answer")
            if st.button("Compare my answer with the calculated answer", key="ctlab_compare_category"):
                normalize = lambda x: " / ".join(part.strip().casefold() for part in str(x).split("/"))
                ok = normalize(entered_cat) == normalize(correct_answer)
                if ok:
                    st.success(f"Correct. Answer = **{correct_answer}**.")
                else:
                    st.warning(f"Not quite. The calculated answer is **{correct_answer}**. Recheck the ordered categories and middle position(s).")
                st.session_state.ctlab_answer_checked = True
        else:
            categories = list(series.astype(str).value_counts().index)
            if isinstance(correct_answer, str) and " / " in correct_answer:
                entered_cat = st.multiselect("Your modal category/categories", categories, key="ctlab_category_answer")
                entered_value = " / ".join(entered_cat)
            else:
                entered_value = st.selectbox("Your calculated category", categories, key="ctlab_category_answer")
            if st.button("Compare my answer with the calculated answer", key="ctlab_compare_category"):
                normalize = lambda x: sorted(part.strip().casefold() for part in str(x).split("/"))
                ok = normalize(entered_value) == normalize(correct_answer)
                if ok:
                    st.success(f"Correct. Answer = **{correct_answer}**.")
                else:
                    st.warning(f"Not quite. The calculated answer is **{correct_answer}**. Recheck the frequency table and, for a median, the category order.")
                st.session_state.ctlab_answer_checked = True

with st.expander("Formula guide (open after attempting the activity)"):
    st.markdown(r"""
    **Grouped mean**  
    \(\bar{x}=\frac{\sum fm}{N}\), where \(f\) is class frequency, \(m\) is class midpoint, and \(N=\sum f\).

    **Grouped median**  
    \(\mathrm{Median}=L+\frac{N/2-CF_{\mathrm{before}}}{f_m}\times h\), where \(L\) is the lower boundary of the median class, \(CF_{\mathrm{before}}\) is cumulative frequency before that class, \(f_m\) is its frequency, and \(h\) is class width.

    **Grouped mode**  
    \(\mathrm{Mode}=L+\frac{f_1-f_0}{2f_1-f_0-f_2}\times h\), where \(f_1\) is modal-class frequency and \(f_0, f_2\) are frequencies of the preceding and succeeding classes.

    For a categorical variable, the mode is the category with the highest frequency. For an ordinal variable, the median is found from the ordered categories.
    """)

st.markdown("---")
st.caption("This activity uses a random sample of records from the bundled 10,000-row teaching dataset. Random samples can differ between runs. The numerical class-interval equations produce grouped estimates, not exact raw-data statistics.")


# Population-parameter comparison: use all usable records as the finite teaching population.
st.markdown("## Step 6 — Compare your sample estimate with the 10,000-record population")
st.write("The complete bundled dataset is treated as the teaching population. Compare statistics calculated from your selected sample with the corresponding parameter calculated from every usable record in the dataset.")
population_series = df[variable].dropna().reset_index(drop=True)
pop_n = len(population_series)
sample_mode_values = series.mode(dropna=True).tolist()
pop_mode_values = population_series.mode(dropna=True).tolist()

def display_mode(values):
    if not values:
        return "Not defined"
    return " / ".join(str(v) for v in values)

if numeric_variable:
    sample_mean_raw = float(pd.to_numeric(series, errors="coerce").mean())
    sample_median_raw = float(pd.to_numeric(series, errors="coerce").median())
    pop_numeric = pd.to_numeric(population_series, errors="coerce").dropna()
    population_mean = float(pop_numeric.mean())
    population_median = float(pop_numeric.median())
    population_sd_ct = float(pop_numeric.std(ddof=0))
    comparison_rows = [
        {"Measure": "Mean", "Population parameter (all usable records)": population_mean, "Sample estimate (raw sample)": sample_mean_raw, "Absolute error": abs(sample_mean_raw-population_mean)},
        {"Measure": "Median", "Population parameter (all usable records)": population_median, "Sample estimate (raw sample)": sample_median_raw, "Absolute error": abs(sample_median_raw-population_median)},
    ]
    if selected_measure in answers and answers.get(selected_measure) is not None and selected_measure in {"Mean", "Median"}:
        grouped_val = answers.get(selected_measure)
        if isinstance(grouped_val, (int, float, np.integer, np.floating)) and np.isfinite(grouped_val):
            comparison_rows.append({"Measure": f"Grouped {selected_measure.lower()} estimate", "Population parameter (all usable records)": population_mean if selected_measure == "Mean" else population_median, "Sample estimate (raw sample)": float(grouped_val), "Absolute error": abs(float(grouped_val)-(population_mean if selected_measure == "Mean" else population_median))})
    st.dataframe(pd.DataFrame(comparison_rows), use_container_width=True, hide_index=True)
    st.caption(f"Population parameters are calculated from {pop_n:,} non-missing {variable} values. A grouped-data estimate is approximate; a raw-sample estimate and a grouped estimate are not the same calculation.")

    st.markdown("### How do estimates behave as sample size increases?")
    st.write("The following curve takes progressively larger prefixes of one random ordering of the population. Estimates often become more stable as n increases, but they are not guaranteed to move closer at every single step.")
    if pop_n >= 2:
        rng = np.random.default_rng(20261023)
        shuffled = pop_numeric.to_numpy(dtype=float)[rng.permutation(pop_n)]
        sizes = sorted(set([1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, pop_n]))
        sizes = [v for v in sizes if v <= pop_n]
        curve_rows=[]
        for size in sizes:
            vals=shuffled[:size]
            curve_rows.append({"Sample size":size,"Sample mean":float(np.mean(vals)),"Sample median":float(np.median(vals)),"Mean absolute error":abs(float(np.mean(vals))-population_mean),"Median absolute error":abs(float(np.median(vals))-population_median)})
        curve=pd.DataFrame(curve_rows)
        fig, ax=plt.subplots(figsize=(9,4.4))
        ax.plot(curve["Sample size"],curve["Sample mean"],marker="o",label="Sample mean")
        ax.plot(curve["Sample size"],curve["Sample median"],marker="s",label="Sample median")
        ax.axhline(population_mean,linestyle="--",label=f"Population mean = {population_mean:.3f}")
        ax.axhline(population_median,linestyle=":",label=f"Population median = {population_median:.3f}")
        ax.set_xscale("log")
        ax.set_xlabel("Sample size (log scale)")
        ax.set_ylabel(variable)
        ax.set_title("Sample estimates versus population parameters")
        ax.grid(alpha=.2); ax.legend(); fig.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close(fig)
        with st.expander("Show convergence values"):
            st.dataframe(curve, use_container_width=True, hide_index=True)
else:
    sample_counts = series.astype(str).value_counts(normalize=True)
    pop_counts = population_series.astype(str).value_counts(normalize=True)
    comparison = pd.DataFrame([
        {"Measure": "Mode", "Population parameter": display_mode(pop_mode_values), "Sample estimate": display_mode(sample_mode_values), "Exact match?": set(map(str, sample_mode_values)) == set(map(str, pop_mode_values))},
    ])
    st.dataframe(comparison, use_container_width=True, hide_index=True)
    pop_mode_label = str(pop_mode_values[0]) if pop_mode_values else None
    pop_prop = float(pop_counts.get(pop_mode_label, 0.0)) if pop_mode_label is not None else np.nan
    sample_prop = float(sample_counts.get(pop_mode_label, 0.0)) if pop_mode_label is not None else np.nan
    st.write(f"Population modal category: **{pop_mode_label}**. Its population proportion is **{pop_prop:.3%}**; its proportion in your sample is **{sample_prop:.3%}**.")
    st.caption("Categorical variables do not have a numerical mean or standard deviation. For nominal data, compare the sample mode and category proportions with the population values.")

st.info("Sampling principle: larger samples generally give more stable estimates, but a particular estimate can move farther from the population parameter when the sample size increases. Random sampling variation does not decrease monotonically.")
