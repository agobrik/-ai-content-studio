"""
Coffee Mug - TRUE 3D Generation with Hunyuan3D
Bu sefer GERÇEK 3D model (360 derece geometri!)
"""
import sys
from pathlib import Path

# Add Hunyuan3D to path
sys.path.insert(0, str(Path(__file__).parent / "Hunyuan3D-2"))

print("=" * 70)
print("Coffee Mug - TRUE 3D Reconstruction with Hunyuan3D-2")
print("=" * 70)

print("\n1. Loading Hunyuan3D-DiT model...")
from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline

pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(
    'tencent/Hunyuan3D-2',
    subfolder='hunyuan3d-dit-v2-0'
)
print("SUCCESS: Model loaded")

# Use the most recent 2D coffee mug image from MiDaS test
print("\n2. Finding recent coffee mug 2D image...")
temp_dir = Path(__file__).parent / "output" / "temp_3d"
if temp_dir.exists():
    images = sorted(temp_dir.glob("sd_image_*.png"))
    if images:
        latest_image = images[-1]
        print(f"Using: {latest_image.name}")
    else:
        print("ERROR: No SD images found")
        sys.exit(1)
else:
    print("ERROR: temp_3d directory not found")
    sys.exit(1)

print("\n3. Generating TRUE 3D mesh from coffee mug image...")
print("   This creates REAL 360-degree geometry, not depth extrusion!")
print("   Processing...")

try:
    # Generate TRUE 3D mesh
    mesh = pipeline(image=str(latest_image))[0]

    print(f"\nSUCCESS: TRUE 3D mesh generated!")
    print(f"  Vertices: {len(mesh.vertices):,}")
    print(f"  Faces: {len(mesh.faces):,}")
    print(f"  Is watertight: {mesh.is_watertight}")

    # Save mesh
    output_dir = Path(__file__).parent / "output" / "models_3d"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "coffee_mug_HUNYUAN3D_TRUE_3D.glb"

    mesh.export(str(output_path))

    print(f"\nSUCCESS: TRUE 3D model saved to:")
    print(f"  {output_path}")

    # Get file size
    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"  File size: {file_size_mb:.2f} MB")

    print("\n" + "=" * 70)
    print("SUCCESS: Coffee Mug TRUE 3D Reconstruction Complete!")
    print("=" * 70)

    print("\nFARK:")
    print("  MiDaS (ESKİ):  Depth-based, düz arka yüz, 2.5D kabartma")
    print("  Hunyuan3D (YENİ): GERÇEK 3D, 360 derece geometri, kulp dahil!")

    print(f"\nModeli aç ve gör:")
    print(f"  Windows 3D Viewer: {output_path}")
    print(f"  Web: https://gltf-viewer.donmccurdy.com/")

except Exception as e:
    print(f"\nERROR: Generation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
