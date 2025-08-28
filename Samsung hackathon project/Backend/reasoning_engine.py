from data_store import get_app_power_scores

class ReasoningEngine:
    def __init__(self, total_budget):
        self.total_budget = total_budget
        self.app_scores = get_app_power_scores()
        self.allocated_budget = 0

    def plan_allocation(self, predicted_app_sequence):
        """
        Allocates the total energy budget across a predicted app sequence.
        
        :param predicted_app_sequence: A list of app names.
        :return: A list of throttling directives.
        """
        throttling_directives = []
        remaining_budget = self.total_budget
        
        # Determine total 'power need' of the session
        total_power_need = sum(self.app_scores.get(app, self.app_scores['medium_power_app']) for app in predicted_app_sequence)
        
        if total_power_need == 0:
            return []

        # Simple Proportional Allocation Strategy
        for app in predicted_app_sequence:
            power_score = self.app_scores.get(app, self.app_scores['medium_power_app'])
            
            # Calculate the proportion of budget for this app
            proportional_budget = (power_score / total_power_need) * self.total_budget
            
            directive = {
                'app': app,
                'priority': 'high' if power_score >= 4 else 'low',
                'allocated_percentage': proportional_budget,
                'action': 'full_performance' # Default action
            }
            
            # Rule-based Throttling
            if proportional_budget > remaining_budget:
                directive['action'] = 'throttle_aggressively'
            elif directive['priority'] == 'low':
                directive['action'] = 'throttle_lightly'
            
            throttling_directives.append(directive)
            remaining_budget -= proportional_budget
            
        self.allocated_budget = self.total_budget - remaining_budget
        
        return throttling_directives
        