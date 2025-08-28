class ActuationKernel:
    def __init__(self):
        self.simulated_battery = 0

    def set_initial_battery(self, battery_level):
        self.simulated_battery = battery_level
        print(f"[{self.simulated_battery}%] INFO: Session started.")

    def apply_directives(self, directives):
        """
        Simulates applying the throttling directives and logs the outcome.
        
        :param directives: A list of directives from the Planner.
        """
        simulated_time = 0
        for directive in directives:
            app_name = directive['app']
            action = directive['action']
            allocated_budget = directive['allocated_percentage']
            
            simulated_time += 15 # Simulate 15 minutes of usage per app

            if action == 'full_performance':
                simulated_drain = allocated_budget
                self.simulated_battery -= simulated_drain
                print(f"[{self.simulated_battery:.2f}%] LOG: {app_name} is running at full performance. Drained {simulated_drain:.2f}% battery.")
            
            elif action == 'throttle_lightly':
                simulated_drain = allocated_budget * 0.7 # Simulate 30% reduction
                self.simulated_battery -= simulated_drain
                print(f"[{self.simulated_battery:.2f}%] LOG: {app_name} is lightly throttled to save power. Drained {simulated_drain:.2f}% battery.")
                
            elif action == 'throttle_aggressively':
                simulated_drain = allocated_budget * 0.4 # Simulate 60% reduction
                self.simulated_battery -= simulated_drain
                print(f"[{self.simulated_battery:.2f}%] LOG: {app_name} is aggressively throttled. Drained {simulated_drain:.2f}% battery.")
            
            if self.simulated_battery <= 0:
                print("BATTERY LOW: The device ran out of battery!")
                break