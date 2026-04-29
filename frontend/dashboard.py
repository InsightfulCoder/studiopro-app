import streamlit as st
from utils.ui_utils import section_header, safe_image_display, safe_rerun, inject_custom_css
from database.db_manager import get_connection
import base64
import os

# Internal Page Imports
from frontend.image_processing import image_processing_page
from frontend.profile import profile_page
from frontend.settings import render_settings_page

def get_img_base64_fallback(file_path):
    if not os.path.exists(file_path):
        return ""
    try:
        with open(file_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

def get_recent_activity(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 'generation' as type, style_applied as detail, processing_date as date 
            FROM image_history WHERE user_id = ?
            UNION ALL
            SELECT 'payment' as type, amount as detail, transaction_date as date 
            FROM transactions WHERE user_id = ?
            ORDER BY date DESC LIMIT 5
        """, (user_id, user_id))
        rows = cursor.fetchall()
        conn.close()
        return rows
    except:
        return []

def dashboard_page():
    user = st.session_state.user
    inject_custom_css()
    
    # 1. Professional Sidebar Navigation
    with st.sidebar:
        initials = user['username'][0].upper() if user['username'] else "U"
        st.markdown(f"""
<div class="profile-badge" style="margin-bottom: 2rem;">
    <div class="profile-avatar">{initials}</div>
    <div>
        <div style="font-weight: 700; color: var(--text-main); font-size: 1.1rem;">{user['username']}</div>
        <div style="font-size: 0.75rem; color: var(--accent-primary); font-weight: 800; text-transform: uppercase;">Pro Member</div>
    </div>
</div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='font-size: 0.7rem; font-weight: 800; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 1.5rem;'>Workspace</p>", unsafe_allow_html=True)
        
        # Enhanced Navigation Buttons
        menu_items = {
            "🏠 Dashboard": "dashboard_home",
            "📤 Upload Image": "studio",
            "🎨 AI Styles": "styles",
            "🖼️ Gallery": "gallery",
            "💾 My Creations": "history",
            "👤 Account": "profile",
            "⚙️ Settings": "settings"
        }
        
        # Initialize internal navigation state
        if "sidebar_nav" not in st.session_state:
            st.session_state.sidebar_nav = "🏠 Dashboard"
            
        for label, key in menu_items.items():
            btn_color = "var(--accent-primary)" if st.session_state.sidebar_nav == label else "transparent"
            if st.button(label, key=f"side_{key}", use_container_width=True):
                st.session_state.sidebar_nav = label
                safe_rerun()
                
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
        if st.button("🚪 Sign Out", key="logout_btn", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = "home"
            safe_rerun()

    # 2. Page Routing based on Sidebar
    current_mode = st.session_state.sidebar_nav
    
    if current_mode == "🏠 Dashboard":
        render_dashboard_overview(user)
    elif current_mode == "📤 Upload Image":
        image_processing_page()
    elif current_mode == "💾 My Creations" or current_mode == "👤 Account":
        profile_page()
    elif current_mode == "🎨 AI Styles" or current_mode == "🖼️ Gallery":
        render_gallery_view()
    elif current_mode == "⚙️ Settings":
        render_settings_page()
    else:
        st.markdown(f"### {current_mode}")
        st.info("This module is currently being optimized for the V3 engine.")

def render_dashboard_overview(user):
    st.markdown(f"""
<div style="animation: reveal 0.8s ease-out forwards;">
    <h1 style="font-size: 3.2rem; margin-bottom: 0.5rem; font-weight: 800; background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Welcome back, {user['username']}</h1>
    <p style="color: var(--text-muted); font-size: 1.1rem; margin-bottom: 3rem;">Your neural creativity suite is ready.</p>
</div>
    """, unsafe_allow_html=True)
    
    # Unified Stats Row
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM image_history WHERE user_id = ?", (user['user_id'],))
        total_imgs = c.fetchone()[0]
        conn.close()
    except:
        total_imgs = 0
    
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(f"""
<div class="stat-card">
    <div class="stat-icon">🎨</div>
    <div class="stat-value">{total_imgs}</div>
    <div class="stat-label">Total Creations</div>
</div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown(f"""
<div class="stat-card">
    <div class="stat-icon">⚡</div>
    <div class="stat-value">Instant</div>
    <div class="stat-label">Neural Speed</div>
</div>
        """, unsafe_allow_html=True)
    with s3:
        st.markdown(f"""
<div class="stat-card">
    <div class="stat-icon">💎</div>
    <div class="stat-value">Premium</div>
    <div class="stat-label">License Type</div>
</div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Main Content Area
    col_left, col_right = st.columns([1.6, 1], gap="large")
    
    with col_left:
        st.markdown("### 🕒 Recent Neural Activity")
        activity = get_recent_activity(user['user_id'])
        
        if activity:
            for act in activity:
                icon = "🎨" if act['type'] == 'generation' else "💳"
                color = "var(--accent-primary)" if act['type'] == 'generation' else "var(--accent-tertiary)"
                st.markdown(f"""
<div class="glass-card" style="display: flex; align-items: center; gap: 1rem; border-left: 4px solid {color};">
    <div style="font-size: 1.5rem;">{icon}</div>
    <div>
        <div style="font-weight: 700; color: white;">{act['detail']}</div>
        <div style="font-size: 0.75rem; color: var(--text-dim);">{act['date']}</div>
    </div>
</div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent activity. Start your first generation!")

    with col_right:
        st.markdown(f"""
<div class="premium-card" style="background: radial-gradient(circle at top right, var(--accent-primary), #FF7E5F); border: none; padding: 2.5rem; overflow: hidden; position: relative;">
    <div style="position: absolute; top: -20px; right: -20px; font-size: 8rem; opacity: 0.1; transform: rotate(-15deg);">✨</div>
    <h2 style="color: white; margin-bottom: 1rem; font-weight: 800;">Creative<br>Engine</h2>
    <p style="color: white; opacity: 0.9; font-size: 1rem; line-height: 1.5; margin-bottom: 2.5rem;">Initialize our neural pipeline to process your next set of images.</p>
</div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 LAUNCH STUDIO", use_container_width=True, key="launch_v4"):
            st.session_state.sidebar_nav = "📤 Upload Image"
            safe_rerun()

def render_gallery_view():
    section_header("AI Style Gallery", "Explore the diverse artistic models available in StudioPro.")
    
    styles = [
        ("https://images.unsplash.com/photo-1620641788421-7a1c342ea42e", "3D Pixar"),
        ("https://images.unsplash.com/photo-1607604276583-eef5d076aa5f", "Neo Anime"),
        ("https://images.unsplash.com/photo-1579783901586-d88db74b4fe4", "Oil Painting"),
        ("https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5", "Watercolor"),
        ("https://images.unsplash.com/photo-1513364776144-60967b0f800f", "Sketch Art"),
        ("https://images.unsplash.com/photo-1563089145-599997674d42", "Cyberpunk")
    ]
    
    cols = st.columns(3)
    for i, (url, name) in enumerate(styles):
        with cols[i % 3]:
            st.markdown(f"""
<div class="gallery-card" style="margin-bottom: 2rem;">
    <img src="{url}?auto=format&fit=crop&q=80&w=400" class="gallery-img" style="height: 200px;">
    <div class="gallery-info">
        <div style="font-weight: 700; font-size: 1rem;">{name} Style</div>
        <div style="font-size: 0.75rem; color: var(--text-dim); margin-top: 4px;">Optimized for Portraits</div>
    </div>
</div>
            """, unsafe_allow_html=True)
            if st.button(f"Use {name}", key=f"use_{i}", use_container_width=True):
                st.session_state.sidebar_nav = "📤 Upload Image"
                safe_rerun()
