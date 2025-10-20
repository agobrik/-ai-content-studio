"""
Text-to-Speech Tab - Multilingual TTS interface
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QTextEdit, QGroupBox, QFileDialog, QProgressBar,
    QSlider, QDoubleSpinBox, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from pathlib import Path
import datetime


class TTSWorker(QThread):
    """Worker thread for high-quality TTS generation"""
    finished = pyqtSignal(str)  # audio_path
    error = pyqtSignal(str)  # error_message
    progress = pyqtSignal(int)  # progress_value

    def __init__(self, text, language, speed, output_format, output_dir,
                 engine, voice, reference_audio=None):
        super().__init__()
        self.text = text
        self.language = language
        self.speed = speed
        self.output_format = output_format
        self.output_dir = output_dir
        self.engine = engine
        self.voice = voice
        self.reference_audio = reference_audio

    def run(self):
        """Run high-quality TTS generation"""
        try:
            from core.tts_generator import TTSGenerator

            self.progress.emit(10)

            # Initialize generator with selected engine
            generator = TTSGenerator(
                cache_dir=self.output_dir.parent / "models" / "tts",
                engine=self.engine
            )

            self.progress.emit(30)

            # Generate speech with voice selection
            audio_path = generator.generate(
                text=self.text,
                language=self.language,
                speed=self.speed,
                output_format=self.output_format,
                output_dir=self.output_dir,
                voice=self.voice,
                reference_audio=self.reference_audio
            )

            self.progress.emit(100)
            self.finished.emit(str(audio_path))

        except Exception as e:
            self.error.emit(str(e))


class TTSTab(QWidget):
    """Tab for text-to-speech generation"""

    status_message = pyqtSignal(str)

    def __init__(self, base_dir: Path, config: dict):
        super().__init__()
        self.base_dir = base_dir
        self.config = config
        self.current_audio_path = None
        self.reference_audio_path = None
        self.worker = None

        # Audio player
        self.audio_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.audio_player.setAudioOutput(self.audio_output)

        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        layout = QHBoxLayout()

        # Left panel - Controls
        left_panel = self.create_control_panel()
        layout.addWidget(left_panel, 1)

        # Right panel - Preview/Info
        right_panel = self.create_info_panel()
        layout.addWidget(right_panel, 1)

        self.setLayout(layout)

    def create_control_panel(self):
        """Create control panel"""
        panel = QWidget()
        layout = QVBoxLayout()

        # Text input
        text_group = QGroupBox("Text Input")
        text_layout = QVBoxLayout()

        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText(
            "Enter the text you want to convert to speech...\n\n"
            "Example: Hello, welcome to AI Content Studio!"
        )
        self.text_input.setMinimumHeight(150)
        text_layout.addWidget(self.text_input)

        # Character count
        self.char_count_label = QLabel("Characters: 0")
        self.text_input.textChanged.connect(self.update_char_count)
        text_layout.addWidget(self.char_count_label)

        text_group.setLayout(text_layout)
        layout.addWidget(text_group)

        # Language selection
        lang_group = QGroupBox("Language Settings")
        lang_layout = QVBoxLayout()

        lang_layout.addWidget(QLabel("Language:"))
        self.language_combo = QComboBox()

        # Add supported languages
        languages = [
            ("English", "en"),
            ("Spanish", "es"),
            ("French", "fr"),
            ("German", "de"),
            ("Italian", "it"),
            ("Portuguese", "pt"),
            ("Polish", "pl"),
            ("Turkish", "tr"),
            ("Russian", "ru"),
            ("Dutch", "nl"),
            ("Czech", "cs"),
            ("Arabic", "ar"),
            ("Chinese", "zh-cn"),
            ("Japanese", "ja"),
            ("Korean", "ko"),
            ("Hungarian", "hu"),
            ("Hindi", "hi"),
        ]

        for lang_name, lang_code in languages:
            self.language_combo.addItem(lang_name, lang_code)

        self.language_combo.currentIndexChanged.connect(self.update_voice_options)
        lang_layout.addWidget(self.language_combo)

        lang_group.setLayout(lang_layout)
        layout.addWidget(lang_group)

        # Voice settings
        voice_group = QGroupBox("Voice & Engine Settings")
        voice_layout = QVBoxLayout()

        # Engine selection
        engine_layout = QHBoxLayout()
        engine_layout.addWidget(QLabel("TTS Engine:"))
        self.engine_combo = QComboBox()
        self.engine_combo.addItem("Edge-TTS (High Quality, Online)", "edge")
        self.engine_combo.addItem("Google TTS (Simple, Online)", "gtts")
        self.engine_combo.addItem("pyttsx3 (Offline, System)", "pyttsx3")
        self.engine_combo.currentIndexChanged.connect(self.update_voice_options)
        engine_layout.addWidget(self.engine_combo)
        voice_layout.addLayout(engine_layout)

        # Voice selection
        voice_select_layout = QHBoxLayout()
        voice_select_layout.addWidget(QLabel("Voice:"))
        self.voice_combo = QComboBox()
        voice_select_layout.addWidget(self.voice_combo)
        voice_layout.addLayout(voice_select_layout)

        # Speed control
        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("Speed:"))
        self.speed_spinbox = QDoubleSpinBox()
        self.speed_spinbox.setRange(0.5, 2.0)
        self.speed_spinbox.setSingleStep(0.1)
        self.speed_spinbox.setValue(1.0)
        self.speed_spinbox.setSuffix("x")
        speed_layout.addWidget(self.speed_spinbox)
        voice_layout.addLayout(speed_layout)

        # Voice cloning option (disabled for now)
        # self.voice_clone_checkbox = QCheckBox("Use Reference Audio (Voice Cloning)")
        # self.voice_clone_checkbox.stateChanged.connect(self.toggle_voice_cloning)
        # voice_layout.addWidget(self.voice_clone_checkbox)

        # Hidden reference audio (for future voice cloning)
        # self.reference_audio_btn = QPushButton("Upload Reference Audio")
        # self.reference_audio_btn.clicked.connect(self.upload_reference_audio)
        # self.reference_audio_btn.setEnabled(False)
        # voice_layout.addWidget(self.reference_audio_btn)

        # self.reference_audio_label = QLabel("No reference audio")
        # self.reference_audio_label.setStyleSheet("color: #666; font-style: italic;")
        # voice_layout.addWidget(self.reference_audio_label)

        voice_group.setLayout(voice_layout)
        layout.addWidget(voice_group)

        # Initialize voice options for default engine
        self.update_voice_options()

        # Output format
        format_group = QGroupBox("Output Format")
        format_layout = QVBoxLayout()

        self.format_combo = QComboBox()
        self.format_combo.addItems(["WAV", "MP3"])
        format_layout.addWidget(self.format_combo)

        format_group.setLayout(format_layout)
        layout.addWidget(format_group)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Generate button
        self.generate_btn = QPushButton("Generate Speech")
        self.generate_btn.clicked.connect(self.generate_speech)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        layout.addWidget(self.generate_btn)

        layout.addStretch()

        panel.setLayout(layout)
        return panel

    def create_info_panel(self):
        """Create info panel"""
        panel = QWidget()
        layout = QVBoxLayout()

        # Info label
        layout.addWidget(QLabel("<h3>Audio Player</h3>"))

        # Info text
        info_text = QLabel(
            "Supports 23 languages with natural-sounding voices.\n\n"
            "Features:\n"
            "• Multi-language text-to-speech\n"
            "• Adjustable speech speed\n"
            "• Voice cloning with reference audio\n"
            "• High-quality audio output\n\n"
            "Generated audio will appear here for playback."
        )
        info_text.setWordWrap(True)
        info_text.setStyleSheet("padding: 10px; background-color: #f5f5f5; border-radius: 5px;")
        layout.addWidget(info_text)

        # Playback controls
        playback_group = QGroupBox("Playback Controls")
        playback_layout = QVBoxLayout()

        button_layout = QHBoxLayout()

        self.play_btn = QPushButton("Play")
        self.play_btn.clicked.connect(self.play_audio)
        self.play_btn.setEnabled(False)
        button_layout.addWidget(self.play_btn)

        self.pause_btn = QPushButton("Pause")
        self.pause_btn.clicked.connect(self.pause_audio)
        self.pause_btn.setEnabled(False)
        button_layout.addWidget(self.pause_btn)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop_audio)
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.stop_btn)

        playback_layout.addLayout(button_layout)

        # Volume control
        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel("Volume:"))
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.valueChanged.connect(self.change_volume)
        volume_layout.addWidget(self.volume_slider)
        playback_layout.addLayout(volume_layout)

        playback_group.setLayout(playback_layout)
        layout.addWidget(playback_group)

        # Save button
        self.save_btn = QPushButton("Save Audio As...")
        self.save_btn.clicked.connect(self.save_audio)
        self.save_btn.setEnabled(False)
        layout.addWidget(self.save_btn)

        layout.addStretch()

        panel.setLayout(layout)
        return panel

    def update_char_count(self):
        """Update character count"""
        text = self.text_input.toPlainText()
        self.char_count_label.setText(f"Characters: {len(text)}")

    def update_voice_options(self):
        """Update available voices based on selected engine and language"""
        engine = self.engine_combo.currentData()
        language = self.language_combo.currentData()

        self.voice_combo.clear()

        # Get voices from TTS generator
        try:
            from core.tts_generator import TTSGenerator
            temp_gen = TTSGenerator(engine=engine)
            voices = temp_gen.get_available_voices(language)
            self.voice_combo.addItems(voices)
        except Exception as e:
            print(f"Could not load voices: {e}")
            self.voice_combo.addItem("Default Voice")

    def toggle_voice_cloning(self, state):
        """Toggle voice cloning option"""
        # self.reference_audio_btn.setEnabled(state == Qt.CheckState.Checked.value)
        pass

    def upload_reference_audio(self):
        """Upload reference audio for voice cloning"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Reference Audio",
            "",
            "Audio Files (*.wav *.mp3 *.flac)"
        )

        if file_path:
            self.reference_audio_path = file_path
            filename = Path(file_path).name
            self.reference_audio_label.setText(f"Reference: {filename}")
            self.status_message.emit(f"Reference audio loaded: {filename}")

    def generate_speech(self):
        """Generate speech from text"""
        text = self.text_input.toPlainText().strip()

        if not text:
            self.status_message.emit("Error: Please enter text")
            return

        # Disable generate button
        self.generate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        self.status_message.emit("Generating speech...")

        # Get parameters
        language = self.language_combo.currentData()
        speed = self.speed_spinbox.value()
        output_format = self.format_combo.currentText().lower()
        engine = self.engine_combo.currentData()
        voice_text = self.voice_combo.currentText()

        # Extract voice ID from text (e.g., "en-US-AriaNeural (Female)" -> "en-US-AriaNeural")
        voice = voice_text.split(" (")[0] if " (" in voice_text else voice_text

        reference_audio = None
        # if self.voice_clone_checkbox.isChecked() and self.reference_audio_path:
        #     reference_audio = self.reference_audio_path

        output_dir = self.base_dir / "output" / "audio"

        # Create worker thread with engine and voice
        self.worker = TTSWorker(
            text, language, speed, output_format, output_dir,
            engine, voice, reference_audio
        )
        self.worker.finished.connect(self.on_generation_finished)
        self.worker.error.connect(self.on_generation_error)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.start()

    def on_generation_finished(self, audio_path):
        """Handle generation completion"""
        self.current_audio_path = audio_path

        # Enable buttons
        self.play_btn.setEnabled(True)
        self.pause_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)

        # Load audio
        self.audio_player.setSource(QUrl.fromLocalFile(audio_path))

        self.status_message.emit(f"Speech generated successfully: {audio_path}")

    def on_generation_error(self, error_msg):
        """Handle generation error"""
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_message.emit(f"Error: {error_msg}")

    def play_audio(self):
        """Play generated audio"""
        self.audio_player.play()

    def pause_audio(self):
        """Pause audio playback"""
        self.audio_player.pause()

    def stop_audio(self):
        """Stop audio playback"""
        self.audio_player.stop()

    def change_volume(self, value):
        """Change audio volume"""
        self.audio_output.setVolume(value / 100.0)

    def save_audio(self):
        """Save current audio to user-selected location"""
        if not self.current_audio_path:
            return

        ext = Path(self.current_audio_path).suffix
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Audio",
            "",
            f"{ext.upper()[1:]} File (*{ext})"
        )

        if file_path:
            try:
                import shutil
                shutil.copy(self.current_audio_path, file_path)
                self.status_message.emit(f"Audio saved to: {file_path}")
            except Exception as e:
                self.status_message.emit(f"Error saving audio: {e}")
