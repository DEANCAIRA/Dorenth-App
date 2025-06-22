import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Financial Metrics Comparison Tool",
    layout="wide"
)

# --- Title & Description ---
st.title("📊 Financial Metrics Comparison Tool")
st.write("""
This app allows you to compare financial metrics across multiple companies. 
Upload Excel files containing financial data and select metrics to compare.
""")

# --- Upload Section ---
st.header("1. Upload Financial Data")
uploaded_files = st.file_uploader(
    "Upload Excel files containing financial data",
    type=["xlsx", "xls"],
    accept_multiple_files=True
)

company_data = {}
if uploaded_files:
    for file in uploaded_files:
        try:
            df = pd.read_excel(file, sheet_name="Sheet1", header=None)
            company_name = file.name.split('.')[0]
            company_data[company_name] = df
        except Exception as e:
            st.error(f"Failed to read {file.name}: {e}")

# --- Use sample data if no upload ---
if not company_data:
    st.info("No files uploaded. Using sample data for demonstration.")
    df_alpha = pd.DataFrame({
        0: [0, "Year", "EBITDA", "Revenue", "% Margin"],
        1: [0, "", "EBITDA", "Revenue", "% Margin"],
        2: [0, 2020, 100, 500, 20],
        3: [0, 2021, 120, 550, 22],
        4: [0, 2022, 140, 600, 23]
    })
    df_omega = pd.DataFrame({
        0: [0, "Year", "EBITDA", "Revenue", "% Margin"],
        1: [0, "", "EBITDA", "Revenue", "% Margin"],
        2: [0, 2020, 80, 400, 18],
        3: [0, 2021, 90, 450, 19],
        4: [0, 2022, 100, 480, 21]
    })
    company_data = {
        "ALPHA": df_alpha,
        "OMEGA": df_omega
    }

# --- Metric Extraction Logic ---
def get_available_metrics(dataframes):
    metrics = set()
    for df in dataframes.values():
        labels = df[1].astype(str).str.lower().str.strip().tolist()
        metrics.update([m for m in labels if m and m not in ['year', '']])
    return sorted(metrics)

def extract_metric(df, metric_name):
    df[1] = df[1].astype(str)

    # Auto-detect year row
    for i in range(5):
        row_values = df.iloc[i, 2:].tolist()
        if all(isinstance(v, (int, float)) or str(v).startswith("20") for v in row_values):
            years = [str(int(v)) if isinstance(v, (int, float)) and not pd.isna(v) else str(v) for v in row_values]
            break
    else:
        years = [f"Year {i}" for i in range(1, df.shape[1] - 2 + 1)]

    match_row = df[df[1].str.lower().str.strip() == metric_name.lower().strip()]
    if not match_row.empty:
        values = match_row.iloc[0, 2:].tolist()
        return pd.DataFrame({"Year": years, "Value": values})
    else:
