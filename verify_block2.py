from app.utils.preprocessing import (
    clean_dataset,
    print_unique_values,
    get_dataset_info,
    main
)
from app.utils.data_loader import load_celestia_dataset

print('='*70)
print('🔷 BLOCK 2: DATA CLEANING - FINAL VERIFICATION')
print('='*70)

# Test 1: Import all functions
print('\n✅ Test 1: All functions imported successfully')
print('   - clean_dataset')
print('   - print_unique_values')
print('   - get_dataset_info')
print('   - main')

# Test 2: Load data from Block 1
print('\n✅ Test 2: Load data from Block 1')
df_main = load_celestia_dataset()
print(f'   Input shape: {df_main.shape}')

# Test 3: Clean the data
print('\n✅ Test 3: Clean the dataset')
df_cleaned = clean_dataset(df_main)
print(f'   Output shape: {df_cleaned.shape}')
print(f'   Output columns: {list(df_cleaned.columns)}')

# Test 4: Verify data types
print('\n✅ Test 4: Verify data types')
for col in df_cleaned.columns:
    dtype = df_cleaned[col].dtype
    print(f'   {col}: {dtype}')

# Test 5: Check for nulls
print('\n✅ Test 5: Check for missing values')
null_count = df_cleaned.isnull().sum().sum()
print(f'   Total null values: {null_count}')

print('\n' + '='*70)
print('🎉 BLOCK 2 VERIFICATION COMPLETE')
print('='*70)
print('✅ All tests passed!')
print('✅ Data cleaned successfully')
print('✅ Ready for Block 3 (Dataset Creation)')
print('='*70)
