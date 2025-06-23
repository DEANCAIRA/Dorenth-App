import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Financial Metrics Comparison Tool", layout="wide")
st.title("📊 Financial Metrics Comparison Tool")

# --- Embedded sample data (you can replace with your actual)
df_alpha = pd.DataFrame({
    0: [0, "Year", "2020", "2021", "2022"],
    1: [0, "", "2020", "2021", "2022"],
    2: [0, "EBITDA", 100, 120, 140],
    3: [0, "Revenue", 500, 550, 600]
}).T.reset_index(drop=True)

df_omega = pd.DataFrame({
    0: [0, "Year", "2020", "2021", "2022"],
    1: [0, "", "2020", "2021", "2022"],
    2: [0, "EBITDA", 80, 90, 100],
    3: [0, "Revenue", 400, 450, 480]
}).T.reset_index(drop=True)

company_data = {
    "ALPHA": df_alpha,
    "OMEGA": df_omega
}

# --- Extract metrics from embedded data
def get_available_metrics(dataframes):
    metrics = set()
    for df in dataframes.values():
        for i in range(2, len(df)):
            metric = df.iloc[i, 1]
            if isinstance(metric, str) and metric.lower().strip() not in ["", "year"]:
                metrics.add(metric.lower().strip())
    return sorted(metrics)

def extract_metric(df, metric_name):
    years = []
    values = []
    for i in range(2, len(df)):
        year = df.iloc[i, 2]
        metric = df.iloc[i, 1]
        value = df.iloc[i, 3] if df.shape[1] > 3 else None

        if str(metric).lower().strip() == metric_name.lower().strip():
            years.append(str(year))
            values.append(value)

    return pd.DataFrame({"Year": years, "Value": values})

# --- UI
st.header("1. Select Metric")
all_metrics = get_available_metrics(company_data)
search = st.text_input("Search metric (e.g. EBITDA)").lower()
filtered_metrics = [m for m in all_metrics if search in m]
selected_metric = st.selectbox("Choose a metric", options=filtered_metrics if filtered_metrics else all_metrics)

if selected_metric:
    st.header(f"2. Comparison of '{selected_metric.upper()}'")
    df_plot = pd.DataFrame()

    for name, df in company_data.items():
        extracted = extract_metric(df, selected_metric)
        if not extracted.empty:
            extracted["Company"] = name
            df_plot = pd.concat([df_plot, extracted])

    if not df_plot.empty:
        df_plot["Year"] = df_plot["Year"].astype(str)

        year_options = sorted(df_plot["Year"].unique())
        selected_years = st.multiselect("Filter by year (optional)", options=year_options, default=year_options)
        df_plot = df_plot[df_plot["Year"].isin(selected_years)]

        tab1, tab2 = st.tabs(["📈 Chart View", "📋 Table View"])

        with tab1:
            fig = px.line(df_plot, x="Year", y="Value", color="Company", markers=True)
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            pivot = df_plot.pivot(index="Year", columns="Company", values="Value")
            st.dataframe(pivot, use_container_width=True)
            csv = pivot.to_csv()
            st.download_button("Download CSV", data=csv, file_name=f"{selected_metric}_comparison.csv", mime="text/csv")
    else:
        st.warning("No data found for the selected metric.")
