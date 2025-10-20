"""
Test Hunyuan3D-2 Shape Generation (TRUE 3D)
This will generate actual 3D geometry from a 2D image
"""
import sys
from pathlib import Path

# Add Hunyuan3D to path
sys.path.insert(0, str(Path(__file__).parent / "Hunyuan3D-2"))

print("=" * 70)
print("Testing Hunyuan3D-2 TRUE 3D Generation")
print("=" * 70)

print("\n1. Importing Hunyuan3D pipeline...")
try:
    from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline
    print("SUCCESS: Hunyuan3D imported")
except Exception as e:
    print(f"ERROR: Failed to import Hunyuan3D: {e}")
    sys.exit(1)

print("\n2. Loading Hunyuan3D-DiT model...")
print("   This will download ~1.1GB on first use...")
try:
    pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(
        'tencent/Hunyuan3D-2',
        subfolder='hunyuan3d-dit-v2-0'
    )
    print("SUCCESS: Model loaded")
except Exception as e:
    print(f"ERROR: Failed to load model: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n3. Generating 3D mesh from test image...")
print("   Using: Hunyuan3D-2/assets/demo.png")

try:
    test_image = Path(__file__).parent / "Hunyuan3D-2" / "assets" / "demo.png"

    if not test_image.exists():
        print(f"ERROR: Test image not found: {test_image}")
        sys.exit(1)

    # Generate 3D mesh
    mesh = pipeline(image=str(test_image))[0]

    print(f"\nSUCCESS: 3D mesh generated!")
    print(f"  Vertices: {len(mesh.vertices)}")
    print(f"  Faces: {len(mesh.faces)}")
    print(f"  Is watertight: {mesh.is_watertight}")

    # Save mesh
    output_dir = Path(__file__).parent / "output" / "hunyuan3d_tests"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "test_output.glb"

    mesh.export(str(output_path))
    print(f"\nSUCCESS: Mesh saved to: {output_path}")

    print("\n" + "=" * 70)
    print("SUCCESS: Hunyuan3D TRUE 3D generation working!")
    print("=" * 70)
    print("\nThis is REAL 3D geometry, not depth-based extrusion!")
    print("Next step: Generate coffee mug with full 360 geometry")

except Exception as e:
    print(f"\nERROR: Generation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
