import streamlit as st
import streamlit.components.v1 as components
from utils.razorpay_manager import create_razorpay_order, RAZORPAY_KEY_ID
from backend.transactions import create_order

def payment_page():
    st.header("💳 Secure Checkout")
    
    if 'output_paths' not in st.session_state:
        st.warning("No image found to process. Please go back to Image Processing.")
        if st.button("Go to Processing"):
            st.session_state.page = "dashboard"
            st.rerun()
        return

    st.write("---")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Order Summary")
        st.image(st.session_state.output_paths['processed'], use_container_width=True)
        st.write(f"**Style:** {st.session_state.output_paths['style']}")
        st.write("**Total Amount:** ₹50.00")

    with col2:
        st.subheader("Payment Details")
        st.info("You are paying for an HD, watermark-free download.")
        
        # 1. Create Order in Razorpay and DB
        if 'razorpay_order' not in st.session_state:
            receipt_id = f"REC_{st.session_state.user['user_id']}"
            order = create_razorpay_order(50, receipt_id)
            if order:
                st.session_state.razorpay_order = order
                create_order(st.session_state.user['user_id'], 50)
            else:
                st.error("Failed to initialize payment gateway.")
                return

        # 2. Razorpay Button (using HTML component)
        order_id = st.session_state.razorpay_order['id']
        amount = 5000 # in paise
        
        razorpay_html = f"""
            <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
            <script>
            var options = {{
                "key": "{RAZORPAY_KEY_ID}",
                "amount": "{amount}",
                "currency": "INR",
                "name": "StudioPro AI",
                "description": "Image Cartoonizer HD Download",
                "order_id": "{order_id}",
                "handler": function (response){{
                    window.parent.postMessage({{
                        type: 'razorpay_success',
                        payment_id: response.razorpay_payment_id,
                        order_id: response.razorpay_order_id,
                        signature: response.razorpay_signature
                    }}, "*");
                }},
                "theme": {{
                    "color": "#F37254"
                }}
            }};
            var rzp1 = new Razorpay(options);
            document.getElementById('pay-button').onclick = function(e){{
                rzp1.open();
                e.preventDefault();
            }}
            </script>
            <button id="pay-button" style="background-color: #F37254; color: white; padding: 10px 24px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px;">
                Pay with Razorpay
            </button>
        """
        
        # Note: In a real app, you'd need a way to listen to that 'postMessage'
        # For this prototype, we'll use the bypass below for Milestone 3 verification.
        components.html(razorpay_html, height=100)
        
        st.write("---")
        # Manual bypass for testing
        if st.checkbox("Bypass Payment for testing (Demo Mode)"):
            if st.button("Confirm Payment & Download"):
                st.session_state.page = "download"
                st.rerun()

    if st.button("Back to Dashboard"):
        st.session_state.razorpay_order = None
        st.session_state.page = "dashboard"
        st.rerun()

