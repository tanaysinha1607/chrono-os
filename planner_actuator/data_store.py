import json

def get_app_data():
    """
    Returns dictionaries containing app IDs, categories, and power scores.
    This is a more sophisticated version of the static data store.
    """
    # Unique IDs for each app, not used by the planner but good for structure.
    app_ids = {
        "Code.exe": 0, "chrome.exe": 1, "ApplicationFrameHost.exe": 2, 
        "Spotify.exe": 3, "ShellExperienceHost.exe": 4, "ShellHost.exe": 5, 
        "ms-teams.exe": 6, "SearchHost.exe": 7, "Canva.exe": 8, 
        "SnippingTool.exe": 9, "PickerHost.exe": 10, "onlinent.exe": 11, 
        "AsusKeyboardHost.exe": 12, "WindowsTerminal.exe": 13, "PredatorSense.exe": 14, 
        "LockApp.exe": 15, "GitHubDesktop.exe": 16, "Riot Client.exe": 17, 
        "brave.exe": 18, "VALORANT-Win64-Shipping.exe": 19, "EXCEL.EXE": 20,
        "unknown_app": 999 
    }

    # A mapping from app names to broader categories.
    app_categories = {
        "Code.exe": "dev_tool", "chrome.exe": "web_browser", 
        "ApplicationFrameHost.exe": "os_utility", "Spotify.exe": "media", 
        "ShellExperienceHost.exe": "os_utility", "ShellHost.exe": "os_utility", 
        "ms-teams.exe": "work_tool", "SearchHost.exe": "os_utility", "Canva.exe": "creative_tool", 
        "SnippingTool.exe": "os_utility", "PickerHost.exe": "os_utility", "onlinent.exe": "gaming", 
        "AsusKeyboardHost.exe": "system_utility", "WindowsTerminal.exe": "dev_tool", 
        "PredatorSense.exe": "system_utility", "LockApp.exe": "os_utility", 
        "GitHubDesktop.exe": "dev_tool", "Riot Client.exe": "gaming", 
        "brave.exe": "web_browser", "VALORANT-Win64-Shipping.exe": "gaming", 
        "EXCEL.EXE": "work_tool", "unknown_app": "miscellaneous" 
    }

    # Power scores based on app categories.
    category_power_scores = {
        "dev_tool": 3,
        "web_browser": 4,
        "os_utility": 1,
        "media": 3,
        "work_tool": 2,
        "creative_tool": 4,
        "system_utility": 1,
        "gaming": 5,
        "miscellaneous": 2  # Default score for unknown apps
    }
    
    return app_ids, app_categories, category_power_scores
