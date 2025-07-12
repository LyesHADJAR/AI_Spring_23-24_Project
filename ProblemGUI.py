import streamlit as st
import pandas as pd
import io
import sys
import csv

from DataLoader import DataLoader
from main import mycountry, search_for_year

# ----- STREAMLIT CONFIG -----
st.set_page_config(page_title="🌱 Agricultural Land Optimizer", layout="centered")

# ----- CUSTOM CSS for GREEN THEME -----
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            background-color: #001f00;
            color: #ccffcc;
        }
        .stButton > button {
            background-color: #006600;
            color: white;
            font-weight: bold;
            border-radius: 10px;
        }
        .stDownloadButton > button {
            background-color: #228B22;
            color: white;
            font-weight: bold;
            border-radius: 10px;
        }
        .stTextInput, .stSelectbox {
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ----- APP TITLE -----
st.title("🌱 Agricultural Land Optimizer")

# ----- FILE UPLOAD -----
wilaya_file = st.file_uploader("📄 Upload Wilaya CSV File", type=["csv"])
product_file = st.file_uploader("📄 Upload Product CSV File", type=["csv"])

# ----- SEARCH METHOD SELECTOR -----
search_methods = ["IDA_Star", "IDS", "steepest", "UCS"]
search_method = st.selectbox("🔍 Select Search Method", ["Select Search Method"] + search_methods)

# ----- OUTPUT PLACEHOLDER -----
output_buffer = io.StringIO()

# ----- RUN SEARCH -----
if st.button("🚀 Run Search"):
    if not wilaya_file or not product_file:
        st.error("❌ Please upload both the Wilaya and Product CSV files.")
    elif search_method == "Select Search Method":
        st.error("❌ Please select a valid search method.")
    else:
        try:
            # Process data
            cities_data, consumption, total_production, prices = DataLoader.load_country_data(
                wilaya_file, product_file
            )
            country = mycountry(cities_data, consumption, prices)

            # Redirect stdout
            old_stdout = sys.stdout
            sys.stdout = output_buffer

            search_for_year(country, search_method)

            sys.stdout = old_stdout
            output_text = output_buffer.getvalue()

            # Show results
            st.subheader("📋 Search Results")
            st.text_area("Output", output_text, height=400)

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
