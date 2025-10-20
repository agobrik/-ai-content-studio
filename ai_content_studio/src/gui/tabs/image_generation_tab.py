"""
Image Generation Tab - Stable Diffusion interface
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QSpinBox, QDoubleSpinBox,
    QTextEdit, QGroupBox, QFileDialog, QScrollArea, QProgressBar, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QPixmap, QImage
from pathlib import Path
import datetime


class ImageGenerationWorker(QThread):
    """Worker thread for high-quality image generation"""
    finished = pyqtSignal(str)  # image_path
    error = pyqtSignal(str)  # error_message
    progress = pyqtSignal(int)  # progress_value

    def __init__(self, prompt, negative_prompt, model_name, steps, guidance_scale,
                 width, height, num_images, output_dir, transparent_bg, use_refiner):
        super().__init__()
        self.prompt = prompt
        self.negative_prompt = negative_prompt
        self.model_name = model_name
        self.steps = steps
        self.guidance_scale = guidance_scale
        self.width = width
        self.height = height
        self.num_images = num_images
        self.output_dir = output_dir
        self.transparent_bg = transparent_bg
        self.use_refiner = use_refiner

    def run(self):
        """Run high-quality image generation"""
        try:
            from core.image_generator import ImageGenerator

            self.progress.emit(10)

            # Initialize generator with quality settings
            generator = ImageGenerator(
                model_name=self.model_name,
                cache_dir=self.output_dir.parent / "models" / "stable_diffusion",
                use_refiner=self.use_refiner
            )

            self.progress.emit(30)

            # Generate images
            for i in range(self.num_images):
                image_path = generator.generate(
                    prompt=self.prompt,
                    negative_prompt=self.negative_prompt,
                    num_inference_steps=self.steps,
                    guidance_scale=self.guidance_scale,
                    width=self.width,
                    height=self.height,
                    output_dir=self.output_dir,
                    transparent_background=self.transparent_bg
                )

                progress_value = 30 + int((70 / self.num_images) * (i + 1))
                self.progress.emit(progress_value)

                self.finished.emit(str(image_path))

        except Exception as e:
            self.error.emit(str(e))


class ImageGenerationTab(QWidget):
    """Tab for 2D image generation using Stable Diffusion"""

    status_message = pyqtSignal(str)

    def __init__(self, base_dir: Path, config: dict):
        super().__init__()
        self.base_dir = base_dir
        self.config = config
        self.current_image_path = None
        self.worker = None

        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        layout = QHBoxLayout()

        # Left panel - Controls
        left_panel = self.create_control_panel()
        layout.addWidget(left_panel, 1)

        # Right panel - Preview
        right_panel = self.create_preview_panel()
        layout.addWidget(right_panel, 2)

        self.setLayout(layout)

    def create_control_panel(self):
        """Create control panel"""
        panel = QWidget()
        layout = QVBoxLayout()

        # Prompt input
        prompt_group = QGroupBox("Prompt")
        prompt_layout = QVBoxLayout()

        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText(
            "Enter your image description here...\n"
            "Example: A beautiful landscape with mountains and a lake at sunset"
        )
        self.prompt_input.setMaximumHeight(100)
        prompt_layout.addWidget(self.prompt_input)

        prompt_group.setLayout(prompt_layout)
        layout.addWidget(prompt_group)

        # Negative prompt
        neg_prompt_group = QGroupBox("Negative Prompt (Optional)")
        neg_layout = QVBoxLayout()

        self.negative_prompt_input = QTextEdit()
        self.negative_prompt_input.setPlaceholderText(
            "Things to avoid in the image..."
        )
        self.negative_prompt_input.setMaximumHeight(60)
        neg_layout.addWidget(self.negative_prompt_input)

        neg_prompt_group.setLayout(neg_layout)
        layout.addWidget(neg_prompt_group)

        # Model selection
        model_group = QGroupBox("Model Settings")
        model_layout = QVBoxLayout()

        model_layout.addWidget(QLabel("Model:"))
        self.model_combo = QComboBox()
        models = self.config.get('models', {}).get('stable_diffusion', {}).get(
            'available_models', ['stabilityai/stable-diffusion-2-1']
        )
        self.model_combo.addItems(models)
        model_layout.addWidget(self.model_combo)

        model_group.setLayout(model_layout)
        layout.addWidget(model_group)

        # Generation parameters
        params_group = QGroupBox("Generation Parameters")
        params_layout = QVBoxLayout()

        # Steps
        steps_layout = QHBoxLayout()
        steps_layout.addWidget(QLabel("Steps:"))
        self.steps_spinbox = QSpinBox()
        self.steps_spinbox.setRange(1, 150)
        self.steps_spinbox.setValue(
            self.config.get('generation', {}).get('image', {}).get('default_steps', 50)
        )
        steps_layout.addWidget(self.steps_spinbox)
        params_layout.addLayout(steps_layout)

        # Guidance Scale
        guidance_layout = QHBoxLayout()
        guidance_layout.addWidget(QLabel("Guidance Scale:"))
        self.guidance_spinbox = QDoubleSpinBox()
        self.guidance_spinbox.setRange(1.0, 20.0)
        self.guidance_spinbox.setSingleStep(0.5)
        self.guidance_spinbox.setValue(
            self.config.get('generation', {}).get('image', {}).get('default_guidance_scale', 7.5)
        )
        guidance_layout.addWidget(self.guidance_spinbox)
        params_layout.addLayout(guidance_layout)

        # Width
        width_layout = QHBoxLayout()
        width_layout.addWidget(QLabel("Width:"))
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(256, 1024)
        self.width_spinbox.setSingleStep(64)
        self.width_spinbox.setValue(
            self.config.get('generation', {}).get('image', {}).get('default_width', 512)
        )
        width_layout.addWidget(self.width_spinbox)
        params_layout.addLayout(width_layout)

        # Height
        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel("Height:"))
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setRange(256, 1024)
        self.height_spinbox.setSingleStep(64)
        self.height_spinbox.setValue(
            self.config.get('generation', {}).get('image', {}).get('default_height', 512)
        )
        height_layout.addWidget(self.height_spinbox)
        params_layout.addLayout(height_layout)

        # Number of images
        num_images_layout = QHBoxLayout()
        num_images_layout.addWidget(QLabel("Number of Images:"))
        self.num_images_spinbox = QSpinBox()
        self.num_images_spinbox.setRange(1, 10)
        self.num_images_spinbox.setValue(1)
        num_images_layout.addWidget(self.num_images_spinbox)
        params_layout.addLayout(num_images_layout)

        params_group.setLayout(params_layout)
        layout.addWidget(params_group)

        # Quality options
        quality_group = QGroupBox("Quality Options")
        quality_layout = QVBoxLayout()

        # Transparent background checkbox
        self.transparent_checkbox = QCheckBox("Remove Background (Transparent PNG)")
        self.transparent_checkbox.setChecked(
            self.config.get('generation', {}).get('image', {}).get('transparent_background', False)
        )
        self.transparent_checkbox.setToolTip("Removes background and creates transparent PNG (requires rembg)")
        quality_layout.addWidget(self.transparent_checkbox)

        # Use refiner checkbox (only for SDXL)
        self.refiner_checkbox = QCheckBox("Use SDXL Refiner (Enhanced Quality)")
        self.refiner_checkbox.setChecked(
            self.config.get('models', {}).get('stable_diffusion', {}).get('use_refiner', False)
        )
        self.refiner_checkbox.setToolTip("Uses SDXL refiner for even higher quality (requires more VRAM)")
        quality_layout.addWidget(self.refiner_checkbox)

        quality_group.setLayout(quality_layout)
        layout.addWidget(quality_group)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Generate button
        self.generate_btn = QPushButton("Generate Image")
        self.generate_btn.clicked.connect(self.generate_image)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(self.generate_btn)

        layout.addStretch()

        panel.setLayout(layout)
        return panel

    def create_preview_panel(self):
        """Create preview panel"""
        panel = QWidget()
        layout = QVBoxLayout()

        # Preview label
        layout.addWidget(QLabel("<h3>Preview</h3>"))

        # Image preview
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #ccc;
                background-color: #f9f9f9;
                min-height: 400px;
            }
        """)
        self.preview_label.setText("Generated image will appear here")

        # Scroll area for preview
        scroll = QScrollArea()
        scroll.setWidget(self.preview_label)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        # Action buttons
        button_layout = QHBoxLayout()

        self.save_btn = QPushButton("Save As...")
        self.save_btn.clicked.connect(self.save_image)
        self.save_btn.setEnabled(False)
        button_layout.addWidget(self.save_btn)

        self.use_for_3d_btn = QPushButton("Use for 3D Generation")
        self.use_for_3d_btn.clicked.connect(self.use_for_3d)
        self.use_for_3d_btn.setEnabled(False)
        button_layout.addWidget(self.use_for_3d_btn)

        layout.addLayout(button_layout)

        panel.setLayout(layout)
        return panel

    def generate_image(self):
        """Generate image using Stable Diffusion"""
        prompt = self.prompt_input.toPlainText().strip()

        if not prompt:
            self.status_message.emit("Error: Please enter a prompt")
            return

        # Disable generate button
        self.generate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        self.status_message.emit("Generating image...")

        # Get parameters
        negative_prompt = self.negative_prompt_input.toPlainText().strip()
        model_name = self.model_combo.currentText()
        steps = self.steps_spinbox.value()
        guidance_scale = self.guidance_spinbox.value()
        width = self.width_spinbox.value()
        height = self.height_spinbox.value()
        num_images = self.num_images_spinbox.value()
        transparent_bg = self.transparent_checkbox.isChecked()
        use_refiner = self.refiner_checkbox.isChecked()

        output_dir = self.base_dir / "output" / "images"

        # Create worker thread with quality options
        self.worker = ImageGenerationWorker(
            prompt, negative_prompt, model_name, steps, guidance_scale,
            width, height, num_images, output_dir, transparent_bg, use_refiner
        )
        self.worker.finished.connect(self.on_generation_finished)
        self.worker.error.connect(self.on_generation_error)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.start()

    def on_generation_finished(self, image_path):
        """Handle generation completion"""
        self.current_image_path = image_path

        # Load and display image
        pixmap = QPixmap(image_path)
        self.preview_label.setPixmap(
            pixmap.scaled(
                self.preview_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

        # Enable buttons
        self.save_btn.setEnabled(True)
        self.use_for_3d_btn.setEnabled(True)
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)

        self.status_message.emit(f"Image generated successfully: {image_path}")

    def on_generation_error(self, error_msg):
        """Handle generation error"""
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_message.emit(f"Error: {error_msg}")

    def save_image(self):
        """Save current image to user-selected location"""
        if not self.current_image_path:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            "",
            "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg)"
        )

        if file_path:
            try:
                pixmap = QPixmap(self.current_image_path)
                pixmap.save(file_path)
                self.status_message.emit(f"Image saved to: {file_path}")
            except Exception as e:
                self.status_message.emit(f"Error saving image: {e}")

    def use_for_3d(self):
        """Use current image for 3D generation"""
        if not self.current_image_path:
            return

        # Signal to switch to 3D tab and load image
        # This will be handled by the main window
        self.status_message.emit("Loading image in 3D generation tab...")
