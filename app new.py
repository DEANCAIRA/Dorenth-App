import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="M&A Dashboard",
    layout="wide"
)

# Load data
def get_embedded_ma_data():
    # This should be filled with the full embedded dataset logic
    # For brevity, simulate a sample dictionary with simplified content
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
            ev_ebitda = extract_metric(df, "EV_EBITDA_Multiple")
            debt_ebitda = extract_metric(df, "Debt_EBITDA_Ratio")
            roe = extract_metric(df, "ROE_Percent")
            ma_summary.append({
                "Company": company,
                "EBITDA_2024": float(ebitda.iloc[-1]["Value"]),
                "EV_EBITDA_Multiple": float(ev_ebitda.iloc[-1]["Value"]),
                "Debt_EBITDA_Ratio": float(debt_ebitda.iloc[-1]["Value"]),
                "ROE_Percent": float(roe.iloc[-1]["Value"])
            })
    return pd.DataFrame(ma_summary)


st.title("M&A Valuation Dashboard")

company_data = get_embedded_ma_data()
companies = list(company_data.keys())
selected_companies = st.multiselect("Select Companies", companies, default=companies)

if selected_companies:
    ma_df = calculate_ma_metrics(company_data, selected_companies)
    st.subheader("Valuation Table")
    st.dataframe(ma_df, use_container_width=True)

    st.subheader("Valuation Statistics")
    stats = ma_df.describe().T[["mean", "std", "min", "max"]].round(2)
    st.dataframe(stats, use_container_width=True)

    st.subheader("Metric Visualizations")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg EV/EBITDA", f"{stats.loc['EV_EBITDA_Multiple', 'mean']}x", f"{stats.loc['EV_EBITDA_Multiple', 'std']} std")
    with col2:
        st.metric("Avg Debt/EBITDA", f"{stats.loc['Debt_EBITDA_Ratio', 'mean']}x", f"{stats.loc['Debt_EBITDA_Ratio', 'std']} std")
    with col3:
        st.metric("Avg ROE", f"{stats.loc['ROE_Percent', 'mean']}%", f"{stats.loc['ROE_Percent', 'std']} std")

    st.subheader("Chart: EV/EBITDA Distribution")
    fig = px.bar(ma_df, x="Company", y="EV_EBITDA_Multiple")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Please select at least one company.")
