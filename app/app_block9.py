# -*- coding: utf-8 -*-
"""
GlowGuide - Smart Skincare Recommender
Block 9: Final Output UI Structure

A beginner-friendly skincare recommendation system that combines:
- Rule-based scoring (Block 1)
- Machine learning predictions (Block 4)
- Interactive data exploration (Block 6)
- High performance (Block 7 caching)
- Clean architecture (Block 8 coordinator)

Navigation:
- Home: Project overview and how it works
- Analyze My Skin: Main recommendation engine
- Insights: Data exploration and patterns
"""

import sys
from pathlib import Path

# Setup imports
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

import streamlit as st
import pandas as pd

# Import utilities
from app.utils import (
    get_combined_recommendations,  # Block 8: Orchestrator
    validate_sidebar_inputs,        # Input validation
    get_dataset_info,              # Dataset statistics
    get_model_status               # Model metrics
)

# Import UI components
from app.components import (
    display_combined_recommendations,      # Results display
    display_ml_performance_metrics,        # Model info
    display_eda_dashboard,                 # Data exploration
    display_explainability_breakdown       # Score details
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

# Set page config before any other Streamlit commands
logo_path = Path(__file__).parent / "assets" / "logo.png"
st.set_page_config(
    page_title="GlowGuide - Smart Skincare Recommender",
    page_icon="💆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM STYLING (CSS for beautiful UI)
# ============================================================================

st.markdown("""
<style>
/* Main background */
.main {
    background: linear-gradient(135deg, #ffffff 0%, #fafbfc 100%);
}

/* Typography */
h1 {
    color: #000000;
    font-size: 44px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 12px;
}

h2 {
    color: #000000;
    font-size: 32px;
    font-weight: 700;
    margin-top: 24px;
    margin-bottom: 18px;
}

h3 {
    color: #1f2937;
    font-size: 22px;
    font-weight: 600;
    margin-top: 18px;
}

p {
    color: #4b5563;
    line-height: 1.7;
    font-size: 15px;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
    color: white;
    border: none;
    border-radius: 8px;
    height: 48px;
    font-weight: 600;
    font-size: 15px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.12);
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 25px rgba(0, 0, 0, 0.18);
}

/* Input styling */
.stTextInput > div > div > input,
.stSelectbox > div > div > select,
.stSlider > div > div > div > input {
    border: 2px solid #e5e7eb !important;
    border-radius: 8px !important;
    padding: 12px !important;
    background-color: #fafbfc !important;
}

.stTextInput > div > div > input:focus,
.stSelectbox > div > div > select:focus {
    border-color: #000000 !important;
    background-color: #ffffff !important;
}

/* Cards and containers */
.metric-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

/* Badges */
.success-badge {
    background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
    color: #15803d;
    padding: 16px 20px;
    border-radius: 10px;
    border: 1px solid #86efac;
    margin: 14px 0;
    font-weight: 500;
}

.info-badge {
    background: linear-gradient(135deg, #eff6ff 0%, #f0f9ff 100%);
    color: #0c4a6e;
    padding: 16px 20px;
    border-radius: 10px;
    border: 1px solid #93c5fd;
    margin: 14px 0;
    font-weight: 500;
}

/* Divider */
.divider {
    margin: 28px 0;
    border-top: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# NAVIGATION - Main page selection
# ============================================================================

def create_navigation():
    """
    Create main navigation menu in sidebar.
    Returns the selected page.
    """
    st.sidebar.markdown("# 🎯 GlowGuide")
    st.sidebar.markdown("Smart Skincare Recommender")
    st.sidebar.markdown("---")
    
    # Navigation buttons
    page = st.sidebar.radio(
        "Navigate to:",
        ["🏠 Home", "🔬 Analyze My Skin", "📊 Insights"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ About")
    st.sidebar.markdown(
        "GlowGuide combines rule-based logic and machine learning "
        "to provide personalized skincare recommendations."
    )
    
    return page


# ============================================================================
# PAGE: HOME
# ============================================================================

def page_home():
    """
    Display the home/landing page with project overview.
    """
    # Hero section
    st.markdown("# 💆 Welcome to GlowGuide")
    st.markdown(
        "Your personalized skincare recommendation system powered by "
        "rule-based logic and machine learning"
    )
    
    st.markdown("---")
    
    # Key features section
    st.markdown("## ✨ Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📏 Intelligent Scoring
        - Rule-based algorithm
        - Considers skin type
        - Analyzes concerns
        - Age-personalized
        """)
    
    with col2:
        st.markdown("""
        ### 🧠 Machine Learning
        - K-Nearest Neighbors model
        - Learned patterns
        - Similar user matching
        - 72.5% training accuracy
        """)
    
    with col3:
        st.markdown("""
        ### 📊 Data Insights
        - Interactive dashboards
        - Pattern analysis
        - Ingredient trends
        - Market insights
        """)
    
    st.markdown("---")
    
    # How it works section
    st.markdown("## 🔄 How It Works")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        ### Step 1: Input
        Tell us about your skin:
        - Skin type
        - Concerns
        - Age
        - Preferences
        """)
    
    with col2:
        st.markdown("""
        ### Step 2: Analysis
        Two approaches analyze:
        - Rule-based scoring
        - ML prediction
        - Data patterns
        """)
    
    with col3:
        st.markdown("""
        ### Step 3: Recommend
        Get personalized:
        - Top ingredients
        - Confidence scores
        - Detailed reasoning
        """)
    
    with col4:
        st.markdown("""
        ### Step 4: Explore
        Understand better:
        - Score breakdown
        - Model details
        - Data patterns
        """)
    
    st.markdown("---")
    
    # Call to action
    st.markdown("## 🚀 Ready to Start?")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(
            "Click **Analyze My Skin** in the sidebar to get your "
            "personalized skincare recommendations!"
        )
        
        # Button to go to main page
        if st.button("👉 Analyze My Skin →", use_container_width=True):
            st.session_state.page = "🔬 Analyze My Skin"
            st.rerun()
    
    st.markdown("---")
    
    # Footer with quick stats
    st.markdown("## 📈 By The Numbers")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Training Samples", "50", "Real profiles")
    
    with col2:
        st.metric("Ingredients", "4", "Analyzed")
    
    with col3:
        st.metric("Skin Types", "4", "Supported")
    
    with col4:
        st.metric("ML Accuracy", "72.5%", "Training data")


# ============================================================================
# PAGE: ANALYZE MY SKIN (Main Feature)
# ============================================================================

def page_analyze():
    """
    Display the main analysis page with input and recommendations.
    This is the core feature of GlowGuide.
    """
    
    # ========================================================================
    # SIDEBAR: USER INPUT COLLECTION
    # ========================================================================
    
    st.sidebar.markdown("## 📋 Your Profile")
    
    # Skin Type Input
    skin_type = st.sidebar.selectbox(
        "🧴 Skin Type",
        ["Oily", "Dry", "Combination", "Sensitive"],
        help="Choose the skin type that best describes your skin"
    )
    
    # Skin Concerns Input
    st.sidebar.markdown("### 😟 Skin Concerns")
    skin_concerns = []
    if st.sidebar.checkbox("Acne", key="concern_acne"):
        skin_concerns.append("Acne")
    if st.sidebar.checkbox("Dryness", key="concern_dryness"):
        skin_concerns.append("Dryness")
    if st.sidebar.checkbox("Sensitivity", key="concern_sensitivity"):
        skin_concerns.append("Sensitivity")
    if st.sidebar.checkbox("Aging", key="concern_aging"):
        skin_concerns.append("Aging")
    
    # Default to "No concerns" if none selected
    if not skin_concerns:
        skin_concerns = ["No concerns"]
    
    # Age Input
    age = st.sidebar.slider(
        "👤 Age",
        min_value=13,
        max_value=80,
        value=25,
        step=1,
        help="Your age (13-80)"
    )
    
    # Preferences Input
    st.sidebar.markdown("### ♥️ Preferences")
    alcohol_free = st.sidebar.checkbox("Alcohol-Free", key="pref_alcohol")
    fragrance_free = st.sidebar.checkbox("Fragrance-Free", key="pref_fragrance")
    vegan = st.sidebar.checkbox("Vegan", key="pref_vegan")
    cruelty_free = st.sidebar.checkbox("Cruelty-Free", key="pref_cruelty")
    
    # Action Button
    st.sidebar.markdown("---")
    search_btn = st.sidebar.button(
        "🔬 Get Recommendations",
        use_container_width=True,
        key="analyze_btn"
    )
    
    # ========================================================================
    # MAIN CONTENT: TITLE AND DESCRIPTION
    # ========================================================================
    
    st.markdown("# 🔬 Analyze My Skin")
    st.markdown(
        "Enter your skin profile in the sidebar and click **Get Recommendations** "
        "to receive personalized ingredient suggestions."
    )
    
    st.markdown("---")
    
    # ========================================================================
    # PROCESS RECOMMENDATIONS (if button clicked)
    # ========================================================================
    
    if search_btn:
        # Validate inputs
        is_valid, error_msg = validate_sidebar_inputs(skin_type, skin_concerns, age)
        
        if not is_valid:
            st.error(f"❌ {error_msg}")
            return
        
        # Show loading state
        with st.spinner("🔄 Analyzing your profile..."):
            # Block 8: Orchestrator - handles all business logic
            # This keeps app.py focused on UI only!
            results = get_combined_recommendations(
                skin_type=skin_type,
                concerns=skin_concerns if skin_concerns != ["No concerns"] else [],
                age=age,
                alcohol_free=alcohol_free,
                fragrance_free=fragrance_free,
                vegan=vegan,
                cruelty_free=cruelty_free,
                top_n=5
            )
        
        # Display success message
        st.markdown(
            '<div class="success-badge">✅ Analysis Complete!</div>',
            unsafe_allow_html=True
        )
        
        st.markdown("---")
        
        # ====================================================================
        # SECTION 1: SCORE-BASED & ML RECOMMENDATIONS (Block 5: Integration)
        # ====================================================================
        
        st.markdown("## 🎯 Your Recommendations")
        
        display_combined_recommendations(
            user_profile=results.user_profile.to_dict(),
            recommendations=results.block1_results,
            ml_result=results.block4_result,
            show_comparison=True
        )
        
        st.markdown("---")
        
        # ====================================================================
        # SECTION 2: DETAILED EXPLANATIONS
        # ====================================================================
        
        st.markdown("## 📖 Detailed Breakdown")
        
        # Score breakdown for top ingredients
        with st.expander("📊 Score Breakdown (Rule-Based)", expanded=False):
            st.markdown(
                "This shows how each ingredient was scored based on your skin profile. "
                "Higher scores mean better matches for your skin type and concerns."
            )
            st.divider()
            
            # Show breakdown for top 3 recommendations
            if len(results.block1_results) >= 3:
                tab1, tab2, tab3 = st.tabs([
                    f"#{results.block1_results[0].ingredient}",
                    f"#{results.block1_results[1].ingredient}",
                    f"#{results.block1_results[2].ingredient}"
                ])
                
                with tab1:
                    display_explainability_breakdown(results.block1_results[0])
                
                with tab2:
                    display_explainability_breakdown(results.block1_results[1])
                
                with tab3:
                    display_explainability_breakdown(results.block1_results[2])
        
        st.markdown("---")
        
        # ====================================================================
        # SECTION 3: MODEL INFORMATION
        # ====================================================================
        
        with st.expander("🧠 ML Model Details", expanded=False):
            st.markdown(
                "Learn about the machine learning model that made the prediction. "
                "This model uses K-Nearest Neighbors to find similar skin profiles "
                "and recommend ingredients based on what worked for similar users."
            )
            st.divider()
            
            display_ml_performance_metrics()
        
        st.markdown("---")
        
        # ====================================================================
        # SECTION 4: YOUR PROFILE SUMMARY
        # ====================================================================
        
        with st.expander("👤 Your Profile Summary", expanded=False):
            st.markdown("### Input Information")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Skin Type", skin_type)
            
            with col2:
                st.metric("Age", age)
            
            with col3:
                st.metric("Concerns", len(skin_concerns))
            
            st.markdown("### Preferences")
            preferences = {
                "Alcohol-Free": alcohol_free,
                "Fragrance-Free": fragrance_free,
                "Vegan": vegan,
                "Cruelty-Free": cruelty_free
            }
            
            pref_list = [k for k, v in preferences.items() if v]
            if pref_list:
                st.markdown(f"✓ {', '.join(pref_list)}")
            else:
                st.markdown("No special preferences selected")
    
    else:
        # Show guidance when no analysis has been run
        st.info(
            "👈 Enter your skin profile in the sidebar and click "
            "**Get Recommendations** to see personalized suggestions!"
        )


# ============================================================================
# PAGE: INSIGHTS (Data Exploration)
# ============================================================================

def page_insights():
    """
    Display the EDA (Exploratory Data Analysis) dashboard.
    Allows users to explore patterns and trends in the data.
    """
    
    st.markdown("# 📊 Insights & Data Exploration")
    st.markdown(
        "Explore patterns in our skincare dataset. Understand what ingredients "
        "work for different skin types and concerns."
    )
    
    st.markdown("---")
    
    # Display dataset statistics
    st.markdown("## 📈 Dataset Overview")
    
    dataset_info = get_dataset_info()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Profiles",
            dataset_info.get("total_profiles", "N/A"),
            "Training samples"
        )
    
    with col2:
        st.metric(
            "Skin Types",
            dataset_info.get("unique_skin_types", "N/A"),
            "Categories"
        )
    
    with col3:
        st.metric(
            "Ingredients",
            dataset_info.get("unique_ingredients", "N/A"),
            "Recommended"
        )
    
    with col4:
        st.metric(
            "Data Quality",
            "100%",
            "No missing values"
        )
    
    st.markdown("---")
    
    # Display the full EDA dashboard
    st.markdown("## 📊 Interactive Visualizations")
    
    display_eda_dashboard()
    
    st.markdown("---")
    
    # Model information
    st.markdown("## 🧠 ML Model Status")
    
    model_status = get_model_status()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Train Accuracy",
            f"{model_status.get('train_accuracy', 'N/A')}%",
            "On training data"
        )
    
    with col2:
        st.metric(
            "Test Accuracy",
            f"{model_status.get('test_accuracy', 'N/A')}%",
            "On test data"
        )
    
    with col3:
        st.metric(
            "Algorithm",
            "KNN (k=3)",
            "K-Nearest Neighbors"
        )


# ============================================================================
# MAIN APP EXECUTION
# ============================================================================

def main():
    """
    Main application entry point.
    Manages page navigation and displays selected page.
    """
    
    # Initialize session state for page tracking
    if "page" not in st.session_state:
        st.session_state.page = "🏠 Home"
    
    # Get current page
    current_page = create_navigation()
    
    # Update session state
    st.session_state.page = current_page
    
    # Display appropriate page based on selection
    if current_page == "🏠 Home":
        page_home()
    
    elif current_page == "🔬 Analyze My Skin":
        page_analyze()
    
    elif current_page == "📊 Insights":
        page_insights()


# ============================================================================
# APP ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
