import psutil
import time
import datetime
import platform
import os

# --- Platform-specific functions to get the foreground app ---

def get_foreground_app_windows():
    """Get the process name of the foreground window on Windows."""
    try:
        import win32gui
        import win32process
        hwnd = win32gui.GetForegroundWindow()
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        return psutil.Process(pid).name()
    except Exception:
        # This can happen if the foreground window closes before we can get its process
        return None
        
def get_foreground_app_linux():
    """A simplified way to get foreground app on Linux via xdotool."""
    # Note: Requires 'xdotool' to be installed (e.g., sudo apt-get install xdotool)
    try:
        output = os.popen('xdotool getwindowfocus getwindowname').read()
        return output.strip()
    except Exception:
        return None

# --- Main Logging Logic ---

def get_active_app_name():
    """Cross-platform function to get the active app name."""
    os_type = platform.system()
    if os_type == "Windows":
        return get_foreground_app_windows()
    elif os_type == "Linux":
        return get_foreground_app_linux()
    # macOS function has been removed as requested
    return None

def log_app_usage(log_file="app_usage_log.csv", interval_seconds=5):
    """Logs the foreground app to a CSV file at a set interval."""
    print("Starting app usage logger... Press Ctrl+C to stop.")
    last_app = None
    
    with open(log_file, "a", encoding='utf-8') as f:
        # Write header if the file is new or empty
        if os.stat(log_file).st_size == 0:
            f.write("timestamp,app_name\n")

        while True:
            try:
                current_app = get_active_app_name()
                
                # Log only when the foreground app changes and is not None
                if current_app and current_app != last_app:
                    timestamp = datetime.datetime.now().isoformat()
                    print(f"{timestamp} -> {current_app}")
                    f.write(f"{timestamp},{current_app}\n")
                    f.flush() # Ensure data is written immediately
                    last_app = current_app
                    
                time.sleep(interval_seconds)
            except KeyboardInterrupt:
                print("\nLogger stopped. Data saved to", log_file)
                break
            except Exception as e:
                # Catch other potential errors (e.g., a process disappearing)
                print(f"An error occurred: {e}")
                time.sleep(interval_seconds)


if __name__ == "__main__":
    # Before running, make sure to install necessary packages:
    # pip install psutil pywin32 # For Windows
    log_app_usage()