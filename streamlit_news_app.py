import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Set page config
st.set_page_config(page_title="📰 Market & Crypto News Dashboard", layout="wide")

# Title
st.title("📈 Market & Crypto News Summary")

# Folder containing news Excel files
NEWS_FOLDER = "D:/OneDrive/Documents/shares/Document/News"

# List available Excel files
files = sorted([f for f in os.listdir(NEWS_FOLDER) if f.endswith(".xlsx")], reverse=True)

if not files:
    st.warning("No news summary files found.")
else:
    selected_file = st.selectbox("Select a news summary file:", files)
    file_path = os.path.join(NEWS_FOLDER, selected_file)

    try:
        df = pd.read_excel(file_path)
        st.success(f"Loaded {selected_file} ✅")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading file: {e}")
