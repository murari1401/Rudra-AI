from core.voice_assistant import VoiceAssistant
from core.auto_actions import (
    scroll_down, scroll_up, click_text_on_screen, open_local_app,
    type_text_on_screen, close_active_window, switch_to_next_tab,
    switch_to_previous_tab, copy_text, paste_text, send_whatsapp_message
)
from core.app_launcher import launch_app_by_name
from core.button_trainer import find_and_click_button

import threading

def is_screen_command(command):
    SCREEN_COMMAND_KEYWORDS = [
        "scroll", "click", "open", "close", "shutdown", "restart",
        "type", "next tab", "previous tab", "copy", "paste"
    ]
    return any(word in command.lower() for word in SCREEN_COMMAND_KEYWORDS)

def is_about_query(command):
    return any(phrase in command.lower() for phrase in ["who made you", "who created you", "your creator"])

def handle_task(va, command):
    try:
        if is_about_query(command):
            va.safe_speak("I was created by B. Murari sir and B. Meghana madam with futuristic vision.")
            return

        if "send message to" in command and "saying" in command:
            try:
                parts = command.split("send message to")[1].strip()
                contact_name, message = parts.split("saying")
                contact_name = contact_name.strip()
                message = message.strip()
                if send_whatsapp_message(contact_name, message):
                    va.safe_speak(f"Message sent to {contact_name}")
                else:
                    va.safe_speak("Failed to send the message.")
                return
            except Exception as e:
                print(f"❌ WhatsApp message error: {e}")
                va.safe_speak("Sorry, I couldn't understand your message format.")
                return

        if is_screen_command(command):
            command = command.lower()
            if "scroll down" in command:
                scroll_down()
                va.safe_speak("Scrolling down.")
            elif "scroll up" in command:
                scroll_up()
                va.safe_speak("Scrolling up.")
            elif "open" in command:
                app_name = command.replace("open", "").strip()
                if launch_app_by_name(app_name):
                    va.safe_speak(f"Opening {app_name}.")
                else:
                    va.safe_speak(f"Couldn't find or open {app_name}.")
            elif "click" in command:
                words = command.split()
                click_index = words.index("click")
                target_button = words[click_index + 1] if click_index + 1 < len(words) else ""
                target_app = None
                for app_candidate in ["whatsapp", "instagram"]:
                    if app_candidate in command:
                        target_app = app_candidate
                        break
                if target_app and target_button:
                    success = find_and_click_button(target_app, target_button)
                    if success:
                        va.safe_speak(f"Clicked on {target_button} in {target_app}.")
                    else:
                        va.safe_speak(f"Could not find {target_button} in {target_app}.")
                else:
                    va.safe_speak("Please specify which button or app to click.")
            elif "type" in command:
                text = command.replace("type", "").strip()
                if text:
                    type_text_on_screen(text)
                    va.safe_speak(f"Typed: {text}")
                else:
                    va.safe_speak("Please tell me what to type.")
            elif "close" in command:
                close_active_window()
                va.safe_speak("Window closed.")
            elif "next tab" in command:
                switch_to_next_tab()
                va.safe_speak("Next tab.")
            elif "previous tab" in command:
                switch_to_previous_tab()
                va.safe_speak("Previous tab.")
            elif "copy" in command:
                copy_text()
                va.safe_speak("Copied.")
            elif "paste" in command:
                paste_text()
                va.safe_speak("Pasted.")
            else:
                va.safe_speak("Command not recognized.")
        else:
            va.handle_query(command)

    except Exception as e:
        print(f"❌ Error in task: {e}")
        va.safe_speak("Something went wrong while processing your request.")

def main():
    va = VoiceAssistant()
    va.safe_speak("Rudra system activated. Waiting for your command, sir.")

    while True:
        command = va.listen()
        if not command:
            continue
        if "exit" in command or "stop" in command:
            va.safe_speak("Goodbye, sir.")
            break
        thread = threading.Thread(target=handle_task, args=(va, command))
        thread.start()

if __name__ == "__main__":
    main()
