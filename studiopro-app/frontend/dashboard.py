import streamlit as st
from frontend.image_processing import image_processing_page
from utils.ui_utils import section_header

def dashboard_page():
    user = st.session_state.user
    
    # Sidebar Navigation with custom styling
    with st.sidebar:
        st.markdown(f"### Welcome, <br><span style='color: #A855F7;'>{user['username']}</span>", unsafe_allow_html=True)
        st.write("---")
        app_mode = st.radio("Navigation", ["Overview", "Artistic Studio", "Transaction History", "User Profile"])
        st.write("---")
        if st.button("Logout"):
            st.session_state.user = None
            st.session_state.page = "login"
            st.rerun()

    if app_mode == "Overview":
        section_header("Dashboard Overview", "Monitor your creative activity")
        
        # Stats Cards in Glassmorphism style
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.metric("Total Edits", "12")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.metric("Images Processed", "5")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col3:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.metric("Plan", "Pro")
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.write("---")
        st.subheader("🚀 Quick Start")
        st.info("Ready to transform your logos? Head over to the **Artistic Studio**.")

    elif app_mode == "Artistic Studio":
        image_processing_page()
        
    elif app_mode == "Transaction History":
        section_header("Transaction History", "View your previous payments")
        st.info("No recent transactions found.")
        
    elif app_mode == "User Profile":
        from frontend.profile import profile_page
        profile_page()

if __name__ == "__main__":
    dashboard_page()
