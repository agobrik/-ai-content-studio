"""
Test script for Coffee Mug 3D Generation
This tests the full pipeline: Text -> 2D Image -> 3D Model
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.model_3d_generator import Model3DGenerator


def test_coffee_mug_3d():
    """Test 3D model generation for a simple coffee mug"""
    print("=" * 70)
    print("Testing Coffee Mug 3D Generation")
    print("=" * 70)

    # Initialize generator
    base_dir = Path(__file__).parent.parent
    cache_dir = base_dir / "models" / "3d_cache"
    output_dir = base_dir / "output" / "models_3d"

    print("\n1. Initializing 3D Model Generator...")
    generator = Model3DGenerator(cache_dir=cache_dir)

    print(f"\n2. Available methods: {generator.available_methods}")

    # Test with simple prompt
    prompt = "coffee mug"

    print(f"\n3. Generating 3D model from prompt: '{prompt}'")
    print("   This will:")
    print("   - Step 1: Generate a 2D image using Stable Diffusion")
    print("   - Step 2: Convert 2D image to 3D using best available method")
    print()

    try:
        # Generate with MiDaS (best quality available without complex setup)
        model_path = generator.generate_from_text(
            prompt=prompt,
            negative_prompt="blurry, low quality, distorted, multiple objects",
            output_format="glb",
            output_dir=output_dir,
            method="midas",  # Use MiDaS for reliable quality
            extrusion_depth=0.8  # Higher depth for better 3D effect
        )

        print(f"\nSUCCESS: Test completed!")
        print(f"SUCCESS: 3D model saved to: {model_path}")
        print(f"\n" + "=" * 70)
        print("SUCCESS: Coffee mug 3D model generated!")
        print("=" * 70)
        print(f"\nTo view the model:")
        print(f"1. Open Windows 3D Viewer")
        print(f"2. Open file: {model_path}")
        print(f"3. Or drag and drop to https://gltf-viewer.donmccurdy.com/")

        return model_path

    except Exception as e:
        print(f"\nFAILED: Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        print("\n" + "=" * 70)
        print("FAILED: Coffee mug 3D model generation")
        print("=" * 70)
        return None


if __name__ == "__main__":
    result = test_coffee_mug_3d()
    sys.exit(0 if result else 1)
