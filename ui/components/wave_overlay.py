from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QRectF, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import (QPainter, QPainterPath, QColor, QLinearGradient,
                        QFont, QPen, QFontDatabase, QRadialGradient)
import math

class WaveOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._phase = 0
        self._amplitude = 5
        self._is_listening = False
        self._setup_animation()

        # Add text display properties
        self._output_text = ""
        self._output_opacity = 0.0
        self._text_block_height = 0.0

        # Load custom font
        QFontDatabase.addApplicationFont("assets/fonts/Rajdhani-Medium.ttf")
        self.text_font = QFont("Rajdhani", 16)

        # Setup text animations
        self._setup_text_animations()

    def _setup_animation(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_wave)
        self.timer.start(50)

    def set_listening(self, listening: bool):
        self._is_listening = listening
        self._amplitude = 20 if listening else 5

    def _update_wave(self):
        self._phase += 0.1
        self.update()

    def _setup_text_animations(self):
        """Setup animations for text block"""
        self.text_fade = QPropertyAnimation(self, b"output_opacity")
        self.text_fade.setDuration(500)
        self.text_fade.setEasingCurve(QEasingCurve.OutCubic)

        self.block_expand = QPropertyAnimation(self, b"text_block_height")
        self.block_expand.setDuration(400)
        self.block_expand.setEasingCurve(QEasingCurve.OutBack)

    def show_text(self, text: str):
        """Show text with animation"""
        self._output_text = text

        # Animate text appearance
        self.text_fade.setStartValue(0.0)
        self.text_fade.setEndValue(1.0)
        self.text_fade.start()

        # Animate block height
        self.block_expand.setStartValue(0.0)
        self.block_expand.setEndValue(120.0)
        self.block_expand.start()

    # Add property getters/setters for animations
    @pyqtProperty(float)
    def output_opacity(self):
        return self._output_opacity

    @output_opacity.setter
    def output_opacity(self, value):
        self._output_opacity = value
        self.update()

    @pyqtProperty(float)
    def text_block_height(self):
        return self._text_block_height

    @text_block_height.setter
    def text_block_height(self, value):
        self._text_block_height = value
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        center_y = height / 2

        # Create wave path
        path = QPainterPath()
        path.moveTo(0, height)

        for x in range(width):
            y = center_y + math.sin(x * 0.02 + self._phase) * self._amplitude
            y += math.sin(x * 0.04 + self._phase * 0.8) * (self._amplitude * 0.5)
            path.lineTo(x, y)

        path.lineTo(width, height)
        path.lineTo(0, height)

        # Create gradient
        gradient = QLinearGradient(0, 0, width, 0)
        if self._is_listening:
            gradient.setColorAt(0, QColor(0, 255, 255, 150))
            gradient.setColorAt(1, QColor(0, 200, 255, 150))
        else:
            gradient.setColorAt(0, QColor(0, 150, 150, 100))
            gradient.setColorAt(1, QColor(0, 100, 150, 100))

        painter.fillPath(path, gradient)

        # Draw text block
        self._draw_text_block(painter)

    def _draw_text_block(self, painter):
        """Draw animated text block"""
        if not self._output_text:
            return

        # Calculate text block dimensions
        width = self.width() * 0.6
        margin = 40
        x = (self.width() - width) / 2
        y = self.height() - self._text_block_height - margin

        # Create block path with curves
        block_rect = QRectF(x, y, width, self._text_block_height)
        path = QPainterPath()
        path.addRoundedRect(block_rect, 20, 20)

        # Create glass effect gradient
        gradient = QRadialGradient(
            block_rect.center(),
            block_rect.width() * 0.5
        )
        gradient.setColorAt(0, QColor(0, 20, 40, int(200 * self._output_opacity)))
        gradient.setColorAt(1, QColor(0, 40, 80, int(200 * self._output_opacity)))

        # Draw block background
        painter.fillPath(path, gradient)

        # Draw glowing border
        glow_color = QColor(0, 255, 255, int(100 * self._output_opacity))
        painter.setPen(QPen(glow_color, 2))
        painter.drawPath(path)

        # Draw text
        if self._output_text:
            painter.setFont(self.text_font)
            text_color = QColor(255, 255, 255, int(255 * self._output_opacity))
            painter.setPen(text_color)
            text_rect = block_rect.adjusted(20, 10, -20, -10)
            painter.drawText(text_rect, Qt.AlignCenter | Qt.TextWordWrap,
                           self._output_text)