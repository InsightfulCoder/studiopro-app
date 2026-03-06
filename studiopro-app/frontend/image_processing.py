import streamlit as st
from PIL import Image
import os
import uuid
from utils.image_utils import cartoonify_classic, pencil_sketch, pencil_color
from utils.ui_utils import section_header

def image_processing_page():
    # Progress check for guests
    is_guest = st.session_state.user is None
    trial_limit = 3
    
    if is_guest and st.session_state.guest_trials >= trial_limit:
        st.warning("🚀 Guest trial limit reached (3/3). Please log in to continue processing and unlocking premium features!")
        col1, col2 = st.columns(2)
        if col1.button("Sign In"):
            st.session_state.page = "login"
            st.rerun()
        if col2.button("Register"):
            st.session_state.page = "registration"
            st.rerun()
        return

    section_header("Artistic Studio", "Transform your image into a masterpiece")
    if is_guest:
        st.info(f"✨ Guest Mode: {st.session_state.guest_trials}/{trial_limit} free trials remaining. [Login](javascript:void(0)) to save history forever!")

    # 1. File Upload with better visual
    uploaded_file = st.file_uploader("Upload Image (JPG, PNG)", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        if uploaded_file.size > 10 * 1024 * 1024:
            st.error("File size exceeds the 10MB limit.")
            return

        image = Image.open(uploaded_file)
        st.session_state.original_image = image
        
        # 2. Style & Params
        col_ctl, col_pre = st.columns([1, 1])
        
        with col_ctl:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Configure Style")
            style = st.selectbox("Choose Visual Effect", 
                              ["Original", "Classic Cartoon", "Pencil Sketch", "Pencil Color"])
            
            with st.expander("Fine-tune Parameters", expanded=True):
                if style == "Classic Cartoon":
                    k = st.slider("Color Depth (K)", 2, 32, 8)
                    d = st.slider("Smoothing (d)", 3, 15, 9)
                elif style in ["Pencil Sketch", "Pencil Color"]:
                    k_size = st.slider("Detail Level", 3, 51, 21, step=2)
                else:
                    st.write("No parameters available for this style.")
            
            if st.button("✨ Apply transformation"):
                with st.spinner(f"Rendering {style}..."):
                    if style == "Classic Cartoon":
                        processed_image = cartoonify_classic(image, k=k, d=d)
                    elif style == "Pencil Sketch":
                        processed_image = pencil_sketch(image, k_size=k_size)
                    elif style == "Pencil Color":
                        processed_image = pencil_color(image, k_size=k_size)
                    else:
                        processed_image = image
                    
                    st.session_state.processed_image = processed_image
                    st.session_state.current_style = style
            st.markdown('</div>', unsafe_allow_html=True)

        with col_pre:
            st.subheader("Preview")
            if 'processed_image' in st.session_state:
                st.image(st.session_state.processed_image, use_container_width=True, caption=st.session_state.get('current_style', 'Preview'))
            else:
                st.image(image, use_container_width=True, caption="Original Image")

        # 4. Result Actions
        if 'processed_image' in st.session_state:
            st.write("---")
            col1, col2 = st.columns([1, 1])
            with col1:
                st.info("Happy with the result? Proceed to download your high-resolution version!")
            with col2:
                if st.button("🚀 Prepare HD Download"):
                    process_and_redirect(style if 'current_style' not in st.session_state else st.session_state.current_style)

def process_and_redirect(style):
    with st.spinner("Saving your progress..."):
        # Save temporary files for the session
        output_dir = "assets/outputs"
        os.makedirs(output_dir, exist_ok=True)
        file_id = uuid.uuid4().hex[:8]
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
            from backend.transactions import log_image_history, get_trial_status
            log_image_history(st.session_state.user['user_id'], orig_path, proc_path, style)
            
            is_eligible, remaining = get_trial_status(st.session_state.user['user_id'])
            if is_eligible:
                st.session_state.page = "download"
                st.success(f"Free trial applied! {remaining} trials remaining.")
            else:
                st.session_state.page = "payment"
                st.success("Image history logged! Redirecting to payment...")
        else:
            # Guest bypass for first 3
            st.session_state.guest_trials += 1
            st.session_state.page = "download"
            st.success(f"Guest trial applied! {3 - st.session_state.guest_trials} remaining.")
            
        st.rerun()

if __name__ == "__main__":
    image_processing_page()
