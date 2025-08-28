from .data_store import get_app_data 
class ReasoningEngine:
    def __init__(self, total_budget):
        self.total_budget = total_budget
        _,self.app_categories, self.category_scores = get_app_data()
        self.allocated_budget = 0

    def _get_power_score_for_app(self, app_name):
        """Finds the power score for a given app name via its category."""
        category = self.app_categories.get(app_name, "default")
        score = self.category_scores.get(category, self.category_scores["miscellaneous"])
        return score

    def plan_allocation(self, predicted_app_sequence):
        """
        Allocates the total energy budget across a predicted app sequence.
        """
        throttling_directives = []
        
        total_power_need = sum(self._get_power_score_for_app(app) for app in predicted_app_sequence)
        
        if total_power_need == 0:
            return []

        for app in predicted_app_sequence:
            power_score = self._get_power_score_for_app(app)
            
            proportional_budget = (power_score / total_power_need) * self.total_budget

            action = 'full_performance' 
            if power_score <= 2: 
                action = 'throttle_lightly'
            
            directive = {
                'app': app,
                'allocated_percentage': proportional_budget,
                'action': action
            }
            
            throttling_directives.append(directive)
            
        return throttling_directives
