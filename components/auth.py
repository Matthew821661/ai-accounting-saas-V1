import streamlit as st


def login_user():
    """Render a very simple login form and return a session dict."""

    st.sidebar.title("Login")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if not email or not password:
            st.sidebar.error("Email and password are required")
            return None
        return {"user": {"id": email.split("@")[0], "email": email}}
    return None
