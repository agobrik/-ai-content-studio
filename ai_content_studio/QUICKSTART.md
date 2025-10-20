# Quick Start Guide

Get AI Content Studio up and running in 5 steps!

## Step 1: Install Python (if not already installed)

Download and install Python 3.9 or higher from [python.org](https://www.python.org/downloads/)

Verify installation:
```bash
python --version
```

## Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**For GPU users (NVIDIA):**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## Step 4: Download AI Models

```bash
python download_models.py
```

This downloads:
- Stable Diffusion (~5-10 GB)
- TripoSR (~1-2 GB)
- TTS Models (~2-3 GB)

Takes 10-30 minutes depending on internet speed.

## Step 5: Launch the App

```bash
# Windows
python src\main.py
# or double-click start.bat

# macOS/Linux
python src/main.py
# or run: bash start.sh
```

## First-Time Usage

### Generate Your First Image
1. Go to "2D Image Generation" tab
2. Enter prompt: "A beautiful landscape with mountains"
3. Click "Generate Image"
4. Wait 30-60 seconds
5. Save or use for 3D generation

### Create Your First 3D Model
1. Go to "3D Model Generation" tab
2. Upload an image or use generated one
3. Select format: GLB
4. Click "Generate 3D Model"
5. Open in Blender or 3D viewer

### Generate Your First Speech
1. Go to "Text-to-Speech" tab
2. Enter text: "Hello, welcome to AI Content Studio"
3. Select language: English
4. Click "Generate Speech"
5. Play and save

## Troubleshooting

**Problem**: Models not downloading
- Check internet connection
- Try downloading one model at a time
- Use `python download_models.py --model sd` for Stable Diffusion only

**Problem**: GPU not detected
- Update NVIDIA drivers
- Install CUDA 11.8+
- Reinstall PyTorch with CUDA

**Problem**: Out of memory
- Reduce image resolution (512x512)
- Use fewer inference steps (20-30)
- Switch to CPU in Settings

**Problem**: Slow performance
- Enable GPU in Settings
- Close other applications
- Use lower quality settings

## Need Help?

- Read the full [README.md](README.md)
- Check [GitHub Issues](https://github.com/yourusername/ai_content_studio/issues)
- Review the [LICENSE](LICENSE) file

## System Check

Run tests to verify everything works:
```bash
python tests/run_all_tests.py
```

This tests all three features and shows what's working.

## Tips for Best Results

**Images:**
- Use detailed prompts (20-50 words)
- Include style keywords: "photorealistic", "oil painting", "digital art"
- Use negative prompts to avoid unwanted elements
- Start with 512x512, increase for final output

**3D Models:**
- Use clear images with good lighting
- Simple objects work better than complex scenes
- GLB format is most compatible
- OBJ format better for editing in 3D software

**Speech:**
- Write naturally (contractions, punctuation)
- Split very long text into paragraphs
- Reference audio should be clear (6+ seconds)
- Experiment with speed (0.8-1.2x recommended)

## Quick Commands Reference

```bash
# Download all models
python download_models.py

# Download specific model
python download_models.py --model sd   # Stable Diffusion
python download_models.py --model 3d   # TripoSR
python download_models.py --model tts  # Text-to-Speech

# Run application
python src/main.py

# Run tests
python tests/run_all_tests.py
python tests/test_image_generation.py
python tests/test_3d_generation.py
python tests/test_tts.py
```

## What's Next?

After getting comfortable with the basics:
1. Experiment with different models in Settings
2. Try batch generation for multiple outputs
3. Use voice cloning with reference audio
4. Export 3D models in different formats
5. Customize settings in `config/config.yaml`

Enjoy creating with AI Content Studio!
