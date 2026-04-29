import streamlit as st
from utils.ui_utils import safe_rerun
import pandas as pd
from utils.ui_utils import section_header

def admin_dashboard_page():
    from backend.transactions import get_admin_stats, get_all_users, get_all_transactions, get_all_activity
    
    # Check admin authorization
    if st.session_state.user['email'] != "admin@studiopro.ai":
        st.error("Unauthorized Access.")
        if st.button("Return Home"):
            st.session_state.page = "home"
            safe_rerun()
        return

    # Sidebar Navigation
    with st.sidebar:
        st.markdown("""
            <div class="profile-badge" style="margin-bottom: 2rem;">
                <div class="profile-avatar" style="background: #FF4B2B;">A</div>
                <div>
                    <div style="font-weight: 700; color: var(--text-main);">System Admin</div>
                    <div style="font-size: 0.75rem; color: var(--text-dim);">admin@studiopro.ai</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='font-size: 0.7rem; font-weight: 800; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.1em; margin-left: 10px; margin-bottom: 10px;'>Admin Panel</p>", unsafe_allow_html=True)
        
        admin_mode = st.radio("ADMIN MENU", [
            "📊 Dashboard Overview", 
            "👥 User Management", 
            "💳 Payment Monitoring", 
            "🖼️ Image Activity"
        ], label_visibility="collapsed")
        
        st.markdown("<div style='flex-grow: 1; height: 100px;'></div>", unsafe_allow_html=True)
        if st.button("🚪 Logout Admin", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = "home"
            safe_rerun()

    if admin_mode == "📊 Dashboard Overview":
        st.markdown("<h1>Admin <span style='color: var(--accent-primary);'>Overview</span></h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: var(--text-muted); margin-bottom: 3rem;'>Monitoring system-wide metrics and performance.</p>", unsafe_allow_html=True)
        
        stats = get_admin_stats()
        
        s1, s2, s3, s4 = st.columns(4)
        with s1:
            st.markdown(f"""<div class="stat-card">
                <div class="stat-icon">👥</div>
                <div class="stat-value">{stats['total_users']}</div>
                <div class="stat-label">Total Users</div>
            </div>""", unsafe_allow_html=True)
        with s2:
            st.markdown(f"""<div class="stat-card">
                <div class="stat-icon">✨</div>
                <div class="stat-value">{stats['total_generations']}</div>
                <div class="stat-label">Total Images</div>
            </div>""", unsafe_allow_html=True)
        with s3:
            st.markdown(f"""<div class="stat-card">
                <div class="stat-icon">💰</div>
                <div class="stat-value">₹{stats['total_revenue']:.2f}</div>
                <div class="stat-label">Total Revenue</div>
            </div>""", unsafe_allow_html=True)
        with s4:
            st.markdown(f"""<div class="stat-card">
                <div class="stat-icon">📈</div>
                <div class="stat-value">{stats['active_today']}</div>
                <div class="stat-label">Active Today</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Recent Activity Preview
        st.markdown("### 🔔 System Pulse")
        activity, _ = get_all_activity()
        if activity:
            df_act = pd.DataFrame(activity[:5])
            st.dataframe(df_act, use_container_width=True)
        else:
            st.info("No activity recorded yet.")

    elif admin_mode == "👥 User Management":
        st.markdown("<h1>User <span style='color: var(--accent-primary);'>Management</span></h1>", unsafe_allow_html=True)
        users = get_all_users()
        
        if users:
            df_users = pd.DataFrame(users)
            search = st.text_input("🔍 Search Users", placeholder="Search by username or email...")
            if search:
                df_users = df_users[df_users['username'].str.contains(search, case=False) | df_users['email'].str.contains(search, case=False)]
            
            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            st.dataframe(df_users, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No users registered yet.")

    elif admin_mode == "💳 Payment Monitoring":
        st.markdown("<h1>Payment <span style='color: var(--accent-primary);'>Monitoring</span></h1>", unsafe_allow_html=True)
        transactions, revenue, success_count = get_all_transactions()
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Total Revenue", f"₹{revenue:.2f}")
        with m2:
            st.metric("Successful Payments", success_count)
        with m3:
            st.metric("Total Transactions", len(transactions))
            
        if transactions:
            df_trans = pd.DataFrame(transactions)
            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            st.dataframe(df_trans, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No transactions recorded yet.")

    elif admin_mode == "🖼️ Image Activity":
        st.markdown("<h1>Image Processing <span style='color: var(--accent-primary);'>Activity</span></h1>", unsafe_allow_html=True)
        activity, popular_style = get_all_activity()
        
        st.success(f"🏆 Most Popular Style: **{popular_style}**")
        
        if activity:
            df_activity = pd.DataFrame(activity)
            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            st.dataframe(df_activity, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No image processing activity yet.")

if __name__ == "__main__":
    admin_dashboard_page()
