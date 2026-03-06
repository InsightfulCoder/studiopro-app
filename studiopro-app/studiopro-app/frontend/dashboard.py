from frontend.image_processing import image_processing_page

def dashboard_page():
    user = st.session_state.user
    st.title(f"👋 Welcome, {user['username']}!")
    
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Go to", ["Dashboard", "Image Processing", "Payment History", "Profile Settings"])
    
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()

    if app_mode == "Dashboard":
        st.subheader("Your Progress")
        col1, col2, col3 = st.columns(3)
        col1.metric("Images Processed", "0")
        col2.metric("Tokens Spent", "0")
        col3.metric("Membership", "Free")
        
        st.write("---")
        st.write("### Quick Actions")
        if st.button("Start Cartoonizing"):
            # Update mode to switch page indirectly (Streamlit radios are reactive)
            st.info("Please select 'Image Processing' from the sidebar.")
            
    elif app_mode == "Image Processing":
        image_processing_page()
        
    elif app_mode == "Payment History":
        st.subheader("📜 Payment History")
        st.write("Milestone 3 feature coming soon!")
        
    elif app_mode == "Profile Settings":
        from frontend.profile import profile_page
        profile_page()

if __name__ == "__main__":
    dashboard_page()
