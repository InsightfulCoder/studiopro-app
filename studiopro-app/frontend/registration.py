import streamlit as st
import sys
import os

# Add the parent directory to sys.path to allow imports from other folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.auth import register_user

def registration_page():
    st.header("📝 Create an Account")
    
    with st.form("registration_form"):
        username = st.text_input("Username")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        # Terms and conditions
        terms = st.checkbox("I agree to the Terms and Conditions")
        
        submit_btn = st.form_submit_button("Sign Up")
        
        if submit_btn:
            if not username or not email or not password:
                st.error("All fields are required.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            elif not terms:
                st.warning("Please accept the Terms and Conditions.")
            else:
                success, message = register_user(username, email, password)
                if success:
                    st.success(message)
                    st.info("You can now go to the login page.")
                    st.balloons()
                else:
                    st.error(message)

    st.write("Already have an account?")
    if st.button("Go to Login"):
        st.session_state.page = "login"
        st.rerun()

if __name__ == "__main__":
    registration_page()
