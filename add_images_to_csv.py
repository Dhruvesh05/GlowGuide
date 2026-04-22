#!/usr/bin/env python3
"""
Script to add image_url column to products.csv
Uses placeholder images for all products
"""

import pandas as pd
from pathlib import Path

# Get the data directory
base_dir = Path(__file__).parent
csv_path = base_dir / "data" / "product.csv"

print("Loading products.csv...")
df = pd.read_csv(csv_path)

print(f"Current columns: {list(df.columns)}")
print(f"Total products: {len(df)}")

# Check if image_url column already exists
if 'image_url' not in df.columns:
    print("\nAdding image_url column...")
    
    # Generate placeholder image URLs
    # Using placeholder service that generates product-like images
    def generate_image_url(product_name: str, idx: int) -> str:
        """Generate placeholder image URL for product"""
        # Using a placeholder image service
        # This generates images with the product category
        product_type = product_name.split()[0][:20]  # First few words as identifier
        
        # Use a simple placeholder pattern
        # This creates unique images based on product index
        color_code = str(abs(hash(product_name)) % 360)  # Generate color based on name
        return f"https://via.placeholder.com/150?text={product_name[:15]}"
    
    # Add image_url column
    df['image_url'] = [generate_image_url(name, idx) for idx, name in enumerate(df['product_name'])]
    
    print("Saving updated CSV...")
    df.to_csv(csv_path, index=False)
    
    print(f"✅ Successfully added image_url column!")
    print(f"New columns: {list(df.columns)}")
    print(f"\nSample image URLs:")
    for i in range(min(3, len(df))):
        print(f"  {df['product_name'].iloc[i]}: {df['image_url'].iloc[i]}")
else:
    print("✅ image_url column already exists!")
    print(f"Sample image URLs:")
    for i in range(min(3, len(df))):
        print(f"  {df['product_name'].iloc[i]}: {df['image_url'].iloc[i]}")

print("\nDone!")
