"""
Settings Tab - Application configuration
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QGroupBox, QFileDialog, QLineEdit, QTextEdit,
    QCheckBox, QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from pathlib import Path

try:
    import torch
    TORCH_AVAILABLE = True
except Exception as e:
    print(f"PyTorch not available: {e}")
    TORCH_AVAILABLE = False
    torch = None


class ModelDownloadWorker(QThread):
    """Worker thread for model download"""
    finished = pyqtSignal()
    error = pyqtSignal(str)
    progress = pyqtSignal(str)  # progress_message

    def __init__(self, model_type, base_dir):
        super().__init__()
        self.model_type = model_type
        self.base_dir = base_dir

    def run(self):
        """Download and verify models"""
        try:
            if self.model_type == "stable_diffusion":
                self.download_stable_diffusion()
            elif self.model_type == "triposr":
                self.download_triposr()
            elif self.model_type == "tts":
                self.download_tts()
            elif self.model_type == "all":
                self.download_stable_diffusion()
                self.download_triposr()
                self.download_tts()

            self.finished.emit()

        except Exception as e:
            self.error.emit(str(e))

    def download_stable_diffusion(self):
        """Download Stable Diffusion models"""
        self.progress.emit("Downloading Stable Diffusion models...")

        from core.image_generator import ImageGenerator

        cache_dir = self.base_dir / "models" / "stable_diffusion"
        generator = ImageGenerator(
            model_name="stabilityai/stable-diffusion-2-1",
            cache_dir=cache_dir
        )
        generator.load_model()

        self.progress.emit("Stable Diffusion models downloaded successfully")

    def download_triposr(self):
        """Download TripoSR models"""
        self.progress.emit("Downloading TripoSR models...")

        from core.model_3d_generator import Model3DGenerator

        cache_dir = self.base_dir / "models" / "triposr"
        generator = Model3DGenerator(cache_dir=cache_dir)
        generator.load_model()

        self.progress.emit("TripoSR models downloaded successfully")

    def download_tts(self):
        """Download TTS models"""
        self.progress.emit("Downloading TTS models...")

        from core.tts_generator import TTSGenerator

        cache_dir = self.base_dir / "models" / "tts"
        generator = TTSGenerator(cache_dir=cache_dir)
        generator.load_model()

        self.progress.emit("TTS models downloaded successfully")


class SettingsTab(QWidget):
    """Tab for application settings"""

    status_message = pyqtSignal(str)

    def __init__(self, base_dir: Path, config: dict):
        super().__init__()
        self.base_dir = base_dir
        self.config = config
        self.download_worker = None

        self.init_ui()
        self.detect_hardware()

    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()

        # Hardware settings
        hardware_group = self.create_hardware_group()
        layout.addWidget(hardware_group)

        # Model management
        model_group = self.create_model_group()
        layout.addWidget(model_group)

        # Output directory settings
        output_group = self.create_output_group()
        layout.addWidget(output_group)

        # System info
        system_group = self.create_system_info_group()
        layout.addWidget(system_group)

        layout.addStretch()

        self.setLayout(layout)

    def create_hardware_group(self):
        """Create hardware settings group"""
        group = QGroupBox("Hardware Settings")
        layout = QVBoxLayout()

        # Device selection
        device_layout = QHBoxLayout()
        device_layout.addWidget(QLabel("Compute Device:"))

        self.device_combo = QComboBox()
        self.device_combo.addItems(["Auto", "CUDA (GPU)", "CPU"])
        device_layout.addWidget(self.device_combo)

        layout.addLayout(device_layout)

        # GPU info
        self.gpu_info_label = QLabel("Detecting hardware...")
        self.gpu_info_label.setWordWrap(True)
        self.gpu_info_label.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        layout.addWidget(self.gpu_info_label)

        group.setLayout(layout)
        return group

    def create_model_group(self):
        """Create model management group"""
        group = QGroupBox("Model Management")
        layout = QVBoxLayout()

        # Model status
        self.model_status_text = QTextEdit()
        self.model_status_text.setReadOnly(True)
        self.model_status_text.setMaximumHeight(150)
        self.model_status_text.setPlaceholderText("Model status will appear here...")
        layout.addWidget(self.model_status_text)

        # Download buttons
        button_layout = QHBoxLayout()

        self.download_sd_btn = QPushButton("Download SD Models")
        self.download_sd_btn.clicked.connect(lambda: self.download_models("stable_diffusion"))
        button_layout.addWidget(self.download_sd_btn)

        self.download_3d_btn = QPushButton("Download 3D Models")
        self.download_3d_btn.clicked.connect(lambda: self.download_models("triposr"))
        button_layout.addWidget(self.download_3d_btn)

        self.download_tts_btn = QPushButton("Download TTS Models")
        self.download_tts_btn.clicked.connect(lambda: self.download_models("tts"))
        button_layout.addWidget(self.download_tts_btn)

        layout.addLayout(button_layout)

        self.download_all_btn = QPushButton("Download All Models")
        self.download_all_btn.clicked.connect(lambda: self.download_models("all"))
        self.download_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(self.download_all_btn)

        # Progress bar
        self.download_progress = QProgressBar()
        self.download_progress.setVisible(False)
        self.download_progress.setRange(0, 0)  # Indeterminate
        layout.addWidget(self.download_progress)

        # Check models button
        check_btn = QPushButton("Check Installed Models")
        check_btn.clicked.connect(self.check_models)
        layout.addWidget(check_btn)

        group.setLayout(layout)
        return group

    def create_output_group(self):
        """Create output directory settings group"""
        group = QGroupBox("Output Directories")
        layout = QVBoxLayout()

        # Output directory selection
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Output Folder:"))

        self.output_path_edit = QLineEdit()
        self.output_path_edit.setText(str(self.base_dir / "output"))
        self.output_path_edit.setReadOnly(True)
        output_layout.addWidget(self.output_path_edit)

        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_output_dir)
        output_layout.addWidget(browse_btn)

        layout.addLayout(output_layout)

        # Open output folder button
        open_btn = QPushButton("Open Output Folder")
        open_btn.clicked.connect(self.open_output_folder)
        layout.addWidget(open_btn)

        group.setLayout(layout)
        return group

    def create_system_info_group(self):
        """Create system information group"""
        group = QGroupBox("System Information")
        layout = QVBoxLayout()

        self.system_info_text = QTextEdit()
        self.system_info_text.setReadOnly(True)
        self.system_info_text.setMaximumHeight(120)
        layout.addWidget(self.system_info_text)

        group.setLayout(layout)
        return group

    def detect_hardware(self):
        """Detect available hardware"""
        info_lines = []

        # Check CUDA availability
        if TORCH_AVAILABLE and torch.cuda.is_available():
            try:
                gpu_name = torch.cuda.get_device_name(0)
                gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
                info_lines.append(f"GPU Available: {gpu_name}")
                info_lines.append(f"GPU Memory: {gpu_memory:.2f} GB")
                self.device_combo.setCurrentText("CUDA (GPU)")
            except Exception as e:
                info_lines.append(f"GPU: Error detecting - {e}")
                self.device_combo.setCurrentText("CPU")
        else:
            info_lines.append("GPU: Not available")
            info_lines.append("Using CPU for inference")
            self.device_combo.setCurrentText("CPU")

        self.gpu_info_label.setText("\n".join(info_lines))

        # System info
        import platform
        import sys

        pytorch_version = torch.__version__ if TORCH_AVAILABLE else "Not installed"

        system_info = f"""Python Version: {sys.version.split()[0]}
PyTorch Version: {pytorch_version}
Platform: {platform.system()} {platform.release()}
Processor: {platform.processor()}
        """

        self.system_info_text.setText(system_info.strip())

    def check_models(self):
        """Check which models are installed"""
        status_lines = ["Checking installed models...\n"]

        # Check Stable Diffusion
        sd_dir = self.base_dir / "models" / "stable_diffusion"
        if sd_dir.exists() and any(sd_dir.iterdir()):
            status_lines.append("✓ Stable Diffusion: Installed")
        else:
            status_lines.append("✗ Stable Diffusion: Not installed")

        # Check TripoSR
        triposr_dir = self.base_dir / "models" / "triposr"
        if triposr_dir.exists() and any(triposr_dir.iterdir()):
            status_lines.append("✓ TripoSR: Installed")
        else:
            status_lines.append("✗ TripoSR: Not installed")

        # Check TTS
        tts_dir = self.base_dir / "models" / "tts"
        if tts_dir.exists() and any(tts_dir.iterdir()):
            status_lines.append("✓ TTS: Installed")
        else:
            status_lines.append("✗ TTS: Not installed")

        self.model_status_text.setText("\n".join(status_lines))
        self.status_message.emit("Model check complete")

    def download_models(self, model_type: str):
        """Download specified models"""
        # Confirm download
        model_names = {
            "stable_diffusion": "Stable Diffusion",
            "triposr": "TripoSR",
            "tts": "Text-to-Speech",
            "all": "All"
        }

        reply = QMessageBox.question(
            self,
            "Download Models",
            f"Download {model_names[model_type]} models?\n\n"
            "This may take several minutes and requires internet connection.\n"
            "Models will be cached for offline use.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.No:
            return

        # Disable buttons
        self.download_sd_btn.setEnabled(False)
        self.download_3d_btn.setEnabled(False)
        self.download_tts_btn.setEnabled(False)
        self.download_all_btn.setEnabled(False)
        self.download_progress.setVisible(True)

        self.model_status_text.append(f"\nStarting download of {model_names[model_type]} models...")

        # Start download worker
        self.download_worker = ModelDownloadWorker(model_type, self.base_dir)
        self.download_worker.finished.connect(self.on_download_finished)
        self.download_worker.error.connect(self.on_download_error)
        self.download_worker.progress.connect(self.on_download_progress)
        self.download_worker.start()

    def on_download_finished(self):
        """Handle download completion"""
        self.download_sd_btn.setEnabled(True)
        self.download_3d_btn.setEnabled(True)
        self.download_tts_btn.setEnabled(True)
        self.download_all_btn.setEnabled(True)
        self.download_progress.setVisible(False)

        self.model_status_text.append("\nDownload completed successfully!")
        self.status_message.emit("Models downloaded successfully")

        QMessageBox.information(
            self,
            "Download Complete",
            "Models have been downloaded and cached successfully.\n"
            "The application can now work offline."
        )

    def on_download_error(self, error_msg):
        """Handle download error"""
        self.download_sd_btn.setEnabled(True)
        self.download_3d_btn.setEnabled(True)
        self.download_tts_btn.setEnabled(True)
        self.download_all_btn.setEnabled(True)
        self.download_progress.setVisible(False)

        self.model_status_text.append(f"\nError: {error_msg}")
        self.status_message.emit(f"Download error: {error_msg}")

        QMessageBox.critical(
            self,
            "Download Error",
            f"Failed to download models:\n\n{error_msg}"
        )

    def on_download_progress(self, message):
        """Handle download progress"""
        self.model_status_text.append(message)
        self.status_message.emit(message)

    def browse_output_dir(self):
        """Browse for output directory"""
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            str(self.base_dir / "output")
        )

        if dir_path:
            self.output_path_edit.setText(dir_path)
            self.status_message.emit(f"Output directory changed to: {dir_path}")

    def open_output_folder(self):
        """Open the output folder"""
        import os
        import platform

        folder_path = Path(self.output_path_edit.text())

        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)

        if platform.system() == "Windows":
            os.startfile(folder_path)
        elif platform.system() == "Darwin":  # macOS
            os.system(f'open "{folder_path}"')
        else:  # Linux
            os.system(f'xdg-open "{folder_path}"')
