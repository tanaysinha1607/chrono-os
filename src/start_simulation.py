import subprocess
import sys
import os
import time

from main import simulate_chrono_os

def start_background_logger():
    
    python_executable = os.path.join(sys.prefix, 'pythonw.exe') if sys.platform == "win32" else sys.executable
    
    logger_script_path = os.path.join('seer_layer', 'data_logger.py')

    print("Starting the background data logger\n")
    
    try:
        subprocess.Popen([python_executable, logger_script_path],
                         creationflags=subprocess.DETACHED_PROCESS,
                         close_fds=True)
        print("Logger is now running silently in the background.")
        print("IMPORTANT: To stop it, open Task Manager and end the 'pythonw.exe' process.")
    except Exception as e:
        print(f"Error starting background logger: {e}")
        print("Please ensure you are running this from an activated virtual environment.")
    time.sleep(2) 

if __name__ == "__main__":
    start_background_logger()
    
    print("\n" + "="*50)
    print("--- Starting the Main ChronoOS Simulation ---")
    print("="*50 + "\n")
    
    simulate_chrono_os()
