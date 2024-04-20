

class Country:
    def __init__(self, cities, consumption):
        self.cities = cities
        self.consumption = consumption

    def __repr__(self):
        return f"Country with cities: {[city.name for city in self.cities]}"