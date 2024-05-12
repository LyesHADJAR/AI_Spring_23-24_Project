# import csv
# import AI
# class DataLoader:
#     @staticmethod
    
#     def load_country_data(city_filename, product_filename):
#         cities = {}
#         consumption = {}
#         total_production = {}
#         prices = {}
#         temp={}
#         # Load city data
#        # Load product data
#         with open(product_filename, newline='') as product_file:
#             product_reader = csv.DictReader(product_file)
#             for product_row in product_reader:
#                 product_name = product_row['product name']
#                 strategic = bool(product_row['strategic'])
#                 removable = False
#                 consumption[product_name] = int(product_row['consumption'])
#                 prices[product_name] = [
#                     float(product_row['summer price']),
#                     float(product_row['fall price']),
#                     float(product_row['winter price']),
#                     float(product_row['spring price'])
#                 ]
        
#         with open(product_filename, newline='') as product_file:
#                     product_reader = csv.DictReader(product_file)
#                     for product_row in product_reader:
#                         product_name=product_row['product name']
#                         season = [product_row['summer season'], product_row['fall season'], product_row['winter season'], product_row['spring season']]
#                         removable = [product_row['removable in summer'], product_row['removable in fall'], product_row['removable in winter'], product_row['removable in spring']]
#                         strategic = bool(product_row['strategic'])
#                         temp[product_name]={}
#                         temp[product_name] = {
#                             'strategic': strategic,
#                             'removable': removable,
#                             'season': season
#                         }
#         # Iterate over city data
#         with open(city_filename, newline='') as city_file:
#             city_reader = csv.DictReader(city_file)
#             for city_row in city_reader:
#                 city_name = city_row['wilaya name']
#                 land_used_by_product=int(city_row['land used by product'])
#                 agriculture_land_str = city_row.get('total land unused', '')
#                 try:
#                     agriculture_land = int(agriculture_land_str)
#                 except ValueError:
#                     agriculture_land = 0
#                 unused_land = agriculture_land
#                 cities[city_name] = {
#                     'agriculture_land': agriculture_land,
#                     'unused_land': unused_land,
#                     'products': {}
#                 }

#                 # Iterate over product data and update city data accordingly
                
#         with open(city_filename,newline='') as city_file:
#             city_reader=csv.DictReader(city_file)
#             for city_row in city_reader:
#                 city_name=city_row['wilaya name']
#                 production=int(city_row['production'])
#                 land_used_by_product=int(city_row['land used by product'])
#                 product_name=city_row['product name']
#                 productivity = production / land_used_by_product if land_used_by_product > 0 else 0
#                 cities[city_name]['products'][product_name]=  {
#                             'land used by product': land_used_by_product,
#                             'production': production,
#                             'productivity': productivity,
#                             'strategic':temp[product_name]['strategic'],
#                             'removable': temp[product_name]['removable'],
#                             'season': temp[product_name]['season']
#                         }

#         return cities, consumption, total_production, prices

# # def main():
# #     # Create some products
# #     wheat = Product("Wheat", 100, 200, False, True, ["Spring", "Summer"])
# #     corn = Product("Corn", 150, False, True, 300, ["Summer", "Fall"])
# #     # Create a city with these products
# #     city1 = City("City1", 500, {"Wheat" : 1000, "Corn" : 500}, {"Wheat": wheat, "Corn": corn})

# #     # Create a country with this city
# #     country1 = Country({"City1" : city1}, {"Wheat": 1000, "Corn": 1000}, {"Wheat" : 700, "Corn" : 900}, {"Wheat": 2, "Corn": 3})

# #     # Print the total production
# #     print("================================================")
# #     print(country1.total_production)

# #     # Update the total production and print it again
# #     print("================================================")
# #     country1.update_production("Wheat", 100)
# #     print(country1.total_production)
# #     print("land used : ",country1.getTotalLandUsed())
# #     print("land unused : ",country1.getUnusedLand())

# #     # Create an AgricultureProblem and find the goal for a given season
# #     print("================================================")
# #     problem = AgricultureProblem(country1, "gjhgfgfjg")
# #     print("================================================")
# #     node = Node(country1, None, None, 0, 0)
# #     n= problem.result(node, ["City1", "Wheat"])
# #     print("land used : ",n.state.getTotalLandUsed())
# #     print("land unused : ",n.state.getUnusedLand())
    

# # if name == "main":
# #     main()


# def mycountry(cities_data, consumption, total_production, prices):
#     productss={}
#     landused={}
#     citis={}
#     for cities in cities_data.keys():    
#         for products in cities_data[cities]['products'].keys():
#             myprod=Product(products,cities_data[cities]['products'][products]['production'],cities_data[cities]['products'][products]['strategic'],cities_data[cities]['products'][products]['removable'],cities_data[cities]['products'][products]['productivity'],cities_data[cities]['products'][products]['season'])
#             productss[products]=myprod
#             landused[products]=cities_data[cities]['products'][products]['land used by product']
#         myciti=City(cities,cities_data[cities]['unused_land'],landused,copy.deepcopy(productss))
#         citis[cities]=myciti
#         landused.clear()
#         productss.clear()
    
#     mycontri=Country(citis,consumption,total_production,prices)
#     return mycontri

# def main():

#     cities_data, consumption, total_production, prices = DataLoader.load_country_data("Wilaya.csv", "products.csv")

#     c=mycountry(cities_data, consumption, total_production, prices)
#     print(c.cities['Adrar'].products['wheat'].production)
# if name == "main":
#     main()
