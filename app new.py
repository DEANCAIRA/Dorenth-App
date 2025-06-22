import streamlit as st
import pandas as pd

def extract_years(df):
    """Extract list of columns that look like years (e.g. 2020, 2021)"""
    df.columns = df.columns.astype(str)
    return [col for col in df.columns if col.isdigit() and len(col) == 4]

def extract_ebitda_value(df, company_name, year):
    # Normalize headers
    df.columns = df.columns.astype(str)

    # Find row where 2nd column contains "EBITDA"
    ebitda_row = df[df.iloc[:, 1].astype(str).str.upper().str.contains("EBITDA", na=False)]

    if ebitda_row.empty:
        return {"Company": company_name, f"EBITDA {year}": "Not found"}

    if year in df.columns:
        value = ebitda_row[year].values[0]
    else:
        try:
            value = ebitda_row.iloc[0, 3]  # fallback
        except:
            value = "Year not found"

    return {"Company": company_name, f"EBITDA {year}": value}

def main():
    st.set_page_config(page_title="EBITDA Extractor", layout="wide")
    st.title("📊 Auto Extract EBITDA from Excel Files")

    st.write("Upload up to 2 Excel files containing financial tables. The app will detect the EBITDA row and let you choose the year to extract.")

    col1, col2 = st.columns(2)

    # Placeholder for dynamic year selection
    available_years = []

    file_data = {}

    with col1:
        file1 = st.file_uploader("Upload ALPHA Excel file", type=["xlsx", "xls"], key="alpha")
        if file1:
            df1 = pd.read_excel(file1, sheet_name=0, skiprows=3)
            file_data["Alpha"] = df1
            available_years += extract_years(df1)

    with col2:
        file2 = st.file_uploader("Upload OMEGA Excel file", type=["xlsx", "xls"], key="omega")
        if file2:
            df2 = pd.read_excel(file2, sheet_name=0, skiprows=3)
            file_data["Omega"] = df2
            available_years += extract_years(df2)

    if file_data:
        # Remove duplicates & sort years
        year_options = sorted(set(available_years))
        if not year_options:
            st.error("❌ No valid year columns (e.g., '2021', '2022') found in the uploaded files.")
            return

        selected_year = st.selectbox("📅 Select year to extract:", year_options)

        # Extract results
        results = []
        for company_name, df in file_data.items():
            result = extract_ebitda_value(df, company_name, selected_year)
            results.append(result)

        result_df = pd.DataFrame(results)
        st.subheader(f"📋 Extracted EBITDA ({selected_year})")
        st.dataframe(result_df)

        # Download result
        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Results as CSV",
            data=csv,
            file_name=f"ebitda_{selected_year}_results.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
