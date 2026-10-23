import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Descriptive Statistics Lab", page_icon="📈", layout="wide")
st.title("📈 Descriptive Statistics Lab")
st.caption("Mean • Median • Mode • Range • Quartiles • IQR • Variance • Standard deviation • Skewness")

DEFAULT_FILE = Path(__file__).resolve().parents[1] / "data" / "Advanced_Health_Records_10000_with_Left_Skew.xlsx"

@st.cache_data
def load_default(path):
    return pd.read_excel(path)

def read_upload(uploaded):
    if uploaded is None:
        return None
    name = uploaded.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded)
    return pd.read_excel(uploaded)

uploaded = st.file_uploader("Optional: upload your own Excel or CSV dataset", type=["xlsx", "xls", "csv"], key="stats_upload")
try:
    if uploaded is not None:
        df = read_upload(uploaded)
        source_label = uploaded.name
    else:
        df = load_default(DEFAULT_FILE)
        source_label = DEFAULT_FILE.name
except Exception as e:
    st.error(f"Could not read the file: {e}")
    st.stop()

st.success(f"Dataset loaded: {source_label} · {len(df):,} rows · {len(df.columns):,} columns")
with st.expander("Preview data"):
    st.dataframe(df.head(20), use_container_width=True)
    st.write("Column types")
    st.dataframe(pd.DataFrame({"Column":df.columns.astype(str), "Data type":df.dtypes.astype(str).values, "Missing values":df.isna().sum().values}), use_container_width=True)

numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) and c.lower() not in {"id"}]
if not numeric_cols:
    st.warning("No numeric columns were detected.")
    st.stop()

left, right = st.columns([2,1])
with left:
    selected = st.selectbox("Choose a numerical variable", numeric_cols, index=numeric_cols.index("Age") if "Age" in numeric_cols else 0)
with right:
    variance_mode = st.radio("Variance / SD convention", ["Sample (n − 1)", "Population (n)"], horizontal=False,
                             help="Sample uses n−1 for variance; population uses N.")
s = pd.to_numeric(df[selected], errors="coerce").dropna()
n = len(s)
if n == 0:
    st.warning("The selected column has no numeric observations.")
    st.stop()

ddof = 1 if variance_mode == "Sample (n − 1)" else 0
variance = float(s.var(ddof=ddof)) if (ddof == 0 or n > 1) else np.nan
sd = float(s.std(ddof=ddof)) if (ddof == 0 or n > 1) else np.nan
q1, median, q3 = s.quantile([0.25,0.5,0.75]).tolist()
mode_values = s.mode().tolist()
mode_text = ", ".join(f"{x:g}" for x in mode_values[:5]) + (" …" if len(mode_values)>5 else "")
skew = float(s.skew()) if n >= 3 else np.nan

st.markdown("### Numerical summary")
m1,m2,m3,m4 = st.columns(4)
m1.metric("Valid n", f"{n:,}")
m2.metric("Mean", f"{s.mean():,.4f}")
m3.metric("Median", f"{median:,.4f}")
m4.metric("Mode", mode_text if mode_text else "No mode")
m1,m2,m3,m4 = st.columns(4)
m1.metric("Minimum", f"{s.min():,.4f}")
m2.metric("Maximum", f"{s.max():,.4f}")
m3.metric("Range", f"{s.max()-s.min():,.4f}")
m4.metric("IQR (Q3 − Q1)", f"{q3-q1:,.4f}")
m1,m2,m3,m4 = st.columns(4)
m1.metric("Q1 (25th percentile)", f"{q1:,.4f}")
m2.metric("Q3 (75th percentile)", f"{q3:,.4f}")
m3.metric(f"{'Sample' if ddof else 'Population'} variance", f"{variance:,.5f}" if pd.notna(variance) else "n too small")
m4.metric(f"{'Sample' if ddof else 'Population'} SD", f"{sd:,.5f}" if pd.notna(sd) else "n too small")

st.markdown("### Visualise the distribution")
c1,c2 = st.columns([3,1])
with c2:
    bins = st.slider("Histogram bins", min_value=5, max_value=80, value=30, step=1)
    show_mean = st.checkbox("Show mean", True)
    show_median = st.checkbox("Show median", True)
with c1:
    fig, ax = plt.subplots()
    ax.hist(s, bins=bins, edgecolor="black")
    if show_mean: ax.axvline(s.mean(), linestyle="--", linewidth=2, label=f"Mean = {s.mean():.3f}")
    if show_median: ax.axvline(median, linestyle="-.", linewidth=2, label=f"Median = {median:.3f}")
    ax.set_title(f"Distribution of {selected}")
    ax.set_xlabel(str(selected))
    ax.set_ylabel("Frequency")
    if show_mean or show_median: ax.legend()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

st.markdown("### Interpretation prompts")
if skew > 0.5:
    shape = "positively (right) skewed"
elif skew < -0.5:
    shape = "negatively (left) skewed"
else:
    shape = "approximately symmetric or only mildly skewed"
st.write(f"- **Skewness (software sample skewness):** {skew:.4f}. By a simple teaching rule, the distribution appears **{shape}**. This threshold is only a rough guide; inspect the histogram as well.")
st.write(f"- **Mean vs median:** mean = {s.mean():.4f}; median = {median:.4f}. Their relationship can provide a clue about asymmetry, but it does not prove the distribution's shape.")
st.write(f"- **Spread:** the middle 50% of observations range from Q1 = {q1:.4f} to Q3 = {q3:.4f}, giving IQR = {q3-q1:.4f}.")
st.write(f"- **Variance method:** {variance_mode}. Variance is in squared units; standard deviation is in the same units as the selected variable.")
st.caption("Skewness is computed by pandas' sample skewness convention. Different formulas can produce slightly different values. Quartiles use pandas' default quantile interpolation.")

with st.expander("Show calculation details"):
    st.code(f"""n = {n}
Mean = sum(x) / n = {s.mean():.6f}
Median = {median:.6f}
Minimum = {s.min():.6f}
Maximum = {s.max():.6f}
Range = maximum - minimum = {s.max()-s.min():.6f}
Q1 = {q1:.6f}
Q3 = {q3:.6f}
IQR = Q3 - Q1 = {q3-q1:.6f}
Variance ({'sample, denominator n-1' if ddof else 'population, denominator n'}) = {variance:.8f}
Standard deviation = sqrt(variance) = {sd:.8f}
Skewness (pandas) = {skew:.6f}""")

csv_summary = pd.DataFrame([{
    "variable": selected, "n": n, "mean": s.mean(), "median": median, "mode": mode_text,
    "minimum": s.min(), "maximum": s.max(), "range": s.max()-s.min(), "Q1": q1, "Q3": q3,
    "IQR": q3-q1, "variance_method": variance_mode, "variance": variance, "standard_deviation": sd, "skewness": skew
}])
st.download_button("Download summary as CSV", csv_summary.to_csv(index=False).encode("utf-8"), file_name="descriptive_summary.csv", mime="text/csv")
