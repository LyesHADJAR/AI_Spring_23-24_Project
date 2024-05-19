import copy
import Node
import random


class AgricultureProblem:
    def __init__(self, initial_state, Search_method, products):
        self.products = products  # list of the products we search for
        # need to add goal state,transition model,path cost
        self.initial_state = copy.deepcopy(initial_state)
        self.Search_method = Search_method
        number_of_products = len(initial_state.total_production.keys())
        self.counters = {}
        for prod in self.products:
            self.counters[prod] = 5
        self.goal_state = self.generate_goal(self.initial_state)

    def cost(self, state):
        return state.getTotalLandUsed()-self.initial_state.getTotalLandUsed()

    def heuristic(self, state):  # products is a list of the season's products
        total_land_needed = 0

        for product in self.products:
            i = 0
            for value in state.cities.keys():
                if i == 0:
                    productivity = (

                        state.cities[value].products[product].production /
                        max(state.cities[value].land_used[product], 1000)
                    )
                    if productivity == 0:
                        while productivity == 0:
                            productivity = random.uniform(1, 15)
                    i += 1
                else:
                    temp = (

                        state.cities[value].products[product].production /
                        max(state.cities[value].land_used[product], 1000)
                    )
                    if temp > productivity and temp != 0:
                        productivity = temp
            production_needed = max(
                0,
                self.goal_state.total_production[product]
                - state.total_production[product],
            )
            # need to define member total_production and its update functions (easy)
            total_land_needed += production_needed / max(productivity, 1)

        return total_land_needed

    def get_best_neighbor(self, node):
        if node.state.getUnusedLand() == 0:
            return None
        best_neighbor = None
        best_value = float("-inf")
        action = None
        for action in self.actionsh(node.state, self.counters):
            child_state = self.resulth(node, action)
            child_value = self.hill_climbing_heuristic(
                child_state, self.counters)
            if child_value > best_value:
                best_neighbor = copy.deepcopy(child_state)
                best_value = child_value
        return best_neighbor

    def result(self, state, action):
        if state.state.getUnusedLand() == 0:
            return None
        newState = copy.deepcopy(state.state)
        neededprod = (
            self.goal_state.total_production[action[1]]
        )

        # the constant to be fixed
        additionalProduction = max(0.9 * max(0, neededprod), 100000)
        additionalLand = 0  # the constatn to be fixed
        productivity = newState.cities[action[0]].products[action[1]].production / max(
            newState.cities[action[0]].land_used[action[1]], 1
        )
        if productivity == 0:
            while productivity == 0:
                productivity = random.uniform(1, 15)
        additionalLand = additionalProduction / productivity
        if newState.cities[action[0]].unused_land <= additionalLand and newState.cities[action[0]].unused_land != 0:
            additionalLand = newState.cities[action[0]].unused_land
            additionalProduction = productivity * additionalLand
        else:
            return None

        newState.add(action[1], additionalProduction)
        newState.cities[action[0]].products[action[1]].production = (
            newState.cities[action[0]].products[action[1]].production
            + additionalProduction
        )
        newState.cities[action[0]].products[action[1]].productivity = newState.cities[
            action[0]
        ].products[action[1]].production / max(
            1, newState.cities[action[0]].land_used[action[1]]
        )
        newState.cities[action[0]].unused_land = max((
            newState.cities[action[0]].unused_land - additionalLand
        ), 0)
        newState.cities[action[0]].land_used[action[1]] += additionalLand
        newNode = Node.Node((newState), state, action, additionalLand, 0)
        newNode.priority = self.As_node_cost(newNode)
        return newNode

    def resulth(self, state, action):
        newState = copy.deepcopy(state.state)
        neededprod = (
            self.goal_state.total_production[action[1]]
        )
        if action[1] == "other":
            return Node.Node(copy.deepcopy(newState), state, action, 0, 0)

        additionalProduction = max((neededprod*4*0.3), 300000)
        additionalLand = 0  # the constatn to be fixed
        productivity = newState.cities[action[0]].products[action[1]].production / max(
            newState.cities[action[0]].land_used[action[1]], 1
        )
        if productivity == 0:
            productivity = 0.4
        additionalLand = additionalProduction / productivity
        if newState.cities[action[0]].unused_land < additionalLand:
            additionalLand = newState.cities[action[0]].unused_land
            additionalProduction = productivity * additionalLand

        newState.add(action[1], additionalProduction)
        newState.cities[action[0]].products[action[1]].production = (
            newState.cities[action[0]].products[action[1]].production
            + additionalProduction
        )
        newState.cities[action[0]].products[action[1]].productivity = newState.cities[
            action[0]
        ].products[action[1]].production / max(
            1, newState.cities[action[0]].land_used[action[1]]
        )
        newState.cities[action[0]].unused_land = (
            max((newState.cities[action[0]].unused_land - additionalLand), 0)
        )
        newState.cities[action[0]].land_used[action[1]] += additionalLand
        newNode = Node.Node(copy.deepcopy(newState), state,
                       action, additionalLand, 0)
        newNode.priority = self.As_node_cost(newNode)
        return newNode

    def goal_test(self, state):
        for product in self.products:
            if (
                state.total_production[product]
                < self.goal_state.total_production[product]
                and product != "other"
            ):

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
            for product in self.products:
                if (
                    state.total_production[product]
                    < self.goal_state.total_production[product]
                ) and state.cities[city].unused_land != 0:

                    actions.append([city, product])

        return actions

    def actionsh(self, state, counters):
        actions = []
        empty = 0
        for Counter in counters:
            if counters[Counter] == 0:
                empty += 1
        if empty == len(list(counters.keys())):
            for Counter in counters:
                counters[Counter] = 5
        for city in state.cities.keys():
            for product in self.products:

                if counters[product] == 0 or state.cities[city].unused_land == 0:
                    continue
                else:
                    actions.append([city, product])

        return actions

    def hill_climbing_heuristic(self, node, counters):
        product = node.action[1]
        oldproduction = node.parent.state.total_production[product]
        if counters[product] > 0:
            return node.state.total_production[product] - oldproduction
        else:
            return float(("-inf"))

    def self_sufficiency(self, state):
        newState = copy.deepcopy(state)
        for product, total_production in state.total_production.items():
            if product not in self.products:
                continue
            if total_production > state.consumption[product] * 1.17:
                continue
            else:
                newState.total_production[product] = state.consumption[product] * 1.17
        return newState

    def generate_goal(self, initial_state):

        new_goal = self.self_sufficiency(initial_state)
        # new_goal =copy.deepcopy( self.initial_state)

        strategic = 0
        non_strategic = 0
        average_productivity = {}
        # we can create a function get productivity that return a dic containing the productivity of a specific product in each wilaya
        for City in initial_state.cities.values():
            for Product in City.products.values():
                if Product.name not in self.products:
                    continue
                average_productivity[Product.name] = 0
                if Product.Strategic == True:
                    strategic += 1
                else:
                    non_strategic += 1
                average_productivity[Product.name] = average_productivity[
                    Product.name
                ] + Product.production / max(
                    City.land_used[Product.name], 1
                )  # to review

        for key in average_productivity.keys():
            average_productivity[key] = average_productivity[key] / len(
                initial_state.cities
            )

        Total_unused_land = (
            initial_state.getUnusedLand()
        )  # need to defind it in country class easy

        number_of_products = len(average_productivity.keys())

        additional_land_strategic = Total_unused_land * 0.6 / number_of_products
        additional_land_non_strategic = Total_unused_land * 0.4 / number_of_products

        Additional_production = dict([])

        for key in average_productivity.keys():
            for City in initial_state.cities.values():
                if key in City.products.keys():
                    if City.products[key].Strategic == True:
                        Additional_production[key] = (
                            average_productivity[key] *
                            additional_land_strategic
                        )
                    else:
                        Additional_production[key] = (
                            average_productivity[key] *
                            additional_land_non_strategic
                        )
                    break

        for key in Additional_production.keys():
            new_goal.update_production(
                key, Additional_production[key]
            )  # needs to be definded ez

        return new_goal
