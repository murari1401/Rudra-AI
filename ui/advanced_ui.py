from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from .components.wave_overlay import WaveOverlay
from .components.about_dialog import AboutDialog

class QCustomEvent(QEvent):
    def __init__(self, event_type, data):
        super().__init__(event_type)
        self.data = data

class ModernRUDRAUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_animations()

    def setup_ui(self):
        # Set window properties
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Main container
        container = QWidget()
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # RUDRA Title
        title = QLabel("RUDRA AI")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #00ffff;")
        layout.addWidget(title)

        # Status label with modern font
        self.status = QLabel("Ready")
        self.status.setFont(QFont("Segoe UI", 12))
        self.status.setStyleSheet("""
            QLabel {
                color: #00ffff;
                font-size: 18px;
                padding: 10px;
                background: rgba(0, 0, 0, 0.5);
                border-radius: 10px;
            }
        """)
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setWordWrap(True)
        layout.addWidget(self.status)

        # Wave overlay
        self.wave = WaveOverlay()
        layout.addWidget(self.wave)

        # Close button
        close_btn = QPushButton("×")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                color: #ffffff;
                background: transparent;
                border: none;
                font-size: 20px;
                padding: 5px;
            }
            QPushButton:hover {
                color: #ff4444;
            }
        """)
        close_btn.setFixedSize(30, 30)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)

        # Add About button
        about_btn = QPushButton("ℹ")
        about_btn.clicked.connect(self.show_about)
        about_btn.setStyleSheet("""
            QPushButton {
                color: #00ffff;
                background: transparent;
                border: none;
                font-size: 18px;
                padding: 5px;
            }
            QPushButton:hover {
                color: #00ccff;
            }
        """)
        about_btn.setFixedSize(30, 30)
        layout.addWidget(about_btn, alignment=Qt.AlignLeft | Qt.AlignTop)

        # Position window on right side of screen
        self._position_window()

    def setup_animations(self):
        self.status_anim = QPropertyAnimation(self.status, b"pos")
        self.status_anim.setDuration(300)
        self.status_anim.setEasingCurve(QEasingCurve.OutBounce)

    def _position_window(self):
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(
            screen.width() - 400,
            screen.height() // 2 - 300,
            350,
            600
        )

    def connect_voice_assistant(self, va):
        """Connect voice assistant signals"""
        try:
            # Connect signals properly
            va.command_received.connect(self.update_status)
            va.error_occurred.connect(self.show_error)
            va.status_changed.connect(self.update_status)
        except Exception as e:
            print(f"❌ Signal connection error: {e}")

    def update_status(self, text):
        """Update UI with styled messages"""
        self.status.setText(text)
        self.wave.set_listening("Listening" in text)
        self._animate_status()

    def _animate_status(self):
        pos = self.status.pos()
        self.status_anim.setStartValue(pos)
        self.status_anim.setEndValue(QPoint(pos.x(), pos.y() + 10))
        self.status_anim.start()
        QTimer.singleShot(150, lambda: self.status_anim.setEndValue(pos))

    def show_error(self, error_msg: str):
        """Display error message"""
        self.status.setText(f"Error: {error_msg}")
        self.status.setStyleSheet("""
            QLabel {
                color: #ff4444;
                background: rgba(255, 0, 0, 0.1);
                border-radius: 10px;
                padding: 10px;
            }
        """)

    def show_about(self):
        about = AboutDialog(self)
        about.exec_()

    def customEvent(self, event):
        """Handle custom events from voice thread"""
        if event.type() == QEvent.User:
            command = event.data
            self.va.process_command(command)