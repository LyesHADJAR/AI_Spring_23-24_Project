import heapq
import copy
import csv
import random
import markdown

class Product:
    def __init__(self, name, production, Strategic, removable, productivity, Season):
        self.name = name  # string
        self.production = production  # int
        self.Strategic = Strategic  # boolean
        self.productivity = productivity  # float
        self.Season = Season  # list of strings
        self.removable = removable  # boolean


class City:
    def __init__(self, name, unused_land, land_used, products):
        self.name = name  # string
        self.unused_land = unused_land  # total (int)
        self.land_used = land_used  # dictionary ( product : land_used )
        self.products = products  # dictionary ( product : Product )


class Country:
    def __init__(self, cities, consumption, total_production, prices):
        self.cities = cities  # dictionary ( city : City )
        self.consumption = consumption  # dictionary ( product : consumption )
        self.total_production = (
            total_production  # dictionary ( product : total_production )
        )
        self.prices = prices  # dictionary ( product : list of prices each season )

    def add(self, citi, value):
        self.total_production[citi] += value


    def to_markdown(self):
        markdown_text = "| City | Product | Land Used | Production |\n"
        markdown_text += "| --- | --- | --- | --- |\n"
        for city in self.cities.values():
            for product in city.products.values():
                if product.name=='':
                    markdown_text += f"| {city.name} | {product.name} | {city.land_used[product.name]} | {product.production} |\n"
        return markdown_text
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

        self.total_production[product_name] += additional_production
        return

    def __eq__(self, object):
        for city in self.cities.keys():
            for products in self.total_production.keys():
                if (
                    self.cities[city].land_used[products]
                    != object.cities[city].land_used[products]):
                    return False
        return True

    def __hash__(self) -> int:
        hashval = 0
        for products in self.total_production.keys():
            hashval += hash(products) * self.total_production[products]
        return int(hashval)


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

    def __gt__(self, other):
        return self.priority > other.priority


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

    def lenght(self):
        return len(self.elements)


class stack:
    def __init__(self):
        self.elements = []
    def clear(self):
        self.elements.clear()
    def get(self):
        item = self.elements[len(self.elements) - 1]
        self.elements.pop(len(self.elements) - 1)
        return item

    def put(self, item,val):
        self.elements.append(item)

    def empty(self):
        return len(self.elements) == 0

    def print(self):
        for i in range(0, len(self.elements)):
            print(self.elements[i])


class queue:
    def __init__(self):
        self.elements = []
    def clear(self):
        self.elements.clear()
    def get(self):
        if not self.empty():
            item = self.elements[0]
            self.elements.pop(0)
            return item

    def put(self, item,val):
        self.elements.append(item)

    def empty(self):
        return len(self.elements) == 0

    def print(self):
        for i in range(0, len(self.elements)):
            print(self.elements[i])




class GraphSearch:
    def __init__(self, problem, strategy):
        self.problem = problem
        self.strategy = strategy

    def general_search(self):
        initial_node = Node(self.problem.initial_state)
        explored = set()
        
        frontier = PriorityQueue()

        if self.strategy == "IDA_star":
            threshold = float("inf")
        elif self.strategy == "IDS":
            depth = 0
            frontier=stack()
        elif self.strategy == "BFS":
            depth = 0
            frontier=queue() 
        frontier.put(initial_node, 0)  
        i = 0

        while not frontier.empty():
            
            # print((frontier).lenght())
            #print(len(frontier.elements))
           #print(len(frontier.elements))
            node = copy.deepcopy(frontier.get())
            #print(node)
            print("==================")
            print("unused needed=")
        
            print(node.state.getTotalLandUsed())
            print(node.state.getUnusedLand())
            print("==================")
            
            #print("unused land is:")
            #print(node.state.getUnusedLand())  
            #print("heuristic is ")
            #print(node.priority)
            #if i<2:
            #             print("-----------------")
            #             print(node.state.total_production)  
            #             i+=1
            #print((frontier).lenght())
            #print("parent")
            #print(node.state.total_production["wheat"])
            if self.strategy == "steepest":
                current_node = node
                best_neighbor = self.problem.get_best_neighbor(current_node)
                if  best_neighbor!=None:
    
                    frontier.put(best_neighbor, best_neighbor.priority)
                else:
                    return node
            else:
                if self.problem.goal_test(node.state):
                    return (node)
                
                    
                explored.add(node.state)
                # print(len(frontier.elements))
                for action in self.problem.actions(node.state):
                    
                    child_node = copy.deepcopy(self.problem.result(node, action))
                    #if i<2 and child_node!=None:
                    #     print("-----------------")
                    #     print("child")
                    #     print(child_node.state.total_production) 
                    #     print(child_node.state.getUnusedLand())
                    #     i+=1
                    if child_node ==None:
                        continue
                    if child_node.state not in explored:
                        frontier.put(copy.deepcopy(child_node), child_node.priority)

                    if self.strategy == "IDA_star":
                        if child_node.priority > threshold:
                            print("STOP==========================================")
                            frontier.clear()
                            frontier.put(initial_node, 0)
                            threshold = min(threshold, child_node.priority)
                    elif self.strategy == "IDS":
                        if node.depth > depth:
                            frontier.clear()
                            frontier.put(initial_node, 0)
                            depth += 1
                            continue


        return "failure"

    def get_path(self, node):
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        return list(reversed(path))


class AgricultureProblem:
    def __init__(self, initial_state, Search_method, products):
        self.products = products  # list of the products we search for
        # need to add goal state,transition model,path cost
        self.initial_state = copy.deepcopy(initial_state)
        self.Search_method = Search_method
        number_of_products = len(initial_state.total_production.keys())
        self.counters = {}
        for prod in self.products:
            self.counters[prod]=5
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
                        
                         state.cities[value].products[product].production/max(state.cities[value].land_used[product],1000)
                    )
                    if productivity==0:
                        while productivity==0:
                            productivity=random.uniform(1,15)
                    i += 1
                else:
                    temp = (
                        
                         state.cities[value].products[product].production/max(state.cities[value].land_used[product],1000)
                    )
                    if temp > productivity and temp!=0:
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
        if node.state.getUnusedLand()==0:
            return None  
        best_neighbor = None
        best_value = float("-inf")
        action = None
        for action in self.actionsh(node.state,self.counters):
            child_state = self.resulth(node, action)
            child_value = self.hill_climbing_heuristic(child_state, self.counters)
            if child_value > best_value:
                best_neighbor = copy.deepcopy(child_state)
                best_value = child_value
        return best_neighbor

    def result(self, state, action):
        if state.state.getUnusedLand()==0:
            return None  
        newState = copy.deepcopy(state.state)
        neededprod = (
            self.goal_state.total_production[action[1]]
        )

        additionalProduction = max(0.3 * max(0, neededprod),100000)  # the constant to be fixed
        additionalLand = 0  # the constatn to be fixed
        productivity = newState.cities[action[0]].products[action[1]].production / max(
            newState.cities[action[0]].land_used[action[1]], 1
        )
        if productivity == 0:
            while productivity==0:
                productivity =random.uniform(1, 15)
        additionalLand = additionalProduction / productivity
        if newState.cities[action[0]].unused_land <= additionalLand and newState.cities[action[0]].unused_land!=0 :
            additionalLand = newState.cities[action[0]].unused_land
            additionalProduction = productivity * additionalLand
        else:
            return None
        # print("===========================")
        # print(newState.total_production[action[1]])
        # print(action[1])

        newState.add(action[1], additionalProduction)
        # print(newState.total_production[action[1]])
        # print("===========================")
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
        ),0)
        newState.cities[action[0]].land_used[action[1]] += additionalLand
        # total_land_used = state.getTotalLandUsed(state) # To be added ez
        # print(newState.cities[action[0]].land_used[action[1]])
        newNode = Node((newState), state, action, additionalLand, 0)
        newNode.priority = self.As_node_cost(newNode)

        # print(newNode.state.total_production)
        return newNode
    def resulth(self, state, action):  
        newState = copy.deepcopy(state.state)
        neededprod = (
            self.goal_state.total_production[action[1]]
        )
        if action[1] == "other":
            return Node(copy.deepcopy(newState), state, action, 0, 0)

        additionalProduction =max( (neededprod*2*0.25),100000) 
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
        # print("===========================")
        # print(newState.total_production[action[1]])
        # print(action[1])

        newState.add(action[1], additionalProduction)
        # print(newState.total_production[action[1]])
        # print("===========================")
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
           max(( newState.cities[action[0]].unused_land - additionalLand),0)
        )
        newState.cities[action[0]].land_used[action[1]] += additionalLand
        # total_land_used = state.getTotalLandUsed(state) # To be added ez
        # print(newState.cities[action[0]].land_used[action[1]])
        newNode = Node(copy.deepcopy(newState), state, action, additionalLand, 0)
        newNode.priority = self.As_node_cost(newNode)
        # print(newNode.state.total_production)
        return newNode
    def goal_test(self, state):
        for product in self.products:
            if (
                state.total_production[product]
                < self.goal_state.total_production[product]
                and product != "other"
            ):

                return False
        print("true")
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
                )and state.cities[city].unused_land!=0:

                    actions.append([city, product])

        return actions
    
    def actionsh(self, state,counters):
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

                    if counters[product] == 0 or state.cities[city].unused_land==0:
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
        ##we can create a function get productivity that return a dic containing the productivity of a specific product in each wilaya
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
                )  ##to review

        for key in average_productivity.keys():
            average_productivity[key] = average_productivity[key] / len(
                initial_state.cities
            )

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
            new_goal.update_production(
                key, Additional_production[key]
            )  # needs to be definded ez
            
        return new_goal


class DataLoader:
    @staticmethod
    def load_country_data(city_filename, product_filename):
        cities = {}
        consumption = {}
        total_production = {}
        prices = {}
        temp = {}
        # Load city data
        # Load product data
        with open(product_filename, newline="") as product_file:
            product_reader = csv.DictReader(product_file)
            for product_row in product_reader:
                product_name = product_row["product name"]
                strategic = bool(product_row["strategic"])
                removable = False
                consumption[product_name] = int(product_row["consumption"])
                prices[product_name] = [
                    float(product_row["summer price"]),
                    float(product_row["fall price"]),
                    float(product_row["winter price"]),
                    float(product_row["spring price"]),
                ]

        with open(product_filename, newline="") as product_file:
            product_reader = csv.DictReader(product_file)
            for product_row in product_reader:
                product_name = product_row["product name"]
                season = [
                    product_row["summer season"],
                    product_row["fall season"],
                    product_row["winter season"],
                    product_row["spring season"],
                ]
                removable = [
                    product_row["removable in summer"],
                    product_row["removable in fall"],
                    product_row["removable in winter"],
                    product_row["removable in spring"],
                ]
                strategic = bool(product_row["strategic"])
                temp[product_name] = {}
                temp[product_name] = {
                    "strategic": strategic,
                    "removable": removable,
                    "season": season,
                }
        # Iterate over city data
        with open(city_filename, newline="") as city_file:
            city_reader = csv.DictReader(city_file)
            for city_row in city_reader:
                city_name = city_row["wilaya name"]
                land_used_by_product = int(city_row["land used by product"])
                agriculture_land_str = city_row.get("total land unused", "")
                try:
                    agriculture_land = int(agriculture_land_str)
                except ValueError:
                    agriculture_land = 0
                unused_land = agriculture_land
                cities[city_name] = {
                    "agriculture_land": agriculture_land,
                    "unused_land": unused_land,
                    "products": {},
                }

                # Iterate over product data and update city data accordingly

        with open(city_filename, newline="") as city_file:
            city_reader = csv.DictReader(city_file)
            for city_row in city_reader:
                city_name = city_row["wilaya name"]
                production = int(city_row["production"])
                land_used_by_product = int(city_row["land used by product"])
                product_name = city_row["product name"]
                productivity = (
                    production / land_used_by_product if land_used_by_product > 0 else 0
                )
                cities[city_name]["products"][product_name] = {
                    "land used by product": land_used_by_product,
                    "production": production,
                    "productivity": productivity,
                    "strategic": temp[product_name]["strategic"],
                    "removable": temp[product_name]["removable"],
                    "season": temp[product_name]["season"],
                }

        return cities, consumption, total_production, prices


# def main():
#     # Create some products
#     wheat = Product("Wheat", 100, 200, False, True, ["Spring", "Summer"])
#     corn = Product("Corn", 150, False, True, 300, ["Summer", "Fall"])

#     # Create a city with these products
#     city1 = City("City1", 500, {"Wheat" : 1000, "Corn" : 500}, {"Wheat": wheat, "Corn": corn})

#     # Create a country with this city
#     country1 = Country({"City1" : city1}, {"Wheat": 1000, "Corn": 1000}, {"Wheat" : 700, "Corn" : 900}, {"Wheat": 2, "Corn": 3})

#     # Print the total production
#     print("================================================")
#     print(country1.total_production)

#     # Update the total production and print it again
#     print("================================================")
#     country1.update_production("Wheat", 100)
#     print(country1.total_production)
#     print("land used : ",country1.getTotalLandUsed())
#     print("land unused : ",country1.getUnusedLand())

#     # Create an AgricultureProblem and find the goal for a given season
#     print("================================================")
#     problem = AgricultureProblem(country1, "gjhgfgfjg")
#     print("================================================")
#     node = Node(country1, None, None, 0, 0)
#     n= problem.result(node, ["City1", "Wheat"])
#     print("land used : ",n.state.getTotalLandUsed())
#     print("land unused : ",n.state.getUnusedLand())


# if __name__ == "__main__":
#     main()


def mycountry(cities_data, consumption, prices):
    productss = {}
    landused = {}
    total_production = {}
    citis = {}
    for cities in cities_data.keys():
        for products in cities_data[cities]["products"].keys():
            if products not in total_production.keys():
                total_production[products] = 0
            total_production[products] += cities_data[cities]["products"][products][
                "production"
            ]
            myprod = Product(
                products,
                cities_data[cities]["products"][products]["production"],
                cities_data[cities]["products"][products]["strategic"],
                cities_data[cities]["products"][products]["removable"],
                cities_data[cities]["products"][products]["productivity"],
                cities_data[cities]["products"][products]["season"],
            )
            productss[products] = copy.deepcopy(myprod)
            landused[products] = cities_data[cities]["products"][products][
                "land used by product"
            ]
        myciti = City(
            cities,
            cities_data[cities]["unused_land"],
            landused,
            copy.deepcopy(productss),
        )
        citis[cities] = copy.deepcopy(myciti)
        landused.clear()
        productss.clear()

    mycontri = Country(citis, consumption, total_production, prices)
    return mycontri


def search_for_year( initial_state,strategy):
    summer_prod=[]
    winter_prod=[]
    fall_prod=[]
    spring_prod=[]
    s_removable=[]
    w_removable=[]
    f_removable=[]
    sp_removable=[0,0,0,0]
    
    #make the goal:
    
    problem = AgricultureProblem(initial_state, strategy,list(initial_state.total_production.keys()))
    goal=copy.deepcopy(problem.goal_state)
    for prod in initial_state.total_production.keys():
        neededprod=goal.total_production[prod]
        count=0
        for i in range(4):
            if int(initial_state.cities[list(initial_state.cities.keys())[0]].products[prod].removable[i])==1 and prod!='other':
                if i==0:
                   s_removable.append(prod)
                elif i==2:
                   w_removable.append(prod)
                elif i==1:
                   f_removable.append(prod)
                elif i==3:
                   sp_removable.append(prod)

            if  initial_state.cities[list(initial_state.cities.keys())[0]].products[prod].Season[i]=='1' and 'other':
                if i==0:
                   summer_prod.append(prod)
                elif i==2:
                   winter_prod.append(prod)
                elif i==1:
                   fall_prod.append(prod)
                elif i==3:
                   spring_prod.append(prod)
                count+=1
        if prod=='wheat':
            print(count)
        goal.total_production[prod]=goal.total_production[prod]/max(1,count)
    problem.goal_state=goal
    print("goal of season aubergines")
    #print(s_removable)
    #print(w_removable)
    #print(fall_prod)
    #print(spring_prod)
    print(goal.total_production['aubergines'])
    print('======================')

        
# make initial state Summer    

    new_initial_state=copy.deepcopy(initial_state)


    #get seasons products
    for prod in new_initial_state.total_production.keys():
        if prod in s_removable:
            for city in new_initial_state.cities.keys():
                new_initial_state.cities[city].unused_land+=new_initial_state.cities[city].land_used[prod]
                new_initial_state.cities[city].land_used[prod]=0
                new_initial_state.cities[city].products[prod].production=0
                new_initial_state.total_production[prod]=0
                
    
    
    
    
    print("================================")
    print(new_initial_state.total_production['wheat'])
    print("================================")

    problem.products=summer_prod
    problem.initial_state=new_initial_state
    
    search = GraphSearch(problem, strategy)
    result = search.general_search()
    print("plan for summer")
    print(result.state.to_markdown())
    print("==============================")
    
   
    #for fall
    new_initial_state=copy.deepcopy(result.state)


    #get seasons products
    for prod in new_initial_state.total_production.keys():
        if prod in f_removable:
            for city in new_initial_state.cities:
                new_initial_state.cities[city].unused_land+=new_initial_state.cities[city].land_used[prod]
                new_initial_state.cities[city].land_used[prod]=0
                new_initial_state.cities[city].products[prod].production=0
                new_initial_state.total_production[prod]=0
    
    
    
    print("================================")
    print(new_initial_state.total_production['wheat'])
    print("================================")

    
    problem.products=fall_prod
    problem.initial_state=copy.deepcopy(new_initial_state)
    
    search = GraphSearch(problem, strategy)
    print(f_removable)
    result = search.general_search()
    print("plan for fall")
    print(result.state.to_markdown())







 #for winter
    new_initial_state=copy.deepcopy(result.state)


    #get seasons products
    for prod in new_initial_state.total_production.keys():
        if prod in w_removable:
            for city in new_initial_state.cities:
                new_initial_state.cities[city].unused_land+=new_initial_state.cities[city].land_used[prod]
                new_initial_state.cities[city].land_used[prod]=0
                new_initial_state.cities[city].products[prod].production=0
                new_initial_state.total_production[prod]=0
    
    
    
    
    problem.initial_state=copy.deepcopy(new_initial_state)
    problem.products=winter_prod
    search = GraphSearch(problem, strategy)
    result = search.general_search()
    #print("plan for winter")
    #print(result.state.to_markdown())
    
    #for spring
    new_initial_state=copy.deepcopy(result.state)


    #get seasons products
    for prod in new_initial_state.total_production.keys():
        if prod in s_removable:
            for city in new_initial_state.cities:
                new_initial_state.cities[city].unused_land+=new_initial_state.cities[city].land_used[prod]
                new_initial_state.cities[city].land_used[prod]=0
                new_initial_state.cities[city].products[prod].production=0
                new_initial_state.total_production[prod]=0
    
    
    
    print("================================")
    print(new_initial_state.total_production['wheat'])
    print("================================")

    
    problem.products=spring_prod
    problem.initial_state=copy.deepcopy(new_initial_state)
    
    search = GraphSearch(problem, strategy)
    result = search.general_search()
    print("plan for spring")
    print(result.state.to_markdown())

def main():
    myproducts = [
        "wheat",
        "corn",
        "dates",
        "potatoes",
        "tomatoes",
        "green pepper",
        "aubergines",
    ]
    myproducts1 = [
        "wheat",
    ]
    myproducts2 = ["aubergines"]
    # Load data using DataLoader
    cities_data, consumption, total_production, prices = DataLoader.load_country_data(
        "Wilaya.csv", "products.csv"
    )
    
    country = mycountry(cities_data, consumption, prices)
    # Create an instance of Country

    # Create an instance of AgricultureProblem
    

    # Create an instance of GraphSearch
    
    # Perform the search


    # Print the result

    search_for_year(country,"UCS")

if __name__ == "__main__":
    main()
