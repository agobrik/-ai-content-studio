"""
3D Model Generation Tab - Text-to-3D and Image-to-3D
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QGroupBox, QFileDialog, QProgressBar, QTextEdit,
    QLineEdit, QSlider, QTabWidget
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QPixmap
from pathlib import Path
import datetime


class Model3DGenerationWorker(QThread):
    """Worker thread for 3D model generation"""
    finished = pyqtSignal(str)  # model_path
    error = pyqtSignal(str)  # error_message
    progress = pyqtSignal(int, str)  # progress_value, status_message

    def __init__(self, mode, **kwargs):
        super().__init__()
        self.mode = mode  # 'text' or 'image'
        self.kwargs = kwargs

    def run(self):
        """Run 3D model generation"""
        try:
            from core.model_3d_generator import Model3DGenerator

            self.progress.emit(5, "Initializing 3D generator...")

            # Initialize generator
            generator = Model3DGenerator(
                cache_dir=self.kwargs.get('cache_dir')
            )

            # Get method
            method = self.kwargs.get('method', 'auto')

            if self.mode == 'text':
                # Text-to-3D generation
                self.progress.emit(10, "Generating 2D image from text...")

                model_path = generator.generate_from_text(
                    prompt=self.kwargs['prompt'],
                    negative_prompt=self.kwargs.get('negative_prompt', ''),
                    output_format=self.kwargs['output_format'],
                    output_dir=self.kwargs['output_dir'],
                    method=method,
                    extrusion_depth=self.kwargs.get('extrusion_depth', 0.5),
                    progress_callback=lambda p, s: self.progress.emit(p, s)
                )

            else:  # image mode
                # Image-to-3D generation
                self.progress.emit(10, "Loading image...")

                model_path = generator.generate_from_image(
                    image_path=self.kwargs['image_path'],
                    output_format=self.kwargs['output_format'],
                    output_dir=self.kwargs['output_dir'],
                    method=method,
                    extrusion_depth=self.kwargs.get('extrusion_depth', 0.5),
                    remove_background=self.kwargs.get('remove_background', False)
                )

                self.progress.emit(100, "3D model generated!")

            self.finished.emit(str(model_path))

        except Exception as e:
            import traceback
            self.error.emit(f"{str(e)}\n\n{traceback.format_exc()}")


class Model3DGenerationTab(QWidget):
    """Tab for 3D model generation - Text or Image input"""

    status_message = pyqtSignal(str)

    def __init__(self, base_dir: Path, config: dict):
        super().__init__()
        self.base_dir = base_dir
        self.config = config
        self.current_image_path = None
        self.current_model_path = None
        self.worker = None

        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()

        # Main tabs for text vs image input
        self.input_tabs = QTabWidget()

        # Text-to-3D tab
        text_tab = self.create_text_input_tab()
        self.input_tabs.addTab(text_tab, "Text-to-3D")

        # Image-to-3D tab
        image_tab = self.create_image_input_tab()
        self.input_tabs.addTab(image_tab, "Image-to-3D")

        layout.addWidget(self.input_tabs)

        # Common settings
        settings_group = self.create_settings_panel()
        layout.addWidget(settings_group)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("color: #666; padding: 5px;")
        layout.addWidget(self.status_label)

        # Generate button
        self.generate_btn = QPushButton("Generate 3D Model")
        self.generate_btn.clicked.connect(self.generate_3d_model)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        layout.addWidget(self.generate_btn)

        # Result panel
        result_panel = self.create_result_panel()
        layout.addWidget(result_panel)

        self.setLayout(layout)

    def create_text_input_tab(self):
        """Create text-to-3D input tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Info label
        info_label = QLabel(
            "<b>Text-to-3D Direct Generation</b><br>"
            "Enter a text description and get a 3D model directly!<br>"
            "<i>Note: This will first generate a 2D image, then convert to 3D.</i><br><br>"
            "<b style='color: #d32f2f;'>⚠ IMPORTANT:</b> Use <b>SIMPLE, SINGLE OBJECT</b> prompts!<br>"
            "<i>Good: 'coffee mug' | Bad: 'kitchen scene with mug and spoon'</i>"
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("padding: 10px; background-color: #e3f2fd; border-radius: 5px;")
        layout.addWidget(info_label)

        # Prompt input
        prompt_group = QGroupBox("3D Model Description")
        prompt_layout = QVBoxLayout()

        self.text_prompt_input = QTextEdit()
        self.text_prompt_input.setPlaceholderText(
            "Describe a SINGLE OBJECT for best results...\n\n"
            "Good Examples:\n"
            "- coffee mug\n"
            "- wooden chair\n"
            "- ceramic vase\n"
            "- metallic trophy\n"
            "- glass bottle\n\n"
            "Tips: Keep it simple, single object, avoid complex scenes!"
        )
        self.text_prompt_input.setMaximumHeight(120)
        prompt_layout.addWidget(self.text_prompt_input)

        prompt_group.setLayout(prompt_layout)
        layout.addWidget(prompt_group)

        # Negative prompt
        neg_prompt_group = QGroupBox("Negative Prompt (Optional)")
        neg_layout = QVBoxLayout()

        self.text_negative_input = QLineEdit()
        self.text_negative_input.setPlaceholderText("What to avoid (blurry, distorted, low quality...)")
        self.text_negative_input.setText("blurry, low quality, distorted, multiple objects")
        neg_layout.addWidget(self.text_negative_input)

        neg_prompt_group.setLayout(neg_layout)
        layout.addWidget(neg_prompt_group)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_image_input_tab(self):
        """Create image-to-3D input tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Info label
        info_label = QLabel(
            "<b>Image-to-3D Conversion</b><br>"
            "Upload an image and convert it to a 3D model."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("padding: 10px; background-color: #fff3e0; border-radius: 5px;")
        layout.addWidget(info_label)

        # Image preview
        image_group = QGroupBox("Input Image")
        image_layout = QVBoxLayout()

        self.image_preview = QLabel()
        self.image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview.setStyleSheet("""
            QLabel {
                border: 2px dashed #ccc;
                background-color: #f9f9f9;
                min-height: 250px;
            }
        """)
        self.image_preview.setText("No image loaded\n\nClick 'Upload Image' below")
        image_layout.addWidget(self.image_preview)

        upload_btn = QPushButton("Upload Image")
        upload_btn.clicked.connect(self.upload_image)
        upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 8px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        image_layout.addWidget(upload_btn)

        image_group.setLayout(image_layout)
        layout.addWidget(image_group)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_settings_panel(self):
        """Create settings panel"""
        group = QGroupBox("3D Generation Settings")
        layout = QVBoxLayout()

        # 3D Generation Method
        method_layout = QHBoxLayout()
        method_layout.addWidget(QLabel("Generation Method:"))
        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "Auto (Best Available)",
            "TripoSR (Best Quality)",
            "MiDaS Depth (Good Quality)",
            "Simple Extrusion (Fast)"
        ])
        self.method_combo.setCurrentText("Auto (Best Available)")
        self.method_combo.currentTextChanged.connect(self.on_method_changed)
        method_layout.addWidget(self.method_combo)
        method_layout.addStretch()
        layout.addLayout(method_layout)

        # Method info
        self.method_info = QLabel(
            "<i>Auto mode will use the best available method (TripoSR > MiDaS > Extrusion)</i>"
        )
        self.method_info.setWordWrap(True)
        self.method_info.setStyleSheet("color: #666; font-size: 11px; padding: 5px;")
        layout.addWidget(self.method_info)

        # Export format
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Export Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["GLB", "OBJ", "STL", "PLY"])
        self.format_combo.setCurrentText("GLB")
        format_layout.addWidget(self.format_combo)
        format_layout.addStretch()
        layout.addLayout(format_layout)

        # Extrusion depth
        depth_layout = QHBoxLayout()
        depth_layout.addWidget(QLabel("Extrusion Depth:"))
        self.depth_slider = QSlider(Qt.Orientation.Horizontal)
        self.depth_slider.setMinimum(10)
        self.depth_slider.setMaximum(200)
        self.depth_slider.setValue(50)
        self.depth_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.depth_slider.setTickInterval(20)
        self.depth_slider.valueChanged.connect(self.update_depth_label)
        depth_layout.addWidget(self.depth_slider)
        self.depth_label = QLabel("0.5")
        self.depth_label.setMinimumWidth(40)
        depth_layout.addWidget(self.depth_label)
        layout.addLayout(depth_layout)

        # Depth info
        self.depth_info = QLabel("<i>Higher values create thicker 3D models (for MiDaS and Extrusion)</i>")
        self.depth_info.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(self.depth_info)

        group.setLayout(layout)
        return group

    def create_result_panel(self):
        """Create result panel"""
        group = QGroupBox("Generated 3D Model")
        layout = QVBoxLayout()

        # Info text
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setPlaceholderText(
            "3D model information will appear here after generation...\n\n"
            "Generated models can be opened with:\n"
            "• GLB: Blender, Three.js viewers, Windows 3D Viewer\n"
            "• OBJ: Most 3D software (Blender, Maya, 3ds Max)\n"
            "• STL: 3D printing software\n"
            "• PLY: MeshLab, CloudCompare"
        )
        self.info_text.setMaximumHeight(150)
        layout.addWidget(self.info_text)

        # Action buttons
        button_layout = QHBoxLayout()

        self.save_btn = QPushButton("Save As...")
        self.save_btn.clicked.connect(self.save_model)
        self.save_btn.setEnabled(False)
        button_layout.addWidget(self.save_btn)

        self.open_folder_btn = QPushButton("Open Output Folder")
        self.open_folder_btn.clicked.connect(self.open_output_folder)
        self.open_folder_btn.setEnabled(False)
        button_layout.addWidget(self.open_folder_btn)

        layout.addLayout(button_layout)

        group.setLayout(layout)
        return group

    def on_method_changed(self, method_text):
        """Handle method selection change"""
        info_texts = {
            "Auto (Best Available)": "<i>Auto mode will use the best available method (TripoSR > MiDaS > Extrusion)</i>",
            "TripoSR (Best Quality)": "<i>TripoSR: State-of-the-art AI that generates full 3D geometry from images. Requires GPU and model download.</i>",
            "MiDaS Depth (Good Quality)": "<i>MiDaS: Uses depth estimation to create detailed 3D surfaces. Good balance of quality and speed.</i>",
            "Simple Extrusion (Fast)": "<i>Simple Extrusion: Basic relief-style 3D. Fast but limited quality. No model download needed.</i>"
        }
        self.method_info.setText(info_texts.get(method_text, ""))

        # Show/hide extrusion depth based on method
        is_triposr = "TripoSR" in method_text
        self.depth_slider.setEnabled(not is_triposr)
        self.depth_label.setEnabled(not is_triposr)
        if is_triposr:
            self.depth_info.setText("<i>Extrusion depth not used for TripoSR (generates true 3D geometry)</i>")
        else:
            self.depth_info.setText("<i>Higher values create thicker 3D models (for MiDaS and Extrusion)</i>")

    def update_depth_label(self, value):
        """Update depth label"""
        depth = value / 100.0
        self.depth_label.setText(f"{depth:.2f}")

    def upload_image(self):
        """Upload an image for 3D generation"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.webp)"
        )

        if file_path:
            self.load_image(file_path)

    def load_image(self, image_path: str):
        """Load an image"""
        self.current_image_path = image_path

        # Display preview
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(
            300, 300,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_preview.setPixmap(scaled_pixmap)

        self.status_message.emit(f"Image loaded: {Path(image_path).name}")

    def generate_3d_model(self):
        """Generate 3D model based on current tab"""
        current_tab = self.input_tabs.currentIndex()

        if current_tab == 0:  # Text-to-3D
            self.generate_from_text()
        else:  # Image-to-3D
            self.generate_from_image()

    def generate_from_text(self):
        """Generate 3D model from text prompt"""
        prompt = self.text_prompt_input.toPlainText().strip()

        if not prompt:
            self.status_message.emit("Error: Please enter a prompt")
            return

        # Disable button and show progress
        self.generate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Starting text-to-3D generation...")

        # Get parameters
        negative_prompt = self.text_negative_input.text().strip()
        output_format = self.format_combo.currentText().lower()
        extrusion_depth = self.depth_slider.value() / 100.0
        output_dir = self.base_dir / "output" / "models_3d"
        cache_dir = self.base_dir / "output" / "models" / "cache"

        # Get selected method
        method = self._get_method_from_combo()

        # Create worker thread
        self.worker = Model3DGenerationWorker(
            mode='text',
            prompt=prompt,
            negative_prompt=negative_prompt,
            output_format=output_format,
            output_dir=output_dir,
            cache_dir=cache_dir,
            extrusion_depth=extrusion_depth,
            method=method
        )
        self.worker.finished.connect(self.on_generation_finished)
        self.worker.error.connect(self.on_generation_error)
        self.worker.progress.connect(self.on_progress_update)
        self.worker.start()

        self.status_message.emit(f"Generating 3D model from text: {prompt[:50]}...")

    def _get_method_from_combo(self):
        """Convert combo box selection to method string"""
        method_text = self.method_combo.currentText()
        if "TripoSR" in method_text:
            return "triposr"
        elif "MiDaS" in method_text:
            return "midas"
        elif "Extrusion" in method_text:
            return "extrusion"
        else:  # Auto
            return "auto"

    def generate_from_image(self):
        """Generate 3D model from uploaded image"""
        if not self.current_image_path:
            self.status_message.emit("Error: Please upload an image first")
            return

        # Disable button and show progress
        self.generate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Starting image-to-3D conversion...")

        # Get parameters
        output_format = self.format_combo.currentText().lower()
        extrusion_depth = self.depth_slider.value() / 100.0
        output_dir = self.base_dir / "output" / "models_3d"
        cache_dir = self.base_dir / "output" / "models" / "cache"

        # Get selected method
        method = self._get_method_from_combo()

        # Create worker thread
        self.worker = Model3DGenerationWorker(
            mode='image',
            image_path=self.current_image_path,
            output_format=output_format,
            output_dir=output_dir,
            cache_dir=cache_dir,
            extrusion_depth=extrusion_depth,
            remove_background=False,
            method=method
        )
        self.worker.finished.connect(self.on_generation_finished)
        self.worker.error.connect(self.on_generation_error)
        self.worker.progress.connect(self.on_progress_update)
        self.worker.start()

        self.status_message.emit("Converting image to 3D model...")

    def on_progress_update(self, value, status):
        """Update progress bar and status"""
        self.progress_bar.setValue(value)
        self.status_label.setText(status)

    def on_generation_finished(self, model_path):
        """Handle generation completion"""
        self.current_model_path = model_path

        # Get file info
        path_obj = Path(model_path)
        file_size = path_obj.stat().st_size / (1024 * 1024)  # MB

        # Display info
        info_text = f"""
3D Model Generated Successfully! ✓

File: {path_obj.name}
Path: {model_path}
Format: {self.format_combo.currentText()}
Size: {file_size:.2f} MB
Extrusion Depth: {self.depth_slider.value() / 100.0:.2f}

The 3D model has been saved and can be opened with compatible viewers.

Next steps:
• Use "Save As..." to copy to another location
• Click "Open Output Folder" to view the file
• Open with Blender, Windows 3D Viewer, or online GLB viewers
        """

        self.info_text.setText(info_text.strip())

        # Enable buttons
        self.save_btn.setEnabled(True)
        self.open_folder_btn.setEnabled(True)
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText("✓ Generation complete!")

        self.status_message.emit(f"3D model generated: {path_obj.name}")

    def on_generation_error(self, error_msg):
        """Handle generation error"""
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText("✗ Generation failed!")
        self.status_message.emit(f"Error generating 3D model")

        self.info_text.setText(f"Error generating 3D model:\n\n{error_msg}")

    def save_model(self):
        """Save current model to user-selected location"""
        if not self.current_model_path:
            return

        ext = Path(self.current_model_path).suffix
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save 3D Model",
            f"model_3d{ext}",
            f"{ext.upper()[1:]} File (*{ext})"
        )

        if file_path:
            try:
                import shutil
                shutil.copy(self.current_model_path, file_path)
                self.status_message.emit(f"Model saved to: {file_path}")
            except Exception as e:
                self.status_message.emit(f"Error saving model: {e}")

    def open_output_folder(self):
        """Open the output folder"""
        if not self.current_model_path:
            output_dir = self.base_dir / "output" / "models_3d"
        else:
            output_dir = Path(self.current_model_path).parent

        import os
        import platform

        if platform.system() == "Windows":
            os.startfile(output_dir)
        elif platform.system() == "Darwin":  # macOS
            os.system(f'open "{output_dir}"')
        else:  # Linux
            os.system(f'xdg-open "{output_dir}"')
