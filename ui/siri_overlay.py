import webbrowser
import threading
import os

def show_siri_overlay():
    path = os.path.abspath("ui/siri_overlay.html")
    webbrowser.open(f"file:///{path}")

def show_siri_async():
    threading.Thread(target=show_siri_overlay).start()
