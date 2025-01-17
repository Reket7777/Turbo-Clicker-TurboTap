import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
from termcolor import colored
from loguru import logger


delay = 0.2                         # delay in seconds
button = Button.left                # button to click
control_key = KeyCode(char='a')     # key to start/pause clicking
stop_key = KeyCode(char='b')        # key to stop the program


class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                time.sleep(self.delay)
            time.sleep(0.05)


mouse = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()


def on_press(key):
    if key == control_key:
        if click_thread.running:
            click_thread.stop_clicking()
            logger.warning(f"Clicking paused, press {control_key} to start again.")
        else:
            click_thread.start_clicking()
            logger.success(f"Clicking started, press {control_key} to pause.")

    elif key == stop_key:
        logger.info('Exiting...')
        click_thread.exit()
        listener.stop()


with Listener(on_press=on_press) as listener:
    logger.info(f"Press {colored(control_key, "green")} to start or pause clicking.")
    logger.info(f"Press {colored(stop_key, "red")} to stop the program.")
    listener.join()
