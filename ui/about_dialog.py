from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import webbrowser

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Animation properties
        self._opacity = 0.0
        self._glow_intensity = 0.0
        self._cards_offset = 100

        # Setup animations
        self.setup_animations()
        self.setup_ui()

        # Start entrance animation
        self.start_entrance_animation()

    def setup_animations(self):
        # Fade in animation
        self.fade_anim = QPropertyAnimation(self, b"opacity")
        self.fade_anim.setDuration(500)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.OutCubic)

        # Glow animation
        self.glow_anim = QPropertyAnimation(self, b"glow_intensity")
        self.glow_anim.setDuration(2000)
        self.glow_anim.setStartValue(0.0)
        self.glow_anim.setEndValue(1.0)
        self.glow_anim.setLoopCount(-1)
        self.glow_anim.setEasingCurve(QEasingCurve.InOutQuad)

        # Cards slide animation
        self.cards_anim = QPropertyAnimation(self, b"cards_offset")
        self.cards_anim.setDuration(800)
        self.cards_anim.setStartValue(100)
        self.cards_anim.setEndValue(0)
        self.cards_anim.setEasingCurve(QEasingCurve.OutBack)

    def start_entrance_animation(self):
        self.fade_anim.start()
        self.glow_anim.start()
        self.cards_anim.start()

    # Property getters/setters for animations
    @pyqtProperty(float)
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.update()

    @pyqtProperty(float)
    def glow_intensity(self):
        return self._glow_intensity

    @glow_intensity.setter
    def glow_intensity(self, value):
        self._glow_intensity = value
        self.update()

    @pyqtProperty(float)
    def cards_offset(self):
        return self._cards_offset

    @cards_offset.setter
    def cards_offset(self, value):
        self._cards_offset = value
        self.update()

    def setup_ui(self):
        self.setFixedSize(500, 600)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("About RUDRA AI")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #00ffff;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Description
        desc = QLabel(
            "RUDRA AI is an advanced artificial intelligence assistant "
            "designed to enhance human-computer interaction through "
            "voice commands, gestures, and natural language processing."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #ffffff; font-size: 14px;")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)

        # Developers Section
        dev_widget = QWidget()
        dev_layout = QVBoxLayout(dev_widget)
        dev_layout.setSpacing(20)

        # Developer 1
        dev1 = self.create_developer_card(
            "B. Murari",
            "Lead Developer & AI Engineer",
            "linkedin.com/in/murari",
            "github.com/murari",
            "murari@email.com"
        )
        dev_layout.addWidget(dev1)

        # Developer 2
        dev2 = self.create_developer_card(
            "B. Meghana",
            "UI/UX Designer & System Architect",
            "linkedin.com/in/meghana",
            "github.com/meghana",
            "meghana@email.com"
        )
        dev_layout.addWidget(dev2)

        layout.addWidget(dev_widget)

        # Close button
        close_btn = QPushButton("×")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                color: #ffffff;
                background: transparent;
                border: none;
                font-size: 20px;
            }
            QPushButton:hover {
                color: #ff4444;
            }
        """)
        close_btn.setFixedSize(30, 30)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)

    def create_developer_card(self, name, role, linkedin, github, email):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: rgba(0, 20, 40, {self._opacity * 0.6});
                border-radius: 15px;
                padding: 10px;
                margin-top: {self._cards_offset}px;
            }}
        """)

        layout = QVBoxLayout(card)

        # Name and Role
        name_label = QLabel(name)
        name_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        name_label.setStyleSheet("color: #00ffff;")
        layout.addWidget(name_label)

        role_label = QLabel(role)
        role_label.setStyleSheet("color: #00ff99;")
        layout.addWidget(role_label)

        # Social Links
        links_widget = QWidget()
        links_layout = QHBoxLayout(links_widget)

        for icon, url in [
            ("LinkedIn", linkedin),
            ("GitHub", github),
            ("Email", f"mailto:{email}")
        ]:
            link = QPushButton(icon)
            link.setCursor(Qt.PointingHandCursor)
            link.clicked.connect(lambda checked, u=url: webbrowser.open(u))
            link.setStyleSheet("""
                QPushButton {
                    color: #ffffff;
                    background: rgba(0, 100, 200, 0.3);
                    border-radius: 10px;
                    padding: 5px 10px;
                }
                QPushButton:hover {
                    background: rgba(0, 150, 255, 0.4);
                }
            """)
            links_layout.addWidget(link)

        layout.addWidget(links_widget)
        return card

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Animated gradient background
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(0, 20, 40, int(230 * self._opacity)))
        gradient.setColorAt(1, QColor(0, 40, 80, int(230 * self._opacity)))

        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)

        # Animated glowing border
        glow_color = QColor(0, 255, 255, int(40 * (0.5 + self._glow_intensity * 0.5)))
        glow = QPen(glow_color, 2)
        painter.setPen(glow)
        painter.drawRoundedRect(self.rect(), 20, 20)

    def mousePressEvent(self, event):
        # Add ripple effect
        pos = event.pos()
        self.add_ripple(pos)
        super().mousePressEvent(event)

    def add_ripple(self, pos):
        ripple = QPropertyAnimation(self, b"ripple_radius")
        ripple.setStartValue(0)
        ripple.setEndValue(100)
        ripple.setDuration(500)
        ripple.setEasingCurve(QEasingCurve.OutQuad)
        ripple.start()

        # Store ripple position
        self._ripple_pos = pos
        self._ripple_radius = 0