from planner_actuator.planner_utils import calculate_session_budget
from planner_actuator.reasoning_engine import ReasoningEngine
from planner_actuator.actuation_kernel import ActuationKernel
from seer_engine import SeerEngine
import time
import psutil 

def get_battery_level():
    battery = psutil.sensors_battery()
    if battery:
        return int(battery.percent)
    return 85

def simulate_chrono_os():
    
    print("--- ChronoOS Simulation Started ---")
    
    # Perception & Prediction
    seer = SeerEngine()
    current_battery = get_battery_level()
    recent_app_history = ["Code.exe", "chrome.exe", "Spotify.exe", "ms-teams.exe", "GitHubDesktop.exe"]
    predicted_app_sequence = seer.predict_next_apps(recent_app_history)
    user_goal = "make it to 5 PM"
    
    print(f"\nUser context detected: {current_battery}% battery. Goal: {user_goal}")
    print(f"Predicted app journey: {predicted_app_sequence}")
    time.sleep(1)

    # Strategy (The Planner)
    session_budget = calculate_session_budget(current_battery)
    print(f"\nPlanner has set a total energy budget of {session_budget}% for this session.")
    time.sleep(1)
    
    planner = ReasoningEngine(total_budget=session_budget)
    throttling_directives = planner.plan_allocation(predicted_app_sequence)
    
    print("\nPlanner's Directives:")
    for directive in throttling_directives:
        print(f"  - App: {directive['app']}, Action: {directive['action']}, Budget: {directive['allocated_percentage']:.2f}%")
    time.sleep(2)
    
    # Allocation & Actuation (The Governor)
    governor = ActuationKernel()
    governor.set_initial_battery(current_battery)
    governor.apply_directives(throttling_directives)
    
    print("\n--- ChronoOS Simulation Complete ---")
    print(f"Final simulated battery level: {governor.simulated_battery:.2f}%")

if __name__ == "__main__":
    simulate_chrono_os()