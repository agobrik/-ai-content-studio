"""
Main Window - Primary application interface with tabbed layout
"""

from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QStatusBar, QMenuBar, QMenu, QMessageBox
)
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QAction
from pathlib import Path
import yaml

from gui.tabs.image_generation_tab import ImageGenerationTab
from gui.tabs.model_3d_generation_tab import Model3DGenerationTab
from gui.tabs.tts_tab import TTSTab
from gui.tabs.settings_tab import SettingsTab


class MainWindow(QMainWindow):
    """Main application window with tabbed interface"""

    def __init__(self, base_dir: Path):
        super().__init__()
        self.base_dir = base_dir
        self.settings = QSettings()

        # Load configuration
        self.config = self.load_config()

        self.init_ui()
        self.restore_geometry()

    def load_config(self):
        """Load application configuration"""
        config_path = self.base_dir / "config" / "config.yaml"
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            QMessageBox.warning(
                self,
                "Configuration Error",
                f"Failed to load configuration: {e}\nUsing defaults."
            )
            return self.get_default_config()

    def get_default_config(self):
        """Get default configuration"""
        return {
            'app': {
                'name': 'AI Content Studio',
                'version': '1.0.0',
                'window_width': 1200,
                'window_height': 800
            }
        }

    def init_ui(self):
        """Initialize the user interface"""
        # Set window properties
        self.setWindowTitle(
            f"{self.config['app']['name']} v{self.config['app']['version']}"
        )
        self.resize(
            self.config['app'].get('window_width', 1200),
            self.config['app'].get('window_height', 800)
        )

        # Create menu bar
        self.create_menu_bar()

        # Create central widget with tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)

        # Create tabs
        self.image_tab = ImageGenerationTab(self.base_dir, self.config)
        self.model_3d_tab = Model3DGenerationTab(self.base_dir, self.config)
        self.tts_tab = TTSTab(self.base_dir, self.config)
        self.settings_tab = SettingsTab(self.base_dir, self.config)

        # Add tabs
        self.tab_widget.addTab(self.image_tab, "2D Image Generation")
        self.tab_widget.addTab(self.model_3d_tab, "3D Model Generation")
        self.tab_widget.addTab(self.tts_tab, "Text-to-Speech")
        self.tab_widget.addTab(self.settings_tab, "Settings")

        # Set central widget
        self.setCentralWidget(self.tab_widget)

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Connect signals
        self.image_tab.status_message.connect(self.status_bar.showMessage)
        self.model_3d_tab.status_message.connect(self.status_bar.showMessage)
        self.tts_tab.status_message.connect(self.status_bar.showMessage)

    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        licenses_action = QAction("&Licenses", self)
        licenses_action.triggered.connect(self.show_licenses)
        help_menu.addAction(licenses_action)

    def show_about(self):
        """Show About dialog"""
        about_text = f"""
        <h2>{self.config['app']['name']}</h2>
        <p>Version {self.config['app']['version']}</p>
        <p>A comprehensive desktop application for AI-powered content creation.</p>
        <br>
        <p><b>Features:</b></p>
        <ul>
            <li>2D Image Generation (Stable Diffusion)</li>
            <li>3D Model Generation (TripoSR)</li>
            <li>Text-to-Speech (Multilingual Support)</li>
        </ul>
        <br>
        <p>All processing happens locally on your machine.</p>
        """
        QMessageBox.about(self, "About", about_text)

    def show_licenses(self):
        """Show licenses information"""
        licenses_text = """
        <h3>Open Source Licenses</h3>
        <p>This application uses the following open-source components:</p>
        <ul>
            <li><b>Stable Diffusion</b> - CreativeML Open RAIL-M License</li>
            <li><b>TripoSR</b> - MIT License</li>
            <li><b>Coqui TTS</b> - MPL 2.0 License</li>
            <li><b>PyQt6</b> - GPL v3 License</li>
            <li><b>PyTorch</b> - BSD-style License</li>
            <li><b>Transformers</b> - Apache 2.0 License</li>
            <li><b>Diffusers</b> - Apache 2.0 License</li>
        </ul>
        <p>Please see the LICENSE file for complete license information.</p>
        """
        QMessageBox.information(self, "Licenses", licenses_text)

    def restore_geometry(self):
        """Restore window geometry from settings"""
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)

        state = self.settings.value("windowState")
        if state:
            self.restoreState(state)

    def closeEvent(self, event):
        """Handle window close event"""
        # Save geometry
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())

        event.accept()
