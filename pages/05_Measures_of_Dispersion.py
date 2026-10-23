import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Measures of Dispersion Lab", page_icon="📏", layout="wide")
st.title("📏 Measures of Dispersion Practice Lab")
st.caption("Range • Quartiles • IQR • Mean absolute deviation • Variance • Standard deviation • Coefficient of variation • Sample-to-population comparison")

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "Advanced_Health_Records_10000_with_Left_Skew.xlsx"

@st.cache_data
def load_data(path):
    return pd.read_excel(path)

def fmt(x, digits=4):
    if x is None or pd.isna(x):
        return "Not defined"
    return f"{float(x):,.{digits}f}"

try:
    df = load_data(str(DATA_FILE))
except Exception as exc:
    st.error(f"Could not load the bundled dataset: {exc}")
    st.stop()

st.info(f"Teaching dataset: {len(df):,} records and {len(df.columns)} columns. It is provided for statistical practice, not as verified clinical evidence.")
with st.expander("Learning objectives and formula guide"):
    st.markdown("""
    - **Range** = maximum − minimum.
    - **Interquartile range (IQR)** = Q3 − Q1; it describes the spread of the middle 50% of observations.
    - **Mean absolute deviation about the mean** = average of |x − x̄|.
    - **Sample variance** = Σ(x − x̄)²/(n − 1); **sample SD** is the square root of sample variance.
    - **Population variance** = Σ(x − μ)²/N; **population SD** is its square root.
    - **Coefficient of variation (CV)** = SD/mean × 100%, usually interpreted for ratio-scale data with a meaningful non-zero mean.

    Sample variance is calculated with the conventional sample-variance formula, and population variance is calculated using all usable population records. The lab focuses on comparing sample estimates with the population parameter as sample size changes.
    """)

numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) and str(c).lower() not in {"id"}]
if not numeric_cols:
    st.warning("No numeric variables are available in the dataset.")
    st.stop()

st.markdown("## Step 1 — Select a variable and sample size")
left, right = st.columns([2, 1])
with left:
    variable = st.selectbox("Select a numerical variable", numeric_cols, index=numeric_cols.index("Age") if "Age" in numeric_cols else 0)
valid_all = pd.to_numeric(df[variable], errors="coerce").dropna()
max_n = int(len(valid_all))
with right:
    sample_n = st.number_input("Your sample size", min_value=1, max_value=max(1, max_n), value=min(100, max(1, max_n)), step=1, help=f"Choose any whole number from 1 to {max_n:,} usable values.")
st.caption(f"Available non-missing values for {variable}: {max_n:,}. Sampling is without replacement.")

if "disp_sample" not in st.session_state:
    st.session_state.disp_sample = None
if "disp_meta" not in st.session_state:
    st.session_state.disp_meta = None
if st.button("🎲 Generate / regenerate random sample", type="primary"):
    st.session_state.disp_sample = valid_all.sample(n=int(sample_n), replace=False, random_state=None).reset_index(drop=True)
    st.session_state.disp_meta = {"variable": variable, "n": int(sample_n)}
    for key in ["disp_answers_checked", "disp_df_choice_saved", "disp_df_checked", "disp_extra_value", "disp_extra_applied"]:
        st.session_state.pop(key, None)

if st.session_state.disp_sample is None:
    st.warning("Choose a variable and sample size, then generate your sample to begin.")
    st.stop()
meta = st.session_state.disp_meta or {}
if meta.get("variable") != variable or meta.get("n") != int(sample_n):
    st.warning("Your variable or sample size has changed. Generate a new sample to apply the change.")
    st.stop()

s = pd.to_numeric(st.session_state.disp_sample, errors="coerce").dropna().reset_index(drop=True)
n = len(s)
if n == 0:
    st.error("No valid numeric values were sampled. Choose another variable or generate a new sample.")
    st.stop()

st.success(f"Sample generated: {n:,} valid observations.")
with st.expander("Preview sample values"):
    st.dataframe(pd.DataFrame({variable: s}), use_container_width=True, hide_index=True)

# Compute all core measures
mean = float(s.mean())
minimum, maximum = float(s.min()), float(s.max())
range_value = maximum - minimum
q1, median, q3 = [float(v) for v in s.quantile([.25, .5, .75]).tolist()]
iqr = q3 - q1
mad_mean = float(np.mean(np.abs(s.to_numpy(dtype=float) - mean)))
ss = float(np.sum((s.to_numpy(dtype=float) - mean) ** 2))
sample_var = ss / (n - 1) if n > 1 else np.nan
sample_sd = float(np.sqrt(sample_var)) if n > 1 else np.nan
pop_var = ss / n
pop_sd = float(np.sqrt(pop_var))
cv = (sample_sd / mean * 100) if n > 1 and mean != 0 else np.nan

st.markdown("## Step 2 — Explore the spread visually")
show_mean = st.checkbox("Show mean on histogram", value=True)
bins = st.slider("Number of histogram bins", min_value=5, max_value=60, value=20)
fig, ax = plt.subplots(figsize=(9, 4.2))
ax.hist(s, bins=bins, edgecolor="black")
if show_mean:
    ax.axvline(mean, linestyle="--", linewidth=2, label=f"Mean = {mean:.3f}")
ax.set_title(f"Sample distribution: {variable} (n={n:,})")
ax.set_xlabel(variable)
ax.set_ylabel("Frequency")
if show_mean:
    ax.legend()
ax.grid(axis="y", alpha=.2)
fig.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)

st.markdown("## Step 3 — Calculate and inspect measures of dispersion")
st.caption("Review the measures, then complete the prediction activity below. Sample variance and SD are undefined for n = 1.")
cols = st.columns(4)
cols[0].metric("Range", fmt(range_value))
cols[1].metric("IQR (Q3 − Q1)", fmt(iqr))
cols[2].metric("Mean absolute deviation", fmt(mad_mean))
cols[3].metric("Coefficient of variation", f"{cv:.2f}%" if pd.notna(cv) else "Not defined")
cols = st.columns(4)
cols[0].metric("Minimum", fmt(minimum))
cols[1].metric("Q1", fmt(q1))
cols[2].metric("Median", fmt(median))
cols[3].metric("Q3", fmt(q3))
cols = st.columns(4)
cols[0].metric("Maximum", fmt(maximum))
cols[1].metric("Sum of squared deviations", fmt(ss))
cols[2].metric("Sample variance", fmt(sample_var))
cols[3].metric("Sample SD", fmt(sample_sd))

with st.expander("Show formulas and calculation details"):
    st.write(f"n = {n}; mean = {fmt(mean)}; Σ(x − x̄)² = {fmt(ss)}")
    st.latex(r"\text{Range}=x_{\max}-x_{\min}")
    st.latex(r"\mathrm{IQR}=Q_3-Q_1")
    st.latex(r"s^2=\frac{\sum (x_i-\bar{x})^2}{n-1},\qquad s=\sqrt{s^2}")
    st.latex(r"\sigma^2=\frac{\sum (x_i-\mu)^2}{N},\qquad \sigma=\sqrt{\sigma^2}")
    st.latex(r"\mathrm{CV}=\frac{s}{\bar{x}}\times100\%")

st.markdown("## Step 4 — Student prediction and answer check")
st.write("Before checking the results, enter your estimates for the range, IQR and sample standard deviation. Answers are checked using a small rounding tolerance.")
with st.form("disp_prediction_form"):
    c1, c2, c3 = st.columns(3)
    pred_range = c1.number_input("Your range", value=0.0, format="%.6f", key="disp_pred_range")
    pred_iqr = c2.number_input("Your IQR", value=0.0, format="%.6f", key="disp_pred_iqr")
    pred_sd = c3.number_input("Your sample SD", value=0.0, format="%.6f", key="disp_pred_sd")
    submitted = st.form_submit_button("Check my answers")
if submitted:
    st.session_state.disp_answers_checked = True
    st.session_state.disp_answers = {"range": pred_range, "iqr": pred_iqr, "sd": pred_sd}
if st.session_state.get("disp_answers_checked", False):
    answers = st.session_state.disp_answers
    targets = {"range": range_value, "iqr": iqr, "sd": sample_sd}
    score = 0
    for key, label in [("range", "Range"), ("iqr", "IQR"), ("sd", "Sample SD")]:
        target = targets[key]
        submitted_value = answers[key]
        if pd.notna(target) and np.isclose(submitted_value, target, rtol=0.01, atol=0.02):
            st.success(f"{label}: correct within tolerance. Reference value = {fmt(target)}.")
            score += 1
        elif pd.isna(target):
            st.info(f"{label}: not defined for this sample size.")
        else:
            st.warning(f"{label}: check your calculation. Reference value = {fmt(target)}.")
    st.metric("Prediction score", f"{score}/3")

st.markdown("## Step 6 — What happens when an extreme value is added?")
st.write("Enter a hypothetical additional observation. Compare range, IQR and sample SD before and after adding it. This is a simulation, not a modification of the source dataset.")
with st.form("disp_outlier_form"):
    extreme = st.number_input("Hypothetical added value", value=float(maximum + max(1, abs(maximum-minimum))), format="%.4f", key="disp_extra_value_input")
    apply_extreme = st.form_submit_button("Compare before and after")
if apply_extreme:
    st.session_state.disp_extra_value = float(extreme)
    st.session_state.disp_extra_applied = True
if st.session_state.get("disp_extra_applied", False):
    extra = float(st.session_state.disp_extra_value)
    altered = pd.concat([s, pd.Series([extra])], ignore_index=True)
    altered_sd = float(altered.std(ddof=1)) if len(altered) > 1 else np.nan
    altered_iqr = float(altered.quantile(.75) - altered.quantile(.25))
    compare = pd.DataFrame([
        {"Measure": "Range", "Original sample": range_value, "With added value": float(altered.max()-altered.min())},
        {"Measure": "IQR", "Original sample": iqr, "With added value": altered_iqr},
        {"Measure": "Sample SD", "Original sample": sample_sd, "With added value": altered_sd},
    ])
    st.dataframe(compare, use_container_width=True, hide_index=True)
    st.caption("The range and SD are sensitive to extreme observations. The IQR is often more resistant, although its value can still change depending on sample size and quartile calculation.")

st.markdown("## Step 7 — Choose a suitable measure of spread")
with st.form("disp_measure_choice_form"):
    choice = st.radio("Which measure is usually more resistant to extreme values?", ["Range", "Standard deviation", "Interquartile range (IQR)", "Coefficient of variation"], index=None)
    choice_submit = st.form_submit_button("Check choice")
if choice_submit:
    st.session_state.disp_df_choice_saved = choice
    st.session_state.disp_df_checked = True
if st.session_state.get("disp_df_checked", False):
    if st.session_state.disp_df_choice_saved == "Interquartile range (IQR)":
        st.success("Correct. IQR describes the middle 50% and is generally less affected by extreme values than range or SD.")
    else:
        st.warning("Review the definitions. IQR is based on Q1 and Q3, so it is generally more resistant to extreme values than range or SD.")

st.download_button("Download sample values as CSV", pd.DataFrame({variable: s}).to_csv(index=False).encode("utf-8"), file_name=f"{variable}_dispersion_sample.csv", mime="text/csv")


st.markdown("## Step 7 — Compare sample SD with the population σ")
population_values = pd.to_numeric(df[variable], errors="coerce").dropna().to_numpy(dtype=float)
N_population = len(population_values)
population_mu = float(np.mean(population_values))
population_sigma = float(np.std(population_values, ddof=0))
current_sample_sd = float(np.std(s.to_numpy(dtype=float), ddof=1)) if n > 1 else np.nan
c1, c2, c3 = st.columns(3)
c1.metric("Population size (usable values)", f"{N_population:,}")
c2.metric("Population SD (σ)", fmt(population_sigma))
c3.metric("Current sample SD", fmt(current_sample_sd))
if n > 1:
    st.metric("Absolute difference |s − σ|", fmt(abs(current_sample_sd-population_sigma)))
st.write("The population SD (σ) is calculated from all usable records in the teaching dataset. Compare it with the sample SD from your selected sample. As sample size increases, estimates generally become more stable and their typical error tends to decrease, although a particular sample estimate can move farther from σ when n increases.")

st.markdown("### How does estimation error change as sample size increases?")
st.write("This experiment repeatedly draws random samples from the finite teaching population at each sample size. It plots the average absolute error of the sample SD relative to population σ. Repeated sampling gives a clearer picture of the overall trend than a single sample path.")
if N_population >= 2:
    default_sizes = [2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, N_population]
    sizes_curve = sorted(set(int(v) for v in default_sizes if 2 <= v <= N_population))
    repetitions = st.slider("Random samples per sample size", min_value=20, max_value=200, value=50, step=10, key="disp_trend_repetitions")
    if st.button("Run sample-size estimation experiment", type="primary", key="disp_run_size_trend"):
        rng_curve = np.random.default_rng(20261023)
        trend_rows = []
        for size in sizes_curve:
            abs_errors = []
            sd_estimates = []
            for _ in range(int(repetitions)):
                # Without replacement. At the full population size, the sample equals the population.
                vals = rng_curve.choice(population_values, size=size, replace=False)
                sd_est = float(np.std(vals, ddof=1)) if size > 1 else np.nan
                if np.isfinite(sd_est):
                    sd_estimates.append(sd_est)
                    abs_errors.append(abs(sd_est - population_sigma))
            trend_rows.append({
                "Sample size": size,
                "Mean sample SD across repetitions": float(np.mean(sd_estimates)) if sd_estimates else np.nan,
                "Mean absolute error from σ": float(np.mean(abs_errors)) if abs_errors else np.nan,
                "Population σ": population_sigma,
            })
        trend_df = pd.DataFrame(trend_rows)
        st.session_state["disp_size_trend_result"] = trend_df
    if "disp_size_trend_result" in st.session_state:
        trend_df = st.session_state["disp_size_trend_result"]
        fig, ax = plt.subplots(figsize=(9, 4.2))
        ax.plot(trend_df["Sample size"], trend_df["Mean absolute error from σ"], marker="o", label="Mean absolute error of sample SD")
        ax.set_xscale("log")
        ax.set_xlabel("Sample size (log scale)")
        ax.set_ylabel("Mean absolute error from population σ")
        ax.set_title(f"Sample SD estimation error versus sample size: {variable}")
        ax.grid(alpha=.2)
        ax.legend()
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        with st.expander("Show sample-size experiment results"):
            st.dataframe(trend_df, use_container_width=True, hide_index=True)
        st.caption("The average error will usually tend to decrease as sample size increases, but finite simulation results may not decrease at every point. At the full population size, the conventional sample SD formula is not exactly identical to population σ because sample SD and population SD use different definitions. The key learning objective is that larger samples generally give more precise estimates, not that every estimate is monotonically closer.")
    else:
        st.info("Select the number of repetitions and click **Run sample-size estimation experiment** to generate the graph and table.")

