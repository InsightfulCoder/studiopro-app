import streamlit as st
st.set_page_config(page_title="StudioPro AI - Cartoonizer", page_icon="✨", layout="wide")

from frontend.registration import registration_page
from frontend.login import login_page
from frontend.dashboard import dashboard_page
from frontend.payment import payment_page
from frontend.download import download_page
from frontend.home import home_page
from frontend.pricing import pricing_page
from frontend.admin_dashboard import admin_dashboard_page
from frontend.legal import terms_page, privacy_page
from utils.ui_utils import inject_custom_css, safe_rerun

inject_custom_css()

# Initialize session state for navigation and user
if 'page' not in st.session_state:
    st.session_state.page = "home" # Start at the home landing page
if 'user' not in st.session_state:
    st.session_state.user = None
if 'guest_trials' not in st.session_state:
    st.session_state.guest_trials = 0

def main():
    # Routing Logic
    if st.session_state.page == "registration":
        registration_page()
    elif st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "payment":
        if not st.session_state.user:
            st.session_state.page = "login"
            safe_rerun()
        payment_page()
    elif st.session_state.page == "download":
        download_page()
    elif st.session_state.page == "studio":
        from frontend.image_processing import image_processing_page
        image_processing_page()
    elif st.session_state.page == "dashboard":
        if not st.session_state.user:
            st.session_state.page = "login"
            safe_rerun()
        dashboard_page()
    elif st.session_state.page == "pricing":
        pricing_page()
    elif st.session_state.page == "admin_dashboard":
        admin_dashboard_page()
    elif st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "terms":
        terms_page()
    elif st.session_state.page == "privacy":
        privacy_page()
    else:
        # Default to home
        home_page()


if __name__ == "__main__":
    main()
