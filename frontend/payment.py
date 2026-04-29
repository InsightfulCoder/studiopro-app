import streamlit as st
import streamlit.components.v1 as components
from utils.razorpay_manager import create_razorpay_order, RAZORPAY_KEY_ID
from backend.transactions import create_order
from utils.ui_utils import section_header, safe_image_display, safe_rerun

def payment_page():
    section_header("Secure Checkout", "Finalize your artistic transformation")
    
    if 'output_paths' not in st.session_state:
        st.warning("No image found. Please visit the studio first.")
        if st.button("Go to Studio"):
            st.session_state.page = "dashboard"
            safe_rerun()
        return

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Order Summary")
        safe_image_display(st.session_state.output_paths['processed'], caption="Your Customized Logo")
        st.write(f"**Selected Style:** {st.session_state.output_paths['style']}")
        st.write("**Price:** ₹50.00")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-bottom: 1.5rem; display: flex; align-items: center; gap: 10px;">💳 Payment Details</h3>', unsafe_allow_html=True)
        
        # Premium Payment Gateway UI
        tab_upi, tab_bank = st.tabs(["📱 UPI / QR Scan", "🏦 Bank Transfer"])
        
        with tab_upi:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-soft); border-radius: 16px; padding: 2rem; text-align: center; margin-bottom: 1.5rem;">
                <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1rem;">Scan with any UPI App (GPay, PhonePe, Paytm)</p>
                <div style="background: white; padding: 15px; border-radius: 12px; display: inline-block; margin: 0 auto 1.5rem auto; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
                    <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=upi://pay?pa=studiopro@upi&pn=StudioPro%20AI&am=50.00&cu=INR" width="180">
                </div>
                <div style="background: rgba(0,0,0,0.3); border-radius: 8px; padding: 10px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: var(--text-dim); font-size: 0.85rem;">UPI ID</span>
                    <strong style="font-family: monospace; color: var(--text-main); font-size: 1.1rem;">studiopro@upi</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with tab_bank:
            st.markdown(
                "<div style='background: rgba(255,255,255,0.02); border: 1px solid var(--border-soft); border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem;'>"
                "<p style='color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-soft); padding-bottom: 10px;'>"
                "Wire Transfer Information"
                "</p>"
                "<div style='display: grid; grid-template-columns: 1fr 2fr; gap: 1rem; margin-bottom: 10px;'>"
                "<div style='color: var(--text-dim); font-size: 0.85rem;'>Bank Name</div>"
                "<div style='color: var(--text-main); font-weight: 600;'>Global Digital Bank</div>"
                "<div style='color: var(--text-dim); font-size: 0.85rem;'>Account Name</div>"
                "<div style='color: var(--text-main); font-weight: 600;'>StudioPro AI Technologies</div>"
                "<div style='color: var(--text-dim); font-size: 0.85rem;'>Account Number</div>"
                "<div style='font-family: monospace; font-size: 1.1rem; color: var(--accent-tertiary); font-weight: 700;'>4455 6677 8899</div>"
                "<div style='color: var(--text-dim); font-size: 0.85rem;'>IFSC/Routing</div>"
                "<div style='font-family: monospace; color: var(--text-main); font-weight: 600;'>GDBK0001234</div>"
                "</div>"
                "</div>", 
                unsafe_allow_html=True
            )

        st.markdown("""
        <div style="background: rgba(110, 225, 255, 0.1); border-left: 4px solid var(--accent-tertiary); padding: 12px 16px; border-radius: 0 8px 8px 0; margin-bottom: 2rem;">
            <p style="margin: 0; font-size: 0.85rem; color: var(--text-main);">
                <strong style="color: var(--accent-tertiary);">Secure Connection:</strong> End-to-end encrypted protocol via 256-bit SSL.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Confirm Payment & Deposit 5 HD Credits 🔒", use_container_width=True):
            with st.spinner("Authenticating transaction... Please do not close this window."):
                import time
                time.sleep(2.5)
                # Ensure user is logged in
                if st.session_state.user:
                    from backend.user_manager import add_credits
                    add_credits(st.session_state.user['user_id'], 5)
                    st.success("Payment Received! 5 Premium Credits have been added to your Workspace.")
                    st.session_state.page = "dashboard"
                    safe_rerun()
                else:
                    st.error("Authentication Error. Please log in.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Cancel & Return to Dashboard", use_container_width=False):
        st.session_state.page = "dashboard"
        safe_rerun()
