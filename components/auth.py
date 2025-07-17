import streamlit as st


def login_user():
    """Render a very simple login form and return a session dict."""

    st.sidebar.title("Login")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        return {"user": {"id": "demo", "email": email}}
    return None
