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
    years = []
    for i in range(10):  # Try first 10 rows
        row_values = df.iloc[i, 2:].tolist()
        numeric_years = pd.to_numeric(row_values, errors="coerce")
        if numeric_years.notna().sum() >= 2:  # at least 2 numbers found
            years = [str(int(y)) if not pd.isna(y) else "" for y in numeric_years]
            break

    if not years:
        years = [f"Year {i}" for i in range(1, df.shape[1] - 1)]

    match_row = df[df[1].str.lower().str.strip() == metric_name.lower().strip()]
    if not match_row.empty:
        values = match_row.iloc[0, 2:].tolist()
        return pd.DataFrame({"Year": years, "Value": values})
    else:
        return pd.DataFrame({"Year": years, "Value": [None] * len(years)})

# --- Metric Selection ---
st.header("2. Select Metrics to Compare")
all_metrics = get_available_metrics(company_data)
search_input = st.text_input("Search for a metric (e.g., EBITDA, Revenue, Profit)").lower()
filtered_metrics = [m for m in all_metrics if search_input in m]
selected_metric = st.selectbox(
    "Select a metric to compare",
    options=filtered_metrics if filtered_metrics else all_metrics
)

# --- Comparison View ---
if selected_metric:
    st.header(f"3. Comparison of '{selected_metric.upper()}'")
    tab1, tab2 = st.tabs(["Chart View", "Table View"])
    plot_df = pd.DataFrame()

    for name, df in company_data.items():
        extracted = extract_metric(df, selected_metric)
        if not extracted.empty:
            extracted["Company"] = name
            plot_df = pd.concat([plot_df, extracted])

    if not plot_df.empty:
        plot_df["Year"] = plot_df["Year"].astype(str)

        # Optional Year Filter
        available_years = sorted(plot_df["Year"].dropna().unique())
        selected_years = st.multiselect("Filter by year (optional)", options=available_years, default=available_years)
        plot_df = plot_df[plot_df["Year"].isin(selected_years)]

        with tab1:
            fig = px.line(
                plot_df,
                x="Year", y="Value", color="Company", markers=True,
                title=f"{selected_metric.upper()} Comparison"
            )
            fig.update_layout(
                xaxis_title="Year",
                yaxis_title=selected_metric.upper(),
                legend_title="Company"
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            pivot = plot_df.pivot_table(index="Year", columns="Company", values="Value", aggfunc="first")
            st.dataframe(pivot, use_container_width=True)
            csv = pivot.to_csv()
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name=f"{selected_metric}_comparison.csv",
                mime="text/csv"
            )
    else:
        st.warning("No matching data found across uploaded files.")
