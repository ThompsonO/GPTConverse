import threading
import keyboard

stop_flag = threading.Event()

def stop_listener():
    while not stop_flag.is_set():
       if keyboard.is_pressed('shift+backspace'):
           stop_flag.set()
           print("Set Stop Flag")

def start():
    stop_thread = threading.Thread(target=stop_listener)
    stop_thread.start()

def running():
    still_running = True

    if stop_flag.is_set():
        still_running = False

    return still_running
