
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
  

def goal_function_for_objective1(self, state):
  for state in state.cities:
    for product in state.products:
      
      production = state.city.products[product.name].production
      consumption = self.goal_state.consumption[product.name]
      landUsed = state.city.products[product.name].land_used
      productivity = production / landUsed
      
      if state.city.products[product.name].production > self.goal_state.consumption[product.name]:
        return True
      else:
        newProd = consumption * ( 1 + (productivity / 1000) ) - production
        newLand = newProd / productivity
        landUsed += newLand
        return True
# We need to discuss how to update the prices here

def goal_function_for_objective1_updated(self, state):
  for product in state.products:
    total_production = sum(city.products[product.name].production for city in state.cities)
    total_consumption = self.goal_state.consumption[product.name]
    total_landUsed = sum(city.products[product.name].land_used for city in state.cities)
    total_productivity = total_production / total_landUsed
    if total_production > total_consumption * 1.05:
      return state
    else:
      # here I need to update the state with the new production and land used
      newProd = total_consumption * ( 1 + (total_productivity / 1000) ) - total_production
      newLand = newProd / total_productivity
      total_landUsed += newLand
      return state
    
