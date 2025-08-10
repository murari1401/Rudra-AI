# core/voice_animation.py

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from PyQt5.QtGui import QPainter, QColor, QBrush
import sys
import threading

class VoiceWaveform(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RUDRA Voice Animation")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(100, 100)
        self.move(50, 50)  # corner position
        self.color = QColor(0, 255, 255, 160)
        self.radius = 20
        self.show()

        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(400)
        self.anim.setStartValue(QRect(self.x(), self.y(), 100, 100))
        self.anim.setEndValue(QRect(self.x()-10, self.y()-10, 120, 120))
        self.anim.setLoopCount(-1)
        self.anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        brush = QBrush(self.color)
        painter.setBrush(brush)
        painter.drawEllipse(10, 10, 80, 80)

def start_voice_animation():
    def run():
        app = QApplication(sys.argv)
        VoiceWaveform()
        sys.exit(app.exec_())

    threading.Thread(target=run, daemon=True).start()
