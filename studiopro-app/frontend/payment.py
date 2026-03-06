import streamlit as st
import streamlit.components.v1 as components
from utils.razorpay_manager import create_razorpay_order, RAZORPAY_KEY_ID
from backend.transactions import create_order
from utils.ui_utils import section_header

def payment_page():
    section_header("Secure Checkout", "Finalize your artistic transformation")
    
    if 'output_paths' not in st.session_state:
        st.warning("No image found. Please visit the studio first.")
        if st.button("Go to Studio"):
            st.session_state.page = "dashboard"
            st.rerun()
        return

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Order Summary")
        st.image(st.session_state.output_paths['processed'], use_container_width=True, caption="Your Customized Logo")
        st.write(f"**Selected Style:** {st.session_state.output_paths['style']}")
        st.write("**Price:** ₹50.00")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Payment Details")
        st.info("Choose a manual payment method below to unlock HD download.")
        
        payment_choice = st.radio("Select Payment Method", ["UPI / QR Code", "Bank Transfer"])
        
        if payment_choice == "UPI / QR Code":
            st.write("**UPI ID:** `studiopro@upi`")
            st.write("Scan the QR code below using any UPI app (GPay, PhonePe, Paytm).")
            # Placeholder for a QR code asset
            st.info("📸 QR Code Asset Placeholder")
        else:
            st.write("**Bank Name:** Global Digital Bank")
            st.write("**Account Name:** StudioPro AI")
            st.write("**Account Number:** `9876543210`")
            st.write("**IFSC Code:** `GDBK0001234`")

        st.write("---")
        st.success("Once payment is completed, please confirm the transaction below.")
        
        if st.button("Confirm Payment & Download"):
            with st.spinner("Verifying transaction..."):
                # Simulated verification
                import time
                time.sleep(2)
                st.session_state.page = "download"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Exit to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()
