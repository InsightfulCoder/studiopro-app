import streamlit as st
import sys
import os
from database.db_manager import get_connection
from utils.ui_utils import section_header

def profile_page():
    user = st.session_state.user
    section_header(f"Account: {user['username']}", "Manage your creative profile")
    
    tab1, tab2 = st.tabs(["📊 Analytics", "🖼️ Creative History"])
    
    conn = get_connection()
    cursor = conn.cursor()
    
    with tab1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Your Stats")
        # Real statistics from DB
        cursor.execute("SELECT COUNT(*) FROM image_history WHERE user_id = ?", (user['user_id'],))
        total_images = cursor.fetchone()[0]
        
        col1, col2 = st.columns(2)
        col1.metric("Lifetime Generations", total_images)
        col2.metric("Membership", "Premium User")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        cursor.execute("SELECT * FROM image_history WHERE user_id = ? ORDER BY processing_date DESC", (user['user_id'],))
        history = cursor.fetchall()
        
        if not history:
            st.info("No projects yet. Start creating in the Artistic Studio!")
        else:
            for item in history:
                with st.container(border=True):
                    c1, c2 = st.columns([1, 3])
                    with c1:
                        if os.path.exists(item['processed_image_path']):
                            st.image(item['processed_image_path'], use_container_width=True)
                    with c2:
                        st.subheader(f"{item['style_applied']} Style")
                        st.write(f"Created on: {item['processing_date']}")
                        if st.button("View Details", key=f"view_{item['image_id']}"):
                            st.session_state.output_paths = {
                                "processed": item['processed_image_path'],
                                "style": item['style_applied']
                            }
                            st.session_state.page = "download"
                            st.rerun()

    conn.close()
