import time
import threading
import platform
import random
import sys

from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
from termcolor import colored

from loguru import logger

if platform.system() == "Windows":
    from win10toast import ToastNotifier
else:
    from AppKit import NSUserNotification, NSUserNotificationCenter


# ___ logger settings ___
logger.remove()
logger.add(
    sys.stdout,
    format="{time:DD-MM-YYYY HH:mm:ss} | <level>{level:<7}</level> | {message}",
    colorize=True,
)


# ____ delay settings ____
min_delay = 0.3                    # min delay between clicks in seconds
max_delay = 0.4                    # max delay between clicks in seconds
pause_interval = 0.5               # pause interval in minutes
min_pause = 5                      # min pause duration in seconds
max_pause = 10                     # max pause duration in seconds


random_delay = random.uniform(min_delay, max_delay)
delay = random_delay

# ____ button settings ____
# system notification True/False(Error with Windows, MacOS - Ok)
system_notification = False
button = Button.left                # button to click
control_key = KeyCode(char='a')     # key to start/pause clicking
stop_key = KeyCode(char='b')        # key to stop the program


if platform.system() == "Windows":
    class WindowsNotifier:
        def __init__(self, title: str, message: str):
            self.title = title
            self.message = message
            self.notifier = ToastNotifier()

        def send_notification(self):
            self.notifier.show_toast(self.title, self.message, duration=5)

        def run(self):
            self.send_notification()
    sys_notifier = WindowsNotifier
else:
    class MacOSNotifier:
        def __init__(self, title: str, message: str):
            self.title = title
            self.message = message

        def send_notification(self):
            notification = NSUserNotification.alloc().init()
            notification.setTitle_(self.title)
            notification.setInformativeText_(self.message)
            NSUserNotificationCenter.defaultUserNotificationCenter(
            ).deliverNotification_(notification)

        def run(self):
            self.send_notification()
    sys_notifier = MacOSNotifier


class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True
        if system_notification:
            notifier = sys_notifier("Autoclicker is running!", "Time for coffee! ☕")
            notifier.run()

    def stop_clicking(self):
        self.running = False
        if system_notification:
            notifier = sys_notifier("Autoclicker stopped!", "Back to work!")
            notifier.run()

    def smooth_move(self, x_offset, y_offset, duration=1):
        steps = 50  # Number of small steps for smooth movement
        x_step = x_offset / steps
        y_step = y_offset / steps
        step_delay = duration / steps

        for _ in range(steps):
            mouse.move(x_step, y_step)
            time.sleep(step_delay)

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self, pause_interval=pause_interval, min_pause=min_pause, max_pause=max_pause):
        last_pause_time = time.time()
        pause_interval = pause_interval * 60  # pause interval in seconds * 60

        while self.program_running:
            while self.running:
                current_time = time.time()

                if current_time - last_pause_time >= pause_interval:
                    pause_duration = random.uniform(min_pause, max_pause)
                    x_offset = random.randint(-200, 150)
                    y_offset = random.randint(-200, 150)
                    move_duration = random.uniform(1, 3)
                    self.smooth_move(x_offset, y_offset, move_duration)
                    logger.info(f"Mouse moved by ({x_offset}, {y_offset}).")

                    logger.info(
                        f"Pausing clicking for {pause_duration:.2f} seconds.")
                    time.sleep(pause_duration)
                    last_pause_time = current_time

                mouse.click(self.button)
                time.sleep(self.delay)


mouse = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()


def on_press(key):
    try:
        if key == control_key:
            if click_thread.running:
                click_thread.stop_clicking()
                logger.warning(
                    f"Clicking paused, press {colored(control_key, 'green')} to start again.")
            else:
                click_thread.start_clicking()
                logger.success(
                    f"Clicking started, press {colored(control_key, 'green')} to pause.")

        elif key == stop_key:
            logger.info('Exiting...')
            click_thread.exit()
            listener.stop()  # Ensure listener is stopped properly
    except Exception as e:
        logger.error(f"Error in key press handling: {e}")


try:
    with Listener(on_press=on_press) as listener:
        logger.info("Mouse clicker is running.")
        logger.info(
            f"Press {colored(control_key, 'green')} to start or pause clicking.")
        logger.info(f"Press {colored(stop_key, 'red')} to stop the program.")
        listener.join()
except KeyboardInterrupt:
    logger.info('Exiting...')
    click_thread.exit()
    listener.stop()
    sys.exit(0)
