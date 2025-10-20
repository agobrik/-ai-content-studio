#!/usr/bin/env python3
"""
Model Download Script
Automated script to download and cache all AI models
"""

import sys
import argparse
from pathlib import Path
import torch


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def check_gpu():
    """Check GPU availability"""
    print_header("Hardware Detection")

    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        print(f"✓ GPU Available: {gpu_name}")
        print(f"✓ GPU Memory: {gpu_memory:.2f} GB")
        return True
    else:
        print("! No GPU detected - models will run on CPU")
        print("  (This will be slower but still functional)")
        return False


def download_stable_diffusion(base_dir: Path):
    """Download Stable Diffusion models"""
    print_header("Downloading Stable Diffusion Models")

    try:
        sys.path.insert(0, str(base_dir / "src"))
        from core.image_generator import ImageGenerator

        cache_dir = base_dir / "models" / "stable_diffusion"
        cache_dir.mkdir(parents=True, exist_ok=True)

        print("Downloading: stabilityai/stable-diffusion-2-1")
        print("This may take several minutes...")

        generator = ImageGenerator(
            model_name="stabilityai/stable-diffusion-2-1",
            cache_dir=cache_dir
        )
        generator.load_model()

        print("\n✓ Stable Diffusion models downloaded successfully!")
        return True

    except Exception as e:
        print(f"\n✗ Error downloading Stable Diffusion: {e}")
        return False


def download_triposr(base_dir: Path):
    """Download TripoSR models"""
    print_header("Downloading TripoSR Models")

    try:
        sys.path.insert(0, str(base_dir / "src"))
        from core.model_3d_generator import Model3DGenerator

        cache_dir = base_dir / "models" / "triposr"
        cache_dir.mkdir(parents=True, exist_ok=True)

        print("Downloading: stabilityai/TripoSR")
        print("This may take several minutes...")

        generator = Model3DGenerator(cache_dir=cache_dir)
        generator.load_model()

        print("\n✓ TripoSR models downloaded successfully!")
        return True

    except Exception as e:
        print(f"\n✗ Error downloading TripoSR: {e}")
        print("  (TripoSR will use fallback mode)")
        return True  # Non-critical error


def download_tts(base_dir: Path):
    """Download TTS models"""
    print_header("Downloading Text-to-Speech Models")

    try:
        sys.path.insert(0, str(base_dir / "src"))
        from core.tts_generator import TTSGenerator

        cache_dir = base_dir / "models" / "tts"
        cache_dir.mkdir(parents=True, exist_ok=True)

        print("Downloading: XTTS-v2 (Multilingual TTS)")
        print("This may take several minutes...")

        generator = TTSGenerator(cache_dir=cache_dir)
        generator.load_model()

        print("\n✓ TTS models downloaded successfully!")
        return True

    except Exception as e:
        print(f"\n✗ Error downloading TTS: {e}")
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Download AI models for AI Content Studio"
    )
    parser.add_argument(
        "--model",
        choices=["all", "sd", "3d", "tts"],
        default="all",
        help="Which model(s) to download (default: all)"
    )
    parser.add_argument(
        "--skip-gpu-check",
        action="store_true",
        help="Skip GPU availability check"
    )

    args = parser.parse_args()

    print_header("AI Content Studio - Model Download Script")
    print("This script will download and cache AI models for offline use.")
    print("Make sure you have a stable internet connection.")

    # Get base directory
    base_dir = Path(__file__).parent.absolute()
    print(f"\nBase directory: {base_dir}")

    # Check GPU
    if not args.skip_gpu_check:
        check_gpu()

    # Track success
    success = True

    # Download models based on selection
    if args.model in ["all", "sd"]:
        if not download_stable_diffusion(base_dir):
            success = False

    if args.model in ["all", "3d"]:
        if not download_triposr(base_dir):
            pass  # Non-critical

    if args.model in ["all", "tts"]:
        if not download_tts(base_dir):
            success = False

    # Final summary
    print_header("Download Summary")

    if success:
        print("✓ All models downloaded successfully!")
        print("\nYou can now run the application offline.")
        print("To start the application, run:")
        print("  python src/main.py")
    else:
        print("! Some models failed to download.")
        print("  Please check the error messages above.")
        print("  You can try again later or run the app with limited functionality.")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
