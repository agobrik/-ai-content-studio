"""
Run all tests for AI Content Studio
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def run_all_tests():
    """Run all test scripts"""
    print("\n" + "=" * 70)
    print("AI CONTENT STUDIO - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print("\nThis will test all three main features:")
    print("1. Image Generation (Stable Diffusion)")
    print("2. 3D Model Generation (TripoSR)")
    print("3. Text-to-Speech (Coqui TTS)")
    print("\nNote: This may take 10-20 minutes on first run (downloading models)")
    print("=" * 70)

    input("\nPress Enter to continue or Ctrl+C to cancel...")

    results = {
        "image_generation": False,
        "3d_generation": False,
        "tts_generation": False
    }

    # Test 1: Image Generation
    print("\n\n")
    print("#" * 70)
    print("# TEST 1/3: IMAGE GENERATION")
    print("#" * 70)
    try:
        from test_image_generation import test_image_generation
        image_path = test_image_generation()
        results["image_generation"] = True
    except Exception as e:
        print(f"\n✗ Image generation test failed: {e}")
        image_path = None

    # Test 2: 3D Model Generation
    print("\n\n")
    print("#" * 70)
    print("# TEST 2/3: 3D MODEL GENERATION")
    print("#" * 70)
    try:
        from test_3d_generation import test_3d_generation
        test_3d_generation(image_path=image_path)
        results["3d_generation"] = True
    except Exception as e:
        print(f"\n✗ 3D model generation test failed: {e}")

    # Test 3: Text-to-Speech
    print("\n\n")
    print("#" * 70)
    print("# TEST 3/3: TEXT-TO-SPEECH")
    print("#" * 70)
    try:
        from test_tts import test_tts_generation
        test_tts_generation()
        results["tts_generation"] = True
    except Exception as e:
        print(f"\n✗ TTS generation test failed: {e}")

    # Final summary
    print("\n\n")
    print("=" * 70)
    print("FINAL TEST SUMMARY")
    print("=" * 70)

    passed = sum(results.values())
    total = len(results)

    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name.replace('_', ' ').title()}: {status}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("\nYour AI Content Studio installation is working correctly.")
        print("You can now run the application with: python src/main.py")
        return 0
    else:
        print("\n⚠ SOME TESTS FAILED")
        print("\nPlease check the error messages above and:")
        print("1. Ensure all dependencies are installed")
        print("2. Verify models are downloaded correctly")
        print("3. Check system requirements (GPU, RAM, etc.)")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
