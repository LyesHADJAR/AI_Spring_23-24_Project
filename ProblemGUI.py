import streamlit as st
import pandas as pd
import io
import sys
import csv

from DataLoader import DataLoader
from main import mycountry, search_for_year

st.set_page_config(page_title="Agricultural Land Optimizer", layout="centered")

st.title("🌱 Agricultural Land Optimizer")

# Upload CSV files
wilaya_file = st.file_uploader("📄 Upload Wilaya CSV File", type=["csv"])
product_file = st.file_uploader("📄 Upload Product CSV File", type=["csv"])

# Search Method Selection
search_methods = ["IDA_Star", "IDS", "steepest", "UCS"]
search_method = st.selectbox("🔍 Select Search Method", ["Select Search Method"] + search_methods)

# Output buffer for redirected stdout
output_buffer = io.StringIO()

# Run search
if st.button("🚀 Run Search"):
    if not wilaya_file or not product_file:
        st.error("❌ Please upload both the Wilaya and Product CSV files.")
    elif search_method == "Select Search Method":
        st.error("❌ Please select a valid search method.")
    else:
        try:
            # Read uploaded files into DataLoader
            cities_data, consumption, total_production, prices = DataLoader.load_country_data(
                wilaya_file, product_file
            )
            country = mycountry(cities_data, consumption, prices)

            # Redirect stdout to buffer
            old_stdout = sys.stdout
            sys.stdout = output_buffer

            # Run search
            search_for_year(country, search_method)

            # Reset stdout
            sys.stdout = old_stdout

            # Get search result
            output_text = output_buffer.getvalue()

            # Display result
            st.subheader("📋 Search Output")
            st.text_area("Results", output_text, height=400)

            # CSV Export
            csv_lines = [line for line in output_text.split("\n") if line.strip()]
            csv_buffer = io.StringIO()
            writer = csv.writer(csv_buffer)

            for line in csv_lines:
                fields = [f.strip() for f in line.split("|")]
                writer.writerow(fields)

            st.download_button(
                label="📥 Download Output as CSV",
                data=csv_buffer.getvalue(),
                file_name="search_output.csv",
                mime="text/csv"
            )

        except Exception as e:
            sys.stdout = old_stdout
            st.error(f"❌ An error occurred: {e}")
