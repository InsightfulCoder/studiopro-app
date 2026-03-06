import streamlit as st
import os

def download_page():
    st.title("✅ Your HD Cartoonized Logo")
    st.success("Payment confirmed! Your image is ready for download.")
    
    if 'output_paths' not in st.session_state:
        st.error("No image found. Please restart the process.")
        if st.button("Back to Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()
        return

    processed_path = st.session_state.output_paths['processed']
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(processed_path, caption="Final Cartoonized Version", use_container_width=True)
    
    with col2:
        st.subheader("📥 Download Links")
        st.write("---")
        
        with open(processed_path, "rb") as file:
            btn = st.download_button(
                    label="Download high-resolution image",
                    data=file,
                    file_name="cartoonized_logo.png",
                    mime="image/png"
                )
        
        st.write("---")
        st.info("You can also find this image in your profile history.")

    if st.button("Finish & Return to Dashboard"):
        # Cleanup session for next process
        del st.session_state.original_image
        del st.session_state.processed_image
        del st.session_state.output_paths
        if 'razorpay_order' in st.session_state:
            del st.session_state.razorpay_order
        st.session_state.page = "dashboard"
        st.rerun()
