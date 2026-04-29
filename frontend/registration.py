import streamlit as st
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.auth import register_user
from utils.ui_utils import section_header, safe_rerun

def registration_page():
    # Centered container
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.6, 1])
    
    with col2:
        st.markdown(f"""
            <div class="premium-card" style="padding: 3.5rem; border-radius: 40px; animation: reveal 0.8s ease-out forwards;">
                <div style="text-align: center; margin-bottom: 3rem;">
                    <div style="width: 80px; height: 80px; border-radius: 24px; background: var(--accent-gradient); display: flex; align-items: center; justify-content: center; font-size: 2.5rem; margin: 0 auto 1.5rem; box-shadow: var(--shadow-glow);">✨</div>
                    <h2 style="font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem;">Join Orbit</h2>
                    <p style="color: var(--text-muted); font-size: 1rem;">Become part of the world's most advanced AI creative network.</p>
                </div>
        """, unsafe_allow_html=True)
        
        with st.form("registration_form_v3"):
            email = st.text_input("Email Address", placeholder="user@example.com")
            username = st.text_input("Choose Username", placeholder="e.g. creative_genius")
            password = st.text_input("Security Password", type="password", help="Minimum 8 characters")
            confirm_password = st.text_input("Verify Password", type="password")
            
            terms = st.checkbox("Accept Terms of Service & Neural Privacy Policy")
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("INITIALIZE ACCOUNT", use_container_width=True)
            
            if submit:
                if not username or not email or not password:
                    st.error("All parameters are required.")
                elif password != confirm_password:
                    st.error("Key mismatch: Passwords do not match.")
                elif not terms:
                    st.warning("Please acknowledge the neural privacy policy.")
                else:
                    success, message = register_user(username, email, password)
                    if success:
                        st.success("Synchronizing account... Welcome aboard!")
                        st.balloons()
                        st.session_state.page = "login"
                        safe_rerun()
                    else:
                        st.error(message)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        if st.button("Already a member? Sign in", key="nav_to_login"):
            st.session_state.page = "login"
            safe_rerun()
        st.markdown('</div></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    registration_page()
