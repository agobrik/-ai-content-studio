# AI Content Studio

A production-ready desktop application that integrates three powerful AI tools for content creation:
- **Stable Diffusion** - Generate stunning 2D images from text prompts
- **TripoSR** - Convert 2D images into 3D models
- **Coqui TTS (XTTS-v2)** - Multilingual text-to-speech with 23 language support

## Features

### 2D Image Generation
- Text-to-image generation using Stable Diffusion
- Support for multiple models (SD 1.5, SD 2.1, SDXL)
- Customizable generation parameters (steps, guidance scale, resolution)
- Batch generation support
- Export as PNG or JPEG

### 3D Model Generation
- Convert any 2D image to a 3D model
- Powered by TripoSR technology
- Export in multiple formats: GLB, OBJ, STL
- Compatible with Blender, 3D printers, and game engines

### Text-to-Speech
- Support for 23 languages including English, Spanish, French, German, Turkish, Arabic, Chinese, Japanese, and more
- Natural-sounding voices with emotion control
- Adjustable speech speed
- Voice cloning with reference audio
- Export as WAV or MP3

### Additional Features
- **Offline Operation** - All models run locally after initial download
- **GPU Acceleration** - Automatic GPU detection and utilization
- **Model Management** - Easy download and management of AI models
- **User-Friendly Interface** - Clean, intuitive PyQt6-based GUI
- **Progress Tracking** - Real-time progress bars for all operations

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **RAM**: 8 GB (16 GB recommended)
- **Storage**: 20 GB free space (for models and outputs)
- **Python**: 3.9 or higher

### Recommended Requirements
- **GPU**: NVIDIA GPU with 6+ GB VRAM (for faster generation)
- **RAM**: 16 GB or more
- **Storage**: 50 GB free space
- **CUDA**: 11.8 or higher (for GPU acceleration)

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/ai_content_studio.git
cd ai_content_studio
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note for Windows users**: If you have an NVIDIA GPU, install PyTorch with CUDA support:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Step 4: Download AI Models
Run the automated model download script:
```bash
python download_models.py
```

This will download:
- Stable Diffusion models (~5-10 GB)
- TripoSR models (~1-2 GB)
- TTS models (~2-3 GB)

**Options:**
```bash
# Download specific model only
python download_models.py --model sd    # Stable Diffusion only
python download_models.py --model 3d    # TripoSR only
python download_models.py --model tts   # TTS only

# Download all models (default)
python download_models.py --model all
```

### Step 5: Launch the Application
```bash
python src/main.py
```

## Usage Guide

### Generating 2D Images
1. Navigate to the "2D Image Generation" tab
2. Enter your prompt (e.g., "A beautiful sunset over mountains")
3. Optionally add a negative prompt to avoid unwanted elements
4. Adjust generation parameters:
   - **Steps**: 20-50 for quick results, 50-100 for higher quality
   - **Guidance Scale**: 7-15 (higher = more prompt adherence)
   - **Resolution**: 512x512 (fast) to 1024x1024 (high quality)
5. Click "Generate Image"
6. Save or use the image for 3D generation

### Creating 3D Models
1. Navigate to the "3D Model Generation" tab
2. Upload an image or use one generated in the previous tab
3. Select export format (GLB recommended for most uses)
4. Click "Generate 3D Model"
5. Save the model or open the output folder

### Generating Speech
1. Navigate to the "Text-to-Speech" tab
2. Enter or paste your text
3. Select language from the dropdown
4. Adjust speech speed if needed
5. (Optional) Upload reference audio for voice cloning
6. Select output format (WAV or MP3)
7. Click "Generate Speech"
8. Use playback controls to preview
9. Save the audio file

### Managing Models
1. Go to the "Settings" tab
2. Check installed models with "Check Installed Models"
3. Download additional models as needed
4. View system information and GPU status

## Troubleshooting

### GPU Not Detected
- Ensure NVIDIA drivers are up to date
- Install CUDA toolkit (11.8 or higher)
- Reinstall PyTorch with CUDA support

### Out of Memory Errors
- Reduce image resolution
- Close other applications
- Use CPU mode in Settings (slower but uses less VRAM)

### Model Download Failures
- Check internet connection
- Try downloading models one at a time
- Manually download from HuggingFace and place in `models/` directory

### Slow Generation
- Enable GPU in Settings
- Reduce number of inference steps
- Use lower resolution settings
- Close background applications

## File Structure

```
ai_content_studio/
├── src/
│   ├── main.py                 # Application entry point
│   ├── core/                   # Core AI modules
│   │   ├── image_generator.py
│   │   ├── model_3d_generator.py
│   │   └── tts_generator.py
│   └── gui/                    # GUI components
│       ├── main_window.py
│       └── tabs/
│           ├── image_generation_tab.py
│           ├── model_3d_generation_tab.py
│           ├── tts_tab.py
│           └── settings_tab.py
├── config/
│   └── config.yaml             # Configuration file
├── models/                     # Cached AI models
├── output/                     # Generated content
│   ├── images/
│   ├── models_3d/
│   └── audio/
├── requirements.txt            # Python dependencies
├── download_models.py          # Model download script
└── README.md                   # This file
```

## Licenses

This application uses several open-source components:

- **Stable Diffusion**: CreativeML Open RAIL-M License
- **TripoSR**: MIT License
- **Coqui TTS**: Mozilla Public License 2.0
- **PyQt6**: GPL v3
- **PyTorch**: BSD-style License
- **Transformers**: Apache 2.0
- **Diffusers**: Apache 2.0

See the LICENSE file for complete information.

## Known Limitations

- TripoSR may use a simplified fallback mode if the full model fails to load
- Voice cloning requires high-quality reference audio (at least 6 seconds)
- Very long text may need to be split for TTS generation
- 3D models are optimized for visualization, may need refinement for 3D printing

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## Support

For issues, questions, or feature requests:
1. Check the Troubleshooting section
2. Search existing GitHub issues
3. Create a new issue with detailed information

## Roadmap

Future enhancements planned:
- [ ] Real-time 3D model preview
- [ ] Batch processing for all features
- [ ] Custom model fine-tuning
- [ ] Cloud backup integration
- [ ] Animation support for 3D models
- [ ] More TTS voice options

## Credits

Developed using:
- Stable Diffusion by Stability AI
- TripoSR by Stability AI
- Coqui TTS by Coqui
- PyQt6 for the GUI framework

## License

MIT License - See LICENSE file for details

---

**Version**: 1.0.0
**Last Updated**: 2024

For more information, visit the [documentation](docs/) or [GitHub repository](https://github.com/yourusername/ai_content_studio).
