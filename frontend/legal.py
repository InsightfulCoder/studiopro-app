import streamlit as st
from utils.ui_utils import safe_rerun

def terms_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        safe_rerun()
        
    st.markdown("""
<div class="premium-card" style="padding: 4rem; animation: reveal 0.8s ease-out forwards;">
    <h1 style="font-size: 3.5rem; margin-bottom: 2rem; font-weight: 800; background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Terms of Service</h1>
    <p style="color: var(--text-muted); line-height: 1.8;">Last updated: March 2026</p>
    <hr style="border: 0; border-top: 1px solid var(--border-soft); margin: 2rem 0;">
    
    <h3 style="color: white; margin-top: 2rem;">1. Acceptance of Terms</h3>
    <p style="color: var(--text-muted); line-height: 1.8;">
        By accessing and using StudioPro AI, you agree to be bound by these Terms of Service. If you do not agree to these terms, please do not use our services.
    </p>
    
    <h3 style="color: white; margin-top: 2rem;">2. Service Description</h3>
    <p style="color: var(--text-muted); line-height: 1.8;">
        StudioPro AI provides AI-powered image transformation services. We reserve the right to modify or discontinue the service at any time without notice.
    </p>
    
    <h3 style="color: white; margin-top: 2rem;">3. User Content</h3>
    <p style="color: var(--text-muted); line-height: 1.8;">
        You retain ownership of the images you upload. However, by using the service, you grant us a license to process your content for the purpose of providing the results.
    </p>
    
    <h3 style="color: white; margin-top: 2rem;">4. Prohibited Use</h3>
    <p style="color: var(--text-muted); line-height: 1.8;">
        You may not use StudioPro AI to generate harmful, illegal, or copyright-infringing content.
    </p>
    
    <h3 style="color: white; margin-top: 2rem;">5. Limitation of Liability</h3>
    <p style="color: var(--text-muted); line-height: 1.8;">
        StudioPro AI is provided "as is". We are not liable for any damages arising from the use or inability to use the service.
    </p>
</div>
    """, unsafe_allow_html=True)

def privacy_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        safe_rerun()
        
    st.markdown("""
<div class="premium-card" style="padding: 4rem; animation: reveal 0.8s ease-out forwards;">
    <h1 style="font-size: 3.5rem; margin-bottom: 2rem; font-weight: 800; background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Privacy Policy</h1>
    <p style="color: var(--text-muted); line-height: 1.8;">Last updated: March 2026</p>
    <hr style="border: 0; border-top: 1px solid var(--border-soft); margin: 2rem 0;">
    
    <h3 style="color: white; margin-top: 2rem;">1. Data Collection</h3>
    <p style="color: var(--text-muted); line-height: 1.8;">
        We collect information you provide directly to us, such as when you create an account or upload images for processing.
    </p>
    
    <h3 style="color: white; margin-top: 2rem;">2. Use of Information</h3>
    <p style="color: var(--text-muted); line-height: 1.8;">
        We use the information we collect to provide, maintain, and improve our services, and to process your transactions.
    </p>
    
    <h3 style="color: white; margin-top: 2rem;">3. Data Security</h3>
    <p style="color: var(--text-muted); line-height: 1.8;">
        We implement reasonable security measures to protect your personal information from unauthorized access or disclosure.
    </p>
    
    <h3 style="color: white; margin-top: 2rem;">4. Third-Party Services</h3>
    <p style="color: var(--text-muted); line-height: 1.8;">
        We may use third-party services for payment processing and analytics. These services have their own privacy policies.
    </p>
    
    <h3 style="color: white; margin-top: 2rem;">5. Your Choices</h3>
    <p style="color: var(--text-muted); line-height: 1.8;">
        You can access and update your account information through your dashboard settings.
    </p>
</div>
    """, unsafe_allow_html=True)
