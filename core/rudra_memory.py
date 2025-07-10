# core/rudra_memory.py

visible_elements = set()
last_command = ""

def remember_element(text):
    visible_elements.add(text.lower())

def match_element(command):
    for elem in visible_elements:
        if elem in command:
            return elem
    return None

def set_last_command(cmd):
    global last_command
    last_command = cmd

def get_last_command():
    return last_command
