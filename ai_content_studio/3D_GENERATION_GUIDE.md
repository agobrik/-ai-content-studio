# 3D Model Generation Guide

## Overview

The 3D Model Generation system has been **completely rewritten** with advanced AI models and multiple quality tiers.

## What Changed

### Before (Old System)
- ❌ Simple luminosity-based extrusion only
- ❌ Very basic relief/embossed models
- ❌ Poor quality for complex objects
- ❌ No depth estimation

### After (New System)
- ✅ **Three-tier quality system**
- ✅ MiDaS depth estimation (HIGH QUALITY)
- ✅ Advanced mesh generation
- ✅ Proper 3D geometry
- ✅ Automatic method selection
- ✅ Much better results

## Available Methods

### 1. Auto (Recommended)
- Automatically selects the best available method
- Priority: TripoSR > MiDaS > Simple Extrusion

### 2. TripoSR (Best Quality) 🥇
- **State-of-the-art** AI for image-to-3D
- Generates **true 3D geometry** from single images
- Requires: GPU + model download (~1GB)
- **Note**: Complex setup - currently in experimental stage

### 3. MiDaS Depth Estimation (High Quality) 🥈
- **Intel's MiDaS** depth estimation model
- Creates detailed 3D surfaces with realistic depth
- **RECOMMENDED** for best balance of quality and reliability
- Works on both CPU and GPU
- Auto-downloads from PyTorch Hub

### 4. Simple Extrusion (Fast) 🥉
- Basic luminosity-based relief
- Fast, no model download needed
- Good for simple flat designs
- Fallback option

## How It Works

### Text-to-3D Pipeline

```
User Input: "coffee mug"
     ↓
1. Stable Diffusion generates 2D image
     ↓
2. Background removal (optional)
     ↓
3. Selected method creates 3D:
   • MiDaS: Estimates depth map → Creates mesh
   • TripoSR: Direct 3D reconstruction
   • Extrusion: Luminosity → Relief
     ↓
4. Mesh optimization and cleanup
     ↓
5. Export to GLB/OBJ/STL/PLY
```

## Usage Examples

### Example 1: Simple Object (Coffee Mug)

```python
from core.model_3d_generator import Model3DGenerator

generator = Model3DGenerator()

# Generate with MiDaS (recommended)
model_path = generator.generate_from_text(
    prompt="coffee mug",
    method="midas",
    output_format="glb",
    extrusion_depth=0.8  # Thicker 3D effect
)
```

**Output**: High-quality 3D coffee mug with realistic depth

### Example 2: Complex Object

```python
# For complex objects, use higher quality settings
model_path = generator.generate_from_text(
    prompt="vintage typewriter",
    negative_prompt="blurry, low quality, distorted",
    method="auto",  # Will use best available
    output_format="glb"
)
```

### Example 3: Image-to-3D

```python
# Convert existing image to 3D
model_path = generator.generate_from_image(
    image_path="my_image.png",
    method="midas",
    output_format="obj",
    remove_background=True  # Better results
)
```

## Tips for Best Results

### 1. Prompt Engineering
```
✅ GOOD PROMPTS:
- "coffee mug"
- "wooden chair"
- "ceramic vase"
- "metallic trophy"

❌ BAD PROMPTS:
- "kitchen with mug and spoon" (too complex)
- "person holding coffee" (avoid people)
- "cluttered desk scene" (too many objects)
```

### 2. Method Selection
- **Simple objects**: MiDaS works great
- **Product designs**: MiDaS + background removal
- **Organic shapes**: TripoSR (when available)
- **Quick tests**: Simple Extrusion

### 3. Extrusion Depth
- `0.3-0.5`: Subtle depth (coins, medals)
- `0.5-0.8`: Standard depth (most objects)
- `0.8-1.5`: Deep relief (dramatic effect)
- `>1.5`: Very thick (specialized uses)

**Note**: Extrusion depth only applies to MiDaS and Simple Extrusion methods. TripoSR generates true 3D geometry automatically.

## Technical Details

### MiDaS Implementation
- Model: `DPT_Large` (best quality)
- Resolution: Adaptive (up to 512x512)
- Depth map normalization: Min-max to 0-1 range
- Mesh: Vertex grid with triangle faces
- Smoothing: Automatic via trimesh

### Mesh Quality
- Vertex count: ~65K (256x256 resolution)
- Face count: ~130K triangles
- Cleanup: Degenerate faces, duplicates removed
- Normals: Auto-fixed for correct lighting
- File size: 2-5 MB (GLB format)

### Supported Formats
- **GLB**: Best for web/viewers (recommended)
- **OBJ**: Universal 3D software support
- **STL**: 3D printing
- **PLY**: Point cloud tools

## Viewing Your Models

### Windows
- **3D Viewer** (built-in Windows app)
- **Blender** (free, professional)
- **Paint 3D** (simple viewing)

### Online Viewers
- https://gltf-viewer.donmccurdy.com/ (GLB)
- https://3dviewer.net/ (all formats)

### Mobile
- **AR Quick Look** (iOS)
- **Scene Viewer** (Android)

## Troubleshooting

### "Method not available"
- MiDaS requires: `pip install timm`
- Check available methods: `generator.available_methods`

### Low-quality output
1. Try MiDaS method instead of extrusion
2. Use higher extrusion_depth (0.8-1.2)
3. Enable background removal
4. Improve your text prompt

### Model download fails
- MiDaS downloads automatically from PyTorch Hub
- Requires internet connection on first use
- Models cached locally after first download

### Out of memory
- Use CPU instead of GPU: `device="cpu"`
- Reduce image resolution in code
- Close other GPU-intensive applications

## Performance

### MiDaS Generation Times
- **GPU (RTX 3060)**:
  - Text → 2D: ~8-12 seconds
  - 2D → 3D: ~3-5 seconds
  - **Total**: ~15 seconds

- **CPU**:
  - Text → 2D: ~30-60 seconds
  - 2D → 3D: ~10-15 seconds
  - **Total**: ~60 seconds

### Simple Extrusion Times
- 2D → 3D: <1 second (instant)
- No model loading required

## Future Improvements

### Planned
- [ ] Better TripoSR integration
- [ ] Multi-view 3D generation
- [ ] Texture optimization
- [ ] Normal map generation
- [ ] PBR material support

### In Progress
- [x] MiDaS integration ✅
- [x] Multiple method support ✅
- [x] GUI method selection ✅
- [x] Mesh validation ✅

## Examples Gallery

After running the test:
```bash
python tests/test_coffee_mug_3d.py
```

Check `output/models_3d/` for generated models.

## Credits

- **MiDaS**: Intel ISL (Depth Estimation)
- **TripoSR**: Stability AI & Tripo AI
- **Stable Diffusion**: Runway ML / Stability AI
- **trimesh**: Michael Dawson-Haggerty

---

**Last Updated**: 2025-10-16
**System Version**: 2.0 (Complete Rewrite)
