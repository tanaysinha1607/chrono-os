from planner_utils import calculate_session_budget
from reasoning_engine import ReasoningEngine
from actuation_kernel import ActuationKernel
import time

def simulate_chrono_os():
    """
    Main function to simulate the ChronoOS workflow.
    """
    print("--- ChronoOS Simulation Started ---")
    
    # Step 1: Perception & Prediction (Simulated)
    current_battery = 85
    predicted_app_sequence = ["Spotify", "Google Maps", "Reddit", "Slack"]
    user_goal = "make it to 5 PM"
    
    print(f"\nUser context detected: {current_battery}% battery. Goal: {user_goal}")
    print(f"Predicted app journey: {predicted_app_sequence}")
    time.sleep(1)

    # Step 2: Strategy (The Planner)
    session_budget = calculate_session_budget(current_battery)
    print(f"\nPlanner has set a total energy budget of {session_budget}% for this session.")
    time.sleep(1)
    
    planner = ReasoningEngine(total_budget=session_budget)
    throttling_directives = planner.plan_allocation(predicted_app_sequence)
    
    print("\nPlanner's Directives:")
    for directive in throttling_directives:
        print(f"  - App: {directive['app']}, Action: {directive['action']}, Budget: {directive['allocated_percentage']:.2f}%")
    time.sleep(2)
    
    # Step 3: Allocation & Actuation (The Governor)
    governor = ActuationKernel()
    governor.set_initial_battery(current_battery)
    governor.apply_directives(throttling_directives)
    
    print("\n--- ChronoOS Simulation Complete ---")
    print(f"Final simulated battery level: {governor.simulated_battery:.2f}%")

if __name__ == "__main__":
    simulate_chrono_os()