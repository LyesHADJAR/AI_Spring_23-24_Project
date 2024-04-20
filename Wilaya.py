

class City:
    def __init__(self, name, agriculture_land, unused_land, products):
        self.name = name
        self.agriculture_land = agriculture_land
        self.unused_land = unused_land
        self.products = sorted(products, key=lambda x: (x.production, x.prices))