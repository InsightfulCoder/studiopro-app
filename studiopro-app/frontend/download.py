import streamlit as st
import os
from utils.ui_utils import section_header

def download_page():
    section_header("Download Ready", "Your masterpiece is ready for the world")
    
    if 'output_paths' not in st.session_state:
        st.error("No image found.")
        st.session_state.page = "dashboard"
        st.rerun()
        return

    processed_path = st.session_state.output_paths['processed']
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.image(processed_path, use_container_width=True, caption="Final Render")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card" style="height: 100%;">', unsafe_allow_html=True)
        st.subheader("📥 Your Assets")
        st.write("---")
        
        with open(processed_path, "rb") as file:
            st.download_button(
                    label="Download High-Res PNG",
                    data=file,
                    file_name="cartoonized_logo.png",
                    mime="image/png"
                )
        
        st.write("---")
        st.success("Transaction verified. Thank you for using StudioPro AI!")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Finish & Return Home"):
        # Cleanup
        keys_to_del = ['original_image', 'processed_image', 'output_paths', 'razorpay_order', 'current_style']
        for k in keys_to_del:
            if k in st.session_state:
                del st.session_state[k]
        st.session_state.page = "dashboard"
        st.rerun()
