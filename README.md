# Turbo-Clicker for Eclipse TurboTap

### **Turbo Clicker with Hotkeys**

This script is a customizable **auto clicker** that automates mouse clicks with a configurable delay. It allows users to start, stop, and terminate the auto clicker using predefined hotkeys.

<img width="777" alt="image" src="https://github.com/user-attachments/assets/e8e917b4-35e5-4d31-8607-b4c670028086" />

#### Features:
1. **Automated Mouse Clicking**:
   - Simulates left mouse button clicks with a time interval specified by the `delay` variable.
2. **Hotkey Controls**:
   - Press `a` (configurable via the `control_key` variable) to toggle auto-clicking on or off.
   - Press `b` (configurable via the `stop_key` variable) to stop the script completely.
3. **Flexible Configuration**:
   - Adjust the `delay` variable to set the interval between clicks.
   - Easily switch between left or right mouse button by modifying the `button` variable.
4. **Smooth Operation**:
   - Utilizes nested loops to maintain responsiveness and prevent crashes.
   - Quickly reacts to hotkey presses without noticeable delays.
5. **Multithreading**:
   - Uses the `threading` module to run the auto-clicker in the background, allowing seamless interaction with the script.

#### Use Cases:
- Automating repetitive clicking tasks on your computer.
- Assisting in games where auto-clicking is permitted.
- Conducting user interface testing requiring repeated clicks.

The script is written in Python, leveraging the `pynput` library for mouse and keyboard interaction and `threading` for parallel execution of tasks. This lightweight and customizable tool is ideal for anyone looking to automate mouse interactions efficiently.
