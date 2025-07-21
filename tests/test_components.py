import os
import sys
import types
import importlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class DummySidebar:
    def __init__(self, email="", password="", click=True):
        self.email = email
        self.password = password
        self.click = click
        self.error_message = None

    def title(self, *args, **kwargs):
        pass

    def text_input(self, label, type=None):
        return self.email if label == "Email" else self.password

    def button(self, label):
        return self.click

    def error(self, msg):
        self.error_message = msg


class DummyUpload:
    def __init__(self):
        self.name = "invoice.pdf"

    def read(self):
        return b"dummy"


class DummyStreamlit:
    def __init__(self, sidebar):
        self.sidebar = sidebar
        self.success_msg = None
        self.warning_msg = None
        self.error_msg = None
        self.tables = []

    # sidebar proxy methods for convenience
    def subheader(self, *args, **kwargs):
        pass

    def file_uploader(self, *args, **kwargs):
        return DummyUpload()

    def error(self, msg):
        self.error_msg = msg

    def write(self, *args, **kwargs):
        pass

    def table(self, data):
        self.tables.append(data)

    def success(self, msg):
        self.success_msg = msg

    def warning(self, msg):
        self.warning_msg = msg


def test_login_user_success(monkeypatch):
    sidebar = DummySidebar(email="user@example.com", password="secret", click=True)
    st = DummyStreamlit(sidebar)
    monkeypatch.setitem(sys.modules, "streamlit", st)
    import components.auth as auth
    importlib.reload(auth)
    session = auth.login_user()
    assert session["user"]["email"] == "user@example.com"
    assert sidebar.error_message is None


def test_login_user_missing(monkeypatch):
    sidebar = DummySidebar(email="", password="", click=True)
    st = DummyStreamlit(sidebar)
    monkeypatch.setitem(sys.modules, "streamlit", st)
    import components.auth as auth
    importlib.reload(auth)
    session = auth.login_user()
    assert session is None
    assert sidebar.error_message == "Email and password are required"


def test_run_invoice_matcher_success(monkeypatch):
    sidebar = DummySidebar()
    st = DummyStreamlit(sidebar)
    monkeypatch.setitem(sys.modules, "streamlit", st)

    import components.invoice_matcher_ui as imui
    monkeypatch.setattr(imui, "extract_invoice_data_from_pdf", lambda x: {"amount": 100, "supplier": "ACME", "date": "2023-01-01"})
    monkeypatch.setattr(imui, "match_invoice_to_bank", lambda data, rows: (90, rows[0]))
    importlib.reload(imui)

    imui.run_invoice_matcher([{"Description": "ACME Goods", "Amount": "100"}])
    assert st.success_msg

