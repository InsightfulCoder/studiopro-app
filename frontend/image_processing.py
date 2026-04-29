import streamlit as st
from PIL import Image
import os
import uuid
from utils.image_utils import (cartoonify_classic, pencil_sketch, pencil_color, 
                               style_anime, style_pixar, style_comic, style_watercolor)
from utils.ui_utils import section_header, safe_rerun
import io, base64

@st.cache_data
def get_image_preview_64(_img, max_size=(800, 800)):
    """Generates an optimized base64 thumbnail for previewing."""
    preview = _img.copy()
    if preview.mode in ("RGBA", "P"):
        preview = preview.convert("RGB")
    preview.thumbnail(max_size)
    buffered = io.BytesIO()
    preview.save(buffered, format="JPEG", quality=80)
    return base64.b64encode(buffered.getvalue()).decode()

def image_processing_page():
        # The application expects a user session to process HD images.
        # User auth is enforced at the download step.

    # Header
    st.markdown(f"""
<div style="animation: reveal 0.8s ease-out forwards;">
    <h1 style="font-size: 3.5rem; letter-spacing: -0.05em; font-weight: 800; background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Artistic Studio</h1>
    <p style="color: var(--text-muted); font-size: 1.1rem; margin-bottom: 4rem;">The professional creative workspace for AI-powered imagery.</p>
</div>
    """, unsafe_allow_html=True)

    # 1. Main Studio Interface
    col_ctl, col_pre = st.columns([1, 1.4], gap="large")
    
    with col_ctl:
        st.markdown('<div class="premium-card" style="border-radius: 32px; padding: 2.5rem;">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-bottom: 0.5rem;">Input Layer</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: var(--text-dim); font-size: 0.85rem; margin-bottom: 2rem;">Upload your source asset to begin styling.</p>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        
        if uploaded_file is not None:
            if uploaded_file.size > 10 * 1024 * 1024:
                st.error("File size exceeds the 10MB limit.")
                return
            
            # Check if this is a new image to reset state
            if 'last_uploaded_file' not in st.session_state or st.session_state.last_uploaded_file != uploaded_file.name:
                if 'processed_image' in st.session_state:
                    del st.session_state['processed_image']
                st.session_state.last_uploaded_file = uploaded_file.name
                
            image = Image.open(uploaded_file)
            st.session_state.original_image = image
            
            st.markdown("<br><hr style='border: 0; border-top: 1px solid var(--border-soft); margin: 2rem 0;'><br>", unsafe_allow_html=True)
            st.markdown('<h3 style="margin-bottom: 0.5rem;">Neural Style</h3>', unsafe_allow_html=True)
            st.markdown('<p style="color: var(--text-dim); font-size: 0.85rem; margin-bottom: 2rem;">Choose your transformation parameters.</p>', unsafe_allow_html=True)

            style_options = ["Original", "Pixar 3D", "Anime Mode", "Comic Pop", "Watercolor", "Classic Cartoon", "Pencil Sketch", "Pencil Color"]
            style = st.selectbox("Choose Visual Effect", style_options, label_visibility="collapsed")
            
            # Param block
            if style == "Classic Cartoon":
                k = st.slider("Color Depth (K)", 2, 32, 8)
                d = st.slider("Smoothing (d)", 3, 15, 9)
            elif style in ["Pencil Sketch", "Pencil Color"]:
                k_size = st.slider("Detail Level", 3, 51, 21, step=2)
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            if st.button("✨ START TRANSFORMATION", use_container_width=True, key="studio_process_v4"):
                with st.spinner(f"Neural processing in progress..."):
                    if style == "Classic Cartoon":
                        processed_image = cartoonify_classic(image, k=k, d=d)
                    elif style == "Pencil Sketch":
                        processed_image = pencil_sketch(image, k_size=k_size)
                    elif style == "Pencil Color":
                        processed_image = pencil_color(image, k_size=k_size)
                    elif style == "Pixar 3D":
                        processed_image = style_pixar(image)
                    elif style == "Anime Mode":
                        processed_image = style_anime(image)
                    elif style == "Comic Pop":
                        processed_image = style_comic(image)
                    elif style == "Watercolor":
                        processed_image = style_watercolor(image)
                    else:
                        processed_image = image
                    
                    st.session_state.processed_image = processed_image
                    st.session_state.current_style = style
        st.markdown('</div>', unsafe_allow_html=True)

    with col_pre:
        if uploaded_file is None:
            st.markdown(f"""
                <div style="height: 600px; background: rgba(255,255,255,0.01); border: 2px dashed var(--border-soft); border-radius: 40px; display: flex; flex-direction: column; align-items: center; justify-content: center; color: var(--text-dim);">
                    <div style="font-size: 4rem; margin-bottom: 1.5rem; opacity: 0.5;">🖼️</div>
                    <div style="font-weight: 600; font-size: 1.2rem;">Studio Preview Empty</div>
                    <div style="font-size: 0.9rem;">Your masterpiece will appear here after upload.</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            if 'processed_image' in st.session_state:
                # Optimized Result Display
                st.markdown(f"""
                    <div style="background: rgba(10,10,11,0.5); border: 1px solid var(--border-soft); border-radius: 40px; padding: 1.5rem; position: relative; animation: reveal 1s ease-out forwards;">
                        <div style="position: absolute; top: 1.5rem; right: 1.5rem; background: var(--accent-gradient); padding: 8px 20px; border-radius: 12px; font-weight: 800; font-size: 0.8rem; z-index: 10; box-shadow: var(--shadow-glow);">STUDIO RENDER</div>
                """, unsafe_allow_html=True)
                
                import time
                unique_key = f"editor_slider_v4_{int(time.time()*100)}"
                comp_val = st.slider("Comparison Slider", 0, 100, 50, label_visibility="collapsed", key=unique_key)
                orig_64 = get_image_preview_64(image)
                proc_64 = get_image_preview_64(st.session_state.processed_image)

                st.markdown(f"""
                        <div class="comp-container" style="height: 550px; border-radius: 28px; margin-top: 1rem;">
                            <img class="after-image" src="data:image/jpeg;base64,{proc_64}" style="width: 100%; height: 100%; object-fit: cover;">
                            <div class="before-image" style="width: {comp_val}%; height: 100%; position: absolute; top: 0; left: 0; overflow: hidden; border-right: 3px solid #FFF;">
                                <img src="data:image/jpeg;base64,{orig_64}" style="width: {10000 / (comp_val if comp_val > 0 else 1)}%; height: 100%; object-fit: cover;">
                            </div>
                            <div class="comp-badge badge-left" style="top: 20px; left: 20px;">Original</div>
                            <div class="comp-badge badge-right" style="top: 20px; right: 20px;">AI Rendered</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Pro Actions
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🚀 PREPARE HD DOWNLOAD", use_container_width=True, key=f"hd_download_v4_{int(time.time())}"):
                    process_and_redirect(style if 'current_style' not in st.session_state else st.session_state.current_style)
            else:
                import time
                # Initial Upload Preview
                st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-soft); border-radius: 40px; padding: 2rem; display: flex; flex-direction: column; align-items: center;">
                        <img src="data:image/jpeg;base64,{get_image_preview_64(image)}?t={int(time.time()*100)}" style="width: 100%; border-radius: 24px; box-shadow: var(--shadow-premium);">
                        <p style="margin-top: 2rem; font-weight: 600; color: var(--text-muted);">Asset Loaded Successfully</p>
                    </div>
                """, unsafe_allow_html=True)

def process_and_redirect(style):
    with st.spinner("Saving neural state..."):
        import time
        output_dir = "assets/outputs"
        os.makedirs(output_dir, exist_ok=True)
        file_id = f"{uuid.uuid4().hex[:8]}_{int(time.time())}"
        orig_path = os.path.join(output_dir, f"orig_{file_id}.png")
        proc_path = os.path.join(output_dir, f"proc_{file_id}.png")
        
        st.session_state.original_image.save(orig_path)
        st.session_state.processed_image.save(proc_path)
        
        st.session_state.output_paths = {
            "original": orig_path,
            "processed": proc_path,
            "style": style
        }

        if st.session_state.user:
            from backend.transactions import log_image_history
            from backend.user_manager import get_credits, deduct_credit
            
            user_id = st.session_state.user['user_id']
            log_image_history(user_id, orig_path, proc_path, style)
            
            # 1. Enforce Premium Credits for HD Downloads
            credits = get_credits(user_id)
            if credits > 0:
                if deduct_credit(user_id):
                    st.session_state.page = "download"
                    st.success(f"1 HD Credit used. You have {credits - 1} credits remaining.")
                else:
                    st.error("Error processing credit deduction.")
            else:
                st.warning("You need HD Credits to download this masterpiece! Please become a Pro Member.")
                st.session_state.page = "payment"
        else:
            st.warning("Please sign in or create an account to save and download your creations.")
            st.session_state.page = "login"
            
        safe_rerun()
