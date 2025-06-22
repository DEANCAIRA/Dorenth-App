import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
    st.set_page_config(page_title="Demand Analyzer", layout="wide")
    st.title("📊 Dorenth Demand Analyzer")

    # File upload
    uploaded_file = st.file_uploader("📂 Upload Excel file (must include Year, Category, Value columns)", type=["xlsx", "xls"])

    if uploaded_file:
        try:
            # Read Excel file
            df = pd.read_excel(uploaded_file)
            st.success("✅ File uploaded and read successfully!")

            # Show raw data
            st.subheader("🔍 Preview of Uploaded Data")
            st.dataframe(df, use_container_width=True)

            # Check required columns
            required_cols = {"Year", "Category", "Value"}
            if not required_cols.issubset(df.columns):
                st.error(f"❌ Missing columns: {required_cols - set(df.columns)}")
                return

            # Pivot table
            st.subheader("📈 Aggregated Data (Pivot Table)")
            pivot_table = df.pivot_table(index="Year", columns="Category", values="Value", aggfunc="sum")
            st.dataframe(pivot_table, use_container_width=True)

            # Chart
            st.subheader("📊 Visualization")
            fig, ax = plt.subplots(figsize=(10, 5))
            pivot_table.plot(kind="bar", ax=ax)
            st.pyplot(fig)

            # Download analyzed result
            st.subheader("⬇️ Download Processed
