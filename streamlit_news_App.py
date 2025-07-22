import streamlit as st
import pandas as pd
import os
from bs4 import BeautifulSoup

# Streamlit config
st.set_page_config(page_title="?? Market & Crypto News Summary", layout="wide")
NEWS_DIR = r"D:\OneDrive\Documents\shares\Document\News"

st.markdown("## ?? Market & Crypto News Summary")

# Exit App button
if st.button("? Exit App"):
    import os
    os._exit(0)

# List available Excel files
files = sorted([f for f in os.listdir(NEWS_DIR) if f.endswith(".xlsx")], reverse=True)
if not files:
    st.warning("No news files found.")
    st.stop()

# File selector
selected_file = st.selectbox("?? Select a news summary file:", files)
file_path = os.path.join(NEWS_DIR, selected_file)

# Load file
try:
    df = pd.read_excel(file_path)
    st.success(f"Loaded {selected_file} ?")
except Exception as e:
    st.error(f"Error reading file: {e}")
    st.stop()

# Search box
search = st.text_input("?? Search news by keyword (title, summary or link):")
if search:
    df = df[df.apply(lambda row: search.lower() in str(row['title']).lower() or
                                 search.lower() in str(row['summary']).lower() or
                                 search.lower() in str(row['link']).lower(), axis=1)]

if df.empty:
    st.info("No matching results.")
    st.stop()

# Display news grouped by source
for source, group in df.groupby("source"):
    st.markdown(f"### ?? <u>{source}</u>", unsafe_allow_html=True)

    for _, row in group.iterrows():
        title = row['title'] or ""
        link = row['link'] or ""
        raw_summary = row['summary'] or ""

        # Clean raw HTML (like Cointelegraph image tags)
        try:
            soup = BeautifulSoup(raw_summary, "html.parser")
            for img in soup.find_all("img"):
                img.decompose()
            summary_text = soup.get_text().strip()
        except:
            summary_text = raw_summary

        # Format HTML with requested font sizes
        title_html = f"<div style='font-size:22px; color:#1f77b4; font-weight:bold'>{title}</div>"
        link_html = f"<a href='{link}' target='_blank' style='font-size:20px; font-weight:500'>?? Read more</a>"
        summary_html = f"<div style='color:#222; font-size:20px; margin-top:6px'>{summary_text}</div>"

        # Final card layout
        card_html = f"""
        <div style='margin-bottom:28px'>
            {title_html}
            {link_html}
            {summary_html}
        </div>
        <hr style='border-top:1px solid #ccc'>
        """
        st.markdown(card_html, unsafe_allow_html=True)
