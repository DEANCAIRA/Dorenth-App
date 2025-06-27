import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="M&A Decision Support Tool - Indonesian Companies",
    layout="wide"
)

# Load data
def get_embedded_ma_data():
    # [Simulated embedded data for demonstration. Replace with full embedded dataset logic.]
    return {
        "Food_PT_SampleCompany": pd.DataFrame([
            [0, "Year", "2020", "2021", "2022", "2023", "2024"],
            [0, "EBITDA", 5, 5.5, 6, 6.5, 7],
            [0, "EV_EBITDA_Multiple", 8, 8.5, 9, 9.5, 10],
            [0, "Debt_EBITDA_Ratio", 2, 2.1, 2.2, 2.3, 2.4],
            [0, "ROE_Percent", 14, 15, 16, 17, 18]
        ])
    }

def extract_metric(df, metric_name):
    df[1] = df[1].astype(str)
    year_row = df.iloc[0, 2:].tolist()
    years = [str(int(y)) if str(y).replace('.', '').isdigit() else y for y in year_row]
    match_row = df[df[1].str.lower().str.strip() == metric_name.lower().strip()]
    if not match_row.empty:
        values = match_row.iloc[0, 2:].tolist()
        min_len = min(len(values), len(years))
        return pd.DataFrame({"Year": years[:min_len], "Value": values[:min_len]})
    else:
        return pd.DataFrame({"Year": years, "Value": [None] * len(years)})

def calculate_ma_metrics(company_data, selected_companies):
    ma_summary = []
    for company in selected_companies:
        if company in company_data:
            df = company_data[company]
            ebitda = extract_metric(df, "EBITDA")
            revenue = extract_metric(df, "Revenue")
            ev = extract_metric(df, "Enterprise_Value")
            market_cap = extract_metric(df, "Market_Cap")
            ev_ebitda = extract_metric(df, "EV_EBITDA_Multiple")
            debt_ebitda = extract_metric(df, "Debt_EBITDA_Ratio")
            roe = extract_metric(df, "ROE_Percent")
            ma_summary.append({
                "Company": company,
                "EBITDA_2024": float(ebitda.iloc[-1]["Value"]),
                "Revenue_2024": float(revenue.iloc[-1]["Value"]),
                "Enterprise_Value_2024": float(ev.iloc[-1]["Value"]),
                "Market_Cap_2024": float(market_cap.iloc[-1]["Value"]),
                "EV_EBITDA_Multiple": float(ev_ebitda.iloc[-1]["Value"]),
                "Debt_EBITDA_Ratio": float(debt_ebitda.iloc[-1]["Value"]),
                "ROE_Percent": float(roe.iloc[-1]["Value"])
            })
    return pd.DataFrame(ma_summary)

st.title("🇮🇩 M&A Decision Support Tool - Indonesian Companies")

company_data = get_embedded_ma_data()
companies = list(company_data.keys())
selected_companies = st.multiselect("Select Companies", companies, default=companies)

if selected_companies:
    ma_df = calculate_ma_metrics(company_data, selected_companies)
    st.subheader("M&A Valuation Dashboard")
    st.dataframe(ma_df, use_container_width=True)

    st.subheader("Valuation Statistics")
    stats = ma_df.describe().T[["mean", "std", "min", "max"]].round(2)
    st.dataframe(stats, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average EV/EBITDA", f"{stats.loc['EV_EBITDA_Multiple', 'mean']}x", f"{stats.loc['EV_EBITDA_Multiple', 'std']} std")
    with col2:
        st.metric("Average Debt/EBITDA", f"{stats.loc['Debt_EBITDA_Ratio', 'mean']}x", f"{stats.loc['Debt_EBITDA_Ratio', 'std']} std")
    with col3:
        st.metric("Average ROE", f"{stats.loc['ROE_Percent', 'mean']}%", f"{stats.loc['ROE_Percent', 'std']} std")

    st.subheader("Trend Analysis")
    metric_options = ["EBITDA", "Revenue", "Enterprise_Value", "Market_Cap", "EV_EBITDA_Multiple", "Debt_EBITDA_Ratio", "ROE_Percent"]
    selected_metric = st.selectbox("Select Metric", metric_options)
    trend_data = pd.DataFrame()

    for company in selected_companies:
        df = extract_metric(company_data[company], selected_metric)
        df["Company"] = company
        trend_data = pd.concat([trend_data, df], ignore_index=True)

    trend_data.dropna(inplace=True)
    trend_data["Value"] = pd.to_numeric(trend_data["Value"], errors='coerce')
    trend_data.dropna(inplace=True)
    st.plotly_chart(px.line(trend_data, x="Year", y="Value", color="Company", title=f"{selected_metric} Trend"), use_container_width=True)

else:
    st.warning("Please select at least one company.")

# Footer
st.markdown("---")
st.markdown("**M&A Decision Support Tool** | Indonesian Market Analysis | Financial data for educational purposes")
