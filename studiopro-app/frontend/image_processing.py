import streamlit as st
from PIL import Image
import os
import uuid
from utils.image_utils import cartoonify_classic, pencil_sketch, pencil_color

def image_processing_page():
    st.header("🖼️ Image Processing")
    st.write("Upload an image and select a style to transform it!")

    # 1. File Upload
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "bmp"])

    if uploaded_file is not None:
        if uploaded_file.size > 10 * 1024 * 1024:
            st.error("File size exceeds 10MB limit.")
            return

        image = Image.open(uploaded_file)
        st.session_state.original_image = image
        
        # 2. Style Selection
        st.write("---")
        st.subheader("Select Style")
        
        style = st.radio("Choose an artistic effect:", 
                         ["Original", "Classic Cartoon", "Sketch", "Pencil Color"], 
                         horizontal=True)
        
        # Parameters for styles (optional but recommended in task)
        with st.expander("Adjust Parameters"):
            if style == "Classic Cartoon":
                k = st.slider("Color Levels (K)", 2, 32, 8)
                d = st.slider("Smoothing Intensity (d)", 3, 15, 9)
            elif style in ["Sketch", "Pencil Color"]:
                k_size = st.slider("Sketch Thickness", 3, 51, 21, step=2)
            else:
                st.write("No parameters for current style.")

        # 3. Process Image
        processed_image = image
        if st.button("✨ Apply Effect"):
            with st.spinner(f"Applying {style}..."):
                if style == "Classic Cartoon":
                    processed_image = cartoonify_classic(image, k=k, d=d)
                elif style == "Sketch":
                    processed_image = pencil_sketch(image, k_size=k_size)
                elif style == "Pencil Color":
                    processed_image = pencil_color(image, k_size=k_size)
                
                st.session_state.processed_image = processed_image
                st.success("Processing complete!")

        # 4. Comparison View
        if 'processed_image' in st.session_state:
            st.write("---")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Original")
                st.image(image, use_container_width=True)
            with col2:
                st.subheader(f"Processed ({style})")
                st.image(st.session_state.processed_image, use_container_width=True)
            
            # Download options
            st.write("---")
            if st.button("🚀 Prepare for Download"):
                with st.spinner("Preparing your high-quality download..."):
                    # 5. Save images and log to DB
                    output_dir = "assets/outputs"
                    os.makedirs(output_dir, exist_ok=True)
                    
                    # Generate unique filenames
                    file_id = uuid.uuid4().hex[:8]
                    orig_name = f"orig_{file_id}.png"
                    proc_name = f"proc_{file_id}.png"
                    
                    orig_path = os.path.join(output_dir, orig_name)
                    proc_path = os.path.join(output_dir, proc_name)
                    
                    st.session_state.original_image.save(orig_path)
                    st.session_state.processed_image.save(proc_path)
                    
                    # Log to database
                    from backend.transactions import log_image_history
                    log_image_history(
                        st.session_state.user['user_id'],
                        orig_path,
                        proc_path,
                        style
                    )
                    
                    st.session_state.output_paths = {
                        "original": orig_path,
                        "processed": proc_path,
                        "style": style
                    }
                    
                    st.session_state.page = "payment"
                    st.success("Image history logged! Redirecting to payment...")
                    st.rerun()



if __name__ == "__main__":
    image_processing_page()
