# File imports
import AgricultureProblem
import City
import Country
# import DataLoader
import GraphSearch
import ProblemGUI
import Product

# Utility imports
import copy
import random
import csv

class DataLoader:
    @staticmethod
    def load_country_data(city_filename, product_filename):
        cities = {}
        consumption = {}
        total_production = {}
        prices = {}
        temp={}
        # Load city data
       # Load product data
        with open(product_filename, newline='') as product_file:
            product_reader = csv.DictReader(product_file)
            for product_row in product_reader:
                product_name = product_row['product name']
                strategic = bool(product_row['strategic'])
                removable = False
                consumption[product_name] = int(product_row['consumption'])
                prices[product_name] = [
                    float(product_row['summer price']),
                    float(product_row['fall price']),
                    float(product_row['winter price']),
                    float(product_row['spring price'])
                ]
        
        with open(product_filename, newline='') as product_file:
                    product_reader = csv.DictReader(product_file)
                    for product_row in product_reader:
                        product_name=product_row['product name']
                        season = [product_row['summer season'], product_row['fall season'], product_row['winter season'], product_row['spring season']]
                        removable = [product_row['removable in summer'], product_row['removable in fall'], product_row['removable in winter'], product_row['removable in spring']]
                        strategic = bool(product_row['strategic'])
                        temp[product_name]={}
                        temp[product_name] = {
                            'strategic': strategic,
                            'removable': removable,
                            'season': season
                        }
        # Iterate over city data
        with open(city_filename, newline='') as city_file:
            city_reader = csv.DictReader(city_file)
            for city_row in city_reader:
                city_name = city_row['wilaya name']
                land_used_by_product=int(city_row['land used by product'])
                agriculture_land_str = city_row.get('total land unused', '')
                try:
                    agriculture_land = int(agriculture_land_str)
                except ValueError:
                    agriculture_land = 0
                unused_land = agriculture_land
                cities[city_name] = {
                    'agriculture_land': agriculture_land,
                    'unused_land': unused_land,
                    'products': {}
                }

                # Iterate over product data and update city data accordingly
                
        with open(city_filename,newline='') as city_file:
            city_reader=csv.DictReader(city_file)
            for city_row in city_reader:
                city_name=city_row['wilaya name']
                production=int(city_row['production'])
                land_used_by_product=int(city_row['land used by product'])
                product_name=city_row['product name']
                productivity = production / land_used_by_product if land_used_by_product > 0 else 0
                cities[city_name]['products'][product_name]=  {
                            'land used by product': land_used_by_product,
                            'production': production,
                            'productivity': productivity,
                            'strategic':temp[product_name]['strategic'],
                            'removable': temp[product_name]['removable'],
                            'season': temp[product_name]['season']
                        }

        return cities, consumption, total_production, prices


def mycountry(cities_data, consumption, prices):
    productss = {}
    landused = {}
    total_production = {}
    citis = {}
    for cities in cities_data.keys():    
        for products in cities_data[cities]['products'].keys():
            if products not in total_production.keys():
                total_production[products]=0
            total_production[products] += cities_data[cities]['products'][products]['production']
            myprod = Product.Product(products,cities_data[cities]['products'][products]['production'],cities_data[cities]['products'][products]['strategic'],cities_data[cities]['products'][products]['removable'],cities_data[cities]['products'][products]['productivity'],cities_data[cities]['products'][products]['season'])
            productss[products] = copy.deepcopy(myprod)
            landused[products] = cities_data[cities]['products'][products]['land used by product']
        myciti = City.City(cities,cities_data[cities]['unused_land'],landused,copy.deepcopy(productss))
        citis[cities] = copy.deepcopy(myciti)
        landused.clear()
        productss.clear()
    
    mycontri = Country.Country(citis,consumption,total_production,prices)
    return mycontri

def main():
    # Load data using DataLoader
    cities_data, consumption, total_production, prices = DataLoader.load_country_data("Wilaya.csv", "products.csv")
    
    # Create an instance of Country
    country = mycountry(cities_data, consumption,  prices)

    # Create an instance of AgricultureProblem
    problem = AgricultureProblem.AgricultureProblem(country, "UCS")

    # Create an instance of GraphSearch
    search = GraphSearch.GraphSearch(problem, "UCS")

    # Perform the search
    result = search.general_search()

    # Print the result
    print(result)

if __name__ == "__main__":
    main()
