import heapq


class Product:
    def __init__(self, name, prices, land_used, production):
        self.name = name
        self.prices = prices
        self.land_used = land_used
        self.production = production


class City:
    def __init__(self, name, agriculture_land, unused_land, products):
        self.name = name
        self.agriculture_land = agriculture_land
        self.unused_land = unused_land
        self.products = sorted(products, key=lambda x: (x.production, x.prices))


class Country:
    def __init__(self, cities, consumption):
        self.cities = cities
        self.consumption = consumption

    def __repr__(self):
        return f"Country with cities: {[city.name for city in self.cities]}"


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


class Search:
    def __init__(self):
        pass

    def general_search(self, problem, frontier):
        explored = set()
        initial_node = Node(problem.initial_state)
        frontier.put(initial_node, 0)

        while not frontier.empty():
            current_node = frontier.get()

            if problem.goal_test(current_node.state):
                return current_node

            explored.add(current_node.state)
            for action in problem.actions(current_node.state):
                child_state = problem.result(current_node.state, action)
                if child_state not in explored:
                    child_node = Node(state=child_state, parent=current_node)
                    child_cost = problem.cost(child_state)
                    frontier.put(child_node, child_cost)
                    explored.add(child_state)

        return None


class AgricultureProblem:
    def __init__(
        self, initial_state, Search_method, objective
    ):  # need to add goal state,transition model,path cost
        self.initial_state = initial_state
        self.Search_method = Search_method
        self.objective = objective

    def cost(self, state):
        total_land_used = sum(
            product.land_used for city in state.cities for product in city.products
        )
        return total_land_used

    def heuristic(self, state, products):  # products is a list of the season's products
        total_land_needed = 0

        for product in products:
            for i in range(0, len(state.cities)):
                if i == 0:
                    productivity = (
                        state.cities[i].products[product.name].land_used
                        / state.cities[i].products[product.name].production
                    )
                else:
                    temp = (
                        state.cities[i].products[product.name].land_used
                        / state.cities[i].products[product.name].production
                    )
                    if temp < productivity:
                        productivity = temp
            production_needed = (
                self.goal_state.total_production[product]
                - state.total_production[product]
            )
            # need to define member total_production and its update functions (easy)
            total_land_needed += production_needed / productivity

        return total_land_needed

    def goal_finder(self, objective_number):
        if objective_number == 1:
            return self.goal_function_for_objective1
        elif objective_number == 2:
            return self.goal_function_for_objective2
        elif objective_number == 3:
            return self.goal_function_for_objective3
        else:
            raise ValueError("Invalid objective number")

    def goal_function_for_objective3(self, state):
        for product in state.products:
            total_production = sum(
                city.products[product.name].production for city in state.cities
            )
            if total_production < self.goal_state.consumption[product.name]:
                return False
        return True

    def result(self, state, action):
        return action

    def goal_test(self, state):
        goal_function = self.goal_finder(len(self.objective))
        return goal_function(state)

    def As_node_cost(self, node):
        heuristic_cost = self.heuristic(node.state)
        if self.Search_method == "IDA_star":
            node.priority = heuristic_cost + node.cost
        elif self.Search_method == "UCS":
            node.priority = node.cost
        else:
            node.priority = heuristic_cost
        return node.priority

    def search(self):
        search = Search()

        if self.Search_method == "UCS":
            return search.general_search(self, PriorityQueue())

        elif self.Search_method == "IDS":
            return self.ids_search(search)

        elif self.Search_method == "IDA_star":
            return self.ida_star_search(search)

        return None

    def ids_search(self, search):
        depth = 0
        while True:
            result = search.general_search(self, PriorityQueue())
            if result == "FOUND":
                return result
            if result == float("inf"):
                return None
            depth += 1

    def ida_star_search(self, search):
        threshold = self.As_node_cost(Node(self.initial_state))
        while True:
            result = search.depth_limited_search(
                self, Node(self.initial_state), threshold
            )
            if result == "FOUND":
                return result
            if result == float("inf"):
                return None
            threshold = result

    def actions(self, state):
        return []

    # This part is for Hill Climbing ( steapest ascent )
    def Hill_Climbing(self, state):
        current_state = state
        while True:
            neighbor = self.best_neighbor(current_state)
            if self.heuristic_hill_climbing(neighbor) >= self.heuristic_hill_climbing(current_state):
                return current_state
            current_state = neighbor
            
    def best_neighbor(self, state):
        best_state = state
        for action in self.actions(state):
            neighbor = self.result(state, action)
            if self.heuristic_hill_climbing(neighbor) > self.heuristic_hill_climbing(best_state):
                best_state = neighbor
        return best_state
      
    def heuristic_hill_climbing(self, state):
        average_productivity = sum(city.products[product.name].production / city.products[product.name].land_used
                                   for city in state.cities for product in city.products) / len(state.products)
        return self.state.products[0].production / self.state.products[0].land_used - average_productivity
