import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Frequency Distributions", page_icon="📊", layout="wide")
st.title("📊 Frequency Distributions")
st.caption("Categorical counts • Ungrouped frequency • Grouped frequency • Relative and cumulative frequency")

DEFAULT_FILE = Path(__file__).resolve().parents[1] / "data" / "Advanced_Health_Records_10000_with_Left_Skew.xlsx"

@st.cache_data
def load_default(path):
    return pd.read_excel(path)

def read_upload(uploaded):
    if uploaded is None: return None
    if uploaded.name.lower().endswith(".csv"): return pd.read_csv(uploaded)
    return pd.read_excel(uploaded)

uploaded = st.file_uploader("Optional: upload your own Excel or CSV dataset", type=["xlsx", "xls", "csv"], key="freq_upload")
try:
    df = read_upload(uploaded) if uploaded is not None else load_default(DEFAULT_FILE)
except Exception as e:
    st.error(f"Could not read the file: {e}")
    st.stop()

st.write(f"Loaded **{len(df):,} rows** and **{len(df.columns)} columns**.")
with st.expander("Preview data"):
    st.dataframe(df.head(15), use_container_width=True)

columns = list(df.columns)
selected = st.selectbox("Choose a variable", columns, index=columns.index("Age") if "Age" in columns else 0)
series = df[selected].dropna()
if series.empty:
    st.warning("The selected column contains no non-missing values.")
    st.stop()

is_numeric = pd.api.types.is_numeric_dtype(series)
st.write(f"**Variable type detected:** {'Numerical' if is_numeric else 'Categorical/text'} · **Valid observations:** {len(series):,} · **Missing:** {df[selected].isna().sum():,}")

if is_numeric:
    mode = st.radio("Frequency table type", ["Grouped intervals", "Ungrouped exact values"], horizontal=True)
    if mode == "Grouped intervals":
        values = pd.to_numeric(series, errors="coerce").dropna().astype(float)
        data_min, data_max = float(values.min()), float(values.max())
        st.markdown("### Student task: construct your own class intervals")
        st.write(f"Data range: **{data_min:g} to {data_max:g}** · Range = **{data_max - data_min:g}** · Valid observations = **{len(values):,}**")
        st.write("Decide the class boundaries yourself. Enter boundaries in increasing order, separated by commas. The first boundary must be at or below the minimum and the last boundary must be at or above the maximum.")
        boundary_text = st.text_input(
            "Your class boundaries",
            value="",
            placeholder=f"Example only: {data_min:g}, ... , {data_max:g}",
            help="For equal-width classes, use equally spaced boundaries. Unequal-width classes are also allowed. Do not repeat a boundary."
        )
        if not boundary_text.strip():
            st.info("Enter your boundaries to generate the frequency table. For example, decide how many classes you want, calculate a suitable class width, and type all class boundaries.")
            st.stop()
        try:
            edges = np.array([float(item.strip()) for item in boundary_text.split(",") if item.strip() != ""], dtype=float)
        except ValueError:
            st.error("Please enter numbers only, separated by commas.")
            st.stop()
        if len(edges) < 2:
            st.error("Enter at least two boundaries to create one class interval.")
            st.stop()
        if not np.all(np.diff(edges) > 0):
            st.error("Boundaries must be strictly increasing, with no repeated values.")
            st.stop()
        if edges[0] > data_min or edges[-1] < data_max:
            st.error(f"Your boundaries must cover the full data range ({data_min:g} to {data_max:g}). Adjust the first and/or last boundary.")
            st.stop()

        counts, _ = np.histogram(values.to_numpy(), bins=edges)
        labels = []
        for i in range(len(edges) - 1):
            closing = "]" if i == len(edges) - 2 else ")"
            labels.append(f"[{edges[i]:g}, {edges[i+1]:g}{closing}")
        table = pd.DataFrame({"Class interval": labels, "Lower boundary": edges[:-1], "Upper boundary": edges[1:], "Frequency": counts})
        table["Relative frequency"] = table["Frequency"] / counts.sum()
        table["Percentage (%)"] = table["Relative frequency"] * 100
        table["Cumulative frequency"] = table["Frequency"].cumsum()
        table["Cumulative percentage (%)"] = table["Percentage (%)"].cumsum()
        st.success(f"You created **{len(edges)-1} class intervals**. Total frequency = **{counts.sum():,}**.")
        widths = np.diff(edges)
        if np.allclose(widths, widths[0]):
            st.write(f"Your class width is **{widths[0]:g}** (equal-width intervals).")
        else:
            st.write("Your intervals have unequal widths. When comparing histogram bar heights, consider using frequency density (frequency ÷ class width).")
        st.dataframe(table, use_container_width=True, hide_index=True)
        fig, ax = plt.subplots()
        ax.hist(values.to_numpy(), bins=edges, edgecolor="black")
        ax.set_title(f"Histogram of {selected} using student-defined intervals")
        ax.set_xlabel(str(selected)); ax.set_ylabel("Frequency")
        st.pyplot(fig, use_container_width=True); plt.close(fig)
        st.caption("Intervals are left-closed and right-open, [a, b), except the final interval, which includes its upper boundary. The app counts observations using the boundaries you entered.")
    else:
        if series.nunique() > 200:
            st.warning(f"This variable has {series.nunique():,} distinct observed values. The exact-value table is limited to the 200 most frequent values.")
        vc = series.value_counts().head(200).sort_index()
        table = pd.DataFrame({"Value": vc.index.astype(str), "Frequency": vc.values})
        total = len(series)
        table["Relative frequency"] = table["Frequency"] / total
        table["Percentage (%)"] = table["Relative frequency"] * 100
        table["Cumulative frequency"] = table["Frequency"].cumsum()
        st.dataframe(table, use_container_width=True, hide_index=True)
else:
    vc = series.astype(str).value_counts(dropna=False)
    table = pd.DataFrame({"Category": vc.index, "Frequency": vc.values})
    table["Relative frequency"] = table["Frequency"] / vc.sum()
    table["Percentage (%)"] = table["Relative frequency"] * 100
    table["Cumulative frequency"] = table["Frequency"].cumsum()
    st.dataframe(table, use_container_width=True, hide_index=True)
    fig, ax = plt.subplots()
    vc.plot(kind="bar", ax=ax)
    ax.set_title(f"Frequency by {selected}")
    ax.set_xlabel(str(selected)); ax.set_ylabel("Frequency")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True); plt.close(fig)
    st.caption("Cumulative frequency is mathematically calculable for categories, but is only substantively meaningful when the categories have a natural order.")

st.download_button("Download frequency table as CSV", table.to_csv(index=False).encode("utf-8"), file_name="frequency_distribution.csv", mime="text/csv")
