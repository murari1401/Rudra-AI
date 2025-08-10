import tkinter as tk
from PIL import Image, ImageTk
import os
import threading
import time
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys

class RUDRAInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_conversation()
        self.setup_animation()

    def setup_window(self):
        self.title("RUDRA AI")
        self.configure(bg="#3f51b5")  # Indigo theme
        self.attributes('-fullscreen', True)
        self.state('zoomed')  # Start maximized

    def setup_conversation(self):
        # Chat window with dark theme
        self.conversation = tk.Text(
            self,
            bg="#232946",
            fg="#ffffff",
            font=("Segoe UI", 12),
            wrap=tk.WORD,
            padx=20,
            pady=20
        )
        self.conversation.pack(expand=True, fill="both", padx=40, pady=40)

    def setup_animation(self):
        self.anim_frame = tk.Frame(self, bg="#3f51b5")
        self.anim_frame.pack(side="bottom", fill="x", pady=20)
        self.anim_label = tk.Label(self.anim_frame, bg="#3f51b5")
        self.anim_label.pack()

    def add_message(self, who, msg):
        """Add a message to the conversation"""
        timestamp = time.strftime("%H:%M:%S")
        self.conversation.configure(state='normal')
        self.conversation.insert('end', f"[{timestamp}] {who}: {msg}\n")
        self.conversation.see('end')
        self.conversation.configure(state='disabled')

    def show_animation(self):
        """Show the RUDRA animation"""
        try:
            if os.path.exists("assets/rudra_animation.gif"):
                self.current_animation = tk.PhotoImage(file="assets/rudra_animation.gif")
                self.anim_label.configure(image=self.current_animation)
        except Exception as e:
            print(f"❌ Animation error: {e}")

    def hide_animation(self):
        """Hide the animation"""
        self.anim_label.configure(image='')

class RUDRAWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the UI components"""
        self.setWindowTitle('RUDRA AI Assistant')
        self.setGeometry(100, 100, 800, 600)

        # Create central widget
        central = QWidget()
        self.setCentralWidget(central)

        # Create layout
        layout = QVBoxLayout(central)

        # Add status label
        self.status = QLabel("RUDRA AI Ready")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setFont(QFont('Arial', 24))
        layout.addWidget(self.status)

        # Style the window
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QLabel {
                color: #00ff00;
                padding: 10px;
            }
        """)

    def update_status(self, message: str):
        """Update the status display"""
        self.status.setText(message)

# Create singleton instance
rudra_ui = None

def get_ui():
    """Get or create the UI instance"""
    global rudra_ui
    if rudra_ui is None:
        rudra_ui = RUDRAInterface()
    return rudra_ui

def show_siri_window(ui_ready=None):
    """Display RUDRA animation window"""
    try:
        # Create Qt application
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)

        # Create and show window
        window = RUDRAWindow()
        window.show()

        if ui_ready:
            ui_ready.set()

        return app.exec_()

    except Exception as e:
        print(f"❌ UI Error: {e}")
        if ui_ready:
            ui_ready.set()
        return 1
