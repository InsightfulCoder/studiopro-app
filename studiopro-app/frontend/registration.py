import streamlit as st
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.auth import register_user
from utils.ui_utils import section_header

def registration_page():
    # Centered container
    col_l, col_m, col_r = st.columns([1, 1.5, 1])
    
    with col_m:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        section_header("Create Account", "Join the StudioPro AI community")
        
        with st.form("registration_form"):
            username = st.text_input("Username", placeholder="e.g. artistic_soul")
            email = st.text_input("Email Address", placeholder="user@example.com")
            password = st.text_input("Password", type="password", help="Use 8+ characters")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            terms = st.checkbox("I agree to the Terms and Conditions")
            
            submit = st.form_submit_button("Sign Up")
            
            if submit:
                if not username or not email or not password:
                    st.error("All fields are required")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                elif not terms:
                    st.warning("Please accept the terms")
                else:
                    success, message = register_user(username, email, password)
                    if success:
                        st.success("Welcome aboard! Redirecting to login...")
                        st.balloons()
                        st.session_state.page = "login"
                        st.rerun()
                    else:
                        st.error(message)
        
        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("Have an account? Go to Login"):
            st.session_state.page = "login"
            st.rerun()

if __name__ == "__main__":
    registration_page()
