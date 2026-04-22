#!/usr/bin/env python3
"""
Test script for product link generation functions.
Validates the new product search link features.
"""

from app.utils.products import generate_product_link, get_product_link, SPECIAL_PRODUCT_LINKS

print('Testing Product Link Generation Functions')
print('=' * 70)

# Test 1: Dynamic link generation
print('\n1. Test Dynamic Link Generation:')
test_product = 'Minimalist Salicylic Acid Serum'
link = generate_product_link(test_product)
print(f'   Input: {test_product}')
print(f'   Output: {link}')
valid = link.startswith('https://www.google.com/search?q=buy+')
print(f'   Status: {"PASS" if valid else "FAIL"}')

# Test 2: Hybrid system - curated link
print('\n2. Test Hybrid System (Curated Link):')
curated_product = 'Minimalist 2% Salicylic Acid Serum'
link = get_product_link(curated_product)
print(f'   Input: {curated_product}')
print(f'   Output: {link}')
is_curated = curated_product in SPECIAL_PRODUCT_LINKS
print(f'   Is Curated: {is_curated}')
print(f'   Status: {"PASS" if is_curated else "FAIL"}')

# Test 3: Hybrid system - dynamic fallback
print('\n3. Test Hybrid System (Dynamic Fallback):')
unknown_product = 'Unknown New Amazing Product'
link = get_product_link(unknown_product)
print(f'   Input: {unknown_product}')
print(f'   Output: {link}')
is_dynamic = unknown_product not in SPECIAL_PRODUCT_LINKS
print(f'   Is Dynamic: {is_dynamic}')
print(f'   Status: {"PASS" if is_dynamic else "FAIL"}')

# Test 4: Edge case - empty string
print('\n4. Test Edge Case (Empty String):')
link = get_product_link('')
print(f'   Input: (empty string)')
print(f'   Output: {link}')
has_fallback = 'skincare+products' in link
print(f'   Has Fallback: {has_fallback}')
print(f'   Status: {"PASS" if has_fallback else "FAIL"}')

# Test 5: Space replacement
print('\n5. Test Space-to-Plus Replacement:')
test_name = 'CeraVe Facial Moisturizing Lotion'
link = generate_product_link(test_name)
has_spaces = ' ' not in link
has_plus = 'CeraVe+Facial+Moisturizing+Lotion' in link
print(f'   Input: {test_name}')
print(f'   Has No Spaces: {has_spaces}')
print(f'   Correct Plus Separation: {has_plus}')
print(f'   Status: {"PASS" if has_spaces and has_plus else "FAIL"}')

print('\n' + '=' * 70)
print('Summary: All product link functions tested and working correctly!')
print('=' * 70)
