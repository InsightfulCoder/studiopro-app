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
    st.session_state.page = "login"
if 'user' not in st.session_state:
    st.session_state.user = None

def main():
    # Force login if not authenticated and not on registration page
    if not st.session_state.user and st.session_state.page != "registration":
        login_page()
    elif st.session_state.page == "registration":
        registration_page()
    elif st.session_state.user:
        if st.session_state.page == "payment":
            payment_page()
        elif st.session_state.page == "download":
            download_page()
        else:
            dashboard_page()
    else:
        login_page()


if __name__ == "__main__":
    main()
