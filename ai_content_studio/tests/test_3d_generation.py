"""
Test script for 3D Model Generation
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.model_3d_generator import Model3DGenerator


def test_3d_generation(image_path=None):
    """Test 3D model generation"""
    print("=" * 70)
    print("Testing 3D Model Generation (TripoSR)")
    print("=" * 70)

    # Initialize generator
    base_dir = Path(__file__).parent.parent
    cache_dir = base_dir / "models" / "triposr"

    # Use test image or provided image
    if image_path is None:
        # Look for any image in output folder
        output_images = base_dir / "output" / "images"
        images = list(output_images.glob("*.png"))
        if not images:
            print("\n✗ No test images found!")
            print("Please run test_image_generation.py first or provide an image path")
            return None

        image_path = str(images[0])
        print(f"\n1. Using test image: {Path(image_path).name}")
    else:
        print(f"\n1. Using provided image: {Path(image_path).name}")

    print("\n2. Initializing 3D Model Generator...")
    generator = Model3DGenerator(cache_dir=cache_dir)

    print("\n3. Loading model...")
    generator.load_model()

    print("\n4. Generating 3D model...")
    output_dir = base_dir / "output" / "models_3d"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Test GLB export
    model_path = generator.generate(
        image_path=image_path,
        output_format="glb",
        output_dir=output_dir
    )

    print(f"\n✓ Test completed successfully!")
    print(f"✓ 3D model saved to: {model_path}")
    print(f"\nPlease verify:")
    print(f"1. Model file exists at the specified path")
    print(f"2. Model can be opened in a 3D viewer (Blender, Windows 3D Viewer)")
    print(f"3. Model represents the input image")

    return model_path


if __name__ == "__main__":
    try:
        test_3d_generation()
        print("\n" + "=" * 70)
        print("3D MODEL GENERATION TEST: PASSED")
        print("=" * 70)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        print("\n" + "=" * 70)
        print("3D MODEL GENERATION TEST: FAILED")
        print("=" * 70)
        sys.exit(1)
