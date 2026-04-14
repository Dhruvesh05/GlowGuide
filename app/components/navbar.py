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
    
    col_logo, col_nav = st.columns([1, 3])
    
    with col_logo:
        st.markdown(
            '<p style="font-size:20px;font-weight:700;color:#6366F1;margin:0;padding:8px 0;">✦ GlowGuide</p>',
            unsafe_allow_html=True
        )
    
    with col_nav:
        nav_cols = st.columns(len(pages))
        for i, page in enumerate(pages):
            with nav_cols[i]:
                if st.button(page, use_container_width=True,
                            type="primary" if st.session_state["active_page"] == page else "secondary"):
                    st.session_state["active_page"] = page
                    st.rerun()
    
    st.divider()
    return st.session_state["active_page"]
