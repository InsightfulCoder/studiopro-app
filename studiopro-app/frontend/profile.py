import streamlit as st
import sys
import os

# Add the parent directory to sys.path to allow imports from other folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.db_manager import get_connection

def profile_page():
    user = st.session_state.user
    st.header(f"👤 User Profile: {user['username']}")
    
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "🖼️ Processing History", "💳 Payment History"])
    
    conn = get_connection()
    cursor = conn.cursor()
    
    with tab1:
        st.subheader("Account Details")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Account Created:** {user['created_at']}")
        
        # Stats
        cursor.execute("SELECT COUNT(*) FROM image_history WHERE user_id = ?", (user['user_id'],))
        total_images = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND payment_status = 'SUCCESS'", (user['user_id'],))
        total_spent = cursor.fetchone()[0] or 0
        
        col1, col2 = st.columns(2)
        col1.metric("Total Images Processed", total_images)
        col2.metric("Total Amount Spent", f"₹{total_spent}")

    with tab2:
        st.subheader("Your Styled Logos")
        cursor.execute("SELECT * FROM image_history WHERE user_id = ? ORDER BY processing_date DESC", (user['user_id'],))
        history = cursor.fetchall()
        
        if not history:
            st.info("You haven't processed any images yet.")
        else:
            for item in history:
                with st.container(border=True):
                    col_img, col_txt = st.columns([1, 2])
                    with col_img:
                        if os.path.exists(item['processed_image_path']):
                            st.image(item['processed_image_path'], use_container_width=True)
                        else:
                            st.write("Image file missing.")
                    with col_txt:
                        st.write(f"**Style:** {item['style_applied']}")
                        st.write(f"**Date:** {item['processing_date']}")
                        if st.button(f"View/Download Again", key=f"dl_{item['image_id']}"):
                            st.session_state.output_paths = {
                                "processed": item['processed_image_path'],
                                "style": item['style_applied']
                            }
                            st.session_state.page = "download"
                            st.rerun()

    with tab3:
        st.subheader("Transaction Records")
        cursor.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY transaction_date DESC", (user['user_id'],))
        txs = cursor.fetchall()
        
        if not txs:
            st.info("No transactions found.")
        else:
            import pandas as pd
            df = pd.DataFrame(txs, columns=["ID", "User ID", "Amount", "Status", "Date", "Method"])
            st.dataframe(df[["ID", "Amount", "Status", "Date", "Method"]], use_container_width=True)

    conn.close()

if __name__ == "__main__":
    profile_page()
