import time
import threading
import platform
import random
import sys

from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
from termcolor import colored
from loguru import logger

import config

if platform.system() == "Windows":
    from win10toast import ToastNotifier
else:
    from AppKit import NSUserNotification, NSUserNotificationCenter

# Налаштування логування
logger.remove()
logger.add(
    sys.stdout,
    format="{time:DD-MM-YYYY HH:mm:ss} | <level>{level:<7}</level> | {message}",
    colorize=True,
)


total_taps = config.TOTAL_TAPS  # Общая количество кликов
# Количество циклов, на которые нужно разделить total_taps
number_of_cycles = config.NUMBER_OF_CYCLES


min_delay = config.MIN_DELAY    # Минимальная задержка между кликами (секунды)
max_delay = config.MAX_DELAY    # Максимальная задержка между кликами (секунды)
# Минимальная длительность паузы между циклами (секунды)
min_pause = config.MIN_PAUSE
# Максимальная длительность паузы между циклами (секунды)
max_pause = config.MAX_PAUSE

# Диапазон случайного увеличения задержки (имитация усталости)
# Минимальное увеличение задержки за клик
min_fatigue_increase = config.MIN_FATIGUE_INCREASE
# Максимальное увеличение задержки за клик
max_fatigue_increase = config.MAX_FATIGUE_INCREASE


system_notification = config.SYSTEM_NOTIFICATION
button = Button.left if config.BUTTON_TYPE == 'left' else Button.right  # Кнопка для клика
# Клавиша для старта/паузы кликов
control_key = KeyCode(char=config.CONTROL_KEY)
stop_key = KeyCode(char=config.STOP_KEY)    # Клавиша для остановки программы


# Функция для случайного распределения total_taps на заданное количество циклов
def partition_taps(total, parts):
    rand_numbers = [random.random() for _ in range(parts)]
    total_rand = sum(rand_numbers)
    parts_values = [int(round(total * (r / total_rand))) for r in rand_numbers]
    diff = total - sum(parts_values)
    parts_values[0] += diff
    return sorted(parts_values, reverse=True)


# Автоматическое распределение кликов по циклам
cycles = partition_taps(total_taps, number_of_cycles)
logger.info(f"Tap distribution among cycles: {cycles}")

# Уведомление для Windows/MacOS
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
    def __init__(self, cycles, min_delay, max_delay, button, min_fatigue_increase, max_fatigue_increase):
        super(ClickMouse, self).__init__()
        self.cycles = cycles                  # Список количества кликов в каждом цикле
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.button = button
        self.min_fatigue_increase = min_fatigue_increase
        self.max_fatigue_increase = max_fatigue_increase
        self.running = False                  # Флаг: клики выполняются или на паузе
        self.program_running = True           # Флаг работы программы
        self.current_delay = random.uniform(self.min_delay, self.max_delay)

    def start_clicking(self):
        self.running = True
        if system_notification:
            notifier = sys_notifier(
                "Turboclicker is running!", "Time for coffee! ☕")
            notifier.run()

    def stop_clicking(self):
        self.running = False
        if system_notification:
            notifier = sys_notifier("Turboclicker stopped!", "Back to work!")
            notifier.run()

    def smooth_move(self, x_offset, y_offset, duration=1):
        steps = 50  # Количество шагов для плавного движения
        x_step = x_offset / steps
        y_step = y_offset / steps
        step_delay = duration / steps
        for _ in range(steps):
            mouse.move(x_step, y_step)
            time.sleep(step_delay)

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        cycle_number = 0
        for cycle_taps in self.cycles:
            cycle_number += 1
            # Засекаем время начала цикла
            cycle_start_time = time.time()
            # В начале каждого цикла сбрасываем задержку до случайного значения в диапазоне [min_delay, max_delay]
            self.current_delay = random.uniform(self.min_delay, self.max_delay)
            logger.info(
                f"Starting cycle {cycle_number} with {cycle_taps} taps. Initial delay: {self.current_delay:.3f} sec")
            for i in range(cycle_taps):
                # Если кликание поставлено на паузу, ждем продолжения
                while not self.running and self.program_running:
                    time.sleep(0.1)
                if not self.program_running:
                    return
                mouse.click(self.button)
                logger.info(
                    f"Cycle {cycle_number}: performed tap {i+1}/{cycle_taps}")
                time.sleep(self.current_delay)
                # Случайное увеличение задержки за клик (в диапазоне min_fatigue_increase - max_fatigue_increase)
                fatigue_increase = random.uniform(
                    self.min_fatigue_increase, self.max_fatigue_increase)
                self.current_delay += fatigue_increase
            # Засекаем время окончания цикла
            cycle_end_time = time.time()
            cycle_duration = cycle_end_time - cycle_start_time
            # Рассчитываем среднюю скорость: кликов в минуту
            taps_per_minute = (cycle_taps / cycle_duration) * 60
            logger.success(
                f"Cycle {cycle_number} completed in {cycle_duration:.2f} sec. Average speed: {taps_per_minute:.2f} taps/min")
            # Между циклами делаем случайную паузу, если это не последний цикл
            if cycle_number < len(self.cycles):
                pause_duration = random.uniform(min_pause, max_pause)
                logger.success(
                    f"Cycle {cycle_number} completed. Pausing for {pause_duration:.2f} seconds before next cycle.")
                time.sleep(pause_duration)

        logger.success(
            "All cycles completed. Waiting for user input to continue.")
        self.stop_clicking()
        while True:
            logger.warning(f"Restart Turboclicker? (y/n):")
            ask = str(input().strip().lower())
            if ask == '' or ask == 'y':
                logger.info("Restarting Turboclicker...")
                logger.info(f"Press {colored(control_key, 'green')} to start")
                click_thread.run()  # Restart the clicking process
                break
            elif ask == 'n':
                logger.info('Exiting...')
                click_thread.exit()
                listener.stop()
                sys.exit()


mouse = Controller()
click_thread = ClickMouse(cycles, min_delay, max_delay,
                          button, min_fatigue_increase, max_fatigue_increase)
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
            listener.stop()  # Остановка слушателя клавиатуры
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
    sys.exit()
