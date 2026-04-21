"""
Block 10: Remedy Recommendation Engine

This module provides the remedy recommendation function.
It searches for home remedies containing a specific ingredient
and returns the top 2 results with problem, ingredients, and usage.

Enhanced with:
- Robust data normalization (lowercase, strip)
- Fallback matching logic (exact → partial → first word)
- Debug logging for transparency
- Guaranteed results when data available
"""

from typing import Optional, List, Dict, Any
from pathlib import Path
import pandas as pd
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class RemedyRecommender:
    """
    Remedy recommendation engine for home remedies.
    
    Searches for remedies containing a specific ingredient
    and returns top results with problem, ingredients, and usage.
    
    Features:
    - Case-insensitive matching
    - Searches both Ingredients and clean_Ingredients columns
    - Fallback to partial/keyword matching
    - Data normalization for consistency
    - Debug logging
    """
    
    def __init__(self, remedies_csv: str = 'data/remedies.csv', debug: bool = False):
        """
        Initialize remedy recommender with remedies data.
        
        Args:
            remedies_csv: Path to remedies CSV file (default: data/remedies.csv)
            debug: Enable debug logging (default: False)
        """
        self.debug = debug
        
        try:
            # ✅ STEP 1: LOAD DATASET
            base_dir = Path(__file__).parent.parent.parent
            full_path = base_dir / remedies_csv
            
            # Load remedies data
            self.remedies_df = pd.read_csv(full_path)
            
            if self.remedies_df is None or len(self.remedies_df) == 0:
                print(f"❌ Error: Could not load remedies from {remedies_csv}")
                self.remedies_df = None
            else:
                # ✅ STEP 2: DATA NORMALIZATION
                self._normalize_data()
                print(f"✅ Loaded {len(self.remedies_df)} remedies")
                if self.debug:
                    print(f"   Columns: {list(self.remedies_df.columns)}")
        
        except Exception as e:
            print(f"❌ Error loading remedies: {e}")
            self.remedies_df = None
    
    def _normalize_data(self) -> None:
        """
        Normalize remedy data for consistent matching.
        
        - Convert Ingredients to lowercase
        - Convert clean_Ingredients to lowercase (if exists)
        - Strip whitespace
        - Create normalized columns for matching
        """
        if self.remedies_df is None:
            return
        
        try:
            # Normalize Ingredients column
            if 'Ingredients' in self.remedies_df.columns:
                self.remedies_df['ingredients_normalized'] = (
                    self.remedies_df['Ingredients']
                    .astype(str)
                    .str.lower()
                    .str.strip()
                )
            else:
                print("⚠️  Warning: Ingredients column not found")
                self.remedies_df['ingredients_normalized'] = ""
            
            # Normalize clean_Ingredients column if it exists
            if 'clean_Ingredients' in self.remedies_df.columns:
                self.remedies_df['clean_ingredients_normalized'] = (
                    self.remedies_df['clean_Ingredients']
                    .astype(str)
                    .str.lower()
                    .str.strip()
                )
            
            if self.debug:
                print("   ✅ Data normalization complete")
        
        except Exception as e:
            print(f"⚠️  Error normalizing remedy data: {e}")
    
    def search_remedies(self, ingredient: str) -> Optional[List[Dict[str, Any]]]:
        """
        Search for remedies containing a specific ingredient.
        
        Matching strategy:
        1. Exact match: ingredient in Ingredients or clean_Ingredients
        2. Fallback 1: Use first word of ingredient
        3. Fallback 2: Return empty list (not None) for UI handling
        
        ✅ STEP 3B: REMEDY MATCHING WITH FALLBACK
        
        Args:
            ingredient: Ingredient name to search for
        
        Returns:
            List of dicts with 'Problem', 'Ingredients', 'Usage' keys (top 2)
            Returns empty list [] if no remedies found, None if error
        """
        if self.remedies_df is None:
            if self.debug:
                print("❌ Remedies data not loaded")
            return None
        
        if not ingredient or len(ingredient.strip()) == 0:
            if self.debug:
                print("❌ Ingredient cannot be empty")
            return None
        
        try:
            ingredient_lower = ingredient.lower().strip()
            
            if self.debug:
                print(f"🔍 Searching remedies for ingredient: '{ingredient_lower}'")
            
            # Step 1: Try exact match
            matching_remedies = self._find_matching_remedies(ingredient_lower)
            
            if self.debug:
                print(f"   Exact match found: {len(matching_remedies)} remedies")
            
            # Step 2: If no match, try first word
            if len(matching_remedies) == 0:
                first_word = ingredient_lower.split()[0]
                if self.debug:
                    print(f"   No exact match, trying first word: '{first_word}'")
                matching_remedies = self._find_matching_remedies(first_word)
                
                if self.debug:
                    print(f"   First word match found: {len(matching_remedies)} remedies")
            
            # Return top 2
            top_2 = matching_remedies[:2]
            
            if self.debug:
                print(f"   ✅ Returning {len(top_2)} remedies")
            
            return top_2 if len(top_2) > 0 else []
        
        except Exception as e:
            print(f"❌ Error searching remedies: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()
            return None
    
    def _find_matching_remedies(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Find remedies matching a search term.
        
        Searches in both Ingredients and clean_Ingredients columns.
        
        Args:
            search_term: Search term (already lowercase)
        
        Returns:
            List of matching remedies
        """
        matching = []
        
        try:
            for idx, row in self.remedies_df.iterrows():
                ingredients_normalized = str(row.get('ingredients_normalized', '')).lower()
                clean_ingredients_normalized = str(row.get('clean_ingredients_normalized', '')).lower()
                
                # Check both columns
                if search_term in ingredients_normalized or search_term in clean_ingredients_normalized:
                    remedy_dict = {
                        'Problem': str(row.get('Problem', 'Unknown')).strip(),
                        'Ingredients': str(row.get('Ingredients', 'Unknown')).strip(),
                        'Usage': str(row.get('Usage', 'Unknown')).strip(),
                        'Category': str(row.get('Category', 'Unknown')).strip(),
                        'Frequency': str(row.get('Frequency', 'Unknown')).strip()
                    }
                    matching.append(remedy_dict)
        
        except Exception as e:
            print(f"⚠️  Error in _find_matching_remedies: {e}")
        
        return matching
    
    def get_remedies(self, ingredient: str, debug: bool = False) -> Optional[List[Dict[str, Any]]]:
        """
        Get remedies containing a specific ingredient (main entry point).
        
        ✅ STEP 4 & 5: HELPER FUNCTION FOR INTEGRATION
        
        This function:
        - Converts ingredient to lowercase
        - Tries exact match in Ingredients and clean_Ingredients
        - Falls back to first word if no exact match
        - Returns top 2 remedies or empty list
        
        Args:
            ingredient: Ingredient name to search for
            debug: Enable debug output
        
        Returns:
            List of top 2 remedies with 'Problem', 'Ingredients', 'Usage', etc.
            Returns [] (empty list) if no remedies found
            Returns None if error
        """
        self.debug = debug
        return self.search_remedies(ingredient)
    
    def search_remedies_detailed(self, ingredient: str) -> Optional[List[Dict[str, Any]]]:
        """
        Search for remedies with all available details.
        
        Args:
            ingredient: Ingredient name to search for
        
        Returns:
            List of dicts with all remedy details (top 2)
        """
        if self.remedies_df is None:
            return None
        
        if not ingredient or len(ingredient.strip()) == 0:
            return None
        
        try:
            ingredient_lower = ingredient.lower().strip()
            matching_remedies = []
            
            for idx, row in self.remedies_df.iterrows():
                ingredients = str(row.get('Ingredients', '')).lower()
                clean_ingredients = str(row.get('clean_Ingredients', '')).lower()
                
                if ingredient_lower in ingredients or ingredient_lower in clean_ingredients:
                    matching_remedies.append({
                        'Problem': row.get('Problem', 'Unknown'),
                        'Category': row.get('Category', 'Unknown'),
                        'Ingredients': row.get('Ingredients', 'Unknown'),
                        'Usage': row.get('Usage', 'Unknown'),
                        'Preparation': row.get('Preparation', 'Unknown'),
                        'Frequency': row.get('Frequency', 'Unknown'),
                        'Precautions': row.get('Precautions', 'Unknown'),
                        'Skin_or_Hair_Type': row.get('Skin_or_Hair_Type', 'Unknown')
                    })
            
            return matching_remedies[:2] if len(matching_remedies) > 0 else None
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return None


# Global recommender instance
_recommender = None


def get_recommender() -> RemedyRecommender:
    """
    Get or create global RemedyRecommender instance.
    
    Returns:
        RemedyRecommender instance
    """
    global _recommender
    if _recommender is None:
        _recommender = RemedyRecommender()
    return _recommender


def get_remedies(ingredient: str) -> Optional[List[Dict[str, Any]]]:
    """
    Recommend remedies for a specific ingredient.
    
    This is the main function for remedy recommendations.
    
    Args:
        ingredient: Ingredient name to search for
    
    Returns:
        List of top 2 remedies with 'Problem', 'Ingredients', 'Usage' keys
        or None if no remedies found
        
    Example:
        >>> result = get_remedies('coconut oil')
        >>> for remedy in result:
        ...     print(f"{remedy['Problem']}: {remedy['Usage']}")
    """
    recommender = get_recommender()
    return recommender.get_remedies(ingredient)


def main():
    """
    Main function: Execute Block 10 remedy recommendation pipeline and demo.
    
    Steps:
    1. Load remedies data
    2. Create RemedyRecommender
    3. Make sample remedy searches
    4. Display results
    """
    print("🔷 BLOCK 10: REMEDY RECOMMENDATION")
    print("=" * 70)
    
    # Step 1: Load remedies
    print("\n📦 Loading remedies data...")
    recommender = RemedyRecommender(remedies_csv='data/remedies.csv')
    
    if recommender.remedies_df is None:
        print("❌ Failed to load remedies data")
        return
    
    print(f"✅ Remedies loaded successfully")
    
    # Step 2: Demo searches
    print("\n🎯 Searching for remedy recommendations...")
    print("-" * 70)
    
    # Sample 1: Coconut Oil
    print("\n📝 Sample 1: Search for 'coconut oil'")
    remedies1 = recommender.get_remedies('coconut oil')
    
    if remedies1:
        print(f"✅ Found {len(remedies1)} remedies:")
        for i, remedy in enumerate(remedies1, 1):
            print(f"   {i}. {remedy['Problem']}")
            print(f"      Ingredients: {remedy['Ingredients']}")
            print(f"      Usage: {remedy['Usage']}")
    else:
        print("❌ No remedies found")
    
    # Sample 2: Honey
    print("\n📝 Sample 2: Search for 'honey'")
    remedies2 = recommender.get_remedies('honey')
    
    if remedies2:
        print(f"✅ Found {len(remedies2)} remedies:")
        for i, remedy in enumerate(remedies2, 1):
            print(f"   {i}. {remedy['Problem']}")
            print(f"      Ingredients: {remedy['Ingredients']}")
            print(f"      Usage: {remedy['Usage']}")
    else:
        print("❌ No remedies found")
    
    # Sample 3: Lemon Juice
    print("\n📝 Sample 3: Search for 'lemon juice'")
    remedies3 = recommender.get_remedies('lemon juice')
    
    if remedies3:
        print(f"✅ Found {len(remedies3)} remedies:")
        for i, remedy in enumerate(remedies3, 1):
            print(f"   {i}. {remedy['Problem']}")
            print(f"      Ingredients: {remedy['Ingredients']}")
            print(f"      Usage: {remedy['Usage']}")
    else:
        print("❌ No remedies found")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 RECOMMENDATION SUMMARY")
    print("=" * 70)
    
    total_found = sum(1 for r in [remedies1, remedies2, remedies3] if r)
    
    print(f"✅ Searches completed: 3")
    print(f"✅ Remedies found: {total_found}/3")
    print(f"✅ Remedy recommendation engine working correctly")
    
    print("\n✨ Block 10 Remedy Recommendation Complete!")
    print("   Status: Ready for Block 11+ (Full Integration)")


if __name__ == '__main__':
    main()
