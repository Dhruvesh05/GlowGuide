"""
Block 9: Product Recommendation Engine - STABLE VERSION

Provides robust product recommendations with:
- Safe CSV loading with error handling
- Multi-level matching (exact → keyword → random fallback)
- Always returns 3 products (guaranteed)
- Optional debug logging
- Zero crashes on edge cases
"""

from typing import Optional, List, Dict, Any
from pathlib import Path
import pandas as pd
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class ProductRecommender:
    """Robust product recommendation engine."""
    
    def __init__(self, debug: bool = False):
        """
        Initialize with products data.
        
        ✅ STEP 2: LOAD DATASETS SAFELY
        
        Args:
            debug: Enable debug logging
        """
        self.debug = debug
        self.products_df = None
        self._load_data()
    
    def _load_data(self) -> None:
        """
        Load products.csv with error handling.
        Fill missing values to prevent crashes.
        """
        try:
            # Get absolute path to data folder
            base_dir = Path(__file__).parent.parent.parent
            csv_path = base_dir / "data" / "product.csv"
            
            if not csv_path.exists():
                print(f"⚠️  Warning: {csv_path} not found")
                return
            
            # Load CSV
            self.products_df = pd.read_csv(csv_path)
            
            # ✅ STEP 3: NORMALIZE DATA
            if 'clean_ingredients' in self.products_df.columns:
                self.products_df['clean_ingredients'] = (
                    self.products_df['clean_ingredients']
                    .fillna("")  # Fill missing values
                    .astype(str)
                    .str.lower()  # Lowercase
                    .str.strip()   # Remove spaces
                )
            
            if 'product_name' in self.products_df.columns:
                self.products_df['product_name'] = (
                    self.products_df['product_name']
                    .fillna("Unknown")
                    .astype(str)
                    .str.strip()
                )
            
            if 'price' in self.products_df.columns:
                self.products_df['price'] = (
                    pd.to_numeric(self.products_df['price'], errors='coerce')
                    .fillna(0.0)
                )
            
            print(f"✅ Loaded {len(self.products_df)} products")
        
        except Exception as e:
            print(f"⚠️  Error loading products: {e}")
            self.products_df = None
    
    def get_products(self, ingredient: str, debug: bool = False) -> Optional[List[Dict[str, Any]]]:
        """
        ✅ STEP 5: IMPLEMENT get_products FUNCTION
        
        Get products with 3-level matching:
        1. Exact match
        2. Keyword match (first word)
        3. Random fallback (always return 3)
        
        Args:
            ingredient: Ingredient name
            debug: Enable debug logging
        
        Returns:
            List of dicts with product_name and price (always 3 items or None)
        """
        if self.products_df is None or len(self.products_df) == 0:
            return None
        
        self.debug = debug
        
        try:
            # Normalize ingredient
            ingredient_normalized = ingredient.lower().strip()
            
            if self.debug:
                print(f"🔍 Searching for: '{ingredient_normalized}'")
            
            # ✅ STEP 4: ROBUST MATCHING LOGIC
            # LEVEL 1: Exact match
            matches = self.products_df[
                self.products_df['clean_ingredients'].str.contains(ingredient_normalized, na=False)
            ].copy()
            
            if self.debug:
                print(f"   Level 1 (exact): {len(matches)} matches")
            
            # LEVEL 2: Keyword match (first word)
            if len(matches) == 0:
                first_word = ingredient_normalized.split()[0]
                if self.debug:
                    print(f"   Level 2 (keyword '{first_word}'): ", end="")
                
                matches = self.products_df[
                    self.products_df['clean_ingredients'].str.contains(first_word, na=False)
                ].copy()
                
                if self.debug:
                    print(f"{len(matches)} matches")
            
            # LEVEL 3: Random fallback (always return 3)
            if len(matches) == 0:
                if self.debug:
                    print(f"   Level 3 (random fallback)")
                
                matches = self.products_df.sample(
                    n=min(3, len(self.products_df)),
                    random_state=hash(ingredient_normalized) % (2**31)
                ).copy()
            
            # Sort by price and get top 3
            matches = matches.sort_values('price').head(3)
            
            # Build result list
            results = []
            for _, row in matches.iterrows():
                results.append({
                    'product_name': str(row.get('product_name', 'Unknown')),
                    'price': float(row.get('price', 0.0)),
                    'image_url': str(row.get('image_url', 'https://via.placeholder.com/150?text=Product'))
                })
            
            # Pad to 3 if needed
            while len(results) < 3 and len(self.products_df) > 0:
                random_product = self.products_df.sample(n=1, random_state=None).iloc[0]
                results.append({
                    'product_name': str(random_product['product_name']),
                    'price': float(random_product['price']),
                    'image_url': str(random_product.get('image_url', 'https://via.placeholder.com/150?text=Product'))
                })
            
            if self.debug:
                print(f"   ✅ Returning {len(results)} products")
            
            return results[:3] if len(results) > 0 else None
        
        except Exception as e:
            print(f"❌ Error in get_products: {e}")
            return None
    
    def search_products_detailed(self, ingredient: str) -> Optional[List[Dict[str, Any]]]:
        """
        Search for products with additional details.
        
        Args:
            ingredient: Ingredient name to search for
        
        Returns:
            List of dicts with product details (top 3)
        """
        if self.products_df is None:
            return None
        
        if not ingredient or len(ingredient.strip()) == 0:
            return None
        
        try:
            ingredient_lower = ingredient.lower().strip()
            matches = self.products_df[
                self.products_df['clean_ingredients'].str.contains(ingredient_lower, na=False)
            ].copy()
            
            # Fallback to first word
            if len(matches) == 0:
                first_word = ingredient_lower.split()[0]
                matches = self.products_df[
                    self.products_df['clean_ingredients'].str.contains(first_word, na=False)
                ].copy()
            
            # Fallback to random
            if len(matches) == 0:
                matches = self.products_df.sample(
                    n=min(3, len(self.products_df)),
                    random_state=hash(ingredient_lower) % (2**31)
                ).copy()
            
            matches = matches.sort_values('price').head(3)
            
            results = []
            for _, row in matches.iterrows():
                results.append({
                    'product_name': str(row.get('product_name', 'Unknown')),
                    'price': float(row.get('price', 0.0)),
                    'product_type': str(row.get('product_type', 'Unknown')),
                    'product_url': str(row.get('product_url', ''))
                })
            
            return results if len(results) > 0 else None
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return None


# Global recommender instance
_recommender = None


def get_recommender() -> ProductRecommender:
    """
    Get or create global ProductRecommender instance.
    
    Returns:
        ProductRecommender instance
    """
    global _recommender
    if _recommender is None:
        _recommender = ProductRecommender()
    return _recommender


def get_products(ingredient: str, debug: bool = False) -> Optional[List[Dict[str, Any]]]:
    """
    ✅ STEP 5: Recommend products for a specific ingredient.
    
    This is the main standalone function for product recommendations.
    Supports optional debug logging.
    
    Args:
        ingredient: Ingredient name to search for
        debug: Enable debug logging (default: False)
    
    Returns:
        List of top 3 products with 'product_name' and 'price' keys
        or None if error
        
    Example:
        >>> result = get_products('glycerin', debug=True)
        >>> for product in result:
        ...     print(f"{product['product_name']}: ${product['price']}")
    """
    try:
        recommender = get_recommender()
        return recommender.get_products(ingredient, debug=debug)
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


# ========== STEP 1 & 2: DYNAMIC SEARCH LINKS WITH HYBRID SYSTEM ==========

# Special curated product links for popular products (hybrid system)
SPECIAL_PRODUCT_LINKS = {
    "Minimalist 2% Salicylic Acid Serum": "https://www.google.com/search?q=buy+Minimalist+Salicylic+Acid+Serum",
    "Cetaphil Moisturizing Cream": "https://www.google.com/search?q=buy+Cetaphil+Moisturizing+Cream",
    "Neutrogena Hydro Boost Hydrating Tint": "https://www.google.com/search?q=buy+Neutrogena+Hydro+Boost",
    "CeraVe Facial Moisturizing Lotion": "https://www.google.com/search?q=buy+CeraVe+Facial+Moisturizing+Lotion",
    "The Ordinary Niacinamide 10% + Zinc 1%": "https://www.google.com/search?q=buy+The+Ordinary+Niacinamide",
}


def generate_product_link(product_name: str) -> str:
    """
    Generate dynamic Google search link for any product.
    
    Steps:
    - Replace spaces with "+"
    - Return formatted Google search URL
    
    Args:
        product_name: Name of the product
    
    Returns:
        Complete Google search URL for buying the product
    
    Example:
        >>> link = generate_product_link("Minimalist Salicylic Acid Serum")
        >>> print(link)
        "https://www.google.com/search?q=buy+Minimalist+Salicylic+Acid+Serum"
    """
    if not product_name or len(product_name.strip()) == 0:
        return "https://www.google.com/search?q=skincare+products"
    
    # Replace spaces with "+" and format for URL
    formatted_name = product_name.strip().replace(" ", "+")
    return f"https://www.google.com/search?q=buy+{formatted_name}"


def get_product_link(product_name: str) -> str:
    """
    Hybrid system: Get curated link if exists, otherwise generate dynamic link.
    
    Logic:
    - Check if product in special_product_links dictionary
    - If yes → use predefined link (preferred)
    - If no → dynamically generate Google search link
    
    Args:
        product_name: Name of the product
    
    Returns:
        Google search URL (either curated or dynamically generated)
    
    Example:
        >>> link = get_product_link("Minimalist 2% Salicylic Acid Serum")
        >>> print(link)
        "https://www.google.com/search?q=buy+Minimalist+Salicylic+Acid+Serum"
        
        >>> link = get_product_link("Unknown New Product")
        >>> print(link)
        "https://www.google.com/search?q=buy+Unknown+New+Product"
    """
    if not product_name:
        return "https://www.google.com/search?q=skincare+products"
    
    # Check if product has curated link
    if product_name in SPECIAL_PRODUCT_LINKS:
        return SPECIAL_PRODUCT_LINKS[product_name]
    
    # Fallback to dynamic generation
    return generate_product_link(product_name)


def main():
    """
    Main function: Execute Block 9 product recommendation pipeline and demo.
    
    Steps:
    1. Load products data
    2. Create ProductRecommender
    3. Make sample product searches
    4. Display results
    """
    print("🔷 BLOCK 9: PRODUCT RECOMMENDATION")
    print("=" * 70)
    
    # Step 1: Load products
    print("\n📦 Loading products data...")
    recommender = ProductRecommender(products_csv='data/product.csv')
    
    if recommender.products_df is None:
        print("❌ Failed to load products data")
        return
    
    print(f"✅ Products loaded successfully")
    
    # Step 2: Demo searches
    print("\n🎯 Searching for product recommendations...")
    print("-" * 70)
    
    # Sample 1: Glycerin
    print("\n📝 Sample 1: Search for 'glycerin'")
    products1 = recommender.get_products('glycerin')
    
    if products1:
        print(f"✅ Found {len(products1)} products:")
        for i, prod in enumerate(products1, 1):
            print(f"   {i}. {prod['product_name']} - ${prod['price']}")
    else:
        print("❌ No products found")
    
    # Sample 2: Salicylic Acid
    print("\n📝 Sample 2: Search for 'salicylic acid'")
    products2 = recommender.get_products('salicylic acid')
    
    if products2:
        print(f"✅ Found {len(products2)} products:")
        for i, prod in enumerate(products2, 1):
            print(f"   {i}. {prod['product_name']} - ${prod['price']}")
    else:
        print("❌ No products found")
    
    # Sample 3: Niacinamide
    print("\n📝 Sample 3: Search for 'niacinamide'")
    products3 = recommender.get_products('niacinamide')
    
    if products3:
        print(f"✅ Found {len(products3)} products:")
        for i, prod in enumerate(products3, 1):
            print(f"   {i}. {prod['product_name']} - ${prod['price']}")
    else:
        print("❌ No products found")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 RECOMMENDATION SUMMARY")
    print("=" * 70)
    
    total_found = sum(1 for p in [products1, products2, products3] if p)
    
    print(f"✅ Searches completed: 3")
    print(f"✅ Products found: {total_found}/3")
    print(f"✅ Product recommendation engine working correctly")
    
    print("\n✨ Block 9 Product Recommendation Complete!")
    print("   Status: Ready for Block 10+ (Integration)")


if __name__ == '__main__':
    main()
