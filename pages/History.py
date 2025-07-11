import streamlit as st
import pandas as pd
from utils.auth_db import get_user_history, clear_user_history

# 🔒 Redirect to login page if not logged in
if not st.session_state.get("logged_in"):
    st.switch_page("pages/login_signup.py")

# Page configuration
st.set_page_config(page_title="Prediction History", layout="wide")
st.markdown("### 🧾 Your Prediction History")

# Check if user is logged in
if "username" not in st.session_state:
    st.warning("🔒 Please log in to view your prediction history.")
    st.stop()

# Fetch prediction history from database
try:
    history = get_user_history(st.session_state.username)
except Exception as e:
    st.error(f"Failed to load history: {e}")
    st.stop()

# Show history or message
if not history:
    st.info("No prediction history found for your account.")
else:
    df = pd.DataFrame(history, columns=["Filename", "Prediction", "Confidence"])
    df["Confidence"] = (df["Confidence"]).round(2).astype(str) + '%'
    
    df.index = df.index + 1  # Start index from 1
    st.dataframe(df, use_container_width=True)


    # 🧹 Clear History button
    if st.button("🗑️ Clear All History"):
        clear_user_history(st.session_state.username)
        st.success("✅ History cleared successfully.")
        st.rerun()
