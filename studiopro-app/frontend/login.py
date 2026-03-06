import streamlit as st
import sys
import os

# Add the parent directory to sys.path to allow imports from other folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.auth import authenticate_user

def login_page():
    st.header("🔐 User Login")
    
    with st.form("login_form"):
        username_or_email = st.text_input("Username or Email")
        password = st.text_input("Password", type="password")
        
        submit_btn = st.form_submit_button("Login")
        
        if submit_btn:
            if not username_or_email or not password:
                st.error("Please enter both username/email and password.")
            else:
                success, result = authenticate_user(username_or_email, password)
                if success:
                    st.session_state.user = result
                    st.session_state.page = "dashboard"
                    st.success(f"Welcome back, {result['username']}!")
                    st.rerun()
                else:
                    st.error(result)

    st.write("New user?")
    if st.button("Create an Account"):
        st.session_state.page = "registration"
        st.rerun()

if __name__ == "__main__":
    login_page()
