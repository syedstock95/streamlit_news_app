import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Set page config
st.set_page_config(page_title="?? Market & Crypto News Dashboard", layout="wide")
st.title("?? Market & Crypto News Summary")

# Primary news folder path (local) — adjust if running locally
LOCAL_NEWS_FOLDER = "D:/OneDrive/Documents/shares/Document/News"

# Fallback for deployment (like Streamlit Cloud)
DEFAULT_NEWS_FOLDER = "news"

# Choose folder based on environment
if os.path.exists(LOCAL_NEWS_FOLDER):
    NEWS_FOLDER = LOCAL_NEWS_FOLDER
else:
    NEWS_FOLDER = DEFAULT_NEWS_FOLDER

# Ensure NEWS_FOLDER exists
if not os.path.exists(NEWS_FOLDER):
    os.makedirs(NEWS_FOLDER)

# List Excel files
try:
    files = sorted([f for f in os.listdir(NEWS_FOLDER) if f.endswith(".xlsx")], reverse=True)
except Exception as e:
    st.error(f"? Could not read from folder `{NEWS_FOLDER}`: {e}")
    files = []

# UI to select file
if not files:
    st.warning(f"No news summary files found in `{NEWS_FOLDER}`.")
else:
    selected_file = st.selectbox("?? Select a news summary file:", files)
    file_path = os.path.join(NEWS_FOLDER, selected_file)

    try:
        df = pd.read_excel(file_path)
        st.success(f"? Loaded: {selected_file}")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"? Error loading file: {e}")

# Footer
st.markdown("---")
st.caption("?? News from FMP, Yahoo, CoinDesk, Google News etc.")
st.caption(f"?? Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
