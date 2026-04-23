#!/usr/bin/env python3
"""
GlowGuide Deployment Verification Script

Verifies that all required files are in place for Streamlit Cloud deployment.
Run this before pushing to GitHub to ensure everything is correct.

Usage:
    python VERIFY_DEPLOYMENT.py
"""

import sys
from pathlib import Path
import os

def check_file_exists(path, file_type="file"):
    """Check if a file or directory exists."""
    if path.exists():
        if file_type == "file":
            size = path.stat().st_size / 1024  # KB
            return True, f"✅ {path} ({size:.1f} KB)"
        else:
            return True, f"✅ {path}/"
    else:
        return False, f"❌ {path} (missing)"

def main():
    """Run verification checks."""
    print("\n" + "="*70)
    print("🔍 GLOWGUIDE DEPLOYMENT VERIFICATION")
    print("="*70)
    
    base_dir = Path(__file__).parent
    all_ok = True
    
    # Check folder structure
    print("\n📁 FOLDER STRUCTURE:")
    print("-" * 70)
    
    folders = ["app", "data", "models"]
    for folder in folders:
        ok, msg = check_file_exists(base_dir / folder, "directory")
        print(msg)
        if not ok:
            all_ok = False
    
    # Check .gitignore
    print("\n📋 .GITIGNORE:")
    print("-" * 70)
    gitignore_path = base_dir / ".gitignore"
    ok, msg = check_file_exists(gitignore_path, "file")
    print(msg)
    
    if gitignore_path.exists():
        content = gitignore_path.read_text()
        blocking_patterns = ["*.pkl", "*.csv"]
        bad_lines = [line for line in content.split('\n') if any(p in line for p in blocking_patterns)]
        
        if bad_lines:
            print(f"⚠️  WARNING: .gitignore blocks model/data files:")
            for line in bad_lines:
                print(f"   {line}")
            all_ok = False
        else:
            print("✅ .gitignore allows data and model files")
    
    # Check data files
    print("\n📊 DATA FILES (data/):")
    print("-" * 70)
    required_data = ["celestia_clean.csv", "product.csv", "remedies.csv"]
    data_ok = True
    for filename in required_data:
        ok, msg = check_file_exists(base_dir / "data" / filename)
        print(msg)
        if not ok:
            data_ok = False
            all_ok = False
    
    if data_ok:
        print("✅ All required data files present")
    
    # Check model files
    print("\n🤖 MODEL FILES (models/):")
    print("-" * 70)
    required_models = [
        "knn_model.pkl",
        "kmeans_model.pkl",
        "le_skin.pkl",
        "le_sens.pkl",
        "le_concern.pkl",
        "le_target.pkl"
    ]
    models_ok = True
    for filename in required_models:
        ok, msg = check_file_exists(base_dir / "models" / filename)
        print(msg)
        if not ok:
            models_ok = False
            all_ok = False
    
    if models_ok:
        print("✅ All required model files present")
    
    # Check key Python files
    print("\n🐍 PYTHON FILES:")
    print("-" * 70)
    key_files = [
        "app/app.py",
        "app/utils/model_loader.py",
        "app/utils/data_loader.py"
    ]
    for filepath in key_files:
        ok, msg = check_file_exists(base_dir / filepath)
        print(msg)
        if not ok:
            all_ok = False
    
    # Check requirements
    print("\n📦 REQUIREMENTS:")
    print("-" * 70)
    ok, msg = check_file_exists(base_dir / "requirements.txt")
    print(msg)
    if not ok:
        all_ok = False
    
    # Verify app.py has verification function
    print("\n🔐 CODE VERIFICATION:")
    print("-" * 70)
    app_py = base_dir / "app" / "app.py"
    if app_py.exists():
        try:
            content = app_py.read_text(encoding='utf-8', errors='ignore')
            if "verify_required_files" in content:
                print("✅ app.py has verify_required_files() function")
            else:
                print("⚠️  app.py missing verify_required_files() function")
        except Exception as e:
            print(f"⚠️  Could not read app.py: {e}")
    
    # Check model_loader points to correct directory
    model_loader = base_dir / "app" / "utils" / "model_loader.py"
    if model_loader.exists():
        try:
            content = model_loader.read_text(encoding='utf-8', errors='ignore')
            if 'base_dir / "models"' in content:
                print("✅ model_loader.py loads from models/ directory")
            else:
                print("⚠️  model_loader.py may not load from correct directory")
        except Exception as e:
            print(f"⚠️  Could not read model_loader.py: {e}")
    
    # Final summary
    print("\n" + "="*70)
    if all_ok:
        print("✅ DEPLOYMENT READY!")
        print("="*70)
        print("\n✨ All checks passed. You can safely:")
        print("   1. git add data/ models/")
        print("   2. git commit -m 'Add data and models'")
        print("   3. git push origin main")
        print("   4. Deploy to Streamlit Cloud")
        return 0
    else:
        print("❌ DEPLOYMENT NOT READY")
        print("="*70)
        print("\n⚠️  Fix issues above before deploying!")
        print("\nSee DEPLOYMENT_GUIDE.md for troubleshooting help.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
