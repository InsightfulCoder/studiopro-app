import streamlit as st

def inject_custom_css():
    """Injects premium, modern CSS for a professional look."""
    st.markdown("""
        <style>
        /* Import Premium Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&family=Space+Grotesk:wght@300;500;700&display=swap');

        /* Global Styling */
        html, body, [class*="st-"] {
            font-family: 'Outfit', sans-serif;
        }
        
        h1, h2, h3 {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            color: #FFFFFF;
            letter-spacing: -0.5px;
        }

        /* Auth Page Specific (Dark Text) */
        .auth-container p, .auth-container label, .auth-container span, .auth-container div {
            color: #000000 !important;
        }
        
        .auth-container h2 {
            color: #000000 !important;
        }

        /* Robust Black Text Fix for Auth Inputs */
        .auth-container [data-testid="stTextInput"] input {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            background-color: #f8fafc !important;
        }
        
        .auth-container [data-testid="stTextInput"] label p {
            color: #000000 !important;
        }

        .auth-container [data-testid="stCheckbox"] label p {
            color: #000000 !important;
        }

        /* Glassmorphism Container */
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
        }
        
        /* Auth Card (Light background for black text) */
        .auth-card {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }

        /* Modern Button Styling */
        .stButton>button {
            border-radius: 8px;
            border: none;
            padding: 10px 24px;
            font-weight: 600;
            background: linear-gradient(135deg, #6366F1 0%, #A855F7 100%);
            color: white;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(168, 85, 247, 0.4);
            border: none;
            color: white;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #0F172A;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }

        /* Input Fields */
        .stTextInput>div>div>input {
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: white;
        }
        
        /* Metric Styling */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            color: #A855F7;
        }
        
        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        </style>
    """, unsafe_allow_html=True)

def section_header(title, subtitle=None):
    """Render a professional section header."""
    st.markdown(f"## {title}")
    if subtitle:
        st.markdown(f"<p style='color: #94A3B8; font-size: 1.1rem; margin-top: -10px;'>{subtitle}</p>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 20px 0; border-color: rgba(255, 255, 255, 0.1);'>", unsafe_allow_html=True)
