import streamlit as st

# 🔒 Redirect to login page if not logged in
if not st.session_state.get("logged_in"):
    st.switch_page("pages/login_signup.py")

st.set_page_config(page_title="Profile", layout="centered")
st.markdown("## 👤 Profile")
st.markdown("---")

if st.session_state.get("logged_in"):
    st.success(f"✅ Logged in as: **{st.session_state['username']}**")

    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/149/149071.png", width=80)
    with col2:
        st.markdown("### Account Details")
        st.markdown(f"""
        - **Username:** `{st.session_state['username']}`
        - **Login Time:** `{st.session_state['login_time']}`
        - **Access:** Logged-in user
        """)

    if st.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.login_time = None
        st.success("Logged out successfully.")
        st.rerun()
else:
    st.warning("🔒 You are not logged in.")
    st.info("Please go to the **Login / Signup** page to access your account.")
