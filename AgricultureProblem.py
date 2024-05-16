import copy
import Node

class AgricultureProblem:
    def __init__(self, initial_state, Search_method):  # need to add goal state,transition model,path cost
        self.initial_state = copy.deepcopy(initial_state)
        self.Search_method = Search_method
        number_of_products = len(initial_state.total_production.keys())
        self.counters = []
        for i in range(number_of_products):
            self.counters.append(5) 
        self.goal_state = self.generate_goal(self.initial_state)

    def cost(self, state):
       return state.getTotalLandUsed()

    def heuristic(self, state):  # products is a list of the season's products
        total_land_needed = 0
    
        for product in state.total_production.keys():
          if product=="other":
            continue
          i=0
          for value in state.cities.keys():
                if i == 0:
                    productivity = (
                        state.cities[value].land_used[product]
                        / state.cities[value].products[product].production
                    )
                    i += 1
                else:
                    temp = (
                        state.cities[value].land_used[product]
                        / max(state.cities[value].products[product].production,1)
                    )
                    if temp < productivity:
                        productivity = temp
          production_needed = max(0,
                self.goal_state.total_production[product]
                - state.total_production[product]
            )
            # need to define member total_production and its update functions (easy)
          total_land_needed += production_needed / max(productivity,1)

        return total_land_needed


    def get_best_neighbor(self, node):
      best_neighbor = None
      best_value = float('-inf')
      action=None
      for action in self.actions(node.state):
        child_state = self.result(node, action)
        child_value = self.hill_climbing_heuristic(child_state, self.counters)
        if child_value  > best_value:
            best_neighbor = child_state
            best_value = child_value

      return best_neighbor
   
    def result(self, state, action):
        newState = copy.deepcopy(state.state)
        if action[1]=="other":
            return  Node.Node(copy.deepcopy(newState), state, action, 0, 0)
        additionalProduction = 1000 # the constant to be fixed
        additionalLand = 0 # the constatn to be fixed
        productivity=newState.cities[action[0]].products[action[1]].production/max(newState.cities[action[0]].land_used[action[1]],1)
        if productivity==0:
            productivity=0.4
        additionalLand =additionalProduction/productivity
        if newState.cities[action[0]].unused_land<=additionalLand:
            additionalLand=newState.cities[action[0]].unused_land
            additionalProduction=productivity*additionalLand
        print("===========================")
        print(newState.total_production[action[1]])   
        print(action[1])

        
        newState.add(action[1],additionalProduction) 
        print(newState.total_production[action[1]])
        print("===========================")
        newState.cities[action[0]].products[action[1]].production=newState.cities[action[0]].products[action[1]].production+additionalProduction
        newState.cities[action[0]].products[action[1]].productivity=newState.cities[action[0]].products[action[1]].production/max(1,newState.cities[action[0]].land_used[action[1]])
        newState.cities[action[0]].unused_land=newState.cities[action[0]].unused_land-additionalLand
        newState.cities[action[0]].land_used[action[1]] += additionalLand
        #total_land_used = state.getTotalLandUsed(state) # To be added ez
        #print(newState.cities[action[0]].land_used[action[1]])
        newNode = Node.Node(copy.deepcopy(newState), state, action, additionalLand, 0)
        newNode.priority = self.As_node_cost(newNode)
        print(newNode.state.total_production)
        return newNode

    def goal_test(self, state):
        for product in state.total_production.keys():
            if state.total_production[product] < self.goal_state.total_production[product]:
                return False
        return True
                

    def As_node_cost(self, node):
        heuristic_cost = self.heuristic(node.state)
        if self.Search_method == "IDA_star":
            node.priority = heuristic_cost + node.cost
        elif self.Search_method == "UCS":
            node.priority = node.cost
        else:
            node.priority = heuristic_cost
        return node.priority


    def actions(self, state):
        actions = []
        for city in state.cities.keys():
            for product in state.cities[city].products.keys():
                actions.append([city, product])
                
        return actions
      
    def hill_climbing_heuristic(self, node, counters):
      empty=0
      for Counter in counters:
        if Counter ==0:
          empty+=1
      if empty==len(counters):
        for Counter in counters:
          Counter =5
      
      product = node.action[1]
      oldproduction=node.parent.state.total_prpduction[product]
      if counters[product] > 0:
        return node.state.total_production[product]-oldproduction
      else:
        return float(str('-inf'))
    
    def self_sufficiency(self, state):
      newState = copy.deepcopy(state)
      for product, total_production in state.total_production.items():
        if total_production > state.consumption[product] * 1.17:
            continue
        else:
            newState.total_production[product] = state.consumption[product] * 1.17
      return newState
   
    def generate_goal(self, initial_state):
        new_goal = self.self_sufficiency(initial_state)
        strategic = 0
        non_strategic = 0
        average_productivity = {}
        ##we can create a function get productivity that return a dic containing the productivity of a specific product in each wilaya
        for City in initial_state.cities.values():
            for Product in City.products.values():
                average_productivity[Product.name] =0
                if Product.Strategic == True:
                    strategic += 1
                else:
                    non_strategic += 1
                average_productivity[Product.name] = (
                    average_productivity[Product.name]
                    + Product.production / max(City.land_used[Product.name],1)
                )  ##to review

        for key in average_productivity.keys():
            average_productivity[key] = average_productivity[key] / len(initial_state.cities)  ##or 58

        Total_unused_land = (
            initial_state.getUnusedLand()
        )  ##need to defind it in country class easy

        number_of_products = len(average_productivity.keys())

        additional_land_strategic = Total_unused_land * 0.6 / number_of_products
        additional_land_non_strategic = Total_unused_land * 0.4 / number_of_products

        Additional_production = dict([])

        for key in average_productivity.keys():
            for City in initial_state.cities.values():
                if key in City.products.keys():
                    if City.products[key].Strategic == True:
                        Additional_production[key] = (
                            average_productivity[key] * additional_land_strategic
                        )
                    else:
                        Additional_production[key] = (
                            average_productivity[key] * additional_land_non_strategic
                        )
                    break
                
        for key in Additional_production.keys():
            new_goal.update_production(key, Additional_production[key])  # needs to be definded ez
        return new_goal
