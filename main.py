# File imports
import AgricultureProblem
import City
import Country
from DataLoader import DataLoader
import GraphSearch
import ProblemGUI
import Product

# Utility imports
import copy
import time

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
            myprod = Product.Product(
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
        myciti = City.City(
            cities,
            cities_data[cities]["unused_land"],
            landused,
            copy.deepcopy(productss),
        )
        citis[cities] = copy.deepcopy(myciti)
        landused.clear()
        productss.clear()

    mycontri = Country.Country(citis, consumption, total_production, prices)
    return mycontri


def search_for_year(initial_state, strategy):
    summer_prod = []
    winter_prod = []
    fall_prod = []
    spring_prod = []
    s_removable = []
    w_removable = []
    f_removable = []
    sp_removable = [0, 0, 0, 0]

    # make the goal:

    problem = AgricultureProblem.AgricultureProblem(
        initial_state, strategy, list(initial_state.total_production.keys()))
    goal = copy.deepcopy(problem.goal_state)
    for prod in initial_state.total_production.keys():
        neededprod = goal.total_production[prod]
        count = 0
        for i in range(4):
            if int(initial_state.cities[list(initial_state.cities.keys())[0]].products[prod].removable[i]) == 1 and prod != 'other':
                if i == 0:
                    s_removable.append(prod)
                elif i == 1:
                    w_removable.append(prod)
                elif i == 2:
                    f_removable.append(prod)
                elif i == 3:
                    sp_removable.append(prod)

            if initial_state.cities[list(initial_state.cities.keys())[0]].products[prod].Season[i] == '1' and 'other':
                count += 1
                if i == 0:
                    summer_prod.append(prod)
                elif i == 1:
                    winter_prod.append(prod)
                elif i == 2:
                    fall_prod.append(prod)
                elif i == 3:
                    spring_prod.append(prod)
                count += 1

        goal.total_production[prod] = initial_state.total_production[prod] +\
        \
            neededprod/(
            count
        )
    problem.goal_state = goal


# make initial state Summer

    new_initial_state = copy.deepcopy(initial_state)

    # get seasons products
    for prod in new_initial_state.total_production.keys():
        if prod in s_removable:
            for city in new_initial_state.cities.keys():
                new_initial_state.cities[city].unused_land += new_initial_state.cities[city].land_used[prod]
                new_initial_state.cities[city].land_used[prod] = 0
                new_initial_state.cities[city].products[prod].production = 0

    v = 0
    for prod in goal.total_production.keys():
        v += goal.total_production[prod] - \
            new_initial_state.total_production[prod]
    print('production needed in summer')
    print(v)
    problem.products = summer_prod
    problem.initial_state = new_initial_state

    search = GraphSearch.GraphSearch(problem, strategy)
    result = search.general_search()
    print("plan for summer")
    print(result)

    # for winter
    new_initial_state = copy.deepcopy(result.state)

    # get seasons products
    for prod in new_initial_state.total_production.keys():
        if prod in w_removable:
            for city in new_initial_state.cities:
                new_initial_state.cities[city].unused_land += new_initial_state.cities[city].land_used[prod]
                new_initial_state.cities[city].land_used[prod] = 0
                new_initial_state.cities[city].products[prod].production = 0

    problem.initial_state = new_initial_state
    problem.products = winter_prod
    search = GraphSearch.GraphSearch(problem, strategy)
    result = search.general_search()
    print("plan for winter")
    print(result)

    # for fall
    new_initial_state = copy.deepcopy(result.state)

    # get seasons products
    for prod in new_initial_state.total_production.keys():
        if prod in f_removable:
            for city in new_initial_state.cities:
                new_initial_state.cities[city].unused_land += new_initial_state.cities[city].land_used[prod]
                new_initial_state.cities[city].land_used[prod] = 0
                new_initial_state.cities[city].products[prod].production = 0

    problem.products = fall_prod
    problem.initial_state = new_initial_state

    search = GraphSearch.GraphSearch(problem, strategy)
    print(f_removable)
    result = search.general_search()
    print("plan for fall")
    print(result)
    # for spring
    new_initial_state = copy.deepcopy(result.state)
    # get seasons products
    for prod in new_initial_state.total_production.keys():
        if prod in s_removable:
            for city in new_initial_state.cities:
                new_initial_state.cities[city].unused_land += new_initial_state.cities[city].land_used[prod]
                new_initial_state.cities[city].land_used[prod] = 0
                new_initial_state.cities[city].products[prod].production = 0
    problem.products = spring_prod
    problem.initial_state = new_initial_state

    search = GraphSearch.GraphSearch(problem, strategy)
    result = search.general_search()
    print("plan for spring")
    print(result)


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
        "Wilaya.csv", "products.csv")

    country = mycountry(cities_data, consumption, prices)

    start_of_IDA_star = time.time()
    print("------------------------------------------")
    print("search using IDA_star")
    search_for_year(country, "IDA_Star")
    end_of_IDA_star = time.time()
    print(f"Time taken for IDA_star: {end_of_IDA_star - start_of_IDA_star} seconds")
    
    start_of_IDS = time.time()
    print("------------------------------------------")
    print("search using IDS")
    search_for_year(country, "IDS")
    end_of_IDS = time.time()
    print(f"Time taken for IDS: {end_of_IDS - start_of_IDS} seconds")

    start_of_UCS = time.time()  
    print("------------------------------------------")
    print("search using UCS")
    search_for_year(country, "UCS")
    end_of_UCS = time.time()
    print(f"Time taken for UCS: {end_of_UCS - start_of_UCS} seconds")
    
    start_of_HC = time.time()
    print("------------------------------------------")
    print("search using Hill Climbing")
    search_for_year(country, "steepest")
    end_of_HC = time.time()
    print(f"Time taken for Hill Climbing: {end_of_HC - start_of_HC} seconds")

if __name__ == "__main__":
    main()
