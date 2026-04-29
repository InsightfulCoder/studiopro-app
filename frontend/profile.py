import streamlit as st
import os
from utils.ui_utils import section_header, safe_image_display, safe_rerun
from database.db_manager import get_connection

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
                        safe_image_display(item['processed_image_path'])
                    with c2:
                        st.subheader(f"{item['style_applied']} Style")
                        st.write(f"Created on: {item['processing_date']}")
                        
                        # Action Buttons Row
                        btn_col1, btn_col2, btn_col3 = st.columns(3)
                        
                        with btn_col1:
                            if st.button("View Details", key=f"view_{item['image_id']}", use_container_width=True):
                                st.session_state.output_paths = {
                                    "processed": item['processed_image_path'],
                                    "style": item['style_applied']
                                }
                                st.session_state.page = "download"
                                safe_rerun()
                                
                        with btn_col2:
                            try:
                                with open(item['processed_image_path'], "rb") as file:
                                    st.download_button(
                                        label="Download",
                                        data=file,
                                        file_name=os.path.basename(item['processed_image_path']),
                                        mime="image/png",
                                        key=f"dl_{item['image_id']}",
                                        use_container_width=True
                                    )
                            except Exception:
                                st.button("Unavailable", disabled=True, key=f"dl_err_{item['image_id']}", use_container_width=True)
                                
                        with btn_col3:
                            if st.button("Delete", type="primary", key=f"del_{item['image_id']}", use_container_width=True):
                                # Delete from DB
                                del_conn = get_connection()
                                del_cursor = del_conn.cursor()
                                del_cursor.execute("DELETE FROM image_history WHERE image_id = ?", (item['image_id'],))
                                del_conn.commit()
                                del_conn.close()
                                
                                # Delete from disk
                                try:
                                    if os.path.exists(item['processed_image_path']):
                                        os.remove(item['processed_image_path'])
                                except Exception:
                                    pass
                                    
                                safe_rerun()

    conn.close()
