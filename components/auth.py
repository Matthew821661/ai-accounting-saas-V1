import sqlite3
import streamlit as st
from passlib.hash import bcrypt


DB_PATH = "users.db"


def _get_connection():
    """Return a connection to the user database, creating tables if needed."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE, password_hash TEXT)"
    )
    return conn


def _ensure_default_user():
    """Create a default user on first run so the demo works out of the box."""
    conn = _get_connection()
    cur = conn.execute("SELECT COUNT(*) FROM users")
    count = cur.fetchone()[0]
    if count == 0:
        conn.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            ("admin@example.com", bcrypt.hash("admin")),
        )
        conn.commit()
    conn.close()


def _authenticate(email: str, password: str):
    conn = _get_connection()
    cur = conn.execute("SELECT id, email, password_hash FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()
    if row and bcrypt.verify(password, row[2]):
        return {"id": row[0], "email": row[1]}
    return None


def login_user():
    """Render a login form and return a session dict if authentication succeeds."""

    _ensure_default_user()

    if "user" in st.session_state:
        return {"user": st.session_state["user"]}

    st.sidebar.title("Login")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if not email or not password:
            st.sidebar.error("Email and password are required")
            return None
        user = _authenticate(email, password)
        if user:
            st.session_state["user"] = user
            return {"user": user}
        st.sidebar.error("Invalid email or password")
    return None
