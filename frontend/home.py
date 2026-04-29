import streamlit as st
import base64
import os
from utils.ui_utils import section_header, safe_rerun

@st.cache_data
def get_base64_of_bin_file(bin_file):
    if not os.path.exists(bin_file):
        return ""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def home_page():
    # 1. Premium Navbar
    st.markdown(f"""
        <div class="navbar">
            <div class="nav-logo"><span>✨</span> StudioPro AI</div>
            <div class="nav-links">
                <a href="#features" class="nav-link">Features</a>
                <a href="#how-it-works" class="nav-link">Artistry Slider</a>
                <a href="#gallery" class="nav-link">AI Styles</a>
                <a href="#pricing" class="nav-link">Pricing</a>
            </div>
            <div style="width: 150px;"></div>
        </div>
    """, unsafe_allow_html=True)
    
    # Hero Navbar Button (Login/Dash)
    nav_col1, nav_col2 = st.columns([5, 1])
    with nav_col2:
        if st.session_state.user:
            if st.button("Dashboard", key="nav_dash_v4"):
                st.session_state.page = "dashboard"
                safe_rerun()
        else:
            if st.button("Sign In", key="nav_login_v4"):
                st.session_state.page = "login"
                safe_rerun()

    # 2. Hero Section
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1], gap="large")
    
    with col1:
        st.markdown(f"""
            <div style="animation: reveal 0.8s ease-out forwards; padding-top: 2rem;">
                <div style="display: inline-block; padding: 6px 14px; background: rgba(255,126,95,0.1); border: 1px solid var(--border-glow); border-radius: 50px; color: var(--accent-primary); font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 2rem;">
                    ✨ Powered by Neural Engine V3
                </div>
                <h1 style="font-size: 5.2rem; line-height: 1; margin-bottom: 2rem; font-weight: 800; letter-spacing: -0.04em; background: linear-gradient(to bottom right, #FFFFFF, #94A3B8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    Transform Your Photos Into <span style="background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">AI Art</span>
                </h1>
                <p style="font-size: 1.25rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 3.5rem; max-width: 550px;">
                    StudioPro AI uses proprietary neural pipelines to turn everyday portraits into high-fidelity masterpieces. From Pixar-style 3D to hand-painted watercolors.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        h_btn1, h_btn2 = st.columns([1, 1])
        with h_btn1:
            if st.button("🚀 Start Creating", key="hero_start_v4", use_container_width=True):
                st.session_state.page = "studio"
                safe_rerun()
        with h_btn2:
            if st.button("🖼️ View Gallery", key="hero_gallery_v4", use_container_width=True):
                # Placeholder for local anchor
                pass
    
    with col2:
        st.markdown("""
            <div style="position: relative; animation: float 6s ease-in-out infinite;">
                <div style="position: absolute; top: -15%; left: -15%; width: 130%; height: 130%; background: radial-gradient(circle, var(--accent-glow) 0%, transparent 70%); filter: blur(80px); z-index: -1;"></div>
                <div class="premium-card" style="padding: 10px; border-radius: 40px; background: linear-gradient(135deg, rgba(255,255,255,0.1), transparent);">
                    <img src="https://images.unsplash.com/photo-1620641788421-7a1c342ea42e?auto=format&fit=crop&q=80&w=600" style="width: 100%; border-radius: 32px; box-shadow: 0 30px 60px rgba(0,0,0,0.5);">
                    <div style="position: absolute; bottom: 30px; left: 30px; background: rgba(0,0,0,0.6); backdrop-filter: blur(12px); padding: 12px 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1);">
                        <div style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase;">Style Applied</div>
                        <div style="font-weight: 700; color: white;">3D Cinematic Cartoon</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # 3. Neural Artistry Showcase
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<div id='how-it-works'></div>", unsafe_allow_html=True)
    section_header("Neural Artistry Showcase", "Witness the next generation of creative AI in automated action.")
    
    show_col1, show_col2, show_col3 = st.columns([1, 2, 1], gap="large")
    
    with show_col1:
        st.markdown("""
            <div class="telemetry-card">
                <div class="telemetry-label">Active Model</div>
                <div class="telemetry-value">Titan-X Cartoon</div>
            </div>
            <div class="telemetry-card">
                <div class="telemetry-label">Processing Load</div>
                <div class="telemetry-value">1.4 Teraflops</div>
            </div>
            <div class="telemetry-card">
                <div class="telemetry-label">Neural Fidelity</div>
                <div class="telemetry-value">99.8% Optimized</div>
            </div>
        """, unsafe_allow_html=True)
        
    with show_col2:
        st.markdown(f"""
            <div class="showcase-main-wrapper" style="animation: reveal 1s ease-out forwards;">
                <div class="showcase-badge">
                    <div style="font-size: 0.6rem; color: var(--accent-primary); font-weight: 800; text-transform: uppercase;">Style Applied</div>
                    <div style="font-weight: 700; color: white;">Cinematic Anime V3</div>
                </div>
                <img src="https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&q=80&w=1200" style="width: 100%; border-radius: 32px; box-shadow: 0 40px 100px rgba(0,0,0,0.6);">
                <div style="position: absolute; bottom: 30px; right: 30px; background: rgba(0,0,0,0.6); backdrop-filter: blur(12px); padding: 12px 24px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1);">
                    <div style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase;">Resolution</div>
                    <div style="font-weight: 700; color: white;">8K Ultra HD Render</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with show_col3:
        st.markdown("""
            <div class="telemetry-card" style="height: 100%; display: flex; flex-direction: column; justify-content: center; gap: 2rem;">
                <div>
                    <div class="telemetry-label">Model Pipeline</div>
                    <div style="font-size: 0.9rem; color: var(--text-muted); line-height: 1.4;">Multiple neural layers process light, texture, and geometry in parallel for perfect results.</div>
                </div>
                <div style="background: rgba(255,126,95,0.1); padding: 1.5rem; border-radius: 16px; border: 1px solid var(--border-glow);">
                    <div style="font-weight: 700; color: var(--accent-primary); margin-bottom: 0.5rem;">Turbo Engine</div>
                    <div style="font-size: 0.8rem; color: var(--text-muted);">0.0ms Latency detected in current region.</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # 4. Features Section
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<div id='features'></div>", unsafe_allow_html=True)
    section_header("Engineered for Excellence", "Powerful features that make StudioPro AI the choice for professionals.")
    
    f_cols = st.columns(3)
    features = [
        ("🎨", "AI Cartoon Generator", "Convert any portrait into a stunning digital character in seconds."),
        ("🌈", "12+ Art Styles", "From Pixar and Anime to Watercolor and Sketch style variations."),
        ("🚀", "Turbo Processing", "Our serverless architecture ensures zero wait time for your creations."),
        ("💎", "HD Downloads", "Download your art in ultra-high resolution ready for social or print."),
        ("🖱️", "Drag & Drop", "Simply drop your image and let the neural network do the heavy lifting."),
        ("🛡️", "Secure Vault", "Your images are processed securely and never stored without permission.")
    ]
    
    for i, (icon, title, desc) in enumerate(features):
        with f_cols[i % 3]:
            st.markdown(f"""
                <div class="premium-card" style="margin-bottom: 2rem; border-color: var(--border-soft);">
                    <div class="feature-icon">{icon}</div>
                    <h3 style="margin-bottom: 1rem;">{title}</h3>
                    <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.6;">{desc}</p>
                </div>
            """, unsafe_allow_html=True)

    # 5. Pricing V3
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<div id='pricing'></div>", unsafe_allow_html=True)
    section_header("Transparent Pricing", "Choose the plan that matches your creative volume.")
    
    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown("""
            <div class="pricing-v3-card">
                <h3>Starter</h3>
                <div class="pricing-v3-price">₹0<span>/mo</span></div>
                <ul class="pricing-v3-features">
                    <li>5 Generations / day</li>
                    <li>Standard Styles</li>
                    <li class="disabled">HD Downloads</li>
                    <li class="disabled">Batch Processing</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        st.button("Begin Free", key="price_v3_free", use_container_width=True)
        
    with p2:
        st.markdown("""
            <div class="pricing-v3-card popular">
                <h3>Creator Pro</h3>
                <div class="pricing-v3-price">₹50<span>/image</span></div>
                <ul class="pricing-v3-features">
                    <li>Unlimited Generations</li>
                    <li>All Premium Styles</li>
                    <li>4K Resolution Exports</li>
                    <li>No Watermarks</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        st.button("Unlock Pro", key="price_v3_pro", use_container_width=True)
        
    with p3:
        st.markdown("""
            <div class="pricing-v3-card">
                <h3>Infinite</h3>
                <div class="pricing-v3-price">₹999<span>/mo</span></div>
                <ul class="pricing-v3-features">
                    <li>Fastest Processing</li>
                    <li>Custom Styles Beta</li>
                    <li>API Access</li>
                    <li>24/7 Priority Support</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        st.button("Go Infinite", key="price_v3_creator", use_container_width=True)

    # 7. Footer
    st.markdown("""
        <div class="footer" style="padding-bottom: 2rem;">
            <div style="font-size: 2.5rem; font-weight: 800; color: white; margin-bottom: 1.5rem;">✨ StudioPro AI</div>
            <div style="color: var(--text-muted); margin-bottom: 3rem; max-width: 600px; margin-left: auto; margin-right: auto;">
                Bridging the gap between human creativity and neural intelligence. Join thousands of creators transforming reality into high-fidelity AI art.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Focused Link Row (Terms and Privacy Only)
    f_col1, f_col2, f_col3, f_col4 = st.columns([1, 0.5, 0.5, 1])
    with f_col2:
        if st.button("Terms", key="foot_terms_v4", use_container_width=True):
            st.session_state.page = "terms"
            st.rerun()
    with f_col3:
        if st.button("Privacy", key="foot_priv_v4", use_container_width=True):
            st.session_state.page = "privacy"
            st.rerun()

    st.markdown("""
        <div class="footer" style="margin-top: 2rem;">
            <div style="color: var(--text-dim); font-size: 0.85rem; letter-spacing: 0.05em;">© 2026 STUDIOPRO AI. ALL RIGHTS RESERVED.</div>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    home_page()
