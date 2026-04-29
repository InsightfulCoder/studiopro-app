import streamlit as st
from utils.ui_utils import section_header, safe_rerun

def pricing_page():
    section_header("Choose Your Plan", "Unlock the full power of StudioPro AI")
    
    col1, col2, col3 = st.columns([1, 1.2, 1], gap="large")
    
    with col1:
        st.markdown("""
            <div class="premium-card" style="height: 100%; border: 1px solid var(--border-soft);">
                <h3 style="text-align: center; margin-bottom: 1rem;">Free Trial</h3>
                <div style="font-size: 2.5rem; font-weight: 800; text-align: center; margin-bottom: 2rem;">₹0<span style="font-size: 1rem; color: var(--text-muted);">/month</span></div>
                <ul class="footer-link" style="margin-bottom: 3rem;">
                    <li>✓ 3 Free Image Generations</li>
                    <li>✓ Basic Cartoon Style</li>
                    <li>✓ Standard Resolution</li>
                    <li style="color: var(--text-dim);">✗ HD Download</li>
                    <li style="color: var(--text-dim);">✗ Priority Support</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Start Free", use_container_width=True):
            st.session_state.page = "studio"
            safe_rerun()

    with col2:
        st.markdown("""
            <div class="premium-card popular" style="height: 100%; border: 2px solid var(--accent-primary); background: rgba(255, 126, 95, 0.05);">
                <div style="position: absolute; top: -15px; left: 50%; transform: translateX(-50%); background: var(--accent-primary); color: white; padding: 4px 16px; border-radius: 20px; font-size: 0.75rem; font-weight: 800;">MOST POPULAR</div>
                <h3 style="text-align: center; margin-bottom: 1rem;">Creator Pro</h3>
                <div style="font-size: 2.5rem; font-weight: 800; text-align: center; margin-bottom: 2rem;">₹50<span style="font-size: 1rem; color: var(--text-muted);">/image</span></div>
                <ul class="footer-link" style="margin-bottom: 3rem;">
                    <li>✓ Unlimited Generations</li>
                    <li>✓ All 4 Artistic Styles</li>
                    <li>✓ HD Quality Download</li>
                    <li>✓ No Watermarks</li>
                    <li>✓ Priority Neural Queue</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Unlock Pro Now", key="buy_pro", use_container_width=True):
            if st.session_state.user:
                st.session_state.page = "studio"
            else:
                st.session_state.page = "login"
            safe_rerun()

    with col3:
        st.markdown("""
            <div class="premium-card" style="height: 100%; border: 1px solid var(--border-soft);">
                <h3 style="text-align: center; margin-bottom: 1rem;">Enterprise</h3>
                <div style="font-size: 1.8rem; font-weight: 800; text-align: center; margin-bottom: 2rem;">Custom</div>
                <ul class="footer-link" style="margin-bottom: 3rem;">
                    <li>✓ API Integration</li>
                    <li>✓ Bulk Processing</li>
                    <li>✓ Custom Styles</li>
                    <li>✓ Dedicated Servers</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Contact Sales", key="contact_sales", use_container_width=True):
            st.info("Coming soon! Please contact us at enterprise@studiopro.ai")

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        safe_rerun()

if __name__ == "__main__":
    pricing_page()
