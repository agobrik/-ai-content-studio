"""
Test PyTorch import and functionality
"""
import sys
from pathlib import Path

print("=" * 60)
print("  AI Content Studio - PyTorch Test")
print("=" * 60)
print()

# Test 1: Import PyTorch
print("[1/4] Testing PyTorch import...")
try:
    import torch
    print("[OK] PyTorch imported successfully")
    print(f"  Version: {torch.__version__}")
except Exception as e:
    print(f"[FAIL] Failed to import PyTorch: {e}")
    sys.exit(1)

# Test 2: CUDA availability
print()
print("[2/4] Testing CUDA availability...")
try:
    cuda_available = torch.cuda.is_available()
    if cuda_available:
        print("[OK] CUDA is available")
        print(f"  Device count: {torch.cuda.device_count()}")
        print(f"  Device name: {torch.cuda.get_device_name(0)}")
        print(f"  CUDA version: {torch.version.cuda}")
    else:
        print("[OK] CUDA not available (will use CPU)")
except Exception as e:
    print(f"[WARN] CUDA check failed: {e}")

# Test 3: Create a simple tensor
print()
print("[3/4] Testing tensor operations...")
try:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tensor = torch.randn(3, 3).to(device)
    result = tensor + tensor
    print(f"[OK] Tensor operations work on {device}")
    print(f"  Tensor shape: {tensor.shape}")
except Exception as e:
    print(f"[FAIL] Tensor operations failed: {e}")
    sys.exit(1)

# Test 4: Import other dependencies
print()
print("[4/4] Testing other AI dependencies...")
try:
    import diffusers
    print(f"[OK] Diffusers imported: {diffusers.__version__}")
except Exception as e:
    print(f"[WARN] Diffusers import failed: {e}")

try:
    import transformers
    print(f"[OK] Transformers imported: {transformers.__version__}")
except Exception as e:
    print(f"[WARN] Transformers import failed: {e}")

try:
    from gtts import gTTS
    print("[OK] gTTS imported successfully")
except Exception as e:
    print(f"[WARN] gTTS import failed: {e}")

try:
    from PyQt6.QtWidgets import QApplication
    print("[OK] PyQt6 imported successfully")
except Exception as e:
    print(f"[WARN] PyQt6 import failed: {e}")

# Summary
print()
print("=" * 60)
print("  Test Complete!")
print("=" * 60)
print()
print("PyTorch is ready for AI Content Studio!")
print()
print("Next steps:")
print("  1. Run: start.bat")
print("  2. Test image generation in the app")
print()
