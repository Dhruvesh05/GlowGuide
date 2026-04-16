"""
Explainability UI Component for GlowGuide.

This module provides Streamlit UI components to display ingredient recommendations
with detailed reasoning and scoring breakdowns.
"""

import streamlit as st
from typing import List, Dict
from app.utils import RecommendationResult


def display_recommendation_card(recommendation: RecommendationResult, rank: int = 1):
    """
    Display a single recommendation card with explainability.
    
    Args:
        recommendation: RecommendationResult object containing ingredient, score, and reasoning
        rank: Rank number (1st, 2nd, etc.) for display
    """
    
    # Determine color based on score
    if recommendation.score >= 65:
        color_class = "success"
        score_label = "Excellent Match"
    elif recommendation.score >= 60:
        color_class = "info"
        score_label = "Good Match"
    else:
        color_class = "warning"
        score_label = "Moderate Match"
    
    # Build the card HTML
    html_content = f"""
    <div style="
        background: white;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
        border-left: 5px solid #000000;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    " onmouseover="this.style.boxShadow='0 8px 20px rgba(0, 0, 0, 0.12)'; this.style.transform='translateY(-2px)'" 
      onmouseout="this.style.boxShadow='0 2px 8px rgba(0, 0, 0, 0.08)'; this.style.transform='translateY(0)'">
        
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 16px;">
            <div>
                <span style="
                    background: #f3f4f6;
                    color: #1f2937;
                    padding: 6px 12px;
                    border-radius: 20px;
                    font-size: 12px;
                    font-weight: 600;
                    margin-right: 8px;
                ">#{rank}</span>
                <h3 style="margin: 8px 0 4px 0; font-size: 20px; font-weight: 700; color: #000000;">
                    {recommendation.ingredient}
                </h3>
                <p style="margin: 0; font-size: 13px; color: #6b7280;">{score_label}</p>
            </div>
            <div style="text-align: right;">
                <div style="
                    font-size: 28px;
                    font-weight: 700;
                    color: #000000;
                ">{recommendation.score:.1f}</div>
                <div style="
                    font-size: 12px;
                    color: #6b7280;
                    margin-top: 4px;
                ">out of 100</div>
            </div>
        </div>
        
        <div style="
            background: linear-gradient(90deg, #f3f4f6 0%, #f9fafb 100%);
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 16px;
        ">
            <div style="
                width: 100%;
                background: #e5e7eb;
                height: 6px;
                border-radius: 3px;
                overflow: hidden;
            ">
                <div style="
                    width: {min(recommendation.score, 100)}%;
                    height: 100%;
                    background: linear-gradient(90deg, #000000 0%, #1a1a1a 100%);
                    border-radius: 3px;
                    transition: width 0.5s ease;
                "></div>
            </div>
        </div>
        
        <div style="margin-bottom: 0;">
            <p style="
                margin: 0 0 12px 0;
                font-size: 13px;
                font-weight: 600;
                color: #1f2937;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            ">Why This Recommendation</p>
    """
    
    # Add reasoning bullets
    for reason in recommendation.reasoning:
        html_content += f"""
            <div style="
                display: flex;
                align-items: flex-start;
                margin-bottom: 10px;
                font-size: 14px;
                color: #374151;
                line-height: 1.5;
            ">
                <span style="
                    color: #000000;
                    margin-right: 10px;
                    font-weight: 700;
                    flex-shrink: 0;
                ">•</span>
                <span>{reason}</span>
            </div>
        """
    
    html_content += """
        </div>
    </div>
    """
    
    st.markdown(html_content, unsafe_allow_html=True)


def display_recommendations_grid(
    recommendations: List[RecommendationResult],
    show_top_n: int = 5,
    show_detailed: bool = True,
):
    """
    Display multiple recommendations in a grid format with explainability.
    
    Args:
        recommendations: List of RecommendationResult objects
        show_top_n: Number of top recommendations to display (default 5)
        show_detailed: Whether to show detailed reasoning (default True)
    """
    
    if not recommendations:
        st.warning("No recommendations found. Please adjust your profile.")
        return
    
    # Display top N recommendations
    top_recommendations = recommendations[:show_top_n]
    
    st.markdown(f"### ✨ Top {len(top_recommendations)} Recommended Ingredients")
    st.markdown(f"*Based on your skin profile: skin type, concerns, age, and preferences*")
    st.markdown("<div style='margin: 16px 0;'></div>", unsafe_allow_html=True)
    
    for idx, rec in enumerate(top_recommendations, 1):
        display_recommendation_card(rec, rank=idx)
    
    # Summary section
    st.markdown("<div style='margin: 24px 0;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Top Score",
            value=f"{top_recommendations[0].score:.1f}",
            delta=f"{top_recommendations[0].ingredient}"
        )
    with col2:
        avg_score = sum(r.score for r in top_recommendations) / len(top_recommendations)
        st.metric(
            label="Average Score",
            value=f"{avg_score:.1f}",
            delta="of top 5"
        )
    with col3:
        st.metric(
            label="Recommendations",
            value=len(top_recommendations),
            delta="ingredients"
        )


def display_comparison_table(recommendations: List[RecommendationResult]):
    """
    Display recommendations in a comparison table format.
    
    Args:
        recommendations: List of RecommendationResult objects
    """
    
    if not recommendations:
        return
    
    st.markdown("### 📊 Detailed Comparison")
    
    comparison_data = []
    for idx, rec in enumerate(recommendations[:5], 1):
        comparison_data.append({
            "Rank": f"#{idx}",
            "Ingredient": rec.ingredient,
            "Score": f"{rec.score:.1f}/100",
            "Primary Reason": rec.reasoning[0] if rec.reasoning else "No reasons",
            "Other Factors": " | ".join(rec.reasoning[1:]) if len(rec.reasoning) > 1 else "—"
        })
    
    # Use Streamlit's dataframe with custom styling
    import pandas as pd
    df = pd.DataFrame(comparison_data)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.TextColumn(width=80),
            "Ingredient": st.column_config.TextColumn(width=150),
            "Score": st.column_config.TextColumn(width=100),
            "Primary Reason": st.column_config.TextColumn(width=220),
            "Other Factors": st.column_config.TextColumn(width=300),
        }
    )


def display_explainability_breakdown(recommendation: RecommendationResult):
    """
    Display a detailed breakdown of how the recommendation score was calculated.
    
    Args:
        recommendation: RecommendationResult object
    """
    
    st.markdown(f"### 🔍 Detailed Score Breakdown: {recommendation.ingredient}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Score Summary**")
        st.metric(
            label="Final Score",
            value=f"{recommendation.score:.1f}",
            delta="out of 100"
        )
    
    with col2:
        st.markdown("**Score Components**")
        
        # Extract and categorize reasons
        base_score = 50
        adjustments = []
        
        for reason in recommendation.reasoning:
            # Parse each reason to extract value
            parts = reason.split(" for ")
            if len(parts) > 0:
                adjustment_text = parts[0].replace("+", "")
                adjustments.append({
                    "component": " for ".join(parts[1:]) if len(parts) > 1 else parts[0],
                    "text": reason
                })
        
        st.write(f"**Base Score:** {base_score}/100")
        for adj in adjustments:
            st.write(f"• {adj['text']}")
    
    # Visual breakdown
    st.markdown("**Score Composition**")
    
    breakdown_html = """
    <div style="background: #f9fafb; border-radius: 8px; padding: 16px;">
        <div style="font-size: 13px; color: #6b7280; margin-bottom: 12px;">
            <strong>Base Score:</strong> 50.0 points
        </div>
    """
    
    for reason in recommendation.reasoning:
        breakdown_html += f"""
        <div style="
            background: white;
            padding: 10px 12px;
            margin-bottom: 8px;
            border-radius: 6px;
            border-left: 3px solid #000000;
            font-size: 13px;
            color: #374151;
        ">{reason}</div>
        """
    
    breakdown_html += """
        <div style="
            background: linear-gradient(135deg, #f0f0f0 0%, #e5e5e5 100%);
            padding: 12px;
            margin-top: 12px;
            border-radius: 6px;
            font-weight: 600;
            text-align: right;
            color: #000000;
        ">Final Score: """
    
    breakdown_html += f"{recommendation.score:.1f}/100</div>"
    breakdown_html += "</div>"
    
    st.markdown(breakdown_html, unsafe_allow_html=True)


def display_ingredient_explanation(
    ingredient: str,
    score: float,
    reasoning: List[str],
    user_profile: Dict = None
):
    """
    Display a comprehensive explanation for why an ingredient is recommended.
    
    Args:
        ingredient: Name of the ingredient
        score: Recommendation score (0-100)
        reasoning: List of reasons for the recommendation
        user_profile: Optional user profile dictionary for context
    """
    
    st.markdown(f"## {ingredient}")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.metric("Recommendation Score", f"{score:.1f}/100")
    
    with col2:
        if user_profile:
            skin_type = user_profile.get('skin_type', 'N/A')
            st.metric("For Skin Type", skin_type)
    
    with col3:
        if user_profile:
            concerns = ", ".join(user_profile.get('concerns', [])[:2])
            st.metric("Top Concerns", concerns if concerns else "None")
    
    st.markdown("### Why This Ingredient?")
    
    for idx, reason in enumerate(reasoning, 1):
        st.write(f"**{idx}.** {reason}")
    
    # Add ingredient benefits info
    st.markdown("### Key Benefits")
    
    ingredient_benefits = {
        "Salicylic Acid": [
            "Beta-hydroxy acid (BHA) that exfoliates inside pores",
            "Reduces acne-causing bacteria",
            "Controls excess oil production",
            "Suitable for oily and acne-prone skin"
        ],
        "Hyaluronic Acid": [
            "Humectant that holds 1000x its weight in water",
            "Provides intense hydration",
            "Plumps fine lines and wrinkles",
            "Works on all skin types"
        ],
        "Niacinamide": [
            "Regulates sebum production",
            "Strengthens skin barrier",
            "Reduces redness and inflammation",
            "Universal ingredient for all skin types"
        ],
        "Ceramide": [
            "Lipid that seals and protects skin barrier",
            "Reduces water loss from skin",
            "Soothes irritation",
            "Essential for dry and sensitive skin"
        ],
        "Retinol": [
            "Vitamin A derivative that promotes cell turnover",
            "Reduces fine lines and wrinkles",
            "Improves skin texture",
            "Best for mature and aging skin"
        ],
    }
    
    if ingredient in ingredient_benefits:
        for benefit in ingredient_benefits[ingredient]:
            st.write(f"✓ {benefit}")
