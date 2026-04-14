"""Context-aware sidebar filter panel."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st


def render_sidebar(active_page: str) -> dict:
    """Render sidebar with GlowGuide header, navigation, and context-aware filters."""
    # ========== SIDEBAR HEADER ==========
    st.sidebar.markdown("""
    <div style="padding-bottom: 24px; margin-bottom: 24px; border-bottom: 1px solid #d0d0d0;">
        <p style="font-size: 24px; font-weight: 800; margin: 0; color: #000000;">GlowGuide</p>
        <p style="font-size: 12px; color: #666666; margin: 8px 0 0 0; font-weight: 500;">Skincare Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
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
    <div style="padding: 16px 0; margin-bottom: 24px; border-bottom: 1px solid #d0d0d0;">
    </div>
    """, unsafe_allow_html=True)
    
    # ========== SECTION HEADER FOR FILTERS ==========
    st.sidebar.markdown("""
    <div style="padding-bottom: 20px; margin-bottom: 24px;">
        <h3 style="font-size: 16px; font-weight: 700; margin: 0; color: #000000;">Filters & Settings</h3>
        <p style="font-size: 12px; color: #999999; margin: 8px 0 0 0;">Configure your preferences</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.divider()
    st.sidebar.markdown("""
    <p style="font-size: 11px; color: #999999; text-align: center; margin: 16px 0 0 0;">
        GlowGuide v2.0<br>
        <span style="font-size: 10px;">Powered by ML & Skincare Science</span>
    </p>
    """, unsafe_allow_html=True)
    
    # Return empty dict - filters will be rendered in main area
    return {}
