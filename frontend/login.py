import streamlit as st
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.auth import authenticate_user
from utils.ui_utils import section_header, safe_rerun

def login_page():
    # Centered Layout
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.4, 1])
    
    with col2:
        st.markdown(f"""
            <div class="premium-card" style="padding: 3.5rem; border-radius: 40px; animation: reveal 0.8s ease-out forwards;">
                <div style="text-align: center; margin-bottom: 3rem;">
                    <div style="width: 80px; height: 80px; border-radius: 24px; background: var(--accent-gradient); display: flex; align-items: center; justify-content: center; font-size: 2.5rem; margin: 0 auto 1.5rem; box-shadow: var(--shadow-glow);">🔑</div>
                    <h2 style="font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem;">Welcome back</h2>
                    <p style="color: var(--text-muted); font-size: 1rem;">Enter your credentials to access your studio.</p>
                </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form_v3", clear_on_submit=False):
            username = st.text_input("Username or Email", placeholder="yourname@example.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("SIGN IN TO STUDIO", use_container_width=True)
            
            if submit:
                if not username or not password:
                    st.error("Please fill in all fields.")
                else:
                    success, result = authenticate_user(username, password)
                    if success:
                        st.session_state.user = result
                        st.success(f"Authorization successful. Welcome {result['username']}!")
                        if result['email'] == "admin@studiopro.ai":
                            st.session_state.page = "admin_dashboard"
                        else:
                            st.session_state.page = "dashboard"
                        safe_rerun()
                    else:
                        st.error(result)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("New to StudioPro? Create a workspace", key="nav_to_reg"):
            st.session_state.page = "registration"
            safe_rerun()
        st.markdown('</div></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    login_page()
