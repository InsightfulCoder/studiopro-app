import streamlit as st
from backend.user_manager import update_profile, update_password, get_user_by_id
from utils.ui_utils import safe_rerun

def render_settings_page():
    user = st.session_state.user
    
    st.markdown(f"""
<div style="animation: reveal 0.8s ease-out forwards;">
    <h1 style="font-size: 3.2rem; margin-bottom: 0.5rem; font-weight: 800; background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Workspace Settings</h1>
    <p style="color: var(--text-muted); font-size: 1.1rem; margin-bottom: 3rem;">Manage your account information and security preferences.</p>
</div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["👤 Profile Information", "🔒 Security & Password"])

    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Premium Wallet Display
        from backend.user_manager import get_credits
        credits = get_credits(user['user_id'])
        
        st.markdown(f"""
        <div class="premium-card" style="padding: 2rem; border-radius: 20px; text-align: center; margin-bottom: 2rem; background: rgba(255, 126, 95, 0.05);">
            <div style="font-size: 0.85rem; color: var(--accent-primary); letter-spacing: 0.1em; font-weight: 800; text-transform: uppercase; margin-bottom: 0.5rem;">Available HD Credits</div>
            <div style="font-size: 3.5rem; font-weight: 800; color: var(--text-main); font-family: 'Outfit', sans-serif; line-height: 1;">
                {credits} <span style="font-size: 1.5rem; color: var(--text-dim);">images</span>
            </div>
            <p style="color: var(--text-muted); font-size: 0.9rem; margin-top: 0.5rem;">Purchase more credits from the Artistic Studio.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
<div class="glass-card" style="padding: 2.5rem; border-radius: 24px;">
    <h3 style="margin-bottom: 1.5rem;">Edit Profile</h3>
</div>
        """, unsafe_allow_html=True)
        
        with st.form("profile_update_form"):
            new_username = st.text_input("Username", value=user['username'])
            new_email = st.text_input("Email Address", value=user['email'])
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button("UPDATE PROFILE", use_container_width=True):
                if not new_username or not new_email:
                    st.error("Fields cannot be empty.")
                else:
                    success, message = update_profile(user['user_id'], new_username, new_email)
                    if success:
                        # Refresh session user data
                        fresh_user = get_user_by_id(user['user_id'])
                        st.session_state.user = fresh_user
                        st.success(message)
                        st.info("Username/Email updated. Changes are now live.")
                        st.rerun()
                    else:
                        st.error(message)

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
<div class="glass-card" style="padding: 2.5rem; border-radius: 24px;">
    <h3 style="margin-bottom: 1.5rem;">Security Credentials</h3>
</div>
        """, unsafe_allow_html=True)
        
        with st.form("password_update_form"):
            current_pwd = st.text_input("Current Password", type="password", placeholder="••••••••")
            new_pwd = st.text_input("New Password", type="password", placeholder="••••••••")
            confirm_pwd = st.text_input("Confirm New Password", type="password", placeholder="••••••••")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button("CHANGE PASSWORD", use_container_width=True):
                if new_pwd != confirm_pwd:
                    st.error("New passwords do not match.")
                elif not current_pwd or not new_pwd:
                    st.error("Please fill in all fields.")
                else:
                    success, message = update_password(user['user_id'], current_pwd, new_pwd)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
<div class="premium-card" style="background: rgba(255,255,255,0.02); border-color: var(--border-soft); padding: 2rem;">
    <h4 style="margin-bottom: 1rem;">Danger Zone</h4>
    <p style="color: var(--text-dim); font-size: 0.9rem; margin-bottom: 2rem;">Once you delete your account, there is no going back. Please be certain.</p>
</div>
    """, unsafe_allow_html=True)
    if st.button("DELETE WORKSPACE", key="delete_acc", use_container_width=True):
        st.warning("Account deletion is not yet available in the V3 pilot.")
