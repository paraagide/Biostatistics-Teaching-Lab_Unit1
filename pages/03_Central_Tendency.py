import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Central Tendency", page_icon="🎯", layout="wide")
st.title("🎯 Central Tendency: Mean, Median and Mode")
st.caption("Explore real data, make predictions, check your answers, and investigate the effect of an extreme value.")

DEFAULT_FILE = Path(__file__).resolve().parents[1] / "data" / "Advanced_Health_Records_10000_with_Left_Skew.xlsx"

@st.cache_data
def load_default(path):
    return pd.read_excel(path)

def read_upload(uploaded):
    if uploaded is None:
        return None
    if uploaded.name.lower().endswith(".csv"):
        return pd.read_csv(uploaded)
    return pd.read_excel(uploaded)

def calculate_mode(series):
    modes = series.mode(dropna=True)
    if modes.empty:
        return []
    return modes.tolist()

def fmt_value(value):
    if pd.isna(value):
        return "Not available"
    if isinstance(value, (int, np.integer)) or float(value).is_integer():
        return f"{int(value):,}"
    return f"{float(value):,.3f}"

uploaded = st.file_uploader("Optional: upload your own Excel or CSV dataset", type=["xlsx", "xls", "csv"], key="central_upload")
try:
    df = read_upload(uploaded) if uploaded is not None else load_default(DEFAULT_FILE)
except Exception as e:
    st.error(f"Could not read the file: {e}")
    st.stop()

st.write(f"Loaded **{len(df):,} rows** and **{len(df.columns)} columns**.")
numeric_columns = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) and df[c].notna().any()]
if not numeric_columns:
    st.error("This dataset does not contain a numeric column for this activity.")
    st.stop()

with st.expander("Learning objectives and key ideas", expanded=False):
    st.markdown("""
    - **Mean:** arithmetic average; uses every value and can be strongly affected by extreme observations.
    - **Median:** middle value after sorting; for an even number of observations, average the two middle values.
    - **Mode:** most frequently observed value. A dataset can have no mode or more than one mode.
    - The most appropriate measure depends on the variable type, distribution shape, and question being asked.
    """)

selected = st.selectbox("Choose a numerical variable", numeric_columns, index=numeric_columns.index("Age") if "Age" in numeric_columns else 0)
values = pd.to_numeric(df[selected], errors="coerce").dropna()
if values.empty:
    st.warning("No valid numeric observations are available for this variable.")
    st.stop()

st.markdown("## Activity 1 — Predict, then check")
st.write("First inspect the variable and make your own estimates. Enter your answers below before revealing the calculated values.")
left, right = st.columns([1, 1])
with left:
    st.metric("Valid observations", f"{len(values):,}")
    st.metric("Minimum", fmt_value(values.min()))
with right:
    st.metric("Maximum", fmt_value(values.max()))
    st.metric("Range", fmt_value(values.max() - values.min()))

actual_mean = float(values.mean())
actual_median = float(values.median())
modes = calculate_mode(values)
mode_display = ", ".join(fmt_value(x) for x in modes[:10]) if modes else "No mode"
if len(modes) > 10:
    mode_display += f" (and {len(modes)-10} more)"

with st.form("central_prediction_form"):
    st.markdown("**Your prediction**")
    c1, c2, c3 = st.columns(3)
    with c1:
        predicted_mean = st.number_input("Predicted mean", value=0.0, step=1.0, format="%.4f", key="pred_mean")
    with c2:
        predicted_median = st.number_input("Predicted median", value=0.0, step=1.0, format="%.4f", key="pred_median")
    with c3:
        predicted_mode = st.text_input("Predicted mode(s)", placeholder="Enter value(s), comma-separated", key="pred_mode")
    submitted = st.form_submit_button("Check my predictions")

if submitted:
    tolerance = max(0.01, abs(actual_mean) * 0.005)
    mean_ok = abs(predicted_mean - actual_mean) <= tolerance
    median_ok = abs(predicted_median - actual_median) <= 0.01
    try:
        pred_modes = [float(x.strip()) for x in predicted_mode.split(",") if x.strip()]
        mode_ok = len(pred_modes) == len(modes) and all(any(np.isclose(p, m) for m in modes) for p in pred_modes)
    except ValueError:
        mode_ok = False
    score = int(mean_ok) + int(median_ok) + int(mode_ok)
    st.markdown(f"### Your score: {score}/3")
    if mean_ok:
        st.success("Mean: correct (within the accepted rounding tolerance).")
    else:
        st.info(f"Mean: not quite. Calculated mean = **{fmt_value(actual_mean)}**.")
    if median_ok:
        st.success("Median: correct.")
    else:
        st.info(f"Median: not quite. Calculated median = **{fmt_value(actual_median)}**.")
    if mode_ok:
        st.success("Mode: correct.")
    else:
        st.info(f"Mode: calculated mode(s) = **{mode_display}**. For a multimodal dataset, include all modes shown by the app.")
    st.caption("The mean is accepted within 0.5% of its calculated value (with a minimum tolerance of 0.01) to allow for rounding. The median and mode are checked against observed values.")

if st.button("Reveal calculated answers", key="reveal_central"):
    st.session_state["reveal_central_answers"] = True
if st.session_state.get("reveal_central_answers", False):
    a, b, c = st.columns(3)
    a.metric("Mean", fmt_value(actual_mean))
    b.metric("Median", fmt_value(actual_median))
    c.metric("Mode(s)", mode_display)

st.markdown("## Activity 2 — Visualise the distribution")
show_mean = st.checkbox("Show mean", value=True)
show_median = st.checkbox("Show median", value=True)
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.hist(values, bins="auto", edgecolor="black", alpha=0.75)
if show_mean:
    ax.axvline(actual_mean, linestyle="--", linewidth=2, label=f"Mean = {actual_mean:.2f}")
if show_median:
    ax.axvline(actual_median, linestyle="-", linewidth=2, label=f"Median = {actual_median:.2f}")
ax.set_title(f"Distribution of {selected}")
ax.set_xlabel(str(selected))
ax.set_ylabel("Frequency")
if show_mean or show_median:
    ax.legend()
fig.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)

st.markdown("## Activity 3 — What happens when an extreme value is added?")
st.write("Add one hypothetical high value to a copy of the selected variable. Compare the mean and median before and after. This is a statistical demonstration, not a change to the source dataset.")
max_value = float(values.max())
min_value = float(values.min())
span = max(max_value - min_value, 1.0)
proposed = st.number_input("Hypothetical extreme value", min_value=float(max_value), max_value=float(max_value + span * 100), value=float(max_value + span * 5), step=float(max(span, 1.0)), key="extreme_value")
augmented = pd.concat([values.reset_index(drop=True), pd.Series([proposed])], ignore_index=True)
new_mean = float(augmented.mean())
new_median = float(augmented.median())
change_mean = new_mean - actual_mean
change_median = new_median - actual_median
x1, x2 = st.columns(2)
with x1:
    st.markdown("**Original data**")
    st.metric("Mean", fmt_value(actual_mean))
    st.metric("Median", fmt_value(actual_median))
with x2:
    st.markdown("**After adding one value**")
    st.metric("Mean", fmt_value(new_mean), delta=f"Change: {change_mean:+.3f}")
    st.metric("Median", fmt_value(new_median), delta=f"Change: {change_median:+.3f}")

with st.expander("Interpret your results"):
    st.markdown("""
    1. Did the mean change more than the median?
    2. Why does the mean respond to the magnitude of every observation?
    3. Why can the median be more resistant to an extreme value?
    4. Would you report the mean or median for a strongly skewed distribution? Explain your choice.
    """)

st.markdown("## Activity 4 — Choose the best measure")
st.write("Select the measure that is generally most informative for each situation. These questions test reasoning; in some real analyses, more than one measure may be useful.")
questions = [
    ("A continuous variable is strongly right-skewed because a few observations are very large.", "Median", "The median is resistant to extreme high values."),
    ("A researcher wants the arithmetic average concentration across all sampled batches.", "Mean", "The mean uses the magnitude of every observation."),
    ("A pharmacy wants to identify the most frequently dispensed tablet strength.", "Mode", "The mode identifies the most frequently observed category/value."),
    ("A nominal variable records blood group.", "Mode", "For nominal categories, the mode can identify the most common category; mean and median are not appropriate."),
]
score = 0
for i, (question, answer, explanation) in enumerate(questions, start=1):
    choice = st.radio(f"**Question {i}.** {question}", ["Mean", "Median", "Mode"], key=f"measure_choice_{i}", horizontal=True)
    if st.session_state.get(f"measure_check_{i}", False):
        if choice == answer:
            st.success(f"Correct. {explanation}")
        else:
            st.info(f"Best answer: **{answer}**. {explanation}")
if st.button("Check measure-selection answers"):
    st.session_state["measure_check_1"] = True
    st.session_state["measure_check_2"] = True
    st.session_state["measure_check_3"] = True
    st.session_state["measure_check_4"] = True
    st.rerun()

st.download_button(
    "Download central tendency summary as CSV",
    pd.DataFrame({"Measure": ["Mean", "Median", "Mode(s)"], "Value": [actual_mean, actual_median, mode_display]}).to_csv(index=False).encode("utf-8"),
    file_name=f"{selected}_central_tendency.csv",
    mime="text/csv",
)
st.caption("Dataset note: the bundled records are for teaching and statistical practice. Their summaries should not be treated as clinical advice or as representative of a real patient population without independent evidence about provenance and sampling.")
