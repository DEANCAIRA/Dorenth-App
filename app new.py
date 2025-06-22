import streamlit as st
import pandas as pd

def find_numeric_year_columns(df):
    """Return columns that are exactly 4-digit numbers."""
    df.columns = df.columns.astype(str)
    return [col for col in df.columns if col.isdigit() and len(col) == 4]

def extract_ebitda_by_year(df, company_name, year):
    """Extract EBITDA for a specific year from a financial table."""
    ebitda_row = df[df.iloc[:, 1].astype(str).str.upper().str.contains("EBITDA", na=False)]

    if ebitda_row.empty:
        return (company_name, f"EBITDA row not found")

    try:
        value = ebitda_row[str(year)].values[0]
        return (company_name, value)
    except:
        try:
            fallback = ebitda_row.iloc[0, 3]
            return (company_name, fallback)
        except:
            return (company_name, f"{year} column not found")

def main():
    st.set_page_config(page_title="EBITDA Extractor", layout="wide")
    st.title("📊 Exact EBITDA Extractor (Numeric Year Columns Only)")

    st.markdown("Upload Excel files with a **financial table**, where:")
    st.markdown("- EBITDA is in column 2")
    st.markdown("- Year columns are exactly like `2020`, `2021`, etc.")
    st.markdown("- Skips first 3 rows of each sheet")

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
        all_years = set()
        for df in data.values():
            all_years.update(find_numeric_year_columns(df))

        if not all_years:
            st.error("❌ No numeric 4-digit year columns found.")
            return

        selected_year = st.selectbox("📅 Select year to extract EBITDA:", sorted(all_years))

        results = []
        for name, df in data.items():
            result = extract_ebitda_by_year(df, name, selected_year)
            results.append(result)

        result_df = pd.DataFrame(results, columns=["Company", f"EBITDA {selected_year}"])
        st.subheader("✅ Extracted Results")
        st.dataframe(result_df)

        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download as CSV",
            data=csv,
            file_name=f"ebitda_{selected_year}_results.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
