"""Top navigation bar component."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import streamlit as st


def render_navbar() -> str:
    """Render navigation bar and return active page name."""
    if "active_page" not in st.session_state:
        st.session_state["active_page"] = "Dashboard"
    
    pages = ["Dashboard", "Recommendations", "Market Lab", "VS Mode"]
    
    # Unified GlowGuide Header with Logo
    logo_path = Path(__file__).parent.parent / "assets" / "logo.png"
    
    st.markdown("""
    <style>
        .navbar-glowguide {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 0;
            margin-bottom: 20px;
            border-bottom: 2px solid #e5e7eb;
            gap: 16px;
        }
        
        .navbar-branding {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
        }
        
        .navbar-logo {
            width: 45px;
            height: 45px;
            object-fit: contain;
        }
        
        .navbar-glowguide-title {
            font-size: 24px;
            font-weight: 800;
            margin: 0;
            font-family: 'Space Grotesk', sans-serif;
            color: var(--navbar-text, #000000);
        }
        
        @media (prefers-color-scheme: dark) {
            .navbar-glowguide {
                border-bottom-color: #374151;
            }
            .navbar-glowguide-title {
                color: #ffffff;
            }
        }
        
        @media (prefers-color-scheme: light) {
            .navbar-glowguide {
                border-bottom-color: #e5e7eb;
            }
            .navbar-glowguide-title {
                color: #000000;
            }
        }
    </style>
    
    <div class="navbar-glowguide">
        <div class="navbar-branding">
            <img src="file://""" + str(logo_path) + """" class="navbar-logo" alt="GlowGuide">
            <h2 class="navbar-glowguide-title">GlowGuide</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    nav_cols = st.columns(len(pages))
    for i, page in enumerate(pages):
        with nav_cols[i]:
            if st.button(page, use_container_width=True,
                        type="primary" if st.session_state["active_page"] == page else "secondary"):
                st.session_state["active_page"] = page
                st.rerun()
    
    st.divider()
    return st.session_state["active_page"]
