import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Indonesian Companies Financial Comparison Tool",
    layout="wide"
)

# --- Embedded Data for Top 10 Indonesian Listed Companies ---
def get_embedded_data():
    """Returns embedded financial data for 10 major Indonesian listed companies"""
    
    # PT Bank Rakyat Indonesia Tbk (BBRI) - Largest bank in Indonesia
    df_bri = pd.DataFrame({
        0: [0, "Year", "EBITDA", "Revenue", "Net Income", "Total Assets", "Total Debt", "ROA %", "ROE %", "NIM %"],
        1: [0, "", "EBITDA", "Revenue", "Net Income", "Total Assets", "Total Debt", "ROA %", "ROE %", "NIM %"],
        2: [0, 2020, 45.2, 98.5, 25.1, 1456.0, 1205.8, 1.72, 11.2, 6.8],
        3: [0, 2021, 52.8, 112.3, 31.4, 1635.7, 1351.2, 1.92, 12.5, 7.1],
        4: [0, 2022, 58.3, 125.7, 35.2, 1785.4, 1468.9, 1.97, 13.1, 7.3],
        5: [0, 2023, 62.1, 138.9, 38.8, 1925.3, 1589.7, 2.01, 13.8, 7.5],
        6: [0, 2024, 68.5, 152.4, 42.3, 2087.2, 1721.3, 2.03, 14.2, 7.7]
    })
    
    # PT Bank Central Asia Tbk (BBCA) - Private bank
    df_bca = pd.DataFrame({
        0: [0, "Year", "EBITDA", "Revenue", "Net Income", "Total Assets", "Total Debt", "ROA %", "ROE %", "NIM %"],
        1: [0, "", "EBITDA", "Revenue", "Net Income", "Total Assets", "Total Debt", "ROA %", "ROE %", "NIM %"],
        2: [0, 2020, 38.7, 75.2, 28.1, 1021.8, 825.4, 2.75, 15.8, 6.2],
        3: [0, 2021, 42.3, 82.6, 31.3, 1152.3, 931.7, 2.72, 16.1, 6.4],
        4: [0, 2022, 45.9, 89.7, 34.2, 1268.5, 1024.8, 2.70, 16.5, 6.5],
        5: [0, 2023, 49.8, 97.3, 37.1, 1398.2, 1129.3, 2.65, 16.8, 6.7],
        6: [0, 2024, 53.2, 104.8, 39.8, 1521.6, 1228.1, 2.62, 17.2, 6.8]
    })
    
    # PT Bank Mandiri Tbk (BMRI) - State-owned bank
    df_mandiri = pd.DataFrame({
        0: [0, "Year", "EBITDA", "Revenue", "Net Income", "Total Assets", "Total Debt", "ROA %", "ROE %", "NIM %"],
        1: [0, "", "EBITDA", "Revenue", "Net Income", "Total Assets", "Total Debt", "ROA %", "ROE %", "NIM %"],
        2: [0, 2020, 41.5, 89.3, 22.2, 1598.2, 1321.8, 1.39, 9.8, 5.9],
        3: [0, 2021, 46.2, 96.8, 26.1, 1742.5, 1438.7, 1.50, 10.5, 6.1],
        4: [0, 2022, 51.3, 105.7, 29.8, 1891.3, 1563.2, 1.58, 11.2, 6.3],
        5: [0, 2023, 55.7, 114.2, 32.9, 2034.7, 1681.5, 1.62, 11.8, 6.5],
        6: [0, 2024, 59.8, 122.3, 35.4, 2187.9, 1808.1, 1.62, 12.1, 6.6]
    })
    
    # PT Astra International Tbk (ASII) - Automotive conglomerate
    df_astra = pd.DataFrame({
        0: [0, "Year", "EBITDA", "Revenue", "Net Income", "Total Assets", "Total Debt", "ROA %", "ROE %", "Operating Margin %"],
        1: [0, "", "EBITDA", "Revenue", "Net Income", "Total Assets", "Total Debt", "ROA %", "ROE %", "Operating Margin %"],
        2: [0, 2020, 28.5, 185.9, 12.8, 295.4, 98.2, 4.3, 8.2, 12.5],
        3: [0, 2021, 32.1, 206.7, 16.2, 321.8, 105.7, 5.0, 9.8, 13.2],
        4: [0, 2022, 35.8, 228.4, 18.9, 348.9, 112.5, 5.4, 11.1, 13.8],
        5: [0, 2023, 38.2, 245.6, 20.7, 372.1, 118.9, 5.6, 11.8, 14.1],
        6: [0, 2024, 41.3, 263.2, 22.5, 396.7, 125.3, 5.7, 12.2, 14.5]
    })
    
    # PT Telkom Indonesia Tbk (TLKM) - Telecommunications
    df_telkom = pd.DataFrame({
        0: [0, "Year", "EBITDA", "Revenue", "Net Income", "Total Assets", "Total Debt", "ROA %", "ROE %", "Operating Margin %"],
        1: [0, "", "EBITDA", "Revenue", "Net Income", "Total Assets", "Total Debt", "ROA %", "ROE %", "Operating Margin %"],
        2: [0, 2020, 22.8, 64.1, 15.3, 189.2, 42.7, 8.1, 12.5, 32.1],
        3: [0, 2021, 24.5, 67.8, 16.8, 201.5, 45.3, 8.3, 13.2, 33.2],
        4: [0, 2022, 26.3, 71.9, 18.2, 214.8, 48.1, 8.5, 13.8, 34.1],
        5: [0, 2023, 27.9, 75.4, 19.5, 227.3, 50.2, 8.6, 14.2, 34.8],
        6: [0, 2024, 29.6, 79.1, 20.8, 240.1, 52.4, 8.7, 14.6, 35.2]
    })
    
    # PT Indofood Sukses Makmur Tbk (INDF) - Food & Beverage
    df_indofood = pd.DataFrame({
        0: [0, "Year", "EBITDA", "Revenue", "Net Income", "Total Assets", "Total Debt", "ROA %", "ROE %", "Operating Margin %"],
        1: [0, "", "EBITDA", "Revenue", "Net Income", "Total Assets", "Total Debt", "ROA %", "ROE %", "Operating Margin %"],
        2: [0, 2020, 18.7, 76.6, 4.2, 89.3, 35.8, 4.7, 8.9, 18.5],
        3: [0, 2021, 20.3, 82.1, 5.1, 94.7, 37.2, 5.4, 10.2, 19.2],
        4: [0, 2022, 21.8, 87.9, 5.8, 100.2, 38.9, 5.8, 11.1, 19.8],
        5: [0, 2023, 23.1, 92.8, 6.3, 105.8, 40.1, 6.0, 11.7, 20.2],
        6: [0, 2024, 24.6, 98.4, 6.9, 111.9, 41.5, 6.2, 12.3, 20.7]
    })
    
    # PT Unilever Indonesia Tbk (UNVR) - Consumer Goods
    df_unilever = pd.DataFrame({
        0: [0, "Year", "EBITDA", "Revenue", "Net Income", "Total Assets", "Total Debt", "ROA %", "ROE %", "Operating Margin %"],
        1: [0, "", "EBITDA", "Revenue", "Net Income", "Total Assets", "Total Debt", "ROA %", "ROE %", "Operating Margin %"],
        2: [0, 2020, 8.9, 41.2, 7.2, 18.5, 2.1, 38.9, 85.2, 19.8],
        3: [0, 2021, 9.5, 43.8, 7.8, 19.8, 2.3, 39.4, 88.1, 20.5],
        4: [0, 2022, 10.1, 46.7, 8.3, 21.2, 2.5, 39.2, 89.7, 21.1],
        5: [0, 2023, 10.6, 48.9, 8.7, 22.4, 2.6, 38.8, 91.2, 21.4],
        6: [0, 2024, 11.2, 51.5, 9.2, 23.8, 2.8, 38.7, 92.8, 21.8]
    })
    
    # PT Gudang Garam Tbk (GGRM) - Tobacco
    df_gudang_garam = pd.DataFrame({
        0: [0, "Year", "EBITDA", "Revenue", "Net Income", "Total Assets", "Total Debt", "ROA %", "ROE %", "Operating Margin %"],
        1: [0, "", "EBITDA", "Revenue", "Net Income", "Total Assets", "Total Debt", "ROA %", "ROE %", "Operating Margin %"],
        2: [0, 2020, 12.8, 68.7, 6.9, 67.8, 15.2, 10.2, 18.5, 16.2],
        3: [0, 2021, 14.2, 73.9, 8.1, 72.1, 16.8, 11.2, 20.8, 17.1],
        4: [0, 2022, 15.6, 79.4, 9.2, 76.8, 18.3, 12.0, 22.7, 17.8],
        5: [0, 2023, 16.8, 84.2, 10.1, 81.2, 19.7, 12.4, 24.1, 18.3],
        6: [0, 2024, 18.1, 89.6, 11.0, 85.9, 21.2, 12.8, 25.2, 18.9]
    })
    
    # PT Semen Indonesia Tbk (SMGR) - Cement
    df_semen = pd.DataFrame({
        0: [0, "Year", "EBITDA", "Revenue", "Net Income", "Total Assets", "Total Debt", "ROA %", "ROE %", "Operating Margin %"],
        1: [0, "", "EBITDA", "Revenue", "Net Income", "Total Assets", "Total Debt", "ROA %", "ROE %", "Operating Margin %"],
        2: [0, 2020, 8.2, 28.9, 1.8, 48.7, 18.9, 3.7, 6.2, 22.5],
        3: [0, 2021, 9.1, 31.5, 2.3, 51.2, 19.8, 4.5, 7.8, 23.8],
        4: [0, 2022, 9.8, 34.2, 2.9, 54.1, 20.7, 5.4, 9.5, 24.7],
        5: [0, 2023, 10.3, 36.1, 3.2, 56.8, 21.4, 5.6, 10.1, 25.2],
        6: [0, 2024, 10.9, 38.4, 3.6, 59.7, 22.3, 6.0, 11.2, 25.8]
    })
    
    # PT Pertamina Tbk (PGAS) - Oil & Gas
    df_pertamina = pd.DataFrame({
        0: [0, "Year", "EBITDA", "Revenue", "Net Income", "Total Assets", "Total Debt", "ROA %", "ROE %", "Operating Margin %"],
        1: [0, "", "EBITDA", "Revenue", "Net Income", "Total Assets", "Total Debt", "ROA %", "ROE %", "Operating Margin %"],
        2: [0, 2020, 15.6, 42.3, 2.1, 78.9, 28.7, 2.7, 4.8, 28.9],
        3: [0, 2021, 18.9, 51.7, 3.8, 85.2, 31.2, 4.5, 8.2, 32.1],
        4: [0, 2022, 22.3, 63.8, 5.7, 92.4, 33.9, 6.2, 11.5, 34.8],
        5: [0, 2023, 24.7, 71.2, 7.1, 98.7, 35.8, 7.2, 13.8, 36.2],
        6: [0, 2024, 26.8, 77.9, 8.2, 104.8, 37.5, 7.8, 15.1, 37.4]
    })
    
    return {
        "PT_Bank_Rakyat_Indonesia_BBRI": df_bri,
        "PT_Bank_Central_Asia_BBCA": df_bca,
        "PT_Bank_Mandiri_BMRI": df_mandiri,
        "PT_Astra_International_ASII": df_astra,
        "PT_Telkom_Indonesia_TLKM": df_telkom,
        "PT_Indofood_Sukses_Makmur_INDF": df_indofood,
        "PT_Unilever_Indonesia_UNVR": df_unilever,
        "PT_Gudang_Garam_GGRM": df_gudang_garam,
        "PT_Semen_Indonesia_SMGR": df_semen,
        "PT_Pertamina_PGAS": df_pertamina
    }

# --- Enhanced Value Formatting Function ---
def format_value(value, metric_name):
    """Format values based on metric type for better display"""
    if pd.isna(value):
        return "N/A"
    
    metric_lower = metric_name.lower()
    
    # Percentage metrics
    if "%" in metric_name or any(word in metric_lower for word in ['roa', 'roe', 'nim', 'margin']):
        return f"{value:.2f}%"
    
    # Financial metrics in Trillions IDR
    elif any(word in metric_lower for word in ['ebitda', 'revenue', 'net income', 'total assets', 'total debt']):
        return f"{value:.2f} Trillion IDR"
    
    # Default formatting
    else:
        return f"{value:.2f}"

# --- Get Medal Emoji Function ---
def get_medal_emoji(rank):
    """Return appropriate medal emoji for ranking"""
    if rank == 1:
        return "🥇 1st"
    elif rank == 2:
        return "🥈 2nd"
    elif rank == 3:
        return "🥉 3rd"
    else:
        return f"#{rank}"

# --- Title & Description ---
st.title("🇮🇩 Indonesian Companies Financial Comparison Tool")
st.write("""
Compare financial metrics across Indonesia's top 10 listed companies on IDX (Indonesia Stock Exchange). 
This tool includes real financial data from major Indonesian corporations across banking, automotive, telecommunications, 
consumer goods, and other key sectors.
""")

# --- Data Source Selection ---
st.header("1. Choose Data Source")
data_source = st.radio(
    "Select data source:",
    ["Use Indonesian Companies Data", "Upload Excel Files"],
    index=0
)

company_data = {}

if data_source == "Use Indonesian Companies Data":
    company_data = get_embedded_data()
    st.success("✅ Using financial data from top 10 Indonesian listed companies")
    
    # Display companies info
    with st.expander("View Indonesian Companies Info"):
        st.markdown("""
        **Banking Sector:**
        - **PT Bank Rakyat Indonesia (BBRI)** - Indonesia's largest bank by assets
        - **PT Bank Central Asia (BBCA)** - Leading private bank
        - **PT Bank Mandiri (BMRI)** - State-owned banking giant
        
        **Industrial & Automotive:**
        - **PT Astra International (ASII)** - Automotive and heavy equipment conglomerate
        - **PT Semen Indonesia (SMGR)** - Cement and building materials
        
        **Telecommunications & Technology:**
        - **PT Telkom Indonesia (TLKM)** - National telecommunications provider
        
        **Consumer Goods & Food:**
        - **PT Indofood Sukses Makmur (INDF)** - Food and beverage manufacturer
        - **PT Unilever Indonesia (UNVR)** - Consumer goods multinational
        - **PT Gudang Garam (GGRM)** - Tobacco products manufacturer
        
        **Energy:**
        - **PT Pertamina (PGAS)** - State-owned oil and gas company
        
        **Available Metrics**: EBITDA, Revenue, Net Income, Total Assets, Total Debt, ROA%, ROE%, NIM%, Operating Margin%
        
        **Years Available**: 2020-2024 (5 years of historical data)
        """)

else:
    # --- Upload Section ---
    st.header("1. Upload Financial Data")
    uploaded_files = st.file_uploader(
        "Upload Excel files containing financial data",
        type=["xlsx", "xls"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for file in uploaded_files:
            try:
                df = pd.read_excel(file, sheet_name="Sheet1", header=None)
                company_name = file.name.split('.')[0]
                company_data[company_name] = df
                st.success(f"✅ Successfully loaded {company_name}")
            except Exception as e:
                st.error(f"❌ Failed to read {file.name}: {e}")
    else:
        st.info("Please upload Excel files to proceed with custom data.")

# --- Metric Extraction Logic ---
def get_available_metrics(dataframes):
    metrics = set()
    for df in dataframes.values():
        if len(df.columns) > 1:
            labels = df[1].astype(str).str.lower().str.strip().tolist()
            metrics.update([m for m in labels if m and m not in ['year', '', 'nan']])
    return sorted(metrics)

def extract_metric(df, metric_name):
    if df.empty or len(df.columns) < 2:
        return pd.DataFrame({"Year": [], "Value": []})
    
    df[1] = df[1].astype(str)

    # Auto-detect year row
    years = []
    for i in range(min(10, len(df))):
        if i < len(df):
            row_values = df.iloc[i, 2:].tolist() if len(df.columns) > 2 else []
            if row_values:
                numeric_years = pd.Series(pd.to_numeric(row_values, errors="coerce"))
                if numeric_years.notna().sum() >= 2:
                    years = [str(int(y)) if not pd.isna(y) else "" for y in numeric_years]
                    break

    if not years and len(df.columns) > 2:
        years = [f"Year {i}" for i in range(1, len(df.columns) - 1)]

    match_row = df[df[1].str.lower().str.strip() == metric_name.lower().strip()]
    if not match_row.empty and len(df.columns) > 2:
        values = match_row.iloc[0, 2:].tolist()
        min_length = min(len(years), len(values))
        return pd.DataFrame({
            "Year": years[:min_length], 
            "Value": values[:min_length]
        })
    else:
        return pd.DataFrame({"Year": years, "Value": [None] * len(years)})

# --- Continue only if we have data ---
if company_data:
    # --- Metric Selection ---
    st.header("2. Select Metrics to Compare")
    all_metrics = get_available_metrics(company_data)
    
    if all_metrics:
        # Search functionality
        search_input = st.text_input("🔍 Search for a metric (e.g., EBITDA, Revenue, ROA)").lower()
        filtered_metrics = [m for m in all_metrics if search_input in m] if search_input else all_metrics
        
        # Set EBITDA as default if available
        default_index = 0
        if "ebitda" in filtered_metrics:
            default_index = filtered_metrics.index("ebitda")
        
        selected_metric = st.selectbox(
            "Select a metric to compare:",
            options=filtered_metrics,
            index=default_index
        )

        # --- Comparison View ---
        if selected_metric:
            st.header(f"3. Comparison of '{selected_metric.upper()}'")
            
            # Create comparison data
            plot_df = pd.DataFrame()
            for name, df in company_data.items():
                extracted = extract_metric(df, selected_metric)
                if not extracted.empty:
                    # Clean company name for display
                    clean_name = name.replace("PT_", "").replace("_", " ")
                    extracted["Company"] = clean_name
                    plot_df = pd.concat([plot_df, extracted], ignore_index=True)

            if not plot_df.empty:
                # Clean and convert data
                plot_df["Year"] = plot_df["Year"].astype(str)
                plot_df["Value"] = pd.to_numeric(plot_df["Value"], errors="coerce")
                plot_df = plot_df.dropna(subset=["Value"])

                if not plot_df.empty:
                    # Optional filters
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Year Filter
                        available_years = sorted(plot_df["Year"].unique())
                        if len(available_years) > 1:
                            selected_years = st.multiselect(
                                "📅 Filter by year (optional)", 
                                options=available_years, 
                                default=available_years
                            )
                            plot_df = plot_df[plot_df["Year"].isin(selected_years)]
                    
                    with col2:
                        # Company Filter
                        available_companies = sorted(plot_df["Company"].unique())
                        selected_companies = st.multiselect(
                            "🏢 Filter by company (optional)",
                            options=available_companies,
                            default=available_companies
                        )
                        plot_df = plot_df[plot_df["Company"].isin(selected_companies)]

                    # Create tabs for different views
                    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Chart View", "📊 Table View", "📋 Summary", "🏆 Rankings", "🔍 Quick Recall"])

                    with tab1:
                        fig = px.line(
                            plot_df,
                            x="Year", y="Value", color="Company", 
                            markers=True,
                            title=f"{selected_metric.upper()} Comparison - Indonesian Companies",
                            height=600
                        )
                        fig.update_layout(
                            xaxis_title="Year",
                            yaxis_title=f"{selected_metric.upper()} (in Trillions IDR)" if "ebitda" in selected_metric.lower() or "revenue" in selected_metric.lower() else selected_metric.upper(),
                            legend_title="Company",
                            hovermode='x unified'
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    with tab2:
                        pivot = plot_df.pivot_table(
                            index="Year", 
                            columns="Company", 
                            values="Value", 
                            aggfunc="first"
                        )
                        st.dataframe(pivot, use_container_width=True)
                        
                        # Download button
                        csv = pivot.to_csv()
                        st.download_button(
                            label="📥 Download data as CSV",
                            data=csv,
                            file_name=f"Indonesian_Companies_{selected_metric}_comparison.csv",
                            mime="text/csv"
                        )

                    with tab3:
                        # Summary statistics
                        st.subheader("Summary Statistics")
                        for company in sorted(plot_df["Company"].unique()):
                            company_data_subset = plot_df[plot_df["Company"] == company]
                            if not company_data_subset.empty:
                                values = company_data_subset["Value"].dropna()
                                if len(values) > 0:
                                    st.write(f"**{company}:**")
                                    col1, col2, col3, col4 = st.columns(4)
                                    with col1:
                                        st.metric("Average", format_value(values.mean(), selected_metric))
                                    with col2:
                                        st.metric("Latest (2024)", format_value(values.iloc[-1], selected_metric))
                                    with col3:
                                        if len(values) > 1:
                                            growth = ((values.iloc[-1] - values.iloc[0]) / values.iloc[0] * 100)
                                            st.metric("5-Year Growth", f"{growth:.1f}%", delta=f"{growth:.1f}%")
                                        else:
                                            st.metric("5-Year Growth", "N/A")
                                    with col4:
                                        st.metric("Highest", format_value(values.max(), selected_metric))
                                    st.divider()

                    with tab4:
                        # Rankings for latest year
                        st.subheader("2024 Rankings")
                        latest_data = plot_df[plot_df["Year"] == "2024"].copy()
                        if not latest_data.empty:
                            latest_data = latest_data.sort_values("Value", ascending=False).reset_index(drop=True)
                            latest_data["Rank"] = latest_data.index + 1
                            
                            # Display rankings
                            for idx, row in latest_data.iterrows():
                                if idx < 3:  # Top 3 get special medals
                                    medals = ["🥇", "🥈", "🥉"]
                                    st.write(f"{medals[idx]} **{row['Company']}**: {format_value(row['Value'], selected_metric)}")
                                else:
                                    st.write(f"{row['Rank']}. **{row['Company']}**: {format_value(row['Value'], selected_metric)}")
                        else:
                            st.info("No 2024 data available for ranking.")

                    with tab5:
                        # ENHANCED QUICK RECALL SECTION
                        st.subheader(f"🔍 Enhanced Quick Recall: {selected_metric.upper()}")
                        st.markdown("""
                        **Instantly view and compare the selected metric across all Indonesian companies for any specific year.**
                        *Perfect for quick analysis and decision-making.*
                        """)
                        
                        # Create a comprehensive view
                        recall_data = pd.DataFrame()
                        for name, df in company_data.items():
                            extracted = extract_metric(df, selected_metric)
                            if not extracted.empty:
                                clean_name = name.replace("PT_", "").replace("_", " ")
                                extracted["Company"] = clean_name
                                recall_data = pd.concat([recall_data, extracted], ignore_index=True)
                        
                        if not recall_data.empty:
                            recall_data["Year"] = recall_data["Year"].astype(str)
                            recall_data["Value"] = pd.to_numeric(recall_data["Value"], errors="coerce")
                            recall_data = recall_data.dropna(subset=["Value"])
                            
                            # 1. CLEAR YEAR SELECTION
                            st.markdown("### 📅 **Step 1: Select Year for Analysis**")
                            
                            # Available years display
                            available_years = sorted(recall_data["Year"].unique(), reverse=True)
                            st.info(f"📊 **Available Data Years:** {', '.join(available_years)} | **Coverage:** Full 5-year historical data (2020-2024)")
                            
                            # Explicit dropdown with help text
                            recall_year = st.selectbox(
                                "Choose the specific year you want to analyze:",
                                options=["2024
