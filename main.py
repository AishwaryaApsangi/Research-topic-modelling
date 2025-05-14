import streamlit as st

st.set_page_config(page_title="RA Topic Explorer", page_icon="📄", layout="wide")

st.title("📄 Welcome to RA Topic Modeling Explorer")
st.markdown("""
Explore topic modeling insights from interview transcripts collected for the 'Describing and Understanding Sponsorship' research project.

Navigate through the tabs in the sidebar to:
- Visualize LDA topic word clouds
- View topic-grouped quote samples
- Explore BERTopic clustering results
- Examine raw top keywords per topic
""")
