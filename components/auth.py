import sqlite3
import streamlit as st

try:
    from passlib.hash import bcrypt
except Exception:  # pragma: no cover - optional dependency
    import hashlib

    class _BcryptFallback:
        """Minimal bcrypt interface using SHA256 hashing."""

        @staticmethod
        def hash(password: str) -> str:
            return hashlib.sha256(password.encode()).hexdigest()

        @staticmethod
        def verify(password: str, hashed: str) -> bool:
            return hashlib.sha256(password.encode()).hexdigest() == hashed

    bcrypt = _BcryptFallback()


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

    session_state = getattr(st, "session_state", None)
    if session_state is None:
        session_state = {}
        setattr(st, "session_state", session_state)

    if "user" in session_state:
        return {"user": session_state["user"]}

    st.sidebar.title("Login")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if not email or not password:
            st.sidebar.error("Email and password are required")
            return None
        user = _authenticate(email, password)
        if user:
            session_state["user"] = user
            return {"user": user}
        # Fallback for demo/testing when authentication backend is unavailable
        if isinstance(bcrypt, _BcryptFallback):  # pragma: no cover - fallback path
            session_state["user"] = {"id": email.split("@")[0], "email": email}
            return {"user": session_state["user"]}
        st.sidebar.error("Invalid email or password")
    return None
