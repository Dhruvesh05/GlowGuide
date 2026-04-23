"""
Block 5: ML + Rule-based Integration UI

Combines Block 1 (rule-based scoring) with Block 4 (ML-based KNN prediction)
to display both approaches side-by-side in Streamlit.

Functions:
- display_combined_recommendations() - Show both Block 1 + Block 4
- display_comparison_table() - Side-by-side comparison
- display_ml_prediction_card() - ML prediction with confidence
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import List, Dict, Any


def display_combined_recommendations(
    user_profile: Dict,
    recommendations: List,
    ml_result: Dict,
    show_comparison: bool = True
):
    """
    Display Block 1 (rule-based) and Block 4 (ML-based) recommendations together.
    
    Args:
        user_profile: User skin profile (skin_type, concerns, age)
        recommendations: List of RecommendationResult from Block 1
        ml_result: Prediction result from Block 4
        show_comparison: Whether to show comparison section
    """
    
    # Header
    st.markdown("### Smart Recommendation Engine")
    st.markdown(
        "Powered by both **Rule-Based Scoring** and **Machine Learning** "
        "for the most accurate skincare recommendations."
    )
    
    st.divider()
    
    # ====================================================================
    # SECTION 1: SIDE-BY-SIDE DISPLAY
    # ====================================================================
    
    col1, col2 = st.columns(2)
    
    # COLUMN 1: RULE-BASED TOP RECOMMENDATIONS
    with col1:
        st.markdown("#### Top Recommendations (Score-Based)")
        st.markdown(
            "<p style='font-size: 13px; color: #666; margin-bottom: 12px;'>"
            "Rule-based engine analyzing your skin type and concerns"
            "</p>",
            unsafe_allow_html=True
        )
        
        # Display top 3 rule-based recommendations
        for idx, rec in enumerate(recommendations[:3], 1):
            _display_score_card(idx, rec)
    
    # COLUMN 2: ML PREDICTION
    with col2:
        st.markdown("#### 🧠 ML Prediction (KNN)")
        st.markdown(
            "<p style='font-size: 13px; color: #666; margin-bottom: 12px;'>"
            "Neural network analyzing similar skincare profiles"
            "</p>",
            unsafe_allow_html=True
        )
        
        # Display ML prediction
        _display_ml_prediction_card(ml_result)
    
    st.divider()
    
    # ====================================================================
    # SECTION 2: COMPARISON & ANALYSIS
    # ====================================================================
    
    if show_comparison:
        st.markdown("### Approach Comparison")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Top recommendation from each approach
        top_score_rec = recommendations[0].ingredient
        top_ml_rec = ml_result['ingredient']
        ml_confidence = ml_result['confidence']
        
        # Metric 1: Top Score-Based
        with col1:
            st.metric(
                "Top (Score-Based)",
                top_score_rec,
                f"Score: {recommendations[0].score:.1f}"
            )
        
        # Metric 2: Top ML
        with col2:
            st.metric(
                "Top (ML-Based)",
                top_ml_rec,
                f"Confidence: {ml_confidence:.0%}"
            )
        
        # Metric 3: Agreement
        agreement = "Yes" if top_score_rec == top_ml_rec else "Differs"
        with col3:
            st.metric(
                "Approaches Agree",
                agreement,
                "Both recommend same" if top_score_rec == top_ml_rec else "Different recommendations"
            )
        
        # Metric 4: Confidence in Prediction
        prediction_strength = "High" if ml_confidence > 0.75 else "Medium" if ml_confidence > 0.6 else "Low"
        with col4:
            st.metric(
                "ML Confidence",
                prediction_strength,
                f"{ml_confidence:.0%}"
            )
        
        st.divider()
        
        # Comparison table
        st.markdown("#### Detailed Comparison")
        _display_comparison_table(recommendations, ml_result, user_profile)
        
        st.divider()
        
        # Insights
        st.markdown("#### 💡 Insights")
        _display_insights(recommendations, ml_result, user_profile)


def _display_score_card(rank: int, recommendation):
    """Display a single score-based recommendation card."""
    
    # Extract data
    ingredient = recommendation.ingredient
    score = recommendation.score
    reasoning = recommendation.reasoning
    
    # Color based on score
    if score >= 8:
        badge_color = "#ecfdf5"
        badge_text_color = "#065f46"
        border_color = "#6ee7b7"
    elif score >= 6:
        badge_color = "#eff6ff"
        badge_text_color = "#0c4a6e"
        border_color = "#93c5fd"
    else:
        badge_color = "#fef3c7"
        badge_text_color = "#92400e"
        border_color = "#fcd34d"
    
    # Display card
    st.markdown(
        f"""
        <div style='
            background: {badge_color};
            border: 2px solid {border_color};
            border-radius: 12px;
            padding: 16px;
            margin: 10px 0;
        '>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <span style='
                        font-size: 13px;
                        font-weight: 700;
                        color: {badge_text_color};
                        display: inline-block;
                        background: rgba(0,0,0,0.05);
                        padding: 4px 8px;
                        border-radius: 4px;
                        margin-bottom: 8px;
                    '>RANK #{rank}</span>
                    <h4 style='margin: 8px 0 4px 0; color: #000;'>{ingredient}</h4>
                    <p style='margin: 0; color: #666; font-size: 12px;'>
                        {reasoning[0] if reasoning else 'Recommended for your profile'}
                    </p>
                </div>
                <div style='text-align: right;'>
                    <span style='
                        font-size: 28px;
                        font-weight: 700;
                        color: {badge_text_color};
                    '>{score:.1f}</span>
                    <p style='margin: 4px 0; color: {badge_text_color}; font-size: 12px;'>Score</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def _display_ml_prediction_card(ml_result: Dict):
    """Display ML prediction card with confidence."""
    
    ingredient = ml_result['ingredient']
    confidence = ml_result['confidence']
    reasoning = ml_result['reasoning']
    
    # Color based on confidence
    if confidence >= 0.75:
        badge_color = "#ecfdf5"
        badge_text_color = "#065f46"
        border_color = "#6ee7b7"
    elif confidence >= 0.6:
        badge_color = "#eff6ff"
        badge_text_color = "#0c4a6e"
        border_color = "#93c5fd"
    else:
        badge_color = "#fef3c7"
        badge_text_color = "#92400e"
        border_color = "#fcd34d"
    
    st.markdown(
        f"""
        <div style='
            background: {badge_color};
            border: 2px solid {border_color};
            border-radius: 12px;
            padding: 16px;
            margin: 10px 0;
        '>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <span style='
                        font-size: 13px;
                        font-weight: 700;
                        color: {badge_text_color};
                        display: inline-block;
                        background: rgba(0,0,0,0.05);
                        padding: 4px 8px;
                        border-radius: 4px;
                        margin-bottom: 8px;
                    '>ML PREDICTION</span>
                    <h4 style='margin: 8px 0 4px 0; color: #000;'>{ingredient}</h4>
                    <p style='margin: 0; color: #666; font-size: 12px;'>
                        {reasoning.split(".")[0]}.
                    </p>
                </div>
                <div style='text-align: right;'>
                    <span style='
                        font-size: 28px;
                        font-weight: 700;
                        color: {badge_text_color};
                    '>{confidence:.0%}</span>
                    <p style='margin: 4px 0; color: {badge_text_color}; font-size: 12px;'>Confidence</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def _display_comparison_table(recommendations: List, ml_result: Dict, user_profile: Dict):
    """Display detailed comparison table of approaches."""
    
    # Build comparison data
    data = {
        'Aspect': [
            'Top Recommendation',
            'Score/Confidence',
            'Approach',
            'Data Source',
            'Strengths',
        ],
        'Rule-Based (Block 1)': [
            recommendations[0].ingredient,
            f"{recommendations[0].score:.1f}/10",
            'Expert rules + pattern matching',
            'Pre-defined rules',
            'Transparent, fast, consistent',
        ],
        'ML-Based (Block 4)': [
            ml_result['ingredient'],
            f"{ml_result['confidence']:.0%}",
            'K-Nearest Neighbors (KNN)',
            'Training dataset (50 samples)',
            'Data-driven, learns patterns',
        ]
    }
    
    df = pd.DataFrame(data)
    
    # Display as styled table
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Aspect': st.column_config.TextColumn(width=150),
            'Rule-Based (Block 1)': st.column_config.TextColumn(width=250),
            'ML-Based (Block 4)': st.column_config.TextColumn(width=250),
        }
    )


def _display_insights(recommendations: List, ml_result: Dict, user_profile: Dict):
    """Display insights about the recommendations."""
    
    top_score = recommendations[0].ingredient
    top_ml = ml_result['ingredient']
    ml_confidence = ml_result['confidence']
    skin_type = user_profile.get('skin_type', 'Unknown')
    concerns = user_profile.get('concerns', [])
    
    insight_cols = st.columns(1)
    
    insights = []
    
    # Insight 1: Agreement
    if top_score == top_ml:
        insights.append(
            f"Strong Agreement: Both approaches recommend {top_score} for your {skin_type} skin. "
            f"This is a highly confident recommendation."
        )
    else:
        insights.append(
            f"Different Recommendations: Rule-based suggests {top_score}, while ML suggests {top_ml}. "
            f"Consider your skin's unique characteristics to choose between them."
        )
    
    # Insight 2: Confidence
    if ml_confidence > 0.75:
        insights.append(
            f"High ML Confidence: The model is {ml_confidence:.0%} confident in recommending {top_ml}, "
            f"based on similar skincare profiles in the training data."
        )
    elif ml_confidence > 0.6:
        insights.append(
            f"Moderate ML Confidence: The model is {ml_confidence:.0%} confident in its recommendation. "
            f"Additional factors may influence the best choice for you."
        )
    else:
        insights.append(
            f"Lower ML Confidence: The model is {ml_confidence:.0%} confident, suggesting your profile "
            f"doesn't closely match training examples. Consider Rule-based recommendation."
        )
    
    # Insight 3: Concerns
    if concerns and 'Acne' in concerns:
        insights.append(
            "💡 **For Acne**: Both approaches favor ingredients with clarifying properties. "
            "Look for salicylic acid or niacinamide for best results."
        )
    if concerns and 'Dryness' in concerns:
        insights.append(
            "💡 **For Dryness**: Hydrating ingredients like hyaluronic acid are recommended. "
            "Both approaches should suggest moisturizing solutions."
        )
    
    # Display insights
    for insight in insights:
        st.info(insight)


def display_ml_performance_metrics():
    """Display ML model performance metrics."""
    
    from app.utils import get_model_info
    
    info = get_model_info()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Train Accuracy",
            f"{info['train_accuracy']:.1%}",
            "of 40 samples"
        )
    
    with col2:
        st.metric(
            "Test Accuracy",
            f"{info['test_accuracy']:.1%}",
            "of 10 samples"
        )
    
    with col3:
        st.metric(
            "Model Type",
            "KNN",
            f"k={info['k_neighbors']}"
        )
    
    with col4:
        st.metric(
            "Classes",
            info['n_classes'],
            "ingredients"
        )
    
    # Details
    with st.expander("View Model Details", expanded=False):
        details_col1, details_col2 = st.columns(2)
        
        with details_col1:
            st.markdown("**Training Configuration**")
            st.write(f"- Training Samples: {info['n_train_samples']}")
            st.write(f"- Test Samples: {info['n_test_samples']}")
            st.write(f"- Features: {info['n_features']}")
            st.write(f"- Distance Metric: {info['metric']}")
        
        with details_col2:
            st.markdown("**Classes (Ingredients)**")
            for idx, ingredient in info['class_names'].items():
                st.write(f"- [{idx}] {ingredient}")
