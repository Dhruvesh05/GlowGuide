"""
Block 10: Remedy Recommendation Engine - STABLE VERSION

Provides robust home remedy recommendations with:
- Safe CSV loading with error handling
- Multi-level matching (exact → keyword → random fallback)
- Always returns 2 remedies (guaranteed)
- Optional debug logging
- Zero crashes on edge cases
"""

from typing import Optional, List, Dict, Any
from pathlib import Path
import pandas as pd
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class RemedyRecommender:
    """Robust remedy recommendation engine."""
    
    def __init__(self, debug: bool = False):
        """
        Initialize with remedies data.
        
        ✅ STEP 2: LOAD DATASETS SAFELY
        
        Args:
            debug: Enable debug logging
        """
        self.debug = debug
        self.remedies_df = None
        self._load_data()
    
    def _load_data(self) -> None:
        """
        Load remedies.csv with error handling.
        Fill missing values to prevent crashes.
        """
        try:
            # Get absolute path to data folder
            base_dir = Path(__file__).parent.parent.parent
            csv_path = base_dir / "data" / "remedies.csv"
            
            if not csv_path.exists():
                print(f"⚠️  Warning: {csv_path} not found")
                return
            
            # Load CSV
            self.remedies_df = pd.read_csv(csv_path)
            
            # ✅ STEP 3: NORMALIZE DATA
            if 'Ingredients' in self.remedies_df.columns:
                self.remedies_df['Ingredients'] = (
                    self.remedies_df['Ingredients']
                    .fillna("")
                    .astype(str)
                    .str.lower()
                    .str.strip()
                )
            
            if 'clean_Ingredients' in self.remedies_df.columns:
                self.remedies_df['clean_Ingredients'] = (
                    self.remedies_df['clean_Ingredients']
                    .fillna("")
                    .astype(str)
                    .str.lower()
                    .str.strip()
                )
            
            if 'Problem' in self.remedies_df.columns:
                self.remedies_df['Problem'] = (
                    self.remedies_df['Problem']
                    .fillna("Unknown")
                    .astype(str)
                    .str.strip()
                )
            
            if 'Usage' in self.remedies_df.columns:
                self.remedies_df['Usage'] = (
                    self.remedies_df['Usage']
                    .fillna("Unknown")
                    .astype(str)
                    .str.strip()
                )
            
            print(f"✅ Loaded {len(self.remedies_df)} remedies")
        
        except Exception as e:
            print(f"⚠️  Error loading remedies: {e}")
            self.remedies_df = None
    
    def get_remedies(self, ingredient: str, debug: bool = False) -> Optional[List[Dict[str, Any]]]:
        """
        ✅ STEP 6: IMPLEMENT get_remedies FUNCTION
        
        Get remedies with 3-level matching:
        1. Exact match
        2. Keyword match (first word)
        3. Random fallback (always return 2)
        
        Args:
            ingredient: Ingredient name
            debug: Enable debug logging
        
        Returns:
            List of dicts with Problem, Ingredients, Usage (always 2 items or None)
        """
        if self.remedies_df is None or len(self.remedies_df) == 0:
            return None
        
        self.debug = debug
        
        try:
            # Normalize ingredient
            ingredient_normalized = ingredient.lower().strip()
            
            if self.debug:
                print(f"🔍 Searching remedies for: '{ingredient_normalized}'")
            
            # ✅ STEP 4: ROBUST MATCHING LOGIC
            # LEVEL 1: Exact match (check both Ingredients and clean_Ingredients)
            matches = self.remedies_df[
                (self.remedies_df['Ingredients'].str.contains(ingredient_normalized, na=False)) |
                (self.remedies_df['clean_Ingredients'].str.contains(ingredient_normalized, na=False))
            ].copy()
            
            if self.debug:
                print(f"   Level 1 (exact): {len(matches)} matches")
            
            # LEVEL 2: Keyword match (first word)
            if len(matches) == 0:
                first_word = ingredient_normalized.split()[0]
                if self.debug:
                    print(f"   Level 2 (keyword '{first_word}'): ", end="")
                
                matches = self.remedies_df[
                    (self.remedies_df['Ingredients'].str.contains(first_word, na=False)) |
                    (self.remedies_df['clean_Ingredients'].str.contains(first_word, na=False))
                ].copy()
                
                if self.debug:
                    print(f"{len(matches)} matches")
            
            # LEVEL 3: Random fallback (always return 2)
            if len(matches) == 0:
                if self.debug:
                    print(f"   Level 3 (random fallback)")
                
                matches = self.remedies_df.sample(
                    n=min(2, len(self.remedies_df)),
                    random_state=hash(ingredient_normalized) % (2**31)
                ).copy()
            
            # Get top 2
            matches = matches.head(2)
            
            # Build result list
            results = []
            for _, row in matches.iterrows():
                results.append({
                    'Problem': str(row.get('Problem', 'Unknown')),
                    'Ingredients': str(row.get('Ingredients', 'Unknown')),
                    'Usage': str(row.get('Usage', 'Unknown')),
                    'Category': str(row.get('Category', 'Unknown')),
                    'Frequency': str(row.get('Frequency', 'Unknown'))
                })
            
            # Pad to 2 if needed
            while len(results) < 2 and len(self.remedies_df) > 0:
                random_remedy = self.remedies_df.sample(n=1, random_state=None).iloc[0]
                results.append({
                    'Problem': str(random_remedy['Problem']),
                    'Ingredients': str(random_remedy['Ingredients']),
                    'Usage': str(random_remedy['Usage']),
                    'Category': str(random_remedy['Category']),
                    'Frequency': str(random_remedy['Frequency'])
                })
            
            if self.debug:
                print(f"   ✅ Returning {len(results)} remedies")
            
            return results[:2] if len(results) > 0 else None
        
        except Exception as e:
            print(f"❌ Error in get_remedies: {e}")
            return None
    
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
            
            matches = self.remedies_df[
                (self.remedies_df['Ingredients'].str.contains(ingredient_lower, na=False)) |
                (self.remedies_df['clean_Ingredients'].str.contains(ingredient_lower, na=False))
            ].copy()
            
            # Fallback to first word
            if len(matches) == 0:
                first_word = ingredient_lower.split()[0]
                matches = self.remedies_df[
                    (self.remedies_df['Ingredients'].str.contains(first_word, na=False)) |
                    (self.remedies_df['clean_Ingredients'].str.contains(first_word, na=False))
                ].copy()
            
            # Fallback to random
            if len(matches) == 0:
                matches = self.remedies_df.sample(
                    n=min(2, len(self.remedies_df)),
                    random_state=hash(ingredient_lower) % (2**31)
                ).copy()
            
            matches = matches.head(2)
            
            results = []
            for _, row in matches.iterrows():
                results.append({
                    'Problem': str(row.get('Problem', 'Unknown')),
                    'Category': str(row.get('Category', 'Unknown')),
                    'Ingredients': str(row.get('Ingredients', 'Unknown')),
                    'Usage': str(row.get('Usage', 'Unknown')),
                    'Frequency': str(row.get('Frequency', 'Unknown'))
                })
            
            return results if len(results) > 0 else None
        
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


def get_remedies(ingredient: str, debug: bool = False) -> Optional[List[Dict[str, Any]]]:
    """
    ✅ STEP 6: Recommend remedies for a specific ingredient.
    
    This is the main standalone function for remedy recommendations.
    Supports optional debug logging.
    
    Args:
        ingredient: Ingredient name to search for
        debug: Enable debug logging (default: False)
    
    Returns:
        List of top 2 remedies with Problem, Ingredients, Usage, etc.
        or None if error
        
    Example:
        >>> result = get_remedies('coconut oil', debug=True)
        >>> for remedy in result:
        ...     print(f"{remedy['Problem']}: {remedy['Usage']}")
    """
    try:
        recommender = get_recommender()
        return recommender.get_remedies(ingredient, debug=debug)
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

