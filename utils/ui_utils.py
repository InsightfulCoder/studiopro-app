import streamlit as st

def inject_custom_css():
    """Injects premium, modern CSS for a professional look."""
    st.markdown("""
        <style>
        /* Import Premium Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Outfit:wght@300;400;600;700&display=swap');

        /* Global Styling Variables - Dark Mode V3 */
        :root {
            --bg-page: #0A0A0B;
            --bg-navbar: rgba(10, 10, 11, 0.8);
            --bg-gradient: radial-gradient(circle at 50% -20%, #1A1A1D 0%, #0A0A0B 100%);
            
            --accent-primary: #FF7E5F;
            --accent-secondary: #FEB47B;
            --accent-tertiary: #6DE1FF;
            --accent-gradient: linear-gradient(135deg, #FF7E5F 0%, #FEB47B 100%);
            --accent-glow: rgba(255, 126, 95, 0.3);
            
            --text-main: #F8FAFC;
            --text-muted: #94A3B8;
            --text-dim: #64748B;
            
            --card-glass: rgba(255, 255, 255, 0.03);
            --card-glass-hover: rgba(255, 255, 255, 0.06);
            --border-soft: rgba(255, 255, 255, 0.08);
            --border-glow: rgba(255, 126, 95, 0.2);
            
            --shadow-premium: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
            --shadow-glow: 0 0 30px rgba(255, 126, 95, 0.15);
        }

        /* Essential Animations */
        @keyframes mesh-move {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes float {
            0% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-15px) rotate(1deg); }
            100% { transform: translateY(0px) rotate(0deg); }
        }
        @keyframes pulse-soft {
            0% { opacity: 0.8; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.02); }
            100% { opacity: 0.8; transform: scale(1); }
        }
        @keyframes reveal {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Base Resets & Layout */
        .stApp {
            background-color: var(--bg-page);
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: var(--text-main);
            background-image: 
                radial-gradient(at 0% 0%, rgba(255, 126, 95, 0.05) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(110, 225, 255, 0.05) 0px, transparent 50%);
        }

        /* Deep Gradient Backgrounds */
        .main {
            background: var(--bg-gradient);
            background-attachment: fixed;
        }

        h1, h2, h3, h4 {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            color: var(--text-main);
            letter-spacing: -0.01em;
        }

        /* Navigation Bar */
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.2rem 0;
            background: var(--bg-navbar);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            position: sticky;
            top: 0;
            z-index: 999;
            border-bottom: 1px solid var(--border-soft);
        }
        .nav-logo {
            font-size: 1.6rem;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 10px;
            color: var(--text-main);
        }
        .nav-logo span {
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
            align-items: center;
        }
        
        .nav-link {
            text-decoration: none;
            color: var(--text-muted);
            font-weight: 500;
            font-size: 0.95rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .nav-link:hover {
            color: var(--text-main);
            transform: translateY(-1px);
        }

        /* Premium Dark Cards (Glassmorphism) */
        .premium-card {
            background: var(--card-glass);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 24px;
            border: 1px solid var(--border-soft);
            box-shadow: var(--shadow-premium);
            padding: 2.5rem;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
        }
        .premium-card:hover {
            transform: translateY(-8px);
            background: var(--card-glass-hover);
            border-color: var(--border-glow);
            box-shadow: 0 40px 80px -20px rgba(0,0,0,0.6);
        }
        
        .glass-card {
            background: rgba(255, 255, 255, 0.02);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 1px solid var(--border-soft);
            padding: 1.5rem;
            margin-bottom: 1rem;
        }

        /* Feature Icons */
        .feature-icon {
            width: 64px;
            height: 64px;
            border-radius: 18px;
            background: rgba(255, 126, 95, 0.1);
            color: var(--accent-primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            margin-bottom: 2rem;
            border: 1px solid rgba(255, 126, 95, 0.2);
            transition: all 0.3s ease;
        }
        .premium-card:hover .feature-icon {
            transform: scale(1.1) rotate(5deg);
            background: rgba(255, 126, 95, 0.2);
            box-shadow: 0 0 20px rgba(255, 126, 95, 0.2);
        }

        /* Primary Action Buttons */
        div[data-testid="stFormSubmitButton"] > button, .stButton > button {
            background: linear-gradient(135deg, #FF7E5F 0%, #FEB47B 50%, #FF7E5F 100%) !important;
            background-size: 200% auto !important;
            padding: 14px 32px !important;
            border-radius: 12px !important;
            color: #ffffff !important;
            font-weight: 800 !important;
            border: none !important;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            box-shadow: 0 10px 30px rgba(255, 126, 95, 0.3) !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            font-size: 0.95rem !important;
            animation: mesh-move 4s infinite linear !important;
        }
        div[data-testid="stFormSubmitButton"] > button:hover, .stButton > button:hover {
            transform: translateY(-4px) scale(1.03) !important;
            box-shadow: 0 20px 40px rgba(255, 126, 95, 0.5) !important;
            filter: brightness(1.2) !important;
            background-position: right center !important;
        }
        
        /* Pricing V3 System */
        .pricing-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2rem;
            margin-top: 4rem;
        }
        .pricing-v3-card {
            background: var(--card-glass);
            border: 1px solid var(--border-soft);
            border-radius: 32px;
            padding: 3.5rem 2.5rem;
            text-align: center;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        .pricing-v3-card.popular {
            border: 2px solid var(--accent-primary);
            background: rgba(255, 126, 95, 0.05);
            transform: scale(1.05);
            z-index: 10;
        }
        .pricing-v3-card.popular::before {
            content: 'MOST POPULAR';
            position: absolute;
            top: 20px;
            right: -35px;
            background: var(--accent-primary);
            color: white;
            padding: 5px 40px;
            font-size: 0.7rem;
            font-weight: 900;
            transform: rotate(45deg);
        }
        .pricing-v3-price {
            font-size: 4rem;
            font-weight: 800;
            margin: 2rem 0;
            font-family: 'Outfit', sans-serif;
            letter-spacing: -2px;
        }
        .pricing-v3-price span {
            font-size: 1.1rem;
            color: var(--text-dim);
            font-weight: 500;
            letter-spacing: 0;
        }
        .pricing-v3-features {
            list-style: none;
            padding: 0;
            margin: 2rem 0;
            text-align: left;
            flex-grow: 1;
        }
        .pricing-v3-features li {
            margin-bottom: 1.2rem;
            color: var(--text-muted);
            font-size: 0.95rem;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .pricing-v3-features li::before {
            content: '✓';
            color: var(--accent-primary);
            font-weight: 900;
        }
        .pricing-v3-features li.disabled {
            color: var(--text-dim);
            opacity: 0.5;
        }
        .pricing-v3-features li.disabled::before {
            content: '✕';
            color: var(--text-dim);
        }

        /* Comparison Slider Support */
        .comp-container {
            position: relative;
            width: 100%;
            height: 500px;
            border-radius: 32px;
            overflow: hidden;
            border: 1px solid var(--border-soft);
            box-shadow: var(--shadow-premium);
        }
        .before-after-slider {
            -webkit-appearance: none;
            width: 100%;
            height: 100%;
            background: transparent;
            position: absolute;
            z-index: 100;
            margin: 0;
            cursor: ew-resize;
        }
        .before-after-slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 4px;
            height: 500px;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
            cursor: ew-resize;
        }

        /* Robust Input Field Styling */
        div[data-testid="stTextInput"] label, div[data-testid="stPasswordInput"] label {
            color: #FFFFFF !important; /* Force white labels */
            font-weight: 700 !important;
            margin-bottom: 0.8rem !important;
            font-size: 1rem !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        div[data-testid="stTextInput"] input, div[data-testid="stPasswordInput"] input {
            background-color: #FFFFFF !important; /* Forced white background for black text readability */
            color: #000000 !important; /* Forced black text */
            caret-color: #000000 !important; /* Forced black cursor */
            border: 2px solid var(--border-soft) !important;
            border-radius: 14px !important;
            padding: 14px 18px !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
        }
        div[data-testid="stTextInput"] input:focus, div[data-testid="stPasswordInput"] input:focus {
            border-color: var(--accent-primary) !important;
            box-shadow: 0 0 0 4px rgba(255, 126, 95, 0.2) !important;
            background-color: #FFFFFF !important;
        }

        /* Webkit Autofill Handling */
        input:-webkit-autofill,
        input:-webkit-autofill:hover, 
        input:-webkit-autofill:focus, 
        input:-webkit-autofill:active {
            -webkit-box-shadow: 0 0 0 50px white inset !important; /* Keep background white */
            -webkit-text-fill-color: black !important; /* Keep text black */
            caret-color: black !important;
        }

        /* Sidebar & Navigation */
        [data-testid="stSidebar"] {
            background-color: #0E0E0F;
            border-right: 1px solid var(--border-soft);
        }
        [data-testid="stSidebarNav"] {
            padding-top: 2rem;
        }
        
        /* Stat Cards */
        .stat-card {
            background: var(--card-glass);
            border-radius: 20px;
            padding: 2rem;
            border: 1px solid var(--border-soft);
            text-align: left;
            transition: all 0.3s ease;
        }
        .stat-card:hover {
            border-color: var(--accent-primary);
            box-shadow: 0 20px 40px -10px rgba(0,0,0,0.5);
        }
        
        /* Neural Artistry Showcase Styles */
        .telemetry-card {
            background: rgba(10, 10, 11, 0.4);
            border-radius: 20px;
            border: 1px solid var(--border-soft);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            position: relative;
            overflow: hidden;
        }
        .telemetry-card::after {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,126,95,0.05), transparent);
            animation: mesh-move 3s infinite linear;
        }
        .telemetry-label {
            font-size: 0.65rem;
            font-weight: 800;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 0.15em;
            margin-bottom: 0.5rem;
        }
        .telemetry-value {
            font-family: 'Outfit', sans-serif;
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--text-main);
        }
        .showcase-main-wrapper {
            position: relative;
            border-radius: 40px;
            padding: 10px;
            background: linear-gradient(135deg, var(--border-soft), transparent);
            border: 1px solid var(--border-soft);
        }
        .showcase-badge {
            position: absolute;
            top: 30px;
            left: 30px;
            background: rgba(0,0,0,0.6);
            backdrop-filter: blur(12px);
            padding: 8px 16px;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.1);
            z-index: 10;
        }
        
        /* Footer */
        .footer {
            margin-top: 10rem;
            padding: 6rem 0 4rem;
            border-top: 1px solid var(--border-soft);
            background: rgba(0,0,0,0.3);
            text-align: center;
        }
        
        /* Sidebar Profile Badge */
        .profile-badge {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 12px;
            background: var(--card-glass);
            border-radius: 16px;
            border: 1px solid var(--border-soft);
        }
        .profile-avatar {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: var(--accent-gradient);
            color: #FFFFFF;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            font-weight: 800;
            box-shadow: 0 4px 15px var(--accent-glow);
        }

        /* Gallery Card Styles */
        .gallery-card {
            background: var(--card-glass);
            border-radius: 20px;
            overflow: hidden;
            border: 1px solid var(--border-soft);
            transition: all 0.3s ease;
        }
        .gallery-card:hover {
            border-color: var(--accent-primary);
            transform: translateY(-5px);
        }
        .gallery-img {
            width: 100%;
            object-fit: cover;
            border-bottom: 1px solid var(--border-soft);
        }
        .gallery-info {
            padding: 1rem;
            text-align: center;
        }

        /* Streamlit Tabs Styling */
        button[data-baseweb="tab"] {
            background-color: transparent !important;
            color: var(--text-muted) !important;
            font-family: 'Outfit', sans-serif !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
        }
        button[data-baseweb="tab"]:hover {
            color: var(--accent-primary) !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: var(--text-main) !important;
            border-bottom-color: var(--accent-primary) !important;
        }

        /* Streamlit Metrics Styling */
        div[data-testid="stMetricValue"] {
            color: var(--text-main) !important;
            font-family: 'Outfit', sans-serif !important;
            font-size: 2.5rem !important;
            font-weight: 800 !important;
        }
        div[data-testid="stMetricLabel"] {
            color: var(--text-muted) !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
        }

        /* Streamlit Overrides */
        [data-testid="stHeader"], footer, #MainMenu {visibility: hidden;}
        .block-container {padding-top: 0 !important; max-width: 1200px !important;}
        </style>
    """, unsafe_allow_html=True)

def section_header(title, subtitle=None):
    """Render a professional section header."""
    st.markdown(f"<h2 style='text-align: center; margin-bottom: 0.5rem;'>{title}</h2>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p style='text-align: center; color: var(--text-light); margin-bottom: 3rem;'>{subtitle}</p>", unsafe_allow_html=True)

def safe_rerun():
    """Version-agnostic rerun for Streamlit."""
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

def safe_image_display(image_path, caption=None, use_container_width=True):
    """Safely displays an image or a placeholder if missing."""
    import os
    if os.path.exists(image_path):
        st.image(image_path, caption=caption, use_container_width=use_container_width)
    else:
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.02); border: 2px dashed var(--border-soft); border-radius: 20px; padding: 2rem; text-align: center; color: var(--text-dim);">
                <div style="font-size: 2rem; margin-bottom: 10px;">🖼️</div>
                <div style="font-size: 0.8rem;">Asset not found: {os.path.basename(image_path)}</div>
            </div>
        """, unsafe_allow_html=True)
