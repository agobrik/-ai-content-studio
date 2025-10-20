#!/usr/bin/env python3
"""
Installation Verification Script
Checks if all components are properly installed
"""

import sys
from pathlib import Path


def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def check_python_version():
    """Check Python version"""
    print_section("Python Version Check")

    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")

    if version.major >= 3 and version.minor >= 9:
        print("✓ Python version is adequate (3.9+)")
        return True
    else:
        print("✗ Python 3.9 or higher is required")
        return False


def check_dependencies():
    """Check if required packages are installed"""
    print_section("Dependency Check")

    required_packages = {
        'PyQt6': 'PyQt6',
        'torch': 'PyTorch',
        'diffusers': 'Diffusers',
        'transformers': 'Transformers',
        'TTS': 'Coqui TTS',
        'trimesh': 'Trimesh',
        'numpy': 'NumPy',
        'PIL': 'Pillow',
    }

    all_installed = True

    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"✓ {name}: Installed")
        except ImportError:
            print(f"✗ {name}: Not installed")
            all_installed = False

    return all_installed


def check_gpu():
    """Check GPU availability"""
    print_section("GPU Check")

    try:
        import torch

        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"✓ GPU Available: {gpu_name}")
            print(f"✓ GPU Memory: {gpu_memory:.2f} GB")
            print(f"✓ CUDA Version: {torch.version.cuda}")
            return True
        else:
            print("! GPU not available (will use CPU)")
            print("  Note: This is OK but will be slower")
            return True
    except Exception as e:
        print(f"✗ Error checking GPU: {e}")
        return False


def check_directory_structure():
    """Check if directory structure is correct"""
    print_section("Directory Structure Check")

    base_dir = Path(__file__).parent

    required_dirs = [
        'src',
        'src/core',
        'src/gui',
        'src/gui/tabs',
        'config',
        'output',
        'output/images',
        'output/models_3d',
        'output/audio',
        'tests',
    ]

    all_exist = True

    for dir_path in required_dirs:
        full_path = base_dir / dir_path
        if full_path.exists():
            print(f"✓ {dir_path}/")
        else:
            print(f"✗ {dir_path}/ - MISSING")
            all_exist = False

    return all_exist


def check_core_files():
    """Check if core files exist"""
    print_section("Core Files Check")

    base_dir = Path(__file__).parent

    required_files = [
        'src/main.py',
        'src/core/image_generator.py',
        'src/core/model_3d_generator.py',
        'src/core/tts_generator.py',
        'src/gui/main_window.py',
        'config/config.yaml',
        'requirements.txt',
        'download_models.py',
        'README.md',
        'LICENSE',
    ]

    all_exist = True

    for file_path in required_files:
        full_path = base_dir / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - MISSING")
            all_exist = False

    return all_exist


def check_models():
    """Check if models are downloaded"""
    print_section("Model Check")

    base_dir = Path(__file__).parent
    models_dir = base_dir / "models"

    model_types = ['stable_diffusion', 'triposr', 'tts']

    if not models_dir.exists():
        print("! Models directory not found")
        print("  Run: python download_models.py")
        return False

    models_downloaded = False

    for model_type in model_types:
        model_path = models_dir / model_type
        if model_path.exists() and any(model_path.iterdir()):
            print(f"✓ {model_type}: Downloaded")
            models_downloaded = True
        else:
            print(f"✗ {model_type}: Not downloaded")

    if not models_downloaded:
        print("\n  To download models, run:")
        print("    python download_models.py")

    return models_downloaded


def main():
    """Main verification function"""
    print("\n" + "=" * 60)
    print("  AI CONTENT STUDIO - INSTALLATION VERIFICATION")
    print("=" * 60)

    checks = {
        "Python Version": check_python_version(),
        "Dependencies": check_dependencies(),
        "GPU": check_gpu(),
        "Directory Structure": check_directory_structure(),
        "Core Files": check_core_files(),
        "Models": check_models(),
    }

    # Summary
    print_section("VERIFICATION SUMMARY")

    passed = sum(checks.values())
    total = len(checks)

    for check_name, result in checks.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{check_name}: {status}")

    print(f"\nTotal: {passed}/{total} checks passed")

    # Recommendations
    if passed == total:
        print("\n" + "=" * 60)
        print("  ✓ ALL CHECKS PASSED!")
        print("=" * 60)
        print("\nYour installation is complete and ready to use.")
        print("\nTo start the application:")
        print("  python src/main.py")
        print("\nOr on Windows:")
        print("  start.bat")
        return 0
    else:
        print("\n" + "=" * 60)
        print("  ! SOME CHECKS FAILED")
        print("=" * 60)
        print("\nPlease address the issues above:")

        if not checks["Python Version"]:
            print("\n1. Install Python 3.9 or higher")
            print("   https://www.python.org/downloads/")

        if not checks["Dependencies"]:
            print("\n2. Install dependencies:")
            print("   pip install -r requirements.txt")

        if not checks["Models"]:
            print("\n3. Download AI models:")
            print("   python download_models.py")

        if not checks["Directory Structure"] or not checks["Core Files"]:
            print("\n4. Ensure all project files are present")
            print("   Re-extract or re-clone the repository")

        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nVerification cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)
