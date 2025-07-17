import streamlit as st

from components.auth import login_user
from components.dashboard import launch_dashboard

# Configure the Streamlit page
st.set_page_config(page_title="AI Bookkeeping SaaS", layout="wide")

session = login_user()
if session:
    launch_dashboard(session)
