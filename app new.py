def extract_ebitda_by_year(df, company_name, year):
    df.columns = df.columns.astype(str)
    
    st.write(f"🔍 Columns in {company_name}:", list(df.columns))
    st.write(f"🔍 Sample first few rows from {company_name}:")
    st.dataframe(df.head(10))

    # Show second column values
    st.write(f"📌 Checking column index 1 (2nd column):")
    st.dataframe(df.iloc[:, 1].dropna().astype(str).head(20))

    # Try to find EBITDA in 2nd column
    match = df.iloc[:, 1].astype(str).str.upper().str.contains("EBITDA", na=False)
    st.write(f"🧪 Found EBITDA rows: {match.sum()} rows")

    ebitda_row = df[match]
    if ebitda_row.empty:
        return (company_name, "EBITDA row not found")

    try:
        value = ebitda_row[str(year)].values[0]
        return (company_name, value)
    except:
        try:
            fallback = ebitda_row.iloc[0, 3]
            return (company_name, fallback)
        except:
            return (company_name, f"{year} column not found")
