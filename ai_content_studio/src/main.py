"""
AI Content Studio - Main Application Entry Point
A comprehensive desktop application for AI-powered content creation
"""

import sys
import os
import warnings
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from gui.main_window import MainWindow

# Suppress ONNX runtime warnings (cosmetic issue only)
warnings.filterwarnings('ignore', category=UserWarning, module='diffusers')
warnings.filterwarnings('ignore', message='.*onnxruntime.*')

def setup_paths():
    """Setup necessary paths for the application"""
    base_dir = Path(__file__).parent.parent

    # Create necessary directories
    dirs = [
        base_dir / "models",
        base_dir / "models" / "stable_diffusion",
        base_dir / "models" / "triposr",
        base_dir / "models" / "tts",
        base_dir / "output",
        base_dir / "output" / "images",
        base_dir / "output" / "models_3d",
        base_dir / "output" / "audio",
    ]

    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)

    return base_dir

def main():
    """Main application entry point"""
    print("=" * 60)
    print("AI Content Studio v1.0.0")
    print("High-Quality 2D/3D Generation & Multi-Voice TTS")
    print("=" * 60)
    print("Initializing...")

    # Enable High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    # Setup application paths
    base_dir = setup_paths()

    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("AI Content Studio")
    app.setOrganizationName("AI Content Studio")

    # Create and show main window
    print("Loading UI components...")
    window = MainWindow(base_dir)
    window.show()

    print("Ready! Application started successfully.")
    print("Models will load on-demand when you generate content.")
    print("=" * 60)

    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
