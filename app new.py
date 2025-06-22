import streamlit as st
import pandas as pd

# Normalize column headers to string and extract 4-digit numeric years only
def extract_numeric_year_columns(df):
    df.columns = [str(col).split(".")[0] for col in df.columns]  # normalize 2021.0 ➝ "2021"
    return [col for col in df.columns if col.isdigit() and 2000 <= int(col) <= 2100]

# Locate the EBITDA row from column index 1, then extract value from selected year column
def extract_ebitda(df, company_name, year):
    # Ensure headers are strings
    df.columns = [str(col).split(".")[0] for col in df.columns]
    
    # Match "EBITDA" in second column
    ebitda_row = df[df.iloc[:, 1].astype(str).str.upper().str.contains("EBITDA", na=False)]

    if ebitda_row.empty:
        return (company_name, "EBITDA not found")

    # Extract the value for the selected year
    try:
        value = ebitda_row[year].values[0]
        return (company_name, value)
    except Exception:
        return (company_name, f"No value found for {year}")

def main():
    st.set_page_config(page_title="EBITDA Extractor", layout="wide")
    st.title("📊 Accurate EBITDA Extractor from Excel Files")

    st.markdown("""
    Upload Excel files with:
    - 3 skipped rows before table
    - EBITDA in **second column**
    - Years like `2021`, `2022` in header row
    """)

    col1, col2 = st.columns(2)
    data = {}

    with col1:
        file1 = st.file_uploader("📂 Upload ALPHA.xlsx", type=["xlsx"], key="alpha")
        if file1:
            df1 = pd.read_excel(file1, skiprows=3)
            data["Alpha"] = df1

    with col2:
        file2 = st.file_uploader("📂 Upload OMEGA.xlsx", type=["xlsx"], key="omega")
        if file2:
            df2 = pd.read_excel(file2, skiprows=3)
            data["Omega"] = df2

    if data:
        # Collect all valid numeric year headers
        all_years = set()
        for df in data.values():
            all_years.update(extract_numeric_year_columns(df))

        if not all_years:
            st.error("❌ No valid numeric year columns found.")
            return

        selected_year = st.selectbox("📅 Select year to extract:", sorted(all_years))

        # Run extraction
        results = []
        for name, df in data.items():
            result = extract_ebitda(df, name, selected_year)
            results.append(result)

        result_df = pd.DataFrame(results, columns=["Company", f"EBITDA {selected_year}"])
        st.subheader("✅ Extracted Results")
        st.dataframe(result_df)

        # Download
        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Results as CSV",
            data=csv,
            file_name=f"ebitda_{selected_year}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
