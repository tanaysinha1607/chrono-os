def calculate_session_budget(current_battery_percent, goal_battery_percent=20):
    """
    Calculates the total energy budget for a session based on current battery
    and a defined goal.
    
    :param current_battery_percent: The current battery level (e.g., 85).
    :param goal_battery_percent: The desired battery level to have at the end of the day.
    :return: The total energy budget as a percentage.
    """
    if current_battery_percent <= goal_battery_percent:
        return 0 # No budget left
    
    # Simple linear model: budget is the difference between current and goal.
    # We can add a more complex model later based on time and usage patterns.
    total_budget = current_battery_percent - goal_battery_percent
    
    # For a simple demo, we can cap the budget for a single session to prevent excessive drain.
    return min(total_budget, 10) # Cap at 10% for a typical short session