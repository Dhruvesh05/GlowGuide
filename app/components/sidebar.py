"""Context-aware sidebar filter panel."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st


def render_sidebar(active_page: str) -> dict:
    """Render sidebar with GlowGuide header, navigation, and context-aware filters."""
    # ========== SIDEBAR HEADER - UNIFIED GLOWGUIDE WITH LOGO ==========
    logo_path = Path(__file__).parent.parent / "assets" / "logo.png"
    
    st.sidebar.markdown("""
    <style>
        .sidebar-glowguide-header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            padding-bottom: 24px;
            margin-bottom: 24px;
            border-bottom: 2px solid #e5e7eb;
        }
        
        .sidebar-glowguide-logo {
            width: 45px;
            height: 45px;
            object-fit: contain;
        }
        
        .sidebar-glowguide-title {
            font-size: 22px;
            font-weight: 800;
            margin: 0;
            font-family: 'Space Grotesk', sans-serif;
            color: var(--sidebar-header-text, #000000);
        }
        
        @media (prefers-color-scheme: dark) {
            .sidebar-glowguide-header {
                border-bottom-color: #374151;
            }
            .sidebar-glowguide-title {
                color: #ffffff;
            }
        }
        
        @media (prefers-color-scheme: light) {
            .sidebar-glowguide-header {
                border-bottom-color: #e5e7eb;
            }
            .sidebar-glowguide-title {
                color: #000000;
            }
        }
    </style>
    
    <div class="sidebar-glowguide-header">
        <img src="file://""" + str(logo_path) + """" class="sidebar-glowguide-logo" alt="GlowGuide">
        <h2 class="sidebar-glowguide-title">GlowGuide</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown(
        "<p style='text-align: center; font-size: 12px; color: #9ca3af; margin-bottom: 24px; font-weight: 500;'>Skincare Intelligence</p>",
        unsafe_allow_html=True
    )
    
    # ========== SIDEBAR NAVIGATION ==========
    pages = ["Dashboard", "Recommendations", "Market Lab", "VS Mode"]
    
    for page in pages:
        if st.sidebar.button(
            page,
            key=f"sidebar_nav_{page}",
            use_container_width=True,
            type="primary" if active_page == page else "secondary"
        ):
            st.session_state.active_page = page
            st.rerun()
    
    st.sidebar.markdown("""
    <div style="padding: 16px 0; margin-bottom: 24px; border-bottom: 1px solid #e5e7eb;">
    </div>
    """, unsafe_allow_html=True)
    
    # ========== SECTION HEADER FOR FILTERS ==========
    st.sidebar.markdown("""
    <div style="padding-bottom: 20px; margin-bottom: 24px;">
        <h3 style="font-size: 16px; font-weight: 700; margin: 0; color: #1f2937;">Filters & Settings</h3>
        <p style="font-size: 12px; color: #9ca3af; margin: 8px 0 0 0;">Configure your preferences</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.divider()
    st.sidebar.markdown("""
    <p style="font-size: 12px; color: #9ca3af; text-align: center; margin: 16px 0 0 0;">
        GlowGuide v2.0<br>
        <span style="font-size: 11px;">Powered by ML & Skincare Science</span>
    </p>
    """, unsafe_allow_html=True)
    
    # Return empty dict - filters will be rendered in main area
    return {}
