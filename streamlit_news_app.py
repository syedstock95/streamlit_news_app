import streamlit as st
import pandas as pd
import os

# App title
st.markdown("## 📰 Market News Summary Dashboard")

# Set the news folder path
NEWS_FOLDER = os.path.join(os.path.dirname(__file__), "news")
os.makedirs(NEWS_FOLDER, exist_ok=True)

# Get list of Excel files in the news folder
files = sorted(
    [f for f in os.listdir(NEWS_FOLDER) if f.endswith(".xlsx")],
    reverse=True
)

# Dropdown to select a file
if files:
    selected_file = st.selectbox("?? Select news summary file", files)

    try:
        file_path = os.path.join(NEWS_FOLDER, selected_file)
        df = pd.read_excel(file_path)

        st.success(f"✅ Loaded: {selected_file}")

        # Display DataFrame
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Failed to load {selected_file}: {str(e)}")

else:
    st.warning("⚠️ No .xlsx news summary files found in /news folder.")

