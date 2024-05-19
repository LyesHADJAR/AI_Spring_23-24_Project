# File imports
import AgricultureProblem
import City
import Country
from DataLoader import DataLoader
import GraphSearch
import Product

# Utility imports
import copy
import time
from tabulate import tabulate
import markdown


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
    total_start_time = time.time()
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
                elif i == 2:
                    w_removable.append(prod)
                elif i == 1:
                    f_removable.append(prod)
                elif i == 3:
                    sp_removable.append(prod)

            if initial_state.cities[list(initial_state.cities.keys())[0]].products[prod].Season[i] == '1' and 'other':
                count += 1
                if i == 0:
                    summer_prod.append(prod)
                elif i == 2:
                    winter_prod.append(prod)
                elif i == 1:
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
        v += max(0, goal.total_production[prod] - \
            new_initial_state.total_production[prod])
    print(f'PRODUCTION NEEDED IN SUMMER : {v}')
    problem.products = summer_prod
    problem.initial_state = new_initial_state
    start_time = time.time()
    search = GraphSearch.GraphSearch(problem, strategy)
    result = search.general_search()
    print(">>> PLAN FOR SUMMER")
    markdown_data = result.state.to_markdown().split("\n")
    headers = [x.strip() for x in markdown_data[0].split("|")[1:-1]]
    rows = [[x.strip() for x in row.split("|")[1:-1]]
            for row in markdown_data[1:]]
    print(tabulate(rows, headers=headers, tablefmt="pipe"))
    end_time = time.time()
    print(f"[ >>>>> SEARCH FOR SUMMER SEASON PLAN TOOK <<<<< ]:  {end_time - start_time} seconds")
    print("The total production of each product:")
    markdown_data = result.state.to_markdown_production().split("\n")
    headers = [x.strip() for x in markdown_data[0].split("|")[1:-1]]
    rows = [[x.strip() for x in row.split("|")[1:-1]]
            for row in markdown_data[1:]]
    print(tabulate(rows, headers=headers, tablefmt="pipe"))
    result = new_prices(new_initial_state, result, 0)
    print("The new prices of the summer season:")
    markdown_data = result.state.to_markdown_prices("summer").split("\n")
    headers = [x.strip() for x in markdown_data[0].split("|")[1:-1]]
    rows = [[x.strip() for x in row.split("|")[1:-1]]
            for row in markdown_data[1:]]
    print(tabulate(rows, headers=headers, tablefmt="pipe"))
    # for fall
    new_initial_state = copy.deepcopy(result.state)

    # get seasons products
    for prod in new_initial_state.total_production.keys():
        if prod in f_removable:
            for city in new_initial_state.cities:
                new_initial_state.cities[city].unused_land += new_initial_state.cities[city].land_used[prod]
                new_initial_state.cities[city].land_used[prod] = 0
                new_initial_state.cities[city].products[prod].production = 0
    v = 0
    for prod in goal.total_production.keys():
        v += max(0,goal.total_production[prod] - \
            new_initial_state.total_production[prod])
    print(f'PRODUCTION NEEDED IN FALL : {v}')
    problem.products = fall_prod
    problem.initial_state = new_initial_state
    start_time = time.time()
    search = GraphSearch.GraphSearch(problem, strategy)
    result = search.general_search()
    print(">>> PLAN FOR FALL")
    markdown_data = result.state.to_markdown().split("\n")
    headers = [x.strip() for x in markdown_data[0].split("|")[1:-1]]
    rows = [[x.strip() for x in row.split("|")[1:-1]]
            for row in markdown_data[1:]]
    print(tabulate(rows, headers=headers, tablefmt="pipe"))
    end_time = time.time()
    print(f"[ >>>>> SEARCH FOR FALL SEASON PLAN TOOK <<<<< ]: {end_time - start_time} seconds")
    print("The total production of each product:")
    markdown_data = result.state.to_markdown_production().split("\n")
    headers = [x.strip() for x in markdown_data[0].split("|")[1:-1]]
    rows = [[x.strip() for x in row.split("|")[1:-1]]
            for row in markdown_data[1:]]
    print(tabulate(rows, headers=headers, tablefmt="pipe"))
    result = new_prices(new_initial_state, result, 1)
    print("The new prices of the fall season:")
    markdown_data = result.state.to_markdown_prices("fall").split("\n")
    headers = [x.strip() for x in markdown_data[0].split("|")[1:-1]]
    rows = [[x.strip() for x in row.split("|")[1:-1]]
            for row in markdown_data[1:]]
    print(tabulate(rows, headers=headers, tablefmt="pipe"))

    # for winter
    new_initial_state = copy.deepcopy(result.state)

    # get seasons products
    for prod in new_initial_state.total_production.keys():
        if prod in w_removable:
            for city in new_initial_state.cities:
                new_initial_state.cities[city].unused_land += new_initial_state.cities[city].land_used[prod]
                new_initial_state.cities[city].land_used[prod] = 0
                new_initial_state.cities[city].products[prod].production = 0
    v = 0
    for prod in goal.total_production.keys():
        v += max(0,goal.total_production[prod] - \
            new_initial_state.total_production[prod])
    print(f'PRODUCTION NEEDED IN WINTER : {v}')
    problem.initial_state = new_initial_state
    problem.products = winter_prod
    start_time = time.time()
    search = GraphSearch.GraphSearch(problem, strategy)
    result = search.general_search()
    print(">>> PLAN FOR WINTER")
    markdown_data = result.state.to_markdown().split("\n")
    headers = [x.strip() for x in markdown_data[0].split("|")[1:-1]]
    rows = [[x.strip() for x in row.split("|")[1:-1]]
            for row in markdown_data[1:]]
    print(tabulate(rows, headers=headers, tablefmt="pipe"))
    end_time = time.time()
    print(f"[ >>>>> SEARCH FOR WINTER SEASON PLAN TOOK <<<<< ]:  {end_time - start_time} seconds")
    print("The total production of each product:")
    markdown_data = result.state.to_markdown_production().split("\n")
    headers = [x.strip() for x in markdown_data[0].split("|")[1:-1]]
    rows = [[x.strip() for x in row.split("|")[1:-1]]
            for row in markdown_data[1:]]
    print(tabulate(rows, headers=headers, tablefmt="pipe"))
    result = new_prices(new_initial_state, result, 2)
    print("The new prices of the winter season:")
    markdown_data = result.state.to_markdown_prices("winter").split("\n")
    headers = [x.strip() for x in markdown_data[0].split("|")[1:-1]]
    rows = [[x.strip() for x in row.split("|")[1:-1]]
            for row in markdown_data[1:]]
    print(tabulate(rows, headers=headers, tablefmt="pipe"))

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
    v = 0
    for prod in goal.total_production.keys():
        v += max(0, goal.total_production[prod] -
                 new_initial_state.total_production[prod])
    print(f'PRODUCTION NEEDED IN SPRING : {v}')
    start_time = time.time()
    search = GraphSearch.GraphSearch(problem, strategy)
    result = search.general_search()
    print(">>> PLAN FOR SPRING")
    markdown_data = result.state.to_markdown().split("\n")
    headers = [x.strip() for x in markdown_data[0].split("|")[1:-1]]
    rows = [[x.strip() for x in row.split("|")[1:-1]]
            for row in markdown_data[1:]]
    print(tabulate(rows, headers=headers, tablefmt="pipe"))
    end_time = time.time()
    print(f"[ >>>>> SEARCH FOR SPRING SEASON PLAN TOOK <<<<< ]: {end_time - start_time} seconds")
    total_end_time = time.time()
    print("The total production of each product:")
    markdown_data = result.state.to_markdown_production().split("\n")
    headers = [x.strip() for x in markdown_data[0].split("|")[1:-1]]
    rows = [[x.strip() for x in row.split("|")[1:-1]]
            for row in markdown_data[1:]]
    print(tabulate(rows, headers=headers, tablefmt="pipe"))
    result = new_prices(new_initial_state, result, 1)
    print("The new prices of the spring season:")
    markdown_data = result.state.to_markdown_prices("spring").split("\n")
    headers = [x.strip() for x in markdown_data[0].split("|")[1:-1]]
    rows = [[x.strip() for x in row.split("|")[1:-1]]
            for row in markdown_data[1:]]
    print(tabulate(rows, headers=headers, tablefmt="pipe"))
    print(f"[ >>>>> SEARCH FOR YEAR PLAN TOOK <<<<< ]: {total_end_time - total_start_time} seconds")


def new_prices(initial_state, result, season):
    for city in initial_state.cities.keys():
        for prod in initial_state.cities[city].products.keys():
            result.state.prices[prod][season] = initial_state.prices[prod][season] * \
                initial_state.total_production[prod] / \
                max(1, result.state.total_production[prod])
    return result


def main():
    # Load data using DataLoader
    cities_data, consumption, total_production, prices = DataLoader.load_country_data(
        "Wilaya.csv", "products.csv")

    country = mycountry(cities_data, consumption, prices)

    print("------------------------------------------")
    print("search using IDA_star")
    search_for_year(country, "IDA_Star")

    print("------------------------------------------")
    print("search using IDS")
    search_for_year(country, "IDS")

    print("------------------------------------------")
    print("search using Hill Climbing")
    search_for_year(country, "steepest")

    print("------------------------------------------")
    print("search using UCS")
    search_for_year(country, "UCS")


if __name__ == "__main__":
    main()
