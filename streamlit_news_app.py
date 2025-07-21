import streamlit as st
import pandas as pd
import os

# Set the news folder path
NEWS_FOLDER = "news"

st.set_page_config(page_title="?? Market News Dashboard", layout="wide")
st.title("?? Market News Summary Dashboard")

# Check and list available Excel files
try:
    files = sorted(
        [f for f in os.listdir(NEWS_FOLDER) if f.endswith(".xlsx")],
        reverse=True
    )
except FileNotFoundError:
    st.error("? Error: 'news' folder not found. Please make sure it exists in the same directory.")
    files = []

if files:
    selected_file = st.selectbox("?? Select news summary file", files)

    file_path = os.path.join(NEWS_FOLDER, selected_file)

    try:
        df = pd.read_excel(file_path)
        st.success(f"? Loaded: {selected_file}")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"? Failed to read the Excel file. Reason: {e}")
else:
    st.warning("?? No .xlsx files found in the 'news' folder.")

