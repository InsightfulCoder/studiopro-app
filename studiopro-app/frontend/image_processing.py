import streamlit as st
from PIL import Image
import os
import uuid

def image_processing_page():
    st.header("🖼️ Image Processing")
    st.write("Upload an image to start cartoonizing!")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "bmp"])

    if uploaded_file is not None:
        # Validate file size (max 10MB)
        if uploaded_file.size > 10 * 1024 * 1024:
            st.error("File size exceeds 10MB limit.")
            return

        # Load and display image
        image = Image.open(uploaded_file)
        st.session_state.original_image = image
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original Image")
            st.image(image, use_container_width=True)
            
        with col2:
            st.subheader("Image Details")
            st.write(f"- **Dimensions:** {image.width} x {image.height}")
            st.write(f"- **Format:** {image.format}")
            st.write(f"- **Size:** {uploaded_file.size / 1024:.2f} KB")

        # Save temporarily
        temp_dir = "assets/temp"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, f"{uuid.uuid4()}.{image.format.lower()}")
        image.save(temp_path)
        st.session_state.temp_image_path = temp_path
        
        st.success("Image uploaded successfully!")
        
        st.write("---")
        st.subheader("Next Steps")
        st.write("Proceed to Milestone 2, Task 8-11: Apply Effects (Coming Soon)")

if __name__ == "__main__":
    image_processing_page()
