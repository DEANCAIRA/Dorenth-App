def extract_metric(df, metric_name):
    if df.empty or len(df.columns) < 3:
        return pd.DataFrame({"Year": [], "Value": []})

    # Ensure column 1 is string for searching metric names
    df[1] = df[1].astype(str)

    # Try to locate the year row by searching for numeric-only values in any row
    year_row = None
    for i in range(len(df)):
        possible_years = df.iloc[i, 2:]
        if all(pd.notna(x) and str(x).isdigit() for x in possible_years):
            year_row = df.iloc[i, 2:]
            break

    if year_row is None:
        # Fallback: assume row 2 is the year row (for embedded data)
        year_row = df.iloc[2, 2:]

    # Safely convert year row to string years
    years = [str(int(y)) for y in year_row if pd.notna(y) and str(y).isdigit()]

    # Try to find the matching metric row
    match = df[df[1].str.lower().str.strip() == metric_name.lower().strip()]
    if not match.empty:
        values = match.iloc[0, 2:].tolist()
        min_len = min(len(years), len(values))
        return pd.DataFrame({
            "Year": years[:min_len],
            "Value": values[:min_len]
        })
    else:
        return pd.DataFrame({
            "Year": years,
            "Value": [None] * len(years)
        })
