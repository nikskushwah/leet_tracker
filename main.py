import streamlit as st
from styles import get_css
from database import ensure_database
from app import run_app

st.set_page_config(page_title="Leetcode Tracker", layout="wide", initial_sidebar_state="expanded")
# Load CSS immediately after setting page config.
st.markdown(get_css(), unsafe_allow_html=True)

# Optionally ensure the database exists.
ensure_database()

# Launch the app.
run_app()
