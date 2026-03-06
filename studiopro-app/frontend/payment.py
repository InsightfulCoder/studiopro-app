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
        st.subheader("Payment Gateway")
        st.info("Unlock high-resolution, watermark-free downloads.")
        
        # 1. Create Order
        if 'razorpay_order' not in st.session_state:
            receipt_id = f"REC_{st.session_state.user['user_id']}"
            order = create_razorpay_order(50, receipt_id)
            if order:
                st.session_state.razorpay_order = order
                create_order(st.session_state.user['user_id'], 50)
            else:
                st.error("Gateway error. Please try again later.")

        # 2. Razorpay Integration
        if 'razorpay_order' in st.session_state:
            order_id = st.session_state.razorpay_order['id']
            razorpay_html = f"""
                <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
                <script>
                var options = {{
                    "key": "{RAZORPAY_KEY_ID}",
                    "amount": "5000",
                    "currency": "INR",
                    "name": "StudioPro AI",
                    "order_id": "{order_id}",
                    "handler": function (response){{
                        window.parent.postMessage({{'type': 'payment_success'}}, "*");
                    }},
                    "theme": {{"color": "#A855F7"}}
                }};
                var rzp1 = new Razorpay(options);
                document.getElementById('pay-btn').onclick = function(e){{ rzp1.open(); e.preventDefault(); }}
                </script>
                <button id="pay-btn" style="background: linear-gradient(135deg, #6366F1 0%, #A855F7 100%); color: white; padding: 12px 30px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; width: 100%;">
                    Pay with Razorpay
                </button>
            """
            components.html(razorpay_html, height=80)
        
        st.write("---")
        if st.checkbox("Bypass Payment (Developer Demo)"):
            if st.button("Confirm & Proceed to Download"):
                st.session_state.page = "download"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Exit to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()
