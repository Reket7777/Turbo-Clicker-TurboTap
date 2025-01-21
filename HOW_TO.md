### **Instructions for Running the Auto Clicker Script**

Follow these steps to run the Auto Clicker script:

---

### **1. Install Python**
Download and install Python 3.12+ from [python.org](https://www.python.org/).  
Make sure to check **Add Python to PATH** during installation.

---

### **2. Clone the Repository**
Clone this repository or download the script files.  
```bash
git clone https://github.com/Reket7777/Mouse-Clicker.git
cd <repository_folder>
   ```
---

### **3. Create a Virtual Environment (Optional)**
1. Navigate to the directory where the script is saved:
   ```bash
   cd path/to/your/script
   ```

2. Create venv

   Windows:
   ```bash
   python -m venv venv
   ```
   
   MacOs/Linux
   ```bash
   python3 -m venv venv
   ```

---

### **4. Activate the virtual environment**
   Windows:
   ```bash
   venv\Scripts\activate
   ```

   MacOS/Linux:
   ```bash
   source venv/bin/activate
   ```

---

### **5. Install the required libraries from requirements.txt**
1. Open your terminal or command prompt.

2. Install libraries:

   Windows:
   ```bash
   pip install -r requirements.txt
   ```

   MacOS/Linux:
   ```bash
   pip3 install -r requirements.txt
   ```

---

### **6. Customizing the Script**
You can modify the script to suit your needs:

1. **Change the delay between clicks**:
   - Update `min_delay` and `max_delay` in the script to set custom click intervals in seconds.
   Example:
     ```python
      min_delay = 0.5   # min delay in seconds
      max_delay = 1   # max delay in seconds
     ```

2. **Change the hotkeys**:
   - Modify the `control_key` variable to set a custom key for toggling auto-clicking:
     ```python
     control_key = KeyCode(char='a')  # Replace 'a' with your desired key
     ```

   - Modify the `stop_key` variable to set a custom key for stopping the script:
     ```python
     stop_key = KeyCode(char='b')  # Replace 'b' with your desired key
     ```

---

### **7. Run the Script**
   Windows:
   ```bash
   python mouse_clicker.py
   ```

   MacOS/Linux:
   ```bash
   python3 mouse_clicker.py
   ```



### **8. Exiting the Script**
To stop the script:
- Press the exit hotkey (`b` by default).
- Alternatively, close the terminal or command prompt.

---
