import streamlit as st
import hashlib
import json
import os
from datetime import datetime

st.set_page_config(page_title="Auth App", page_icon="🔐", layout="centered")

DB_FILE = "users_db.json"

# ── Database helpers ──────────────────────────────────────────────────────────

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE) as f:
            return json.load(f)
    return {}

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ── Session state defaults ────────────────────────────────────────────────────

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ── App ───────────────────────────────────────────────────────────────────────

st.title("🔐 User Portal")

# ── LOGGED IN: Dashboard ──────────────────────────────────────────────────────

if st.session_state.logged_in:
    db = load_db()
    user = db.get(st.session_state.username, {})

    st.success(f"Welcome back, **{st.session_state.username}**! 👋")
    st.divider()

    col1, col2 = st.columns(2)
    col1.metric("Username", st.session_state.username)
    col2.metric("Member Since", user.get("joined", "N/A"))

    st.divider()

    if st.button("Logout", type="primary", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# ── LOGGED OUT: Login / Register tabs ────────────────────────────────────────

else:
    tab_login, tab_register = st.tabs(["Login", "Register"])

    # ── Login ──
    with tab_login:
        st.subheader("Sign in to your account")

        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", type="primary", use_container_width=True, key="login_btn"):
            if not username or not password:
                st.warning("Please fill in all fields.")
            else:
                db = load_db()
                if username in db and db[username]["password"] == hash_password(password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

    # ── Register ──
    with tab_register:
        st.subheader("Create a new account")

        new_username = st.text_input("Choose a username", key="reg_username")
        new_password = st.text_input("Choose a password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm password", type="password", key="reg_confirm")

        if st.button("Register", type="primary", use_container_width=True, key="register_btn"):
            if not new_username or not new_password or not confirm_password:
                st.warning("Please fill in all fields.")
            elif len(new_username) < 3:
                st.warning("Username must be at least 3 characters.")
            elif len(new_password) < 6:
                st.warning("Password must be at least 6 characters.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                db = load_db()
                if new_username in db:
                    st.error("Username already taken. Please choose another.")
                else:
                    db[new_username] = {
                        "password": hash_password(new_password),
                        "joined": datetime.now().strftime("%Y-%m-%d"),
                    }
                    save_db(db)
                    st.success("Account created! You can now log in.")