import streamlit as st
import os
from utils.ui_utils import section_header, safe_image_display, safe_rerun

def download_page():
    section_header("Export Studio", "Your masterpiece is ready for high-resolution download.")
    
    if 'output_paths' not in st.session_state:
        st.error("No active session found. Redirecting to dashboard...")
        st.session_state.page = "dashboard"; safe_rerun(); return

    processed_path = st.session_state.output_paths['processed']
    
    col1, col2 = st.columns([1.2, 1], gap="large")
    with col1:
        st.markdown('<div class="premium-card" style="padding: 1rem; border-color: var(--accent-primary);">', unsafe_allow_html=True)
        safe_image_display(processed_path, caption=f"Final Render - {st.session_state.output_paths.get('style', 'AI Art')}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="premium-card" style="height: 100%; display: flex; flex-direction: column; justify-content: center;">', unsafe_allow_html=True)
        st.subheader("📥 Export Assets")
        st.markdown("<p style='color: var(--text-muted);'>Download your high-resolution PNG file ready for professional use.</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        with open(processed_path, "rb") as file:
            st.download_button(
                    label="Download HD PNG",
                    data=file,
                    file_name=f"studiopro_ai_{os.path.basename(processed_path)}",
                    mime="image/png",
                    use_container_width=True
                )
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.success("✨ Artwork optimized & verified.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🚪 Finish & Exit Studio", use_container_width=True):
        # Cleanup session but keep user
        keys_to_del = ['original_image', 'processed_image', 'output_paths', 'razorpay_order', 'current_style']
        for k in keys_to_del:
            if k in st.session_state: del st.session_state[k]
        st.session_state.page = "dashboard"; safe_rerun()
