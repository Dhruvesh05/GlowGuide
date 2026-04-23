"""Product classification result display component."""

import streamlit as st
import pandas as pd
from typing import Optional
from utils.helpers import clean_text, compute_safety_score, parse_ingredients


def render_classification_result(
    product_name: str,
    skin_type: str,
    df: pd.DataFrame,
    classifier,
    vectorizer
) -> None:
    """
    Render product classification result with safety score and confidence metrics.
    """
    if not product_name or not df is not None or classifier is None or vectorizer is None:
        st.warning("Missing required data for classification.")
        return
    
    # Fuzzy match product name
    product_name_lower = product_name.lower()
    matching_products = df[df["Name"].str.lower().str.contains(product_name_lower, na=False)]
    
    if matching_products.empty:
        # No match found - use skin type vector for prediction
        st.warning("Product not found in database. Showing analysis for skin type only.")
        try:
            # Create a feature vector based on skin type
            skin_type_features = [[1 if skin_type.lower() == col.lower() else 0 
                                   for col in ["Combination", "Dry", "Normal", "Oily", "Sensitive"]]]
            prediction = classifier.predict(skin_type_features)[0]
            probabilities = classifier.predict_proba(skin_type_features)[0]
            confidence = max(probabilities) * 100
            safety_score = 60  # Default score
        except Exception as e:
            st.error(f"Error during prediction: {str(e)}")
            return
    else:
        # Match found - use product ingredients
        product = matching_products.iloc[0]
        ingredients_raw = product.get("Ingredients", "")
        
        # Clean and vectorize ingredients
        try:
            cleaned_ingredients = clean_text(ingredients_raw)
            ingredient_vector = vectorizer.transform([cleaned_ingredients])
            prediction = classifier.predict(ingredient_vector)[0]
            probabilities = classifier.predict_proba(ingredient_vector)[0]
            confidence = max(probabilities) * 100
            
            # Compute safety score
            parsed_ingredients = parse_ingredients(ingredients_raw)
            safety_score = compute_safety_score(parsed_ingredients)
        except Exception as e:
            st.error(f"Error processing product: {str(e)}")
            return
    
    # Display metrics in three columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Category", value=prediction)
    
    with col2:
        st.metric(label="Confidence", value=f"{confidence:.1f}%")
    
    with col3:
        st.metric(label="Safety Score", value=f"{safety_score} / 100")
    
    # Display safety badge
    st.divider()
    if safety_score >= 70:
        st.success("Generally well-tolerated")
    elif safety_score >= 40:
        st.warning("⚠ Contains some irritants")
    else:
        st.error("✗ High irritant load detected")
    
    # Show ingredient breakdown if product was found
    if not matching_products.empty:
        with st.expander("View Ingredient Breakdown"):
            product = matching_products.iloc[0]
            ingredients_list = parse_ingredients(product.get("Ingredients", ""))
            if ingredients_list:
                st.markdown(", ".join(ingredients_list))
            else:
                st.info("No ingredients data available.")
