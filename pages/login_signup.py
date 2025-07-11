import streamlit as st
import sqlite3
import hashlib
from datetime import datetime

# ✅ Redirect to app.py after login
if st.session_state.get("redirect_to_app"):
    st.session_state.redirect_to_app = False  # reset the flag
    st.switch_page("app.py")


# ---------- PASSWORD UTILS ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------- DB FUNCTIONS ----------
def create_user_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT,
        created_at TIMESTAMP
    )''')
    conn.commit()
    conn.close()

def add_user(username, email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (username, email, password, created_at) VALUES (?, ?, ?, ?)", 
              (username, email, hash_password(password), datetime.now()))
    conn.commit()
    conn.close()

def email_exists(email):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    result = c.fetchone()
    conn.close()
    return result is not None

def username_exists(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    return result is not None

def verify_user(email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE email=? AND password=?", 
              (email, hash_password(password)))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

# ---------- SESSION SETUP ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.login_time = None

# ---------- UI ----------
st.set_page_config(page_title="Login / Signup", layout="centered")
st.title("🔐 Login / Signup")
create_user_table()

tab1, tab2 = st.tabs(["🔐 Login", "📝 Signup"])

# ---------- LOGIN TAB ----------
with tab1:
    st.subheader("Login to your account")
    with st.form("login_form"):
        email = st.text_input("📧 Email")
        password = st.text_input("🔒 Password", type="password")
        login_btn = st.form_submit_button("Login")

        if login_btn:
            if not email or not password:
                st.error("❗ Please fill in all fields.")
            else:
                user = verify_user(email, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = user
                    st.session_state.login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    st.session_state.redirect_to_app = True

                    st.success(f"✅ Welcome, {user}!")
                    st.toast(f"Welcome, {user}!", icon="✅")
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password.")

                    


# ---------- SIGNUP TAB ----------
with tab2:
    st.subheader("Create a new account")
    with st.form("signup_form"):
        username = st.text_input("👤 Username")
        email = st.text_input("📧 Email")
        password = st.text_input("🔒 Password", type="password")
        confirm_password = st.text_input("🔁 Confirm Password", type="password")
        signup_btn = st.form_submit_button("Create Account")

        if signup_btn:
            if not username or not email or not password or not confirm_password:
                st.error("❗ All fields are required.")
            elif password != confirm_password:
                st.error("❗ Passwords do not match.")
            elif email_exists(email):
                st.error("❗ Email already registered.")
            elif username_exists(username):
                st.error("❗ Username already taken.")
            else:
                add_user(username, email, password)
                st.success("✅ Account created successfully! You can now log in.")
