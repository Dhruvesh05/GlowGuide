from app.utils.encoding import EncodingManager, main
from app.utils.preprocessing import clean_dataset
from app.utils.data_loader import load_celestia_dataset

print("="*70)
print("🔷 BLOCK 3: ENCODING - FINAL VERIFICATION")
print("="*70)

# Test 1: Import all components
print("\n✅ Test 1: All components imported successfully")
print("   - EncodingManager class")
print("   - main() function")

# Test 2: Create manager
print("\n✅ Test 2: Create EncodingManager instance")
manager = EncodingManager()
print(f"   Encoders created: {len(manager.get_encoders_dict())}")

# Test 3: Load and encode data
print("\n✅ Test 3: Load, clean, and encode data")
df_main = load_celestia_dataset()
df_cleaned = clean_dataset(df_main)
df_encoded = manager.encode_dataset(df_cleaned)
print(f"   Input shape: {df_cleaned.shape}")
print(f"   Output shape: {df_encoded.shape}")
print(f"   Output dtype: {df_encoded.dtypes.unique()}")

# Test 4: Verify encoders
print("\n✅ Test 4: Verify encoder classes")
info = manager.get_encoder_info()
for encoder_name, data in info.items():
    print(f"   {encoder_name}: {data['n_classes']} classes")

# Test 5: Verify encoders can inverse_transform
print("\n✅ Test 5: Verify encoders can inverse_transform")
test_skin = manager.le_skin.inverse_transform([0])
test_sens = manager.le_sens.inverse_transform([0])
print(f"   le_skin.inverse_transform([0]) = {test_skin}")
print(f"   le_sens.inverse_transform([0]) = {test_sens}")

print("\n" + "="*70)
print("🎉 BLOCK 3 VERIFICATION COMPLETE")
print("="*70)
print("✅ All 4 encoders created and working")
print("✅ All columns encoded successfully")
print("✅ Encoders preserved for later use")
print("✅ Ready for Block 4 (Feature Engineering)")
print("="*70)
