import heapq
import copy

class Product:
    def __init__(self, name, production, Strategic, removable, productivity, Season):
        self.name = name #string
        self.production = production # int
        self.Strategic = Strategic # boolean
        self.productivity = productivity # float
        self.Season = Season # list of strings
        self.removable = removable # boolean


class City:
    def __init__(self, name, unused_land, land_used, products):
        self.name = name #string
        self.unused_land = unused_land # total (int)
        self.land_used = land_used # dictionary ( product : land_used )
        self.products = products # dictionary ( product : Product )
class Country:
    def __init__(self, cities, consumption , total_production, prices):
        self.cities = cities # dictionary ( city : City )
        self.consumption = consumption # dictionary ( product : consumption )
        self.total_production = total_production # dictionary ( product : total_production )
        self.prices = prices # dictionary ( product : list of prices each season )
    
    def getTotalLandUsed(self):
        total_land_used = 0
        for city in self.cities.values():
          for value in city.land_used.values():
              total_land_used += value
        return total_land_used
    
    def getUnusedLand(self):
        total_land_unused = 0
        for city in self.cities.values():
              total_land_unused += city.unused_land
        return total_land_unused
    

    def update_production(self, product_name, additional_production):
        for city in self.cities.values():
            for product in city.products.values():
                if product.name == product_name:
                    product.production += additional_production
                    self.total_production[product_name] += additional_production
                    return


class Node:
    def __init__(self, state, parent=None, action=None, cost=0, priority=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.priority = priority
        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

class GraphSearch:
    def __init__(self, problem, strategy):
        self.problem = problem
        self.strategy = strategy

    def general_search(self):
        initial_node = Node(self.problem.initial_state)
        explored = set()
        frontier = PriorityQueue()
        frontier.put(initial_node, 0)  

        if self.strategy == "IDA_star":
            threshold = float('inf')  
        elif self.strategy == "IDS":
            depth = 0 

        while not frontier.empty():
            node = frontier.get()

            if self.strategy == "steepest":
                current_node = node
                best_neighbor = self.problem.get_best_neighbor(current_node)
                if best_neighbor:
                    frontier.put(best_neighbor, best_neighbor.priority)
                else:
                    return "failure"     
            else:
                if self.problem.goal_test(node.state):
                    return self.get_path(node)

            explored.add(node.state)

            for action in self.problem.actions(node.state):
                child_node = self.problem.result(node, action)
                if child_node.state not in explored:
                    frontier.put(child_node, child_node.priority)

                if self.strategy == "IDA_star":
                    if child_node.priority > threshold:
                        return "failure"
                    threshold = min(threshold, child_node.priority)
                elif self.strategy == "IDS":
                    if node.depth > depth:
                        return "failure"
                    depth += 1
                elif self.strategy == "UCS":
                    if node.cost > frontier.elements[0][0]:  
                        return "failure"

        return "failure"


    def get_path(self, node):
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        return list(reversed(path))

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
                        / state.cities[value].products[product].production
                    )
                    if temp < productivity:
                        productivity = temp
          production_needed = max(0,
                self.goal_state.total_production[product]
                - state.total_production[product]
            )
            # need to define member total_production and its update functions (easy)
          total_land_needed += production_needed / productivity

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
        additionalProduction = 1000 # the constant to be fixed
        additionalLand = 0 # the constatn to be fixed
        productivity=newState.cities[action[0]].products[action[1]].production/newState.cities[action[0]].land_used[action[1]]
        if productivity==0:
            productivity=0.4
        additionalLand =additionalProduction/productivity
        if newState.cities[action[0]].unused_land>additionalLand:
            additionalLand=newState.cities[action[0]].unused_land
            additionalProduction=productivity*additionalLand
    
        newState.total_production[action[1]] += additionalProduction
        newState.cities[action[0]].land_used[action[1]]+=additionalLand
        newState.cities[action[0]].products[action[1]].production+=additionalProduction
        newState.cities[action[0]].products[action[1]].productivity=newState.cities[action[0]].products[action[1]].production/newState.cities[action[0]].land_used[action[1]]
        newState.cities[action[0]].unused_land=newState.cities[action[0]].unused_land-additionalLand
        newState.cities[action[0]].land_used[action[1]] += additionalLand
        #total_land_used = state.getTotalLandUsed(state) # To be added ez
        newNode = Node(newState, state, action, additionalLand, 0)
        newNode.priority = self.As_node_cost(newNode)
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
                actions.append(city, product)
                
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
                    + Product.production / City.land_used[Product.name]
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
        for key, value in new_goal.total_production.items():
            print(key," : ", value)
        return new_goal

def main():
    # Create some products
    wheat = Product("Wheat", 100, 200, False, True, ["Spring", "Summer"])
    corn = Product("Corn", 150, False, True, 300, ["Summer", "Fall"])

    # Create a city with these products
    city1 = City("City1", 500, {"Wheat" : 1000, "Corn" : 500}, {"Wheat": wheat, "Corn": corn})

    # Create a country with this city
    country1 = Country({"City1" : city1}, {"Wheat": 1000, "Corn": 1000}, {"Wheat" : 700, "Corn" : 900}, {"Wheat": 2, "Corn": 3})

    # Print the total production
    print("================================================")
    print(country1.total_production)

    # Update the total production and print it again
    print("================================================")
    country1.update_production("Wheat", 100)
    print(country1.total_production)

    # Create an AgricultureProblem and find the goal for a given season
    print("================================================")
    problem = AgricultureProblem(country1, "gjhgfgfjg")
    print("================================================")
    node = Node(country1, None, None, 0, 0)
    print(problem.result(node, ["City1", "Wheat"]).state.total_production)
    

if __name__ == "__main__":
    main()
