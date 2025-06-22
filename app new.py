import streamlit as st
import pandas as pd

# ✅ Detect numeric year columns like 2021.0, 2022, etc.
def find_numeric_year_columns(df):
    numeric_cols = []
    for col in df.columns:
        try:
            year = float(col)
            if 2000 <= year <= 2100:
                numeric_cols.append(str(int(year)))
        except:
            continue
    return numeric_cols

# ✅ Extract EBITDA value from 2nd column for a given year
def extract_ebitda_by_year(df, company_name, year_str):
    # Ensure headers are strings
    df.columns = df.columns.astype(str)
    
    # Match "EBITDA" in second column
    try:
        ebitda_row = df[df.iloc[:, 1].astype(str).str.upper().str.contains("EBITDA", na=False)]
    except Exception:
        return (company_name, "EBITDA row not found")

    if ebitda_row.empty:
        return (company_name, "EBITDA row not found")

    try:
        value = ebitda_row[year_str].values[0]
        return (company_name, value)
    except:
        try:
            fallback = ebitda_row.iloc[0, 3]
            return (company_name, f"{year_str} column missing, fallback value: {fallback}")
        except:
            return (company_name, "No value found")

# ✅ Streamlit app
def main():
    st.set_page_config(page_title="EBITDA Extractor", layout="wide")
    st.title("📊 Exact EBITDA Extractor (from Excel Tables)")

    st.markdown("Upload Excel files with:")
    st.markdown("- Skipped header rows (3 rows skipped)")
    st.markdown("- EBITDA written in the **second column** (index 1)")
    st.markdown("- Year columns formatted as numbers (e.g. `2021`, `2022.0`)")

    col1, col2 = st.columns(2)
    data = {}

    with col1:
        file1 = st.file_uploader("📂 Upload ALPHA.xlsx", type=["xlsx"], key="alpha")
        if file1:
            df1 = pd.read_excel(file1, sheet_name=0, skiprows=3)
            data["Alpha"] = df1

    with col2:
        file2 = st.file_uploader("📂 Upload OMEGA.xlsx", type=["xlsx"], key="omega")
        if file2:
            df2 = pd.read_excel(file2, sheet_name=0, skiprows=3)
            data["Omega"] = df2

    if data:
        # Gather valid year columns from both files
        all_years = set()
        for df in data.values():
            all_years.update(find_numeric_year_columns(df))

        if not all_years:
            st.error("❌ No valid year columns found (e.g. '2021', '2022')")
            return

        # Sort and let user select one
        selected_year = st.selectbox("📅 Select year to extract EBITDA:", sorted(all_years))

        # Run extraction
        results = []
        for name, df in data.items():
            result = extract_ebitda_by_year(df, name, selected_year)
            results.append(result)

        result_df = pd.DataFrame(results, columns=["Company", f"EBITDA {selected_year}"])
        st.subheader("✅ Extracted Results")
        st.dataframe(result_df)

        # Download button
        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download as CSV",
            data=csv,
            file_name=f"ebitda_{selected_year}_results.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
