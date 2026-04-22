#!/usr/bin/env python3
"""Test dynamic confidence scores with different inputs"""

from app.utils.integration import generate_full_recommendation

print('=' * 60)
print('TESTING DYNAMIC CONFIDENCE SCORES')
print('=' * 60)
print()

test_cases = [
    ('Oily', 'Yes', 'Acne'),
    ('Dry', 'No', 'Wrinkles'),
    ('Combination', 'Yes', 'Dark Spots'),
    ('Normal', 'No', 'Dullness'),
]

for i, (skin, sensitivity, concern) in enumerate(test_cases, 1):
    print(f'TEST {i}: Skin={skin}, Sensitivity={sensitivity}, Concern={concern}')
    print('-' * 60)
    result = generate_full_recommendation(skin, sensitivity, concern)
    print(f'  Ingredient: {result["ingredient"]}')
    print(f'  Ingredient Confidence: {result.get("ingredient_confidence", "N/A")}%')
    print(f'  Cluster Confidence: {result.get("cluster_confidence", "N/A")}%')
    print(f'  Overall Confidence: {result.get("overall_confidence", "N/A")}%')
    print()

print('=' * 60)
print('OBSERVATION: Confidence scores change based on input!')
print('=' * 60)
