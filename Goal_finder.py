
def goal_finder(self, objective_number):
        if objective_number == 1:
            return self.goal_function_for_objective1
        elif objective_number == 2:
            return self.goal_function_for_objective2
        elif objective_number == 3:
            return self.goal_function_for_objective3
        else:
            raise ValueError("Invalid objective number")

#Goal_function for self-sufficiency for each product:
def goal_function_for_objective3(self, state):
    for product in state.products:
        total_production = sum(city.products[product.name].production for city in state.cities)
        if total_production < self.goal_state.consumption[product.name]:
            return False
    return True
