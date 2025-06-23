import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Indonesian Companies Financial Comparison Tool",
    layout="wide"
)

# --- Embedded Financial Data ---
def get_embedded_data():
    # Embedded data for 10 Indonesian companies (2020-2024)
    from collections import OrderedDict
    companies = OrderedDict({
        "PT_Bank_Rakyat_Indonesia_BBRI": [45.2, 98.5, 25.1, 1456.0, 1205.8, 33.4, 48.2, 17.5],
        "PT_Bank_Central_Asia_BBCA": [38.7, 75.2, 28.1, 1021.8, 825.4, 30.2, 50.1, 18.1],
        "PT_Bank_Mandiri_BMRI": [41.5, 89.3, 22.2, 1598.2, 1321.8, 28.5, 46.3, 17.0],
        "PT_Astra_International_ASII": [28.5, 185.9, 12.8, 295.4, 98.2, 25.3, 36.7, 14.8],
        "PT_Telkom_Indonesia_TLKM": [22.8, 64.1, 15.3, 189.2, 42.7, 27.2, 40.1, 30.5],
        "PT_Indofood_Sukses_Makmur_INDF": [18.7, 76.6, 4.2, 89.3, 35.8, 18.8, 34.6, 16.2],
        "PT_Unilever_Indonesia_UNVR": [8.9, 41.2, 7.2, 18.5, 2.1, 10.4, 52.3, 21.0],
        "PT_Gudang_Garam_GGRM": [12.8, 68.7, 6.9, 67.8, 15.2, 12.5, 37.4, 19.6],
        "PT_Semen_Indonesia_SMGR": [8.2, 28.9, 1.8, 48.7, 18.9, 9.1, 30.2, 22.5],
        "PT_Pertamina_PGAS": [15.6, 42.3, 2.1, 78.9, 28.7, 20.5, 29.8, 24.9]
    })

    years = [2020, 2021, 2022, 2023, 2024]
    metrics = ["EBITDA", "Revenue", "Net Income", "Total Assets", "Total Debt", "Cash Flow", "Gross Margin %", "Operating Margin %"]

    data = {}
    for name, base_values in companies.items():
        rows = [
            [0, "Year"] + [str(y) for y in years],
            [0, ""] + [str(y) for y in years]
        ]
        for i, metric in enumerate(metrics):
            row = [0, metric]
            for j in range(len(years)):
                row.append(round(base_values[i] * (1 + 0.05 * j), 2))
            rows.append(row)
        df = pd.DataFrame(rows)
        data[name] = df

    return data

# --- Metric Extraction ---
def extract_metric(df, metric_name):
    df[1] = df[1].astype(str)

    # Extract years from the second row
    year_row = df.iloc[0, 2:].tolist()
    years = [str(int(y)) if str(y).isdigit() else y for y in year_row]

    match_row = df[df[1].str.lower().str.strip() == metric_name.lower().strip()]
    if not match_row.empty:
        values = match_row.iloc[0, 2:].tolist()
        min_len = min(len(values), len(years))
        return pd.DataFrame({"Year": years[:min_len], "Value": values[:min_len]})
    else:
        return pd.DataFrame({"Year": years, "Value": [None] * len(years)})

# --- App Interface ---
st.title("🇮🇩 Indonesian Companies Financial Comparison Tool")

st.header("1. Choose Data Source")
data_source = st.radio("Select data source:", ["Use Indonesian Companies Data", "Upload Excel Files"], index=0)

company_data = {}
if data_source == "Use Indonesian Companies Data":
    company_data = get_embedded_data()
    st.success("✅ Using embedded financial data.")
else:
    uploaded_files = st.file_uploader("Upload Excel files", type=["xlsx", "xls"], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            try:
                df = pd.read_excel(file, sheet_name=0, header=None)
                company_data[file.name.split('.')[0]] = df
                st.success(f"✅ Loaded {file.name}")
            except Exception as e:
                st.error(f"❌ Failed to load {file.name}: {e}")

if company_data:
    st.header("2. Select Metric")

    def get_available_metrics(dfs):
        metrics = set()
        for df in dfs.values():
            if len(df.columns) > 1:
                labels = df.iloc[2:, 1].astype(str).str.lower().str.strip().tolist()
                metrics.update([m for m in labels if m not in ["year", "", "nan"]])
        return sorted(metrics)

    all_metrics = get_available_metrics(company_data)
    if all_metrics:
        default_idx = all_metrics.index("ebitda") if "ebitda" in all_metrics else 0
        selected_metric = st.selectbox("Select a metric to compare:", all_metrics, index=default_idx)

        st.header(f"3. Comparison of '{selected_metric.upper()}'")

        plot_df = pd.DataFrame()
        for name, df in company_data.items():
            extracted = extract_metric(df, selected_metric)
            if not extracted.empty:
                extracted["Company"] = name.replace("PT_", "").replace("_", " ")
                plot_df = pd.concat([plot_df, extracted], ignore_index=True)

        if not plot_df.empty:
            plot_df["Year"] = plot_df["Year"].astype(str)
            plot_df["Value"] = pd.to_numeric(plot_df["Value"], errors="coerce")
            plot_df.dropna(subset=["Value"], inplace=True)

            st.plotly_chart(px.line(plot_df, x="Year", y="Value", color="Company", markers=True), use_container_width=True)

            st.dataframe(plot_df.pivot_table(index="Year", columns="Company", values="Value"), use_container_width=True)

            st.download_button("📥 Download CSV", data=plot_df.to_csv(index=False), file_name="comparison_data.csv", mime="text/csv")
        else:
            st.warning("No data found for the selected metric.")
    else:
        st.error("No metrics found in the data.")
