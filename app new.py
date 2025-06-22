import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
    st.set_page_config(page_title="Metric Analyzer", layout="wide")
    st.title("📊 Dorenth Business Metric Analyzer")

    uploaded_file = st.file_uploader("📂 Upload Excel file (must include Year, Category, and numeric metric columns)", type=["xlsx", "xls"])

    if uploaded_file:
        try:
            # Read Excel
            df = pd.read_excel(uploaded_file)
            st.success("✅ File uploaded successfully!")

            st.subheader("🔍 Preview of Uploaded Data")
            st.dataframe(df, use_container_width=True)

            # Validate basic structure
            base_cols = {"Year", "Category"}
            if not base_cols.issubset(df.columns):
                st.error(f"❌ Missing columns: {base_cols - set(df.columns)}")
                return

            # Select metric from numeric columns (excluding Year/Category)
            numeric_cols = df.select_dtypes(include='number').columns.difference(["Year"])
            if len(numeric_cols) == 0:
                st.error("❌ No numeric metrics found to analyze.")
                return

            selected_metric = st.selectbox("📌 Select metric to analyze:", numeric_cols)

            # Pivot and show result
            st.subheader(f"📈 Pivot Table: {selected_metric}")
            pivot_table = df.pivot_table(index="Year", columns="Category", values=selected_metric, aggfunc="sum")
            st.dataframe(pivot_table, use_container_width=True)

            # Chart
            st.subheader("📊 Chart")
            fig, ax = plt.subplots(figsize=(10, 5))
            pivot_table.plot(kind="bar", ax=ax)
            st.pyplot(fig)

            # Download
            st.subheader("⬇️ Download Pivot Table")
            csv = pivot_table.reset_index().to_csv(index=False).encode("utf-8")
            st.download_button(
                label=f"Download {selected_metric} Table as CSV",
                data=csv,
                file_name=f"{selected_metric}_pivot.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"⚠️ Error processing file: {e}")

if __name__ == "__main__":
    main()
