"""
Test script for Image Generation
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.image_generator import ImageGenerator


def test_image_generation():
    """Test basic image generation"""
    print("=" * 70)
    print("Testing Image Generation (Stable Diffusion)")
    print("=" * 70)

    # Initialize generator
    base_dir = Path(__file__).parent.parent
    cache_dir = base_dir / "models" / "stable_diffusion"

    print("\n1. Initializing Image Generator...")
    generator = ImageGenerator(
        model_name="stabilityai/stable-diffusion-2-1",
        cache_dir=cache_dir
    )

    print("\n2. Loading model...")
    generator.load_model()

    print("\n3. Generating test image...")
    prompt = "A beautiful landscape with mountains and a lake at sunset, highly detailed, 4k"
    negative_prompt = "blurry, low quality, distorted"

    output_dir = base_dir / "output" / "images"
    output_dir.mkdir(parents=True, exist_ok=True)

    image_path = generator.generate(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=30,  # Using fewer steps for faster testing
        guidance_scale=7.5,
        width=512,
        height=512,
        output_dir=output_dir
    )

    print(f"\n✓ Test completed successfully!")
    print(f"✓ Image saved to: {image_path}")
    print(f"\nPlease verify:")
    print(f"1. Image file exists at the specified path")
    print(f"2. Image matches the prompt description")
    print(f"3. Image quality is acceptable")

    return image_path


if __name__ == "__main__":
    try:
        test_image_generation()
        print("\n" + "=" * 70)
        print("IMAGE GENERATION TEST: PASSED")
        print("=" * 70)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        print("\n" + "=" * 70)
        print("IMAGE GENERATION TEST: FAILED")
        print("=" * 70)
        sys.exit(1)
