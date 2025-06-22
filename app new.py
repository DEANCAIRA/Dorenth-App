import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
    st.set_page_config(page_title="Demand Analyzer", layout="wide")
    st.title("📊 Dorenth Demand Analyzer")

    # Step 1: Upload Excel file
    uploaded_file = st.file_uploader("📂 Upload Excel file (must include Year, Category, Value columns)", type=["xlsx", "xls"])

    if uploaded_file:
        try:
            # Step 2: Read and preview file
            df = pd.read_excel(uploaded_file)
            st.success("✅ File uploaded successfully!")

            st.subheader("🔍 Preview of Uploaded Data")
            st.dataframe(df, use_container_width=True)

            # Step 3: Validate required columns
            required_cols = {"Year", "Category", "Value"}
            if not required_cols.issubset(df.columns):
                st.error(f"❌ Missing required columns: {required_cols - set(df.columns)}")
                return

            # Step 4: Create pivot table (safe aggregation)
            st.subheader("📈 Aggregated Data (Pivot Table)")
            pivot_table = df.pivot_table(index="Year", columns="Category", values="Value", aggfunc="sum")
            st.dataframe(pivot_table, use_container_width=True)

            # Step 5: Plot chart
            st.subheader("📊 Visualization")
            fig, ax = plt.subplots(figsize=(10, 5))
            pivot_table.plot(kind="bar", ax=ax)
            st.pyplot(fig)

            # Step 6: Download processed table
            st.subheader("⬇️ Download Processed Data")
            csv = pivot_table.reset_index().to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Pivot Table as CSV",
                data=csv,
                file_name="analyzed_output.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"⚠️ Error processing file: {e}")

if __name__ == "__main__":
    main()
