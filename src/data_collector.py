import pandas as pd
import os

def get_recent_app_history(num_apps=5):
    
    log_file= os.path.join('seer_layer', 'app_usage_log.csv')
    try:
        df = pd.read_csv(log_file)
        if df.empty:
            print("Warning: Log file is empty. Using a default app history.")
            return ["Code.exe", "chrome.exe", "Spotify.exe", "ms-teams.exe", "GitHubDesktop.exe"]
        
        # Drop consecutive duplicates 
        unique_app_switches = df['app_name'].loc[df['app_name'].shift() != df['app_name']]
        
        # Get the last N apps from this cleaned list
        recent_apps = unique_app_switches.tail(num_apps).tolist()
        return recent_apps
        
    except FileNotFoundError:
        print(f"Warning: Log file '{log_file}' not found. Using a default app history.")
        return ["Code.exe", "chrome.exe", "Spotify.exe", "ms-teams.exe", "GitHubDesktop.exe"]

