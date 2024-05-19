class City:
    def __init__(self, name, unused_land, land_used, products):
        self.name = name  # string
        self.unused_land = unused_land  # total (int)
        self.land_used = land_used  # dictionary ( product : land_used )
        self.products = products  # dictionary ( product : Product )
        
    # def __str__(self):
    #     land_used_details = "\n".join(
    #         f"{product}: {land}" for product, land in self.land_used.items()
    #     )
    #     products_details = "\n".join(
    #         f"{product}: {prod}" for product, prod in self.products.items()
    #     )
    #     return (
    #         f"Name: {self.name}\n"
    #         f"Unused Land: {self.unused_land}\n"
    #         f"Land Used: {land_used_details}\n"
    #         f"Products: {products_details}"
    #     )
