# -*- coding: utf-8 -*-
"""GlowGuide - Smart Skincare Recommender with Minimal Color Theme"""

import sys
from pathlib import Path

# Set up path for imports
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Import utilities
from app.utils import get_combined_recommendations
from app.utils.products import get_product_link
from app.components import (
    display_recommendations_grid,
    display_explainability_breakdown,
    display_combined_recommendations,
    display_ml_performance_metrics,
    display_eda_dashboard,
    display_visualization_selector
)

# Import ML backend functions
from app.utils.integration import generate_full_recommendation
from app.utils.model_loader import ModelLoader
from app.utils.routine_builder import (
    generate_personalized_routine,
    generate_routine_insights
)

# ========== PAGE CONFIG ==========
logo_path = Path(__file__).parent / "assets" / "logo.png"

# Encode logo as base64 data URI so it renders correctly over HTTP
import base64 as _b64
try:
    with open(logo_path, "rb") as _f:
        _logo_b64 = _b64.b64encode(_f.read()).decode()
    LOGO_DATA_URI = f"data:image/png;base64,{_logo_b64}"
except Exception:
    LOGO_DATA_URI = ""  # graceful fallback if file missing

st.set_page_config(
    page_title="GlowGuide - Skincare Assistant",
    page_icon=str(logo_path),
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== FILE PATH VALIDATION ==========
def verify_required_files():
    """
    Verify that all required data and model files exist.
    Uses relative paths for Streamlit Cloud compatibility.
    
    Files required:
    - data/celestia_clean.csv
    - data/product.csv
    - data/remedies.csv
    - models/knn_model.pkl
    - models/kmeans_model.pkl
    - models/le_skin.pkl, le_sens.pkl, le_concern.pkl, le_target.pkl
    
    Deployment: Works on both local and Streamlit Cloud.
    GitHub: All files are tracked (no .gitignore blocking).
    """
    base_dir = Path(__file__).parent.parent
    
    # Check data files
    data_files = [
        "celestia_clean.csv",
        "product.csv",
        "remedies.csv"
    ]
    
    # Check model files
    model_files = [
        "knn_model.pkl",
        "kmeans_model.pkl",
        "le_skin.pkl",
        "le_sens.pkl",
        "le_concern.pkl",
        "le_target.pkl"
    ]
    
    missing_data = []
    for f in data_files:
        path = base_dir / "data" / f
        if not path.exists():
            missing_data.append(f"data/{f}")
    
    missing_models = []
    for f in model_files:
        path = base_dir / "models" / f
        if not path.exists():
            missing_models.append(f"models/{f}")
    
    if missing_data or missing_models:
        error_msg = "Missing Required Files:\n"
        if missing_data:
            error_msg += f"\nData files: {', '.join(missing_data)}"
        if missing_models:
            error_msg += f"\nModel files: {', '.join(missing_models)}"
        error_msg += "\n\nTo fix:\n"
        error_msg += "1. Ensure files exist in GitHub repo\n"
        error_msg += "2. Run: git add data/ models/\n"
        error_msg += "3. Run: git commit -m 'Add data and models'\n"
        error_msg += "4. Run: git push\n"
        error_msg += "5. Redeploy Streamlit Cloud app\n"
        return False, error_msg
    
    return True, "All required files found"

# ========== LOAD ML MODELS (CACHED) ==========
@st.cache_resource
def load_ml_models():
    """Load all pre-trained ML models and encoders once (cached)."""
    # Verify files exist first
    files_ok, status_msg = verify_required_files()
    if not files_ok:
        st.error(status_msg)
        return None
    
    try:
        model_loader = ModelLoader()
        model_loader.load_all()  # ✅ LOAD ALL MODELS FROM DISK
        if not model_loader.is_ready():
            raise Exception("Failed to load all required models")
        return model_loader
    except Exception as e:
        st.error(f"Error loading models: {e}")
        st.info("💡 Tip: Ensure models/ folder has all .pkl files")
        return None

model_loader = load_ml_models()

# ========== SMOOTH SCROLL + SCROLL-REVEAL ANIMATION (JS) ==========
st.markdown("""
<script>
(function() {
  // Wait until Streamlit has finished rendering
  function initScrollReveal() {
    var style = document.createElement('style');
    style.textContent = `
      .reveal-section {
        opacity: 0;
        transform: translateY(28px);
        transition: opacity 0.55s cubic-bezier(0.4,0,0.2,1),
                    transform 0.55s cubic-bezier(0.4,0,0.2,1);
      }
      .reveal-section.is-visible {
        opacity: 1;
        transform: translateY(0);
      }
    `;
    document.head.appendChild(style);

    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
        }
      });
    }, { threshold: 0.08 });

    function tagAndObserve() {
      var containers = document.querySelectorAll(
        '.element-container, [data-testid="stMarkdownContainer"], [data-testid="metric-container"], [data-testid="stExpander"]'
      );
      containers.forEach(function(el) {
        if (!el.classList.contains('reveal-section')) {
          el.classList.add('reveal-section');
          observer.observe(el);
        }
      });
    }

    // Run once and also watch for Streamlit re-renders
    tagAndObserve();
    var mutObs = new MutationObserver(tagAndObserve);
    mutObs.observe(document.body, { childList: true, subtree: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initScrollReveal);
  } else {
    initScrollReveal();
  }
})();
</script>
""", unsafe_allow_html=True)

# ========== CUSTOM CSS - PROFESSIONAL DARK/LIGHT MODE ==========
# NOTE: Streamlit sets [data-theme="dark"] on <html>, NOT prefers-color-scheme.
# We MUST use that attribute selector for dark mode to actually work.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&family=Space+Grotesk:wght@300..700&display=swap');

/* ---- CSS custom properties for light/dark theming ---- */
/* Streamlit sets [data-theme="dark"] on <html> — NOT prefers-color-scheme */
:root {
    --fg:           #111111;
    --fg-muted:     #6b7280;
    --bg-card:      #ffffff;
    --bg-card-alt:  #f8f7ff;
    --border:       #e5e0ff;
    --border-strong:#c4b5fd;
    /* Brand accent — solid, minimal */
    --accent:       #7c3aed;
    --accent-2:     #db2777;
    --accent-light: #ede9fe;
    --btn-bg:       #111111;
    --btn-hover:    #2d2d2d;
    --tab-active-bg: #111111;
    --shadow-sm:    0 2px 8px rgba(124,58,237,0.10);
    --shadow-md:    0 8px 24px rgba(124,58,237,0.18);
    --shadow-lg:    0 16px 40px rgba(124,58,237,0.22);
    scroll-behavior: smooth;
}

[data-theme="dark"] {
    --fg:           #f3f4f6;
    --fg-muted:     #9ca3af;
    --bg-card:      #1e1b2e;
    --bg-card-alt:  #13111f;
    --border:       #312d4e;
    --border-strong:#4c4870;
    --accent:       #a78bfa;
    --accent-2:     #f472b6;
    --accent-light: #2e1065;
    --btn-bg:       #f3f4f6;
    --btn-hover:    #e5e7eb;
    --tab-active-bg: #f3f4f6;
    --shadow-sm:    0 2px 8px rgba(0,0,0,0.4);
    --shadow-md:    0 8px 24px rgba(0,0,0,0.5);
    --shadow-lg:    0 16px 40px rgba(0,0,0,0.6);
}

/* Global smooth scroll */
html {
    scroll-behavior: smooth;
}

/* Reduce cascade thrash — only transition specific props, not `all` */
*, *::before, *::after {
    font-family: 'DM Sans', sans-serif;
    box-sizing: border-box;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ---------- CHART ENTRY ANIMATIONS ---------- */
@keyframes chartBarRise {
    0%   { opacity: 0; transform: scaleY(0); }
    60%  { opacity: 1; }
    100% { opacity: 1; transform: scaleY(1); }
}
@keyframes chartFadeSlideUp {
    0%   { opacity: 0; transform: translateY(18px); }
    100% { opacity: 1; transform: translateY(0); }
}
@keyframes chartPieSpin {
    0%   { opacity: 0; transform: scale(0.7) rotate(-30deg); }
    100% { opacity: 1; transform: scale(1) rotate(0deg); }
}
/* Apply to entire Plotly chart SVG so it gracefully fades+rises in */
.js-plotly-plot .main-svg {
    animation: chartFadeSlideUp 0.65s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}
/* Bar rect elements */
.js-plotly-plot .bars .point > path,
.js-plotly-plot .barlayer .bars path {
    transform-origin: bottom center;
    animation: chartBarRise 0.7s cubic-bezier(0.34,1.56,0.64,1) both;
}
/* Pie / donut slices */
.js-plotly-plot .slice path {
    animation: chartPieSpin 0.8s cubic-bezier(0.34,1.56,0.64,1) both;
}
/* Stagger bars slightly for cascading feel */
.js-plotly-plot .bars .point:nth-child(1) path  { animation-delay: 0.05s; }
.js-plotly-plot .bars .point:nth-child(2) path  { animation-delay: 0.12s; }
.js-plotly-plot .bars .point:nth-child(3) path  { animation-delay: 0.19s; }
.js-plotly-plot .bars .point:nth-child(4) path  { animation-delay: 0.26s; }
.js-plotly-plot .bars .point:nth-child(5) path  { animation-delay: 0.33s; }

/* ---------- MAIN BACKGROUND ---------- */
.main {
    background: var(--bg-card-alt);
}

/* ---------- TABS ---------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    border-bottom: 2px solid var(--border);
    background-color: transparent;
    padding-bottom: 10px;
}
.stTabs [data-baseweb="tab"] {
    padding: 12px 22px;
    font-weight: 600;
    font-size: 14px;
    font-family: 'Space Grotesk', sans-serif;
    border-radius: 10px;
    color: var(--fg-muted);
    background-color: transparent;
    border: 1.5px solid transparent;
    transition: color 0.2s ease, background 0.2s ease, border-color 0.2s ease;
    letter-spacing: 0.2px;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--fg);
    background-color: var(--bg-card);
    border-color: var(--border);
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: #ffffff !important;
    background: var(--tab-active-bg);
    border-color: transparent;
    font-weight: 700;
    box-shadow: var(--shadow-md);
}
[data-theme="dark"] .stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: #ffffff !important;
}

/* ---------- BUTTONS — simple solid ---------- */
.stButton > button {
    background: var(--btn-bg) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    height: 50px !important;
    font-weight: 700 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 15px !important;
    letter-spacing: 0.4px !important;
    box-shadow: var(--shadow-sm) !important;
    transition: transform 0.22s ease, box-shadow 0.22s ease, background 0.2s ease !important;
}
.stButton > button:hover {
    background: var(--btn-hover) !important;
    transform: translateY(-3px) !important;
    box-shadow: var(--shadow-md) !important;
}
.stButton > button:active {
    transform: translateY(-1px) !important;
    box-shadow: var(--shadow-sm) !important;
}
[data-theme="dark"] .stButton > button {
    color: #111111 !important;
}

/* ---------- TYPOGRAPHY ---------- */
h1, h2, h3 {
    color: var(--fg);
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: -0.6px;
}
h1 {
    text-align: center;
    margin-bottom: 16px;
    font-size: 46px;
    font-weight: 800;
    animation: fadeIn 0.6s ease-out;
}
h2 {
    font-size: 32px;
    margin-top: 28px;
    margin-bottom: 18px;
    font-weight: 700;
    animation: slideUp 0.45s ease-out;
}
h3 {
    font-size: 22px;
    margin-top: 18px;
    margin-bottom: 14px;
    font-weight: 600;
}
p {
    color: var(--fg-muted);
    line-height: 1.8;
    font-size: 15px;
}

/* ---------- INPUTS ---------- */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    border: 1.5px solid var(--border-strong) !important;
    border-radius: 10px !important;
    font-size: 14px !important;
    padding: 12px 16px !important;
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg-card) !important;
    color: var(--fg) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
}

/* ---------- LABELS / CHECKBOXES / SLIDERS / RADIO ---------- */
.stSlider label,
.stCheckbox label,
.stRadio label,
.stMultiSelect label,
.stSelectbox label {
    font-weight: 500;
    color: var(--fg);
    font-family: 'DM Sans', sans-serif;
}

/* ---------- METRIC CARDS ---------- */
.metric-card {
    background: var(--bg-card);
    padding: 24px;
    border-radius: 14px;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border);
    transition: box-shadow 0.3s ease, transform 0.3s ease;
    animation: slideUp 0.5s ease-out;
}
.metric-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-4px);
}

/* ---------- PRODUCT CARDS ---------- */
.product-card {
    background: var(--bg-card);
    padding: 20px;
    border-radius: 14px;
    margin: 12px 0;
    border: 1.5px solid var(--border);
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.3s ease, transform 0.3s ease, border-color 0.3s ease;
    animation: slideUp 0.5s ease-out;
}
.product-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-5px);
    border-color: var(--border-strong);
}

/* ---------- PREMIUM CARD ---------- */
.premium-card {
    background: var(--bg-card);
    padding: 26px;
    border-radius: 16px;
    border: 1.5px solid var(--border);
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.3s ease, transform 0.3s ease;
    margin: 14px 0;
}
.premium-card:hover {
    box-shadow: var(--shadow-md);
    border-color: var(--border-strong);
    transform: translateY(-2px);
}

/* ---------- INGREDIENT TAGS ---------- */
.ingredient-tag {
    display: inline-block;
    background: var(--bg-card);
    color: var(--fg);
    padding: 10px 16px;
    border-radius: 24px;
    margin: 5px 5px 5px 0;
    font-size: 13px;
    font-weight: 600;
    border: 1.5px solid var(--border-strong);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: default;
    box-shadow: var(--shadow-sm);
}
.ingredient-tag:hover {
    border-color: var(--fg-muted);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}
.ingredient-tag.safe {
    background: #d1fae5;
    color: #065f46;
    border-color: #6ee7b7;
}
[data-theme="dark"] .ingredient-tag.safe {
    background: #064e3b;
    color: #a7f3d0;
    border-color: #065f46;
}
.ingredient-tag.active {
    background: #ede9fe;
    color: #4c1d95;
    border-color: #c4b5fd;
}
[data-theme="dark"] .ingredient-tag.active {
    background: #2e1065;
    color: #ddd6fe;
    border-color: #6d28d9;
}
.ingredient-tag.warning {
    background: #fef9c3;
    color: #78350f;
    border-color: #fde68a;
}
[data-theme="dark"] .ingredient-tag.warning {
    background: #451a03;
    color: #fde68a;
    border-color: #92400e;
}

/* ---------- BADGES ---------- */
.success-badge {
    background: #ecfdf5;
    color: #065f46;
    padding: 18px 22px;
    border-radius: 12px;
    margin: 14px 0;
    font-weight: 600;
    border: 1.5px solid #6ee7b7;
    animation: slideInLeft 0.5s ease-out;
    box-shadow: 0 4px 12px rgba(16,185,129,0.1);
}
.info-badge {
    background: #eff6ff;
    color: #1e40af;
    padding: 18px 22px;
    border-radius: 12px;
    margin: 14px 0;
    font-weight: 600;
    border: 1.5px solid #93c5fd;
    animation: slideInLeft 0.5s ease-out 0.1s both;
    box-shadow: 0 4px 12px rgba(59,130,246,0.1);
}
.warning-badge {
    background: #fefce8;
    color: #78350f;
    padding: 18px 22px;
    border-radius: 12px;
    margin: 14px 0;
    font-weight: 600;
    border: 1.5px solid #fde68a;
    animation: slideInLeft 0.5s ease-out 0.2s both;
    box-shadow: 0 4px 12px rgba(202,138,4,0.1);
}
.error-badge {
    background: #fef2f2;
    color: #7f1d1d;
    padding: 18px 22px;
    border-radius: 12px;
    margin: 14px 0;
    font-weight: 600;
    border: 1.5px solid #fca5a5;
    animation: slideInLeft 0.5s ease-out 0.3s both;
    box-shadow: 0 4px 12px rgba(239,68,68,0.1);
}
[data-theme="dark"] .success-badge { background: #064e3b; color: #a7f3d0; border-color: #065f46; }
[data-theme="dark"] .info-badge    { background: #1e3a8a; color: #bfdbfe; border-color: #1e40af; }
[data-theme="dark"] .warning-badge { background: #451a03; color: #fde68a; border-color: #92400e; }
[data-theme="dark"] .error-badge   { background: #450a0a; color: #fca5a5; border-color: #7f1d1d; }

/* ---------- DIVIDER ---------- */
.divider {
    margin: 28px 0;
    border-top: 1.5px solid var(--border);
    opacity: 0.9;
}

/* ---------- SIDEBAR ---------- */
.sidebar-header {
    font-size: 17px;
    font-weight: 700;
    color: var(--fg);
    font-family: 'Space Grotesk', sans-serif;
    margin-bottom: 14px;
    padding-bottom: 12px;
    border-bottom: 2px solid var(--fg);
    letter-spacing: -0.3px;
}
[data-theme="dark"] .sidebar-glowguide { border-bottom-color: var(--border); }

/* ---------- TABLE / DATAFRAME ---------- */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border);
}

/* ---------- EXPANDER ---------- */
.streamlit-expanderHeader {
    background-color: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    font-weight: 600;
    color: var(--fg);
    transition: background 0.2s ease;
}
.streamlit-expanderHeader:hover {
    background-color: var(--bg-card-alt);
    border-color: var(--border-strong);
}

/* ---------- PLOTLY CHART CONTAINERS ---------- */
.js-plotly-plot .plotly {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ========== TITLE & SUBTITLE ==========
st.markdown(f"""
<style>
.glowguide-header {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 18px;
    margin-bottom: 8px;
    animation: fadeIn 0.65s ease-out;
    padding: 24px 0 8px;
}}
.glowguide-logo {{
    width: 72px;
    height: 72px;
    object-fit: contain;
    background: transparent;
}}
.glowguide-title {{
    font-size: 52px;
    font-weight: 900;
    margin: 0;
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: -1.2px;
    color: var(--fg, #111111);
    line-height: 1;
}}
.glowguide-subtitle {{
    text-align: center;
    font-size: 15px;
    margin: 0 auto 32px;
    font-weight: 500;
    letter-spacing: 0.3px;
    color: var(--fg-muted, #6b7280);
    max-width: 480px;
}}
.glowguide-badge {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 28px;
    gap: 6px;
}}
.glowguide-badge span {{
    display: inline-block;
    background: transparent;
    font-size: 12px;
    font-weight: 700;
    padding: 5px 16px;
    border-radius: 999px;
    border: 1.5px solid var(--accent, #7c3aed);
    color: var(--accent, #7c3aed);
    letter-spacing: 0.6px;
    font-family: 'Space Grotesk', sans-serif;
    transition: background 0.2s ease;
}}
.glowguide-badge span:hover {{
    background: var(--accent-light, #ede9fe);
}}
</style>

<div class="glowguide-header">
    <img src="{LOGO_DATA_URI}" class="glowguide-logo" alt="GlowGuide Logo">
    <h1 class="glowguide-title">GlowGuide</h1>
</div>
<p class="glowguide-subtitle">Find the perfect skincare products based on your unique skin profile</p>
<div class="glowguide-badge">
    <span>AI-Powered</span>
    <span>Skincare Intelligence</span>
    <span>Personalized</span>
</div>
""", unsafe_allow_html=True)

# ========== SIDEBAR - USER PROFILE ==========
with st.sidebar:
    # Unified GlowGuide Header using base64 logo
    st.markdown(f"""
    <style>
    .sidebar-glowguide {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 11px;
        padding: 8px 0 20px;
        margin-bottom: 20px;
        border-bottom: 1.5px solid var(--border, #e5e7eb);
    }}
    .sidebar-glowguide-logo {{
        width: 40px;
        height: 40px;
        object-fit: contain;
        background: transparent;
    }}
    .sidebar-glowguide-title {{
        font-size: 22px;
        font-weight: 800;
        margin: 0;
        font-family: 'Space Grotesk', sans-serif;
        color: var(--fg, #111111);
        letter-spacing: -0.5px;
    }}
    .sidebar-section-label {{
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: var(--fg-muted, #6b7280);
        margin: 20px 0 10px;
        padding-bottom: 6px;
        border-bottom: 1px solid var(--border, #e5e7eb);
    }}
    </style>
    <div class="sidebar-glowguide">
        <img src="{LOGO_DATA_URI}" class="sidebar-glowguide-logo" alt="GlowGuide">
        <h2 class="sidebar-glowguide-title">GlowGuide</h2>
    </div>
    <p style="text-align:center; font-size:11px; color:var(--fg-muted,#9ca3af); margin:-8px 0 4px; font-weight:600; letter-spacing:0.5px;">SKINCARE INTELLIGENCE</p>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("<p class='sidebar-section-label'>Your Profile</p>", unsafe_allow_html=True)
    
    # ML Backend compatible skin type selector
    skin_type = st.selectbox(
        "Skin Type",
        ["Combination", "Dry", "Normal", "Oily"],
        key="sidebar_skin_type_main"
    )
    
    # Sensitivity level for ML model
    sensitivity = st.radio(
        "Skin Sensitivity",
        ["No", "Yes"],
        horizontal=True,
        key="sidebar_sensitivity_main"
    )
    
    # Primary skin concern for ML model (single selection for prediction)
    primary_concern = st.selectbox(
        "Primary Skin Concern",
        ["Acne", "Dark Circles", "Dark Spots", "Dullness", "Hyperpigmentation", 
         "Open Pores", "Redness", "Sun Tan", "Whiteheads/Blackheads", "Wrinkles"],
        key="sidebar_concern_main"
    )
    
    # Additional concerns (for reference)
    skin_concerns = st.multiselect(
        "Additional Concerns (Optional)",
        ["Dryness", "Oiliness", "Aging", "Sensitivity", "Texture"],
        key="sidebar_concerns_main"
    )
    
    age = st.slider(
        "Age",
        13, 80, 25,
        key="sidebar_age_main"
    )
    
    st.divider()
    
    st.markdown("<h3 style='font-size: 16px; font-weight: 700; margin: 16px 0 12px 0; color: #1f2937;'>Budget & Preferences</h3>", unsafe_allow_html=True)
    
    budget_min, budget_max = st.slider(
        "Budget Range",
        0, 10000, (500, 3000),
        key="sidebar_budget_main"
    )
    
    st.divider()
    
    st.markdown("<p class='sidebar-section-label'>Preferences</p>", unsafe_allow_html=True)
    
    alcohol_free = st.checkbox("Alcohol-Free Only", value=False, key="sidebar_alcohol_main")
    fragrance_free = st.checkbox("Fragrance-Free Only", value=False, key="sidebar_fragrance_main")
    vegan = st.checkbox("Vegan Only", value=False, key="sidebar_vegan_main")
    cruelty_free = st.checkbox("Cruelty-Free Only", value=False, key="sidebar_cruelty_main")

# ========== MAIN CONTENT - TABBED LAYOUT ==========
tab1, tab2, tab3, tab_insights = st.tabs(["Product Search", "Ingredient Analyzer", "Routine Builder", "Insights"])

# ========== TAB 1: PRODUCT SEARCH ==========
with tab1:
    st.markdown("## Find Your Perfect Product")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        product_name = st.text_input(
            "Product Name",
            placeholder="e.g., Moisturizing Cream, Vitamin C Serum",
            key="tab1_product_name"
        )
    with col2:
        brand = st.text_input(
            "Brand (Optional)",
            placeholder="e.g., CeraVe, Neutrogena",
            key="tab1_brand"
        )
    
    col3, col4 = st.columns([1, 1])
    with col3:
        product_type = st.selectbox(
            "Product Type",
            ["Cleanser", "Moisturizer", "Serum", "Mask", "Sunscreen", "Toner", "Eye Cream"],
            key="tab1_type"
        )
    with col4:
        st.write("")
        st.write("")
    
    # Filters
    st.markdown("### Additional Filters")
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        filter_alcohol = st.checkbox("Alcohol-Free", key="tab1_filter_alcohol")
    with f2:
        filter_fragrance = st.checkbox("Fragrance-Free", key="tab1_filter_fragrance")
    with f3:
        filter_vegan = st.checkbox("Vegan", key="tab1_filter_vegan")
    with f4:
        filter_cruelty = st.checkbox("Cruelty-Free", key="tab1_filter_cruelty")
    
    search_btn = st.button("Get Ingredient Recommendations", use_container_width=True, key="tab1_search_btn")
    
    if search_btn:
        # ========== BLOCK 11: ML BACKEND INTEGRATION ==========
        # Call the master integration function that combines:
        # - Block 8: Predictions (ingredient + cluster)
        # - Block 9: Products (top 3)
        # - Block 10: Remedies (top 2)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("## Your Personalized Skincare Recommendation")
        
        with st.spinner("Analyzing your skin profile and finding recommendations..."):
            result = generate_full_recommendation(
                skin=skin_type,
                sensitivity=sensitivity,
                concern=primary_concern,
                model_loader=model_loader
            )
        
        if result and result['success']:
            # ===== DISPLAY INGREDIENT PREDICTION =====
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); 
                            padding: 20px; border-radius: 12px; border: 1.5px solid #d1d5db; text-align: center;'>
                    <p style='color: #666666; font-size: 14px; margin: 0; font-weight: 500;'>RECOMMENDED INGREDIENT</p>
                    <p style='color: #000000; font-size: 24px; margin: 10px 0; font-weight: 700;'>{}</p>
                </div>
                """.format(result['ingredient']), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                            padding: 20px; border-radius: 12px; border: 1.5px solid #60a5fa; text-align: center;'>
                    <p style='color: #0c2d6b; font-size: 14px; margin: 0; font-weight: 500;'>YOUR SKIN CLUSTER</p>
                    <p style='color: #0c2d6b; font-size: 22px; margin: 10px 0; font-weight: 700;'>{}</p>
                </div>
                """.format(result['cluster_label']), unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); 
                            padding: 20px; border-radius: 12px; border: 1.5px solid #6ee7b7; text-align: center;'>
                    <p style='color: #065f46; font-size: 14px; margin: 0; font-weight: 500;'>STATUS</p>
                    <p style='color: #065f46; font-size: 22px; margin: 10px 0; font-weight: 700;'>Ready</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            
            # ===== DISPLAY PRODUCTS =====
            # ✅ STEP 3-4: DYNAMIC PRODUCT CARDS WITH SEARCH LINKS & IMAGES
            products = result.get('products', [])
            if products and len(products) > 0:
                st.markdown("### Top Products with This Ingredient")
                
                # Create clickable product cards in a grid
                # Google icon SVG (official colours)
                GOOGLE_ICON = '''
                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 48 48">
                  <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
                  <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
                  <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
                  <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.18 1.48-4.97 2.36-8.16 2.36-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
                </svg>'''

                cols = st.columns(min(len(products[:3]), 3))
                for idx, product in enumerate(products[:3]):
                    with cols[idx]:
                        product_name = product.get('product_name', 'Unknown Product')
                        price        = product.get('price', 0)
                        search_link  = get_product_link(product_name)

                        st.markdown(f"""
                        <a href="{search_link}" target="_blank" style="text-decoration:none;">
                          <div style="
                            border: 1.5px solid var(--border, #e5e0ff);
                            border-radius: 14px;
                            padding: 20px 16px;
                            background: var(--bg-card, #fff);
                            box-shadow: 0 2px 10px rgba(124,58,237,0.07);
                            text-align: center;
                            transition: box-shadow 0.2s ease, transform 0.2s ease;
                          ">
                            <div style="margin-bottom:12px;">{GOOGLE_ICON}</div>
                            <p style="margin:0 0 6px;font-weight:700;font-size:14px;color:var(--fg,#111);line-height:1.4;">{product_name}</p>
                            <p style="margin:0 0 10px;font-size:13px;color:var(--fg-muted,#6b7280);">&#8377;{price:.0f}</p>
                            <span style="font-size:12px;font-weight:600;color:#4285F4;">Search on Google &rarr;</span>
                          </div>
                        </a>
                        """, unsafe_allow_html=True)
            else:
                # ✅ GRACEFUL FALLBACK MESSAGE
                st.info(f"Limited product data available for **{result.get('ingredient', 'this ingredient')}**. "
                        "Consider searching for alternative products with similar key ingredients.")
            
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            
            # ===== DISPLAY REMEDIES =====
            # ✅ STEP 6: OUTPUT HANDLING
            remedies = result.get('remedies', [])
            if remedies and len(remedies) > 0:
                st.markdown("### Home Remedies for Your Skin Concern")
                
                for idx, remedy in enumerate(remedies, 1):
                    with st.expander(f"Remedy {idx}: {remedy.get('Problem', 'Unknown')}", expanded=(idx == 1)):
                        st.markdown(f"**Problem:** {remedy.get('Problem', 'N/A')}")
                        st.markdown(f"**Category:** {remedy.get('Category', 'N/A')}")
                        st.markdown(f"**Ingredients:** {remedy.get('Ingredients', 'N/A')}")
                        st.markdown(f"**Usage:** {remedy.get('Usage', 'N/A')}")
                        st.markdown(f"**Frequency:** {remedy.get('Frequency', 'N/A')}")
            else:
                # ✅ GRACEFUL FALLBACK MESSAGE
                st.info(f"Limited remedy data available for **{result.get('ingredient', 'this ingredient')}**. "
                        "Consult with a dermatologist for personalized home remedy recommendations.")
            
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            
            # Summary
            st.markdown("<div class='success-badge'>Complete recommendation generated. Share with your dermatologist for personalized advice.</div>", unsafe_allow_html=True)
        
        else:
            error_msg = result.get('error', 'Unknown error') if result else 'Failed to generate recommendation'
            st.error(f"Could not generate recommendation: {error_msg}")
            st.info("Please check your input values and try again.")

# ========== TAB 2: INGREDIENT ANALYZER ==========
with tab2:
    st.markdown("## Analyze Your Ingredients")
    
    ingredients_text = st.text_area(
        "Paste ingredient list",
        placeholder="Paste the ingredient list from your product label here...",
        height=150,
        key="tab2_ingredients"
    )
    
    allergy_input = st.text_input(
        "Known Allergies/Sensitivities",
        placeholder="e.g., Parabens, Sulfates, Essential Oils",
        key="tab2_allergies"
    )
    
    analyze_btn = st.button("Analyze Ingredients", use_container_width=True, key="tab2_analyze_btn")
    
    if analyze_btn and ingredients_text:
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("## Analysis Results")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Safe Ingredients", "12", "+2")
        with col2:
            st.metric("Potential Irritants", "2", "-1")
        with col3:
            st.metric("Active Ingredients", "4", "=")
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### Safe Ingredients")
        st.markdown("""
        <div>
            <span class='ingredient-tag safe'>Glycerin</span>
            <span class='ingredient-tag safe'>Hyaluronic Acid</span>
            <span class='ingredient-tag safe'>Niacinamide</span>
            <span class='ingredient-tag safe'>Panthenol</span>
            <span class='ingredient-tag safe'>Ceramide</span>
            <span class='ingredient-tag safe'>Aloe Vera</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Active Ingredients (Beneficial)")
        st.markdown("""
        <div>
            <span class='ingredient-tag active'>Vitamin C</span>
            <span class='ingredient-tag active'>Retinol</span>
            <span class='ingredient-tag active'>AHA</span>
            <span class='ingredient-tag active'>BHA</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Potential Irritants")
        st.markdown("""
        <div class='warning-badge'>
            <strong>Alcohol Denat</strong> - May cause dryness in sensitive skin
        </div>
        <div class='warning-badge'>
            <strong>Fragrance</strong> - Can trigger sensitivity reactions
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### Ingredient Safety Score")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=82,
            delta={'reference': 60, 'increasing': {'color': '#10b981'}},
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Safety Score", 'font': {'size': 18}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#9ca3af'},
                'bar': {'color': '#6366f1', 'thickness': 0.25},
                'bgcolor': 'rgba(0,0,0,0)',
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 40],  'color': 'rgba(239,68,68,0.15)'},
                    {'range': [40, 70], 'color': 'rgba(251,191,36,0.15)'},
                    {'range': [70, 100],'color': 'rgba(16,185,129,0.15)'}
                ],
                'threshold': {
                    'line': {'color': '#6366f1', 'width': 3},
                    'thickness': 0.75,
                    'value': 82
                }
            }
        ))
        fig_gauge.update_layout(
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#6b7280'),
            transition={'duration': 700, 'easing': 'cubic-in-out'}
        )
        st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': True, 'scrollZoom': True, 'displaylogo': False, 'modeBarButtonsToAdd': ['zoom2d','pan2d','zoomIn2d','zoomOut2d','autoScale2d','resetScale2d','toImage']})
        
        st.markdown("<div class='success-badge'>Safe for your skin profile</div>", unsafe_allow_html=True)

# ========== TAB 3: ROUTINE BUILDER ==========
with tab3:
    st.markdown("## Your Personalized Skincare Routine")
    st.markdown("Based on your skin profile and ML analysis, we'll create a routine using trained dataset recommendations.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        routine_type = st.radio(
            "Choose routine time",
            ["Morning Routine", "Night Routine"],
            horizontal=True,
            key="tab3_routine_type"
        )
    
    with col2:
        routine_focus = st.selectbox(
            "Focus Area",
            ["Hydration", "Anti-aging", "Acne Control", "Brightening", "Sensitive Care"],
            key="tab3_focus"
        )
    
    generate_btn = st.button("Generate Personalized Routine", use_container_width=True, key="tab3_generate_btn")
    
    if generate_btn:
        with st.spinner("Analyzing your profile and generating personalized routine..."):
            # Step 1: Get ML prediction using user's profile
            ml_result = generate_full_recommendation(
                skin=skin_type,
                sensitivity=sensitivity,
                concern=primary_concern,
                model_loader=model_loader
            )
            
            if ml_result and ml_result['success']:
                # Step 2: Generate routine based on ML prediction
                user_profile = {
                    'skin_type': skin_type,
                    'sensitivity': sensitivity,
                    'primary_concern': primary_concern,
                    'age': age,
                    'skin_concerns': skin_concerns,
                    'budget_min': budget_min
                }
                
                routine_type_label = "Morning" if "Morning" in routine_type else "Night"
                
                routine = generate_personalized_routine(
                    user_profile=user_profile,
                    ml_prediction=ml_result,
                    routine_type=routine_type_label,
                    routine_focus=routine_focus
                )
                
                # Step 3: Generate detailed insights
                insights = generate_routine_insights(
                    user_profile=user_profile,
                    ml_prediction=ml_result,
                    routine=routine
                )
                
                if routine['success']:
                    # ===== DISPLAY ROUTINE OVERVIEW =====
                    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                    st.markdown(f"## Your {routine_type}")
                    
                    # Display routine summary cards
                    summary_col1, summary_col2, summary_col3 = st.columns(3)
                    
                    with summary_col1:
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                                    padding: 20px; border-radius: 12px; border: 1.5px solid #60a5fa; text-align: center;'>
                            <p style='color: #0c2d6b; font-size: 14px; margin: 0; font-weight: 500;'>RECOMMENDED INGREDIENT</p>
                            <p style='color: #0c2d6b; font-size: 24px; margin: 10px 0; font-weight: 700;'>{ml_result['ingredient']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with summary_col2:
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); 
                                    padding: 20px; border-radius: 12px; border: 1.5px solid #d1d5db; text-align: center;'>
                            <p style='color: #374151; font-size: 14px; margin: 0; font-weight: 500;'>ROUTINE LENGTH</p>
                            <p style='color: #111827; font-size: 24px; margin: 10px 0; font-weight: 700;'>{routine['total_time']} min</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with summary_col3:
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); 
                                    padding: 20px; border-radius: 12px; border: 1.5px solid #86efac; text-align: center;'>
                            <p style='color: #166534; font-size: 14px; margin: 0; font-weight: 500;'>SKIN TYPE</p>
                            <p style='color: #166534; font-size: 24px; margin: 10px 0; font-weight: 700;'>{skin_type}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                    
                    # ===== VISUALIZATION 1: ROUTINE TIMELINE =====
                    st.markdown("### Routine Timeline - Time Allocation per Step")
                    
                    timeline_data = []
                    for step in routine['steps']:
                        timeline_data.append({
                            'Step': f"{step['step_num']}. {step['product_type']}",
                            'Time': step['time'],
                            'Product': step['name'][:30]
                        })
                    
                    timeline_df = pd.DataFrame(timeline_data)
                    fig_timeline = px.bar(
                        timeline_df,
                        x='Time',
                        y='Step',
                        orientation='h',
                        title='Time Commitment per Step',
                        labels={'Time': 'Minutes', 'Step': 'Routine Step'},
                        color='Time',
                        color_continuous_scale=[[0,'#f9a8d4'],[0.5,'#a78bfa'],[1,'#7c3aed']],
                        text='Time'
                    )
                    fig_timeline.update_traces(textposition='auto')
                    fig_timeline.update_traces(
                        marker_line_width=0,
                        textfont=dict(size=12, color='white')
                    )
                    fig_timeline.update_layout(
                        height=320,
                        showlegend=False,
                        xaxis_title='Minutes',
                        yaxis_title='',
                        hovermode='y unified',
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#6b7280'),
                        xaxis=dict(showgrid=True, gridcolor='rgba(156,163,175,0.15)', zeroline=False),
                        yaxis=dict(showgrid=False),
                        transition={'duration': 600, 'easing': 'cubic-in-out'},
                        margin=dict(l=10, r=10, t=40, b=10)
                    )
                    st.plotly_chart(fig_timeline, use_container_width=True, config={'displayModeBar': True, 'scrollZoom': True, 'displaylogo': False, 'modeBarButtonsToAdd': ['zoom2d','pan2d','zoomIn2d','zoomOut2d','autoScale2d','resetScale2d','toImage']})
                    
                    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                    
                    # ===== DISPLAY ROUTINE STEPS TABLE =====
                    st.markdown("### Routine Steps (In Order)")
                    
                    routine_table_data = []
                    for step in routine['steps']:
                        routine_table_data.append({
                            'Step': f"{step['step_num']}. {step['product_type']}",
                            'Product': step['name'],
                            'Time (min)': step['time'],
                            'Benefit': step['benefit']
                        })
                    
                    routine_df = pd.DataFrame(routine_table_data)
                    st.dataframe(routine_df, use_container_width=True, hide_index=True)
                    
                    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                    
                    # ===== VISUALIZATION 2: PRODUCT BENEFITS DISTRIBUTION =====
                    st.markdown("### Skin Concern Coverage - How This Routine Addresses Your Needs")
                    
                    concern_mapping = {
                        'Acne': 0,
                        'Dark Circles': 0,
                        'Dark Spots': 0,
                        'Dullness': 0,
                        'Hyperpigmentation': 0,
                        'Open Pores': 0,
                        'Redness': 0,
                        'Sun Tan': 0,
                        'Whiteheads/Blackheads': 0,
                        'Wrinkles': 0
                    }
                    
                    benefit_keywords = {
                        'Acne': ['clarifying', 'breakout', 'acne', 'pore', 'control'],
                        'Dark Circles': ['dark circle', 'eye', 'fine line'],
                        'Dark Spots': ['brightening', 'dark', 'spot', 'hyperpigmentation'],
                        'Dullness': ['brightening', 'glow', 'radiant'],
                        'Wrinkles': ['anti-aging', 'firming', 'collagen', 'fine line'],
                        'Redness': ['soothing', 'calming', 'sensitive'],
                    }
                    
                    for step in routine['steps']:
                        benefit_lower = step['benefit'].lower()
                        for concern, keywords in benefit_keywords.items():
                            if any(kw in benefit_lower for kw in keywords):
                                if concern in concern_mapping:
                                    concern_mapping[concern] += 1
                    
                    concern_data = pd.DataFrame([
                        {'Concern': k, 'Coverage': v} 
                        for k, v in concern_mapping.items() 
                        if v > 0
                    ])
                    
                    if len(concern_data) > 0:
                        fig_concerns = px.bar(
                            concern_data,
                            x='Concern',
                            y='Coverage',
                            title='Skin Concern Coverage by This Routine',
                            labels={'Coverage': 'Number of Steps Addressing'},
                            color='Coverage',
                            color_continuous_scale=[[0,'#fce7f3'],[0.5,'#c084fc'],[1,'#7c3aed']],
                            text='Coverage'
                        )
                        fig_concerns.update_traces(textposition='auto')
                        fig_concerns.update_traces(marker_line_width=0)
                        fig_concerns.update_layout(
                            height=360,
                            showlegend=False,
                            xaxis_tickangle=-30,
                            hovermode='x unified',
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#6b7280'),
                            xaxis=dict(showgrid=False, zeroline=False),
                            yaxis=dict(showgrid=True, gridcolor='rgba(156,163,175,0.15)', zeroline=False),
                            transition={'duration': 600, 'easing': 'cubic-in-out'},
                            margin=dict(l=10, r=10, t=40, b=10)
                        )
                        st.plotly_chart(fig_concerns, use_container_width=True, config={'displayModeBar': True, 'scrollZoom': True, 'displaylogo': False, 'modeBarButtonsToAdd': ['zoom2d','pan2d','zoomIn2d','zoomOut2d','autoScale2d','resetScale2d','toImage']})
                    
                    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                    
                    # ===== VISUALIZATION 3: ROUTINE COMPOSITION =====
                    st.markdown("### Routine Composition - Product Types Distribution")
                    
                    product_types = [step['product_type'] for step in routine['steps']]
                    product_type_counts = pd.Series(product_types).value_counts().reset_index()
                    product_type_counts.columns = ['Product Type', 'Count']
                    
                    fig_composition = px.pie(
                        product_type_counts,
                        names='Product Type',
                        values='Count',
                        title='Product Types in Your Routine',
                        color_discrete_sequence=['#6366f1', '#0ea5e9', '#10b981', '#f59e0b', '#ec4899'],
                        hole=0.4  # donut style
                    )
                    fig_composition.update_traces(
                        textposition='inside',
                        textinfo='percent+label',
                        marker=dict(line=dict(color='rgba(0,0,0,0)', width=0))
                    )
                    fig_composition.update_layout(
                        height=360,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#6b7280'),
                        transition={'duration': 600, 'easing': 'cubic-in-out'},
                        margin=dict(l=10, r=10, t=40, b=10),
                        showlegend=True,
                        legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5)
                    )
                    st.plotly_chart(fig_composition, use_container_width=True, config={'displayModeBar': True, 'scrollZoom': True, 'displaylogo': False, 'modeBarButtonsToAdd': ['zoom2d','pan2d','zoomIn2d','zoomOut2d','autoScale2d','resetScale2d','toImage']})
                    
                    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                    
                    # ===== DISPLAY DETAILED STEP BREAKDOWN =====
                    st.markdown("### Step-by-Step Breakdown")
                    
                    for step in routine['steps']:
                        with st.expander(
                            f"Step {step['step_num']}: {step['product_type']} - {step['name']}",
                            expanded=(step['step_num'] == 1)
                        ):
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.markdown(f"**Why This Product?**")
                                st.markdown(f"{step['reason']}")
                                st.markdown(f"\n**Key Benefit:** {step['benefit']}")
                            
                            with col2:
                                st.markdown(f"**Application Time:** {step['time']} minutes")
                                st.markdown(f"**Product Type:** {step['product_type']}")
                    
                    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                    
                    # ===== DISPLAY TIPS =====
                    st.markdown("### Tips for Better Results")
                    
                    tips_html = "<div class='info-badge'>"
                    for idx, tip in enumerate(routine['tips'], 1):
                        tips_html += f"<strong>Tip {idx}:</strong> {tip}<br><br>"
                    tips_html += "</div>"
                    
                    st.markdown(tips_html, unsafe_allow_html=True)
                    
                    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                    
                    # ===== VISUALIZATION 4: ML CONFIDENCE & PERSONALIZATION FACTORS =====
                    st.markdown("### Personalization Analysis - ML Model Insights")
                    
                    col_viz1, col_viz2 = st.columns(2)
                    
                    with col_viz1:
                        st.markdown("#### ML Model Confidence")
                        
                        confidence_data = pd.DataFrame({
                            'Metric': ['Ingredient Accuracy', 'Cluster Assignment', 'Overall Recommendation'],
                            'Score': [
                                ml_result.get('ingredient_confidence', 0),
                                ml_result.get('cluster_confidence', 0),
                                ml_result.get('overall_confidence', 0)
                            ]
                        })
                        
                        fig_confidence = px.bar(
                            confidence_data,
                            x='Score',
                            y='Metric',
                            orientation='h',
                            title='Model Performance Metrics',
                            color='Score',
                            color_continuous_scale=[[0,'#fce7f3'],[0.4,'#c084fc'],[1,'#7c3aed']],
                            text='Score'
                        )
                        fig_confidence.update_traces(
                            textposition='auto',
                            marker_line_width=0
                        )
                        fig_confidence.update_layout(
                            height=300,
                            showlegend=False,
                            xaxis_title='Confidence Score (%)',
                            yaxis_title='',
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#6b7280'),
                            xaxis=dict(showgrid=True, gridcolor='rgba(156,163,175,0.15)', zeroline=False),
                            yaxis=dict(showgrid=False),
                            transition={'duration': 600, 'easing': 'cubic-in-out'},
                            margin=dict(l=10, r=10, t=40, b=10)
                        )
                        st.plotly_chart(fig_confidence, use_container_width=True, config={'displayModeBar': True, 'scrollZoom': True, 'displaylogo': False, 'modeBarButtonsToAdd': ['zoom2d','pan2d','zoomIn2d','zoomOut2d','autoScale2d','resetScale2d','toImage']})
                    
                    with col_viz2:
                        st.markdown("#### Input Profile Summary")
                        
                        profile_metrics = {
                            'Skin Type': skin_type,
                            'Sensitivity': sensitivity,
                            'Primary Concern': primary_concern,
                            'Age': str(age),
                            'Skin Cluster': ml_result['cluster_label']
                        }
                        
                        profile_text = "<div style='padding: 15px; background: #f9fafb; border-radius: 8px; border: 1px solid #e5e7eb;'>"
                        for key, value in profile_metrics.items():
                            profile_text += f"<p style='margin: 8px 0;'><strong>{key}:</strong> {value}</p>"
                        profile_text += "</div>"
                        
                        st.markdown(profile_text, unsafe_allow_html=True)
                    
                    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                    
                    # ===== DISPLAY DETAILED INSIGHTS =====
                    st.markdown("### Routine Personalization Details")
                    
                    # Input Summary
                    with st.expander("Your Input Profile", expanded=True):
                        input_cols = st.columns(2)
                        with input_cols[0]:
                            st.markdown("**Skin Profile:**")
                            for key, value in insights['input_summary'].items():
                                st.markdown(f"• **{key.replace('_', ' ').title()}:** {value}")
                        
                        with input_cols[1]:
                            st.markdown("**ML Analysis:**")
                            for key, value in insights['ml_analysis'].items():
                                st.markdown(f"• **{key.replace('_', ' ').title()}:** {value}")
                    
                    # Personalization Factors
                    with st.expander("Personalization Factors", expanded=True):
                        for factor in insights['personalization_factors']:
                            st.markdown(f"{factor}")
                    
                    # Routine Rationale
                    with st.expander("Why This Routine?", expanded=True):
                        st.markdown(insights['routine_rationale'])
                    
                    # Effectiveness Timeline
                    with st.expander("Expected Results Timeline", expanded=False):
                        st.markdown(f"**You can expect to see changes in:** {insights['effectiveness_timeline']}")
                        st.markdown(
                            "\n**Note:** Consistency is key. Use this routine daily for best results. "
                            "Skin typically needs 4-6 weeks of consistent care to show visible improvements."
                        )
                    
                    # Key Insights
                    with st.expander("Key Insights & Data Points", expanded=True):
                        for insight in insights['key_insights']:
                            st.markdown(f"\n{insight}")
                    
                    st.markdown("<div class='success-badge'>Routine created successfully. Save this page for reference and start using your personalized routine today.</div>", unsafe_allow_html=True)
                
                else:
                    st.error(f"Failed to generate routine: {routine.get('error', 'Unknown error')}")
            else:
                st.error(f"Could not analyze your profile. Error: {ml_result.get('error', 'Unknown error') if ml_result else 'Model not loaded'}")

# ========== TAB 4: INSIGHTS (EDA DASHBOARD) ==========
with tab_insights:
    display_eda_dashboard()

# ========== FOOTER ==========
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown("""
<p style='text-align: center; color: #888888; font-size: 13px; margin-top: 24px;'>
    Made with care using Streamlit | GlowGuide v1.0
</p>
""", unsafe_allow_html=True)
