import os
import subprocess
import winreg
from typing import Dict, Optional


class AppLauncher:
    """Handles application launching with path detection and fallback logic"""

    def __init__(self):
        self.desktop_paths = self._initialize_desktop_paths()
        self.store_apps = {
            "whatsapp": "5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App",
            "instagram": "Facebook.InstagramBeta_8xx8rvfyw5nnt!App",
            "spotify": "SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify"
        }

    def _initialize_desktop_paths(self) -> Dict[str, str]:
        """Detect known desktop applications"""
        return {
            "chrome": self._check_paths([
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe")
            ]),
            "firefox": self._check_paths([
                r"C:\Program Files\Mozilla Firefox\firefox.exe",
                r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
            ]),
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "vlc": self._check_paths([
                r"C:\Program Files\VideoLAN\VLC\vlc.exe",
                r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
            ]),
            "excel": self._find_office_path("Excel.Application"),
            "word": self._find_office_path("Word.Application")
        }

    def _check_paths(self, paths: list) -> Optional[str]:
        for path in paths:
            if os.path.exists(path):
                return path
        return None

    def _find_office_path(self, app_name: str) -> Optional[str]:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                fr"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\{app_name}") as key:
                return winreg.QueryValue(key, None)
        except Exception:
            return None

    def launch_app(self, app_name: str) -> bool:
        """
        Launch app by name. Try store first, then desktop path fallback.
        """
        try:
            app_name = app_name.lower().strip()

            # Try Microsoft Store apps
            if app_name in self.store_apps:
                return self._launch_store_app(app_name)

            # Try known desktop paths
            for name, path in self.desktop_paths.items():
                if name in app_name and path:
                    return self._launch_desktop_app(path)

            # Fallback: open Instagram in browser if not installed
            if "instagram" in app_name:
                return self._launch_web_app("https://www.instagram.com")

            print(f"❌ App not recognized: {app_name}")
            return False

        except Exception as e:
            print(f"❌ Error launching {app_name}: {e}")
            return False

    def _launch_store_app(self, app_name: str) -> bool:
        try:
            app_id = self.store_apps.get(app_name)
            if app_id:
                subprocess.Popen(f"explorer shell:AppsFolder\\{app_id}")
                print(f"✅ Launching Store app: {app_name}")
                return True
            return False
        except Exception as e:
            print(f"❌ Error launching Store app {app_name}: {e}")
            return False

    def _launch_desktop_app(self, path: str) -> bool:
        try:
            subprocess.Popen(path, shell=True)
            print(f"✅ Launching Desktop app: {os.path.basename(path)}")
            return True
        except Exception as e:
            print(f"❌ Error launching desktop app: {e}")
            return False

    def _launch_web_app(self, url: str) -> bool:
        try:
            browser = self.desktop_paths.get("chrome") or "start"
            subprocess.Popen([browser, url], shell=True)
            print(f"🌐 Opening in browser: {url}")
            return True
        except Exception as e:
            print(f"❌ Error opening web app: {e}")
            return False


# Singleton usage
app_launcher = AppLauncher()


def launch_app_by_name(app_name: str) -> bool:
    return app_launcher.launch_app(app_name)
