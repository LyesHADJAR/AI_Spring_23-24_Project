import csv

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
    
    # =========== NEEDED FOR CSP ===========
    def extract_variables(city_filename, products_file):
        variables = {}
        unique_wilaya_names = set()

    # Extract Wilaya names from city data
        with open(city_filename, newline='') as city_file:
            city_reader = csv.DictReader(city_file)
            for city_row in city_reader:
                wilaya_name = city_row['wilaya name']
                if wilaya_name not in variables:
                   variables[wilaya_name] = []

        # Extract Products for each Wilaya
        with open(products_file, newline='') as product_file:
            product_reader = csv.DictReader(product_file)
            for product_row in product_reader:
                product_name = product_row['product name']
                for wilaya_name in variables:
                   variables[wilaya_name].append(product_name.lower().replace(' ', '_'))

        return variables
