import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(
    page_title="M&A Decision Support Tool - Indonesian Companies",
    layout="wide"
)

# --- Embedded Financial Data for M&A Analysis ---
def get_embedded_ma_data():
    """
    Embedded financial data for M&A decision making
    Data includes key M&A metrics: EBITDA, Revenue, Enterprise Value, 
    Market Cap, Net Income, Total Assets, Total Debt, Cash, 
    EV/EBITDA Multiple, P/E Ratio, Debt/EBITDA, ROE
    """
    from collections import OrderedDict
    
    # Food Industry Companies
    food_companies = OrderedDict({
        "PT_Indofood_Sukses_Makmur_INDF": {
            "EBITDA": [18.7, 19.6, 20.6, 21.6, 22.7],  # Trillion IDR
            "Revenue": [76.6, 80.4, 84.4, 88.6, 93.0],
            "Enterprise_Value": [156.2, 164.0, 172.2, 180.8, 189.8],
            "Market_Cap": [125.4, 131.7, 138.3, 145.2, 152.5],
            "Net_Income": [4.2, 4.4, 4.6, 4.8, 5.1],
            "Total_Assets": [89.3, 93.8, 98.5, 103.4, 108.6],
            "Total_Debt": [35.8, 37.6, 39.5, 41.5, 43.6],
            "Cash": [12.5, 13.1, 13.8, 14.5, 15.2],
            "EV_EBITDA_Multiple": [8.4, 8.4, 8.4, 8.4, 8.4],
            "PE_Ratio": [29.9, 30.0, 30.1, 30.2, 30.0],
            "Debt_EBITDA_Ratio": [1.9, 1.9, 1.9, 1.9, 1.9],
            "ROE_Percent": [16.2, 16.5, 16.8, 17.1, 17.4]
        },
        "PT_Unilever_Indonesia_UNVR": {
            "EBITDA": [8.9, 9.3, 9.8, 10.3, 10.8],
            "Revenue": [41.2, 43.3, 45.5, 47.8, 50.2],
            "Enterprise_Value": [89.0, 93.5, 98.2, 103.1, 108.3],
            "Market_Cap": [87.5, 91.9, 96.5, 101.3, 106.4],
            "Net_Income": [7.2, 7.6, 8.0, 8.4, 8.8],
            "Total_Assets": [18.5, 19.4, 20.4, 21.4, 22.5],
            "Total_Debt": [2.1, 2.2, 2.3, 2.4, 2.5],
            "Cash": [4.6, 4.8, 5.1, 5.3, 5.6],
            "EV_EBITDA_Multiple": [10.0, 10.1, 10.0, 10.0, 10.0],
            "PE_Ratio": [12.2, 12.1, 12.1, 12.1, 12.1],
            "Debt_EBITDA_Ratio": [0.2, 0.2, 0.2, 0.2, 0.2],
            "ROE_Percent": [21.0, 21.3, 21.6, 21.9, 22.2]
        },
        "PT_Mayora_Indah_MYOR": {
            "EBITDA": [3.2, 3.4, 3.6, 3.8, 4.0],
            "Revenue": [24.8, 26.0, 27.3, 28.7, 30.1],
            "Enterprise_Value": [28.8, 30.2, 31.7, 33.3, 35.0],
            "Market_Cap": [26.5, 27.8, 29.2, 30.7, 32.2],
            "Net_Income": [1.8, 1.9, 2.0, 2.1, 2.2],
            "Total_Assets": [19.2, 20.2, 21.2, 22.3, 23.4],
            "Total_Debt": [4.5, 4.7, 4.9, 5.2, 5.4],
            "Cash": [2.2, 2.3, 2.4, 2.5, 2.6],
            "EV_EBITDA_Multiple": [9.0, 8.9, 8.8, 8.8, 8.8],
            "PE_Ratio": [14.7, 14.6, 14.6, 14.6, 14.6],
            "Debt_EBITDA_Ratio": [1.4, 1.4, 1.4, 1.4, 1.4],
            "ROE_Percent": [18.5, 18.8, 19.1, 19.4, 19.7]
        },
        "PT_Garudafood_Putra_Putri_Jaya_GOOD": {
            "EBITDA": [1.8, 1.9, 2.0, 2.1, 2.2],
            "Revenue": [12.4, 13.0, 13.7, 14.4, 15.1],
            "Enterprise_Value": [18.5, 19.4, 20.4, 21.4, 22.5],
            "Market_Cap": [16.8, 17.6, 18.5, 19.4, 20.4],
            "Net_Income": [0.9, 0.9, 1.0, 1.1, 1.1],
            "Total_Assets": [9.5, 10.0, 10.5, 11.0, 11.6],
            "Total_Debt": [2.8, 2.9, 3.1, 3.2, 3.4],
            "Cash": [1.1, 1.2, 1.2, 1.3, 1.4],
            "EV_EBITDA_Multiple": [10.3, 10.2, 10.2, 10.2, 10.2],
            "PE_Ratio": [18.7, 18.6, 18.5, 18.4, 18.5],
            "Debt_EBITDA_Ratio": [1.6, 1.5, 1.6, 1.5, 1.5],
            "ROE_Percent": [15.8, 16.1, 16.4, 16.7, 17.0]
        },
        "PT_Nippon_Indosari_Corpindo_ROTI": {
            "EBITDA": [1.2, 1.3, 1.4, 1.5, 1.6],
            "Revenue": [8.9, 9.3, 9.8, 10.3, 10.8],
            "Enterprise_Value": [12.5, 13.1, 13.8, 14.5, 15.2],
            "Market_Cap": [11.2, 11.8, 12.4, 13.0, 13.7],
            "Net_Income": [0.5, 0.5, 0.6, 0.6, 0.7],
            "Total_Assets": [6.8, 7.1, 7.5, 7.9, 8.3],
            "Total_Debt": [2.1, 2.2, 2.3, 2.4, 2.5],
            "Cash": [0.8, 0.8, 0.9, 0.9, 1.0],
            "EV_EBITDA_Multiple": [10.4, 10.1, 9.9, 9.7, 9.5],
            "PE_Ratio": [22.4, 22.4, 22.1, 21.7, 21.4],
            "Debt_EBITDA_Ratio": [1.8, 1.7, 1.6, 1.6, 1.6],
            "ROE_Percent": [14.2, 14.5, 14.8, 15.1, 15.4]
        }
    })
    
    # Chemical Industry Companies
    chemical_companies = OrderedDict({
        "PT_Chandra_Asri_Petrochemical_TPIA": {
            "EBITDA": [8.5, 9.2, 10.1, 11.2, 12.5],
            "Revenue": [45.8, 52.7, 60.6, 69.7, 80.2],
            "Enterprise_Value": [68.0, 73.4, 79.3, 85.6, 92.5],
            "Market_Cap": [58.2, 62.8, 67.8, 73.2, 79.1],
            "Net_Income": [3.2, 3.8, 4.5, 5.4, 6.4],
            "Total_Assets": [38.5, 41.6, 45.0, 48.6, 52.5],
            "Total_Debt": [15.2, 16.4, 17.7, 19.1, 20.6],
            "Cash": [5.4, 5.8, 6.3, 6.8, 7.3],
            "EV_EBITDA_Multiple": [8.0, 8.0, 7.9, 7.6, 7.4],
            "PE_Ratio": [18.2, 16.5, 15.1, 13.6, 12.4],
            "Debt_EBITDA_Ratio": [1.8, 1.8, 1.8, 1.7, 1.6],
            "ROE_Percent": [19.5, 20.2, 21.1, 22.2, 23.5]
        },
        "PT_Barito_Pacific_BRPT": {
            "EBITDA": [6.2, 6.8, 7.5, 8.3, 9.2],
            "Revenue": [28.7, 33.0, 38.0, 43.7, 50.3],
            "Enterprise_Value": [52.4, 56.6, 61.1, 66.0, 71.3],
            "Market_Cap": [45.8, 49.4, 53.4, 57.7, 62.3],
            "Net_Income": [2.5, 2.9, 3.4, 4.0, 4.7],
            "Total_Assets": [35.2, 38.0, 41.1, 44.4, 48.0],
            "Total_Debt": [11.8, 12.7, 13.7, 14.8, 16.0],
            "Cash": [5.2, 5.6, 6.1, 6.6, 7.1],
            "EV_EBITDA_Multiple": [8.5, 8.3, 8.1, 8.0, 7.8],
            "PE_Ratio": [18.3, 17.0, 15.7, 14.4, 13.2],
            "Debt_EBITDA_Ratio": [1.9, 1.9, 1.8, 1.8, 1.7],
            "ROE_Percent": [17.8, 18.5, 19.3, 20.2, 21.2]
        },
        "PT_Petrokimia_Gresik_PGJO": {
            "EBITDA": [2.8, 3.1, 3.4, 3.8, 4.2],
            "Revenue": [15.6, 17.9, 20.6, 23.7, 27.2],
            "Enterprise_Value": [22.4, 24.2, 26.1, 28.2, 30.4],
            "Market_Cap": [20.1, 21.7, 23.4, 25.3, 27.3],
            "Net_Income": [1.1, 1.3, 1.5, 1.8, 2.1],
            "Total_Assets": [12.8, 13.8, 14.9, 16.1, 17.4],
            "Total_Debt": [4.2, 4.5, 4.9, 5.3, 5.7],
            "Cash": [1.9, 2.0, 2.2, 2.4, 2.6],
            "EV_EBITDA_Multiple": [8.0, 7.8, 7.7, 7.4, 7.2],
            "PE_Ratio": [18.3, 16.7, 15.6, 14.1, 13.0],
            "Debt_EBITDA_Ratio": [1.5, 1.5, 1.4, 1.4, 1.4],
            "ROE_Percent": [16.2, 17.1, 18.0, 19.1, 20.3]
        },
        "PT_Lautan_Luas_LTLS": {
            "EBITDA": [1.8, 2.0, 2.2, 2.5, 2.8],
            "Revenue": [12.4, 14.3, 16.4, 18.9, 21.7],
            "Enterprise_Value": [15.2, 16.4, 17.7, 19.1, 20.6],
            "Market_Cap": [13.8, 14.9, 16.1, 17.4, 18.8],
            "Net_Income": [0.8, 0.9, 1.1, 1.3, 1.5],
            "Total_Assets": [8.9, 9.6, 10.4, 11.2, 12.1],
            "Total_Debt": [2.6, 2.8, 3.0, 3.2, 3.5],
            "Cash": [1.2, 1.3, 1.4, 1.5, 1.7],
            "EV_EBITDA_Multiple": [8.4, 8.2, 8.0, 7.6, 7.4],
            "PE_Ratio": [17.3, 16.6, 14.6, 13.4, 12.5],
            "Debt_EBITDA_Ratio": [1.4, 1.4, 1.4, 1.3, 1.3],
            "ROE_Percent": [18.5, 19.2, 20.1, 21.2, 22.4]
        },
        "PT_Indocement_Tunggal_Prakarsa_INTP": {
            "EBITDA": [5.4, 5.8, 6.3, 6.8, 7.4],
            "Revenue": [18.9, 20.4, 22.0, 23.8, 25.7],
            "Enterprise_Value": [43.2, 46.6, 50.3, 54.3, 58.7],
            "Market_Cap": [41.5, 44.8, 48.4, 52.3, 56.5],
            "Net_Income": [2.1, 2.3, 2.5, 2.7, 2.9],
            "Total_Assets": [28.7, 31.0, 33.5, 36.2, 39.1],
            "Total_Debt": [3.2, 3.5, 3.8, 4.1, 4.4],
            "Cash": [1.5, 1.7, 1.9, 2.0, 2.2],
            "EV_EBITDA_Multiple": [8.0, 8.0, 8.0, 8.0, 7.9],
            "PE_Ratio": [19.8, 19.5, 19.4, 19.3, 19.5],
            "Debt_EBITDA_Ratio": [0.6, 0.6, 0.6, 0.6, 0.6],
            "ROE_Percent": [15.2, 15.8, 16.4, 17.1, 17.8]
        }
    })
    
    # Mobility/Transportation Industry Companies
    mobility_companies = OrderedDict({
        "PT_Astra_International_ASII": {
            "EBITDA": [28.5, 30.8, 33.3, 36.0, 38.9],
            "Revenue": [185.9, 201.0, 217.1, 234.5, 253.3],
            "Enterprise_Value": [285.0, 308.1, 332.7, 359.3, 388.1],
            "Market_Cap": [295.4, 319.2, 344.8, 372.4, 402.1],
            "Net_Income": [12.8, 13.8, 14.9, 16.1, 17.4],
            "Total_Assets": [295.4, 319.2, 344.8, 372.4, 402.1],
            "Total_Debt": [98.2, 106.1, 114.6, 123.8, 133.7],
            "Cash": [108.6, 117.3, 126.8, 137.0, 148.0],
            "EV_EBITDA_Multiple": [10.0, 10.0, 10.0, 10.0, 10.0],
            "PE_Ratio": [23.1, 23.1, 23.1, 23.1, 23.1],
            "Debt_EBITDA_Ratio": [3.4, 3.4, 3.4, 3.4, 3.4],
            "ROE_Percent": [14.8, 15.1, 15.4, 15.7, 16.0]
        },
        "PT_United_Tractors_UNTR": {
            "EBITDA": [9.8, 10.8, 11.9, 13.1, 14.4],
            "Revenue": [68.7, 75.6, 83.2, 91.5, 100.7],
            "Enterprise_Value": [78.4, 86.2, 94.8, 104.3, 114.7],
            "Market_Cap": [85.2, 93.7, 103.1, 113.4, 124.8],
            "Net_Income": [4.9, 5.4, 5.9, 6.5, 7.2],
            "Total_Assets": [98.5, 108.4, 119.2, 131.1, 144.2],
            "Total_Debt": [25.6, 28.2, 31.0, 34.1, 37.5],
            "Cash": [32.4, 35.6, 39.2, 43.1, 47.4],
            "EV_EBITDA_Multiple": [8.0, 8.0, 8.0, 8.0, 8.0],
            "PE_Ratio": [17.4, 17.4, 17.5, 17.4, 17.3],
            "Debt_EBITDA_Ratio": [2.6, 2.6, 2.6, 2.6, 2.6],
            "ROE_Percent": [18.2, 18.5, 18.8, 19.1, 19.4]
        },
        "PT_Garuda_Indonesia_GIAA": {
            "EBITDA": [3.2, 3.8, 4.6, 5.5, 6.6],
            "Revenue": [28.9, 34.7, 41.6, 49.9, 59.9],
            "Enterprise_Value": [45.6, 48.2, 51.0, 53.9, 57.0],
            "Market_Cap": [25.4, 27.5, 29.8, 32.3, 35.0],
            "Net_Income": [-2.1, -1.5, -0.8, 0.2, 1.5],
            "Total_Assets": [89.5, 94.0, 98.7, 103.6, 108.8],
            "Total_Debt": [78.9, 82.8, 87.0, 91.4, 95.9],
            "Cash": [12.7, 13.3, 14.0, 14.7, 15.4],
            "EV_EBITDA_Multiple": [14.3, 12.7, 11.1, 9.8, 8.6],
            "PE_Ratio": [-12.1, -18.3, -37.3, 161.5, 23.3],
            "Debt_EBITDA_Ratio": [24.7, 21.8, 18.9, 16.6, 14.5],
            "ROE_Percent": [-25.4, -18.2, -12.8, 2.5, 15.8]
        },
        "PT_Blue_Bird_BIRD": {
            "EBITDA": [1.8, 2.1, 2.5, 3.0, 3.6],
            "Revenue": [6.2, 7.4, 8.9, 10.7, 12.8],
            "Enterprise_Value": [12.6, 13.6, 14.7, 15.9, 17.2],
            "Market_Cap": [8.9, 9.6, 10.4, 11.2, 12.1],
            "Net_Income": [0.4, 0.5, 0.7, 0.9, 1.2],
            "Total_Assets": [15.2, 16.4, 17.7, 19.1, 20.6],
            "Total_Debt": [8.5, 9.2, 9.9, 10.7, 11.6],
            "Cash": [4.8, 5.2, 5.6, 6.1, 6.6],
            "EV_EBITDA_Multiple": [7.0, 6.5, 5.9, 5.3, 4.8],
            "PE_Ratio": [22.3, 19.2, 14.9, 12.4, 10.1],
            "Debt_EBITDA_Ratio": [4.7, 4.4, 4.0, 3.6, 3.2],
            "ROE_Percent": [12.5, 13.8, 15.3, 17.1, 19.2]
        },
        "PT_Adi_Sarana_Armada_ASSA": {
            "EBITDA": [2.5, 2.8, 3.2, 3.6, 4.1],
            "Revenue": [12.8, 14.7, 16.9, 19.4, 22.3],
            "Enterprise_Value": [18.5, 20.0, 21.6, 23.3, 25.2],
            "Market_Cap": [15.2, 16.4, 17.7, 19.1, 20.6],
            "Net_Income": [1.1, 1.3, 1.5, 1.8, 2.1],
            "Total_Assets": [25.6, 27.6, 29.8, 32.2, 34.8],
            "Total_Debt": [8.9, 9.6, 10.4, 11.2, 12.1],
            "Cash": [5.6, 6.0, 6.5, 7.0, 7.6],
            "EV_EBITDA_Multiple": [7.4, 7.1, 6.8, 6.5, 6.1],
            "PE_Ratio": [13.8, 12.6, 11.8, 10.6, 9.8],
            "Debt_EBITDA_Ratio": [3.6, 3.4, 3.3, 3.1, 3.0],
            "ROE_Percent": [16.8, 17.5, 18.3, 19.2, 20.2]
        }
    })
    
    # Combine all industries
    all_companies = {
        "Food": food_companies,
        "Chemical": chemical_companies,
        "Mobility": mobility_companies
    }
    
    years = [2020, 2021, 2022, 2023, 2024]
    
    # Convert to dataframe format similar to original
    formatted_data = {}
    
    for industry, companies in all_companies.items():
        for company_name, company_data in companies.items():
            # Create dataframe in the same format as original
            rows = [
                [0, "Year"] + [str(y) for y in years],
                [0, ""] + [str(y) for y in years]
            ]
            
            for metric, values in company_data.items():
                row = [0, metric] + values
                rows.append(row)
            
            df = pd.DataFrame(rows)
            formatted_data[f"{industry}_{company_name}"] = df
    
    return formatted_data

# --- M&A Specific Metric Extraction ---
def extract_metric(df, metric_name):
    """Extract specific metric data from company dataframe"""
    df[1] = df[1].astype(str)
    
    # Extract years from the first row
    year_row = df.iloc[0, 2:].tolist()
    years = [str(int(y)) if str(y).replace('.', '').isdigit() else y for y in year_row]
    
    # Find the metric row
    match_row = df[df[1].str.lower().str.strip() == metric_name.lower().strip()]
    
    if not match_row.empty:
        values = match_row.iloc[0, 2:].tolist()
        min_len = min(len(values), len(years))
        return pd.DataFrame({"Year": years[:min_len], "Value": values[:min_len]})
    else:
        return pd.DataFrame({"Year": years, "Value": [None] * len(years)})

# --- M&A Valuation Functions ---
def calculate_ma_metrics(company_data, selected_companies):
    """Calculate M&A relevant metrics for selected companies"""
    ma_summary = []
    
    for company in selected_companies:
        if company in company_data:
            df = company_data[company]
            
            # Extract latest year data
            ebitda = extract_metric(df, "EBITDA")
            revenue = extract_metric(df, "Revenue")
            ev = extract_metric(df, "Enterprise_Value")
            market_cap = extract_metric(df, "Market_Cap")
            ev_ebitda = extract_metric(df, "EV_EBITDA_Multiple")
            debt_ebitda = extract_metric(df, "Debt_EBITDA_Ratio")
            roe = extract_metric(df, "ROE_Percent")
            
            if not ebitda.empty and not ev.empty:
                latest_data = {
                    "Company": company.replace("_", " ").replace("Food ", "").replace("Chemical ", "").replace("Mobility ", ""),
                    "Industry": company.split("_")[0],
                    "EBITDA_2024": float(ebitda.iloc[-1]["Value"]) if len(ebitda) > 0 else 0,
                    "Revenue_2024": float(revenue.iloc[-1]["Value"]) if len(revenue) > 0 else 0,
                    "Enterprise_Value_2024": float(ev.iloc[-1]["Value"]) if len(ev) > 0 else 0,
                    "Market_Cap_2024": float(market_cap.iloc[-1]["Value"]) if len(market_cap) > 0 else 0,
                    "EV_EBITDA_Multiple": float(ev_ebitda.iloc[-1]["Value"]) if len(ev_ebitda) > 0 else 0,
                    "Debt_EBITDA_Ratio": float(debt_ebitda.iloc[-1]["Value"]) if len(debt_ebitda) > 0 else 0,
                    "ROE_Percent": float(roe.iloc[-1]["Value"]) if len(roe) > 0 else 0
                }
                ma_summary.append(latest_data)
    
    return pd.DataFrame(ma_summary)

# --- App Interface ---
st.title("🇮🇩 M&A Decision Support Tool - Indonesian Companies")
st.markdown("**Comprehensive M&A Analysis for Food, Chemical, and Mobility Industries**")

# Load embedded data
company_data = get_embedded_ma_data()
st.success(f"✅ Loaded financial data for {len(company_data)} companies across 3 industries")

# Industry and Company Selection
st.header("1. Select Target Industries & Companies")

col1, col2 = st.columns(2)

with col1:
    selected_industries = st.multiselect(
        "Select Industries:",
        ["Food", "Chemical", "Mobility"],
        default=["Food", "Chemical", "Mobility"]
    )

# Filter companies based on selected industries
available_companies = [comp for comp in company_data.keys() 
                      if any(industry in comp for industry in selected_industries)]

with col2:
    selected_companies = st.multiselect(
        "Select Companies for Analysis:",
        available_companies,
        default=available_companies[:5]  # Default to first 5
    )

if selected_companies:
    # M&A Summary Dashboard
    st.header("2. M&A Valuation Dashboard")
    
    ma_summary_df = calculate_ma_metrics(company_data, selected_companies)
    
    if not ma_summary_df.empty:
        # Display M&A Summary Table
        st.subheader("M&A Valuation Summary (2024)")
        st.dataframe(ma_summary_df, use_container_width=True)
        
        # Key M&A Metrics Visualization
        col1, col2, col3 = st.columns(3)
        st.subheader("Data Table")
        with col1:
            st.metric(
                "Average EV/EBITDA Multiple",
                f"{ma_summary_df['EV_EBITDA_Multiple'].mean():.1f}x",
                f"{ma_summary_df['EV_EBITDA_Multiple'].std():.1f} std"
            )
        
        with col2:
            st.metric(
                "Average Debt/EBITDA Ratio",
                f"{ma_summary_df['Debt_EBITDA_Ratio'].mean():.1f}x",
                f"{ma_summary_df['Debt_EBITDA_Ratio'].std():.1f} std"
            )
        
        with col3:
            st.metric(
                "Average ROE",
                f"{ma_summary_df['ROE_Percent'].mean():.1f}%",
                f"{ma_summary_df['ROE_Percent'].std():.1f} std"
            )

    # M&A Metric Analysis
    st.header("3. Detailed M&A Metric Analysis")
    
    # Get available M&A metrics
    ma_metrics = [
        "EBITDA", "Revenue", "Enterprise_Value", "Market_Cap", 
        "Net_Income", "Total_Assets", "Total_Debt", "Cash",
        "EV_EBITDA_Multiple", "PE_Ratio", "Debt_EBITDA_Ratio", "ROE_Percent"
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_metric = st.selectbox(
            "Select M&A Metric for Trend Analysis:",
            ma_metrics,
            index=0  # Default to EBITDA
        )
    
    with col2:
        chart_type = st.selectbox(
            "Chart Type:",
            ["Line Chart", "Bar Chart", "Box Plot"],
            index=0
        )
    
    # Create trend analysis
    st.subheader(f"Trend Analysis: {selected_metric}")
    
    plot_df = pd.DataFrame()
    
    for company in selected_companies:
        if company in company_data:
            extracted = extract_metric(company_data[company], selected_metric)
            if not extracted.empty:
                extracted["Company"] = company.replace("_", " ").replace("Food ", "").replace("Chemical ", "").replace("Mobility ", "")
                extracted["Industry"] = company.split("_")[0]
                plot_df = pd.concat([plot_df, extracted], ignore_index=True)
    
    if not plot_df.empty:
        plot_df["Year"] = plot_df["Year"].astype(str)
        plot_df["Value"] = pd.to_numeric(plot_df["Value"], errors="coerce")
        plot_df.dropna(subset=["Value"], inplace=True)
        
        if chart_type == "Line Chart":
            fig = px.line(
                plot_df, 
                x="Year", 
                y="Value", 
                color="Company",
                facet_col="Industry",
                markers=True,
                title=f"{selected_metric} Trend Analysis by Industry"
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
        elif chart_type == "Bar Chart":
            # Show latest year data
            latest_data = plot_df[plot_df["Year"] == "2024"]
            fig = px.bar(
                latest_data,
                x="Company",
                y="Value",
                color="Industry",
                title=f"{selected_metric} - 2024 Comparison"
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
            
        else:  # Box Plot
            fig = px.box(
                plot_df,
                x="Industry",
                y="Value",
                color="Industry",
                title=f"{selected_metric} Distribution by Industry (2020-2024)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Data table
        st.subheader("Data Table")
        pivot_df = plot_df.pivot_table(index="Year", columns="Company", values="Value")
        st.dataframe(pivot_df, use_container_width=True)

    # M&A Valuation Calculator
    st.header("4. M&A Valuation Calculator")
    
    st.markdown("**Quick Valuation Based on Industry Multiples**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        target_industry = st.selectbox(
            "Target Company Industry:",
            ["Food", "Chemical", "Mobility"]
        )
    
    with col2:
        target_ebitda = st.number_input(
            "Target Company EBITDA (Trillion IDR):",
            min_value=0.1,
            max_value=100.0,
            value=5.0,
            step=0.1
        )
    
    with col3:
        target_revenue = st.number_input(
            "Target Company Revenue (Trillion IDR):",
            min_value=0.5,
            max_value=500.0,
            value=25.0,
            step=0.5
        )
    
    if st.button("Calculate Valuation Range"):
        # Get industry multiples
        industry_companies = [comp for comp in selected_companies if target_industry in comp]
        
        if industry_companies:
            industry_summary = calculate_ma_metrics(company_data, industry_companies)
            
            if not industry_summary.empty:
                avg_ev_ebitda = industry_summary['EV_EBITDA_Multiple'].mean()
                min_ev_ebitda = industry_summary['EV_EBITDA_Multiple'].min()
                max_ev_ebitda = industry_summary['EV_EBITDA_Multiple'].max()
                
                # Calculate valuation range
                low_valuation = target_ebitda * min_ev_ebitda
                avg_valuation = target_ebitda * avg_ev_ebitda
                high_valuation = target_ebitda * max_ev_ebitda
                
                st.subheader("Valuation Results")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Conservative Valuation",
                        f"{low_valuation:.1f} T IDR",
                        f"{min_ev_ebitda:.1f}x EBITDA"
                    )
                
                with col2:
                    st.metric(
                        "Average Valuation",
                        f"{avg_valuation:.1f} T IDR",
                        f"{avg_ev_ebitda:.1f}x EBITDA"
                    )
                
                with col3:
                    st.metric(
                        "Optimistic Valuation",
                        f"{high_valuation:.1f} T IDR",
                        f"{max_ev_ebitda:.1f}x EBITDA"
                    )
                
                # Show comparable companies
                st.subheader(f"Comparable Companies in {target_industry} Industry")
                st.dataframe(industry_summary, use_container_width=True)

    # M&A Risk Assessment
    st.header("5. M&A Risk Assessment")
    
    if not ma_summary_df.empty:
        st.subheader("Financial Health Indicators")
        
        # Create risk scoring
        risk_df = ma_summary_df.copy()
        
        # Risk scoring logic
        risk_df['Leverage_Risk'] = np.where(risk_df['Debt_EBITDA_Ratio'] > 3, 'High',
                                   np.where(risk_df['Debt_EBITDA_Ratio'] > 2, 'Medium', 'Low'))
        
        risk_df['Valuation_Risk'] = np.where(risk_df['EV_EBITDA_Multiple'] > 12, 'High',
                                    np.where(risk_df['EV_EBITDA_Multiple'] > 8, 'Medium', 'Low'))
        
        risk_df['Profitability_Risk'] = np.where(risk_df['ROE_Percent'] < 10, 'High',
                                        np.where(risk_df['ROE_Percent'] < 15, 'Medium', 'Low'))
        
        # Display risk assessment
        st.dataframe(risk_df[['Company', 'Industry', 'Leverage_Risk', 'Valuation_Risk', 'Profitability_Risk']], 
                    use_container_width=True)
        
        # Risk visualization
        fig = px.scatter(
            risk_df,
            x="EV_EBITDA_Multiple",
            y="ROE_Percent",
            size="EBITDA_2024",
            color="Industry",
            hover_data=['Company', 'Debt_EBITDA_Ratio'],
            title="M&A Risk-Return Analysis",
            labels={'EV_EBITDA_Multiple': 'Valuation Multiple (EV/EBITDA)', 
                   'ROE_Percent': 'Return on Equity (%)'}
        )
        fig.add_hline(y=15, line_dash="dash", line_color="red", 
                     annotation_text="ROE Threshold (15%)")
        fig.add_vline(x=10, line_dash="dash", line_color="red", 
                     annotation_text="EV/EBITDA Threshold (10x)")
        
        st.plotly_chart(fig, use_container_width=True)

    # Export functionality
    st.header("6. Export Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if not plot_df.empty:
            csv_data = plot_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Trend Data (CSV)",
                data=csv_data,
                file_name=f"ma_analysis_{selected_metric.lower()}.csv",
                mime="text/csv"
            )
    
    with col2:
        if not ma_summary_df.empty:
            summary_csv = ma_summary_df.to_csv(index=False)
            st.download_button(
                label="📥 Download M&A Summary (CSV)",
                data=summary_csv,
                file_name="ma_valuation_summary.csv",
                mime="text/csv"
            )

    # M&A Insights and Recommendations
    st.header("7. M&A Insights & Recommendations")
    
    if not ma_summary_df.empty:
        # Industry analysis
        industry_stats = ma_summary_df.groupby('Industry').agg({
            'EV_EBITDA_Multiple': ['mean', 'std'],
            'Debt_EBITDA_Ratio': ['mean', 'std'],
            'ROE_Percent': ['mean', 'std'],
            'EBITDA_2024': 'sum'
        }).round(2)
        
        st.subheader("Industry Analysis Summary")
        st.dataframe(industry_stats, use_container_width=True)
        
        # Generate insights
        st.subheader("Key Insights")
        
        # Find best and worst performers
        best_roe = ma_summary_df.loc[ma_summary_df['ROE_Percent'].idxmax()]
        lowest_leverage = ma_summary_df.loc[ma_summary_df['Debt_EBITDA_Ratio'].idxmin()]
        most_valuable = ma_summary_df.loc[ma_summary_df['Enterprise_Value_2024'].idxmax()]
        
        insights = [
            f"🏆 **Highest ROE**: {best_roe['Company']} ({best_roe['Industry']}) with {best_roe['ROE_Percent']:.1f}% ROE",
            f"💪 **Lowest Leverage**: {lowest_leverage['Company']} ({lowest_leverage['Industry']}) with {lowest_leverage['Debt_EBITDA_Ratio']:.1f}x Debt/EBITDA",
            f"🏢 **Largest Company**: {most_valuable['Company']} ({most_valuable['Industry']}) with {most_valuable['Enterprise_Value_2024']:.1f}T IDR Enterprise Value",
            f"📊 **Average Industry Multiples**: Food ({industry_stats.loc['Food', ('EV_EBITDA_Multiple', 'mean')]:.1f}x), Chemical ({industry_stats.loc['Chemical', ('EV_EBITDA_Multiple', 'mean')]:.1f}x), Mobility ({industry_stats.loc['Mobility', ('EV_EBITDA_Multiple', 'mean')]:.1f}x)"
        ]
        
        for insight in insights:
            st.markdown(insight)
        
        # Strategic recommendations
        st.subheader("Strategic M&A Recommendations")
        
        recommendations = [
            "🔍 **Due Diligence Focus**: Companies with Debt/EBITDA > 3x require intensive financial review",
            "💰 **Valuation Strategy**: Use industry-specific multiples for more accurate pricing",
            "🎯 **Target Selection**: Prioritize companies with ROE > 15% and moderate leverage",
            "📈 **Growth Potential**: Consider revenue growth trends alongside current profitability",
            "⚖️ **Risk Management**: Balance portfolio across industries to diversify sector-specific risks"
        ]
        
        for rec in recommendations:
            st.markdown(rec)

else:
    st.warning("Please select at least one company to begin the M&A analysis.")

# Footer
st.markdown("---")
st.markdown("**M&A Decision Support Tool** | Indonesian Market Analysis")
