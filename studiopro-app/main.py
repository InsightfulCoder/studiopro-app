import streamlit as st
from frontend.registration import registration_page
from frontend.login import login_page
from frontend.dashboard import dashboard_page
from frontend.payment import payment_page
from frontend.download import download_page
from utils.ui_utils import inject_custom_css

st.set_page_config(page_title="StudioPro AI - Cartoonizer", page_icon="✨", layout="wide")
inject_custom_css()

# Initialize session state for navigation and user
if 'page' not in st.session_state:
    st.session_state.page = "studio" # Start at the studio for guest trials
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
            st.rerun()
        payment_page()
    elif st.session_state.page == "download":
        download_page()
    elif st.session_state.page == "studio":
        from frontend.image_processing import image_processing_page
        image_processing_page()
    elif st.session_state.page == "dashboard":
        if not st.session_state.user:
            st.session_state.page = "login"
            st.rerun()
        dashboard_page()
    else:
        # Default to studio for guest experience
        from frontend.image_processing import image_processing_page
        image_processing_page()


if __name__ == "__main__":
    main()
