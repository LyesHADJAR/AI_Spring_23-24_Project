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
