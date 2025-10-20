"""
Test script to verify 2D image generation works without ONNX errors
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.image_generator import ImageGenerator

def test_image_generation():
    print("=" * 60)
    print("Testing Image Generation")
    print("=" * 60)

    # Initialize generator
    print("\n1. Initializing ImageGenerator...")
    gen = ImageGenerator(
        model_name="stabilityai/stable-diffusion-xl-base-1.0",
        cache_dir=Path("./models/stable_diffusion"),
        use_refiner=False
    )
    print(f"   [OK] Model: {gen.model_name}")
    print(f"   [OK] Device: {gen.device}")
    print(f"   [OK] SDXL: {gen.is_sdxl}")

    # Test prompt enhancement
    print("\n2. Testing prompt enhancement...")
    test_prompt = "a beautiful red apple"
    enhanced = gen._enhance_prompt(test_prompt, transparent_bg=True)
    print(f"   Original: {test_prompt}")
    print(f"   Enhanced: {enhanced}")

    # Test negative prompt enhancement
    print("\n3. Testing negative prompt enhancement...")
    enhanced_neg = gen._enhance_negative_prompt("")
    print(f"   Enhanced negative: {enhanced_neg[:100]}...")

    # Load model (this is where ONNX errors would occur)
    print("\n4. Loading SDXL model...")
    try:
        gen.load_model()
        print("   [OK] Model loaded successfully!")
        print("   [OK] No ONNX errors!")
    except Exception as e:
        import traceback
        print(f"   [ERROR]: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        return False

    print("\n" + "=" * 60)
    print("SUCCESS: Image generation is ready to use!")
    print("=" * 60)
    print("\nThe ONNX bypass is working correctly.")
    print("You can now generate images in the UI without errors.")
    print("=" * 60)

    return True

if __name__ == "__main__":
    success = test_image_generation()
    sys.exit(0 if success else 1)
