import time
import threading
import random
import sys
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
from termcolor import colored
from loguru import logger


# ___ logger settings ___
logger.remove()
logger.add(
    sys.stdout,
    format="{time:DD-MM-YYYY > HH:mm:ss} | <level>{level: <7}</level> | {message}",
    colorize=True,
)

# ____ delay settings ____
min_delay = 0.15                    # min delay between clicks in seconds
max_delay = 0.8                     # max delay between clicks in seconds
pause_interval = 10                 # pause interval in minutes
min_pause = 10                      # min pause duration in seconds
max_pause = 30                      # max pause duration in seconds

random_delay = random.uniform(min_delay, max_delay)
delay = random_delay

# ____ button settings ____
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

    def run(self, pause_interval=pause_interval, min_pause=min_pause, max_pause=max_pause):
        
        last_pause_time = time.time()             # start time for pause interval
        pause_interval = pause_interval * 60      # pause interval in seconds * 60
        
        while self.program_running:
            while self.running:
                current_time = time.time()
                
                if current_time - last_pause_time >= pause_interval:
                    pause_duration = random.uniform(min_pause, max_pause)   # random pause duration
                    logger.info(f"Pausing clicking for {pause_duration:.2f} seconds.")
                    time.sleep(pause_duration)
                    last_pause_time = current_time

                mouse.click(self.button)
                time.sleep(self.delay)


mouse = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()


def on_press(key):
    if key == control_key:
        if click_thread.running:
            click_thread.stop_clicking()
            logger.warning(f"Clicking paused, press {colored(control_key, "green")} to start again.")
        else:
            click_thread.start_clicking()
            logger.success(f"Clicking started, press {colored(control_key, "green")} to pause.")

    elif key == stop_key:
        logger.info('Exiting...')
        click_thread.exit()
        listener.stop()


with Listener(on_press=on_press) as listener:
    logger.debug("Mouse clicker is running.")
    logger.info(f"Press {colored(control_key, "green")} to start or pause clicking.")
    logger.info(f"Press {colored(stop_key, "red")} to stop the program.")
    listener.join()
