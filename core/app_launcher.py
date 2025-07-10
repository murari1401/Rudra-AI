# core/app_launcher.py

import os
import subprocess

# Mapping app names to their AppUserModelIDs (from Microsoft Store)
APP_IDS = {
    "whatsapp": "5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App",
    "instagram": "Facebook.InstagramBeta_8xx8rvfyw5nnt!App",
    "spotify": "SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe"
}

def launch_app_by_name(app_name):
    app_name = app_name.lower().strip()

    try:
        if app_name in APP_IDS:
            app_id = APP_IDS[app_name]

            if app_id.endswith(".exe"):  # Traditional desktop app
                os.system(f"start {app_id}")
            else:  # Microsoft Store app
                subprocess.Popen(f"explorer shell:AppsFolder\\{app_id}")

            print(f"✅ Launching {app_name}")
            return True
        else:
            print(f"❌ App not recognized: {app_name}")
            return False
    except Exception as e:
        print(f"❌ Error launching {app_name}: {e}")
        return False
