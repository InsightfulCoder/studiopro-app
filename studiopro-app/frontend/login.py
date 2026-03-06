import streamlit as st
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.auth import authenticate_user
from utils.ui_utils import section_header

def login_page():
    col_l, col_m, col_r = st.columns([1, 1.2, 1])
    
    with col_m:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        section_header("Welcome Back", "Please sign in to continue")
        
        with st.form("login_form"):
            username_or_email = st.text_input("Username or Email", placeholder="user@example.com")
            password = st.text_input("Password", type="password")
            
            submit = st.form_submit_button("Sign In")
            
            if submit:
                if not username_or_email or not password:
                    st.error("Please enter both credentials")
                else:
                    success, result = authenticate_user(username_or_email, password)
                    if success:
                        st.session_state.user = result
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error(result)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("New here? Create Account"):
            st.session_state.page = "registration"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    login_page()
