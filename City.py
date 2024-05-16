class City:
    def __init__(self, name, unused_land, land_used, products):
        self.name = name  # string
        self.unused_land = unused_land  # total (int)
        self.land_used = land_used  # dictionary ( product : land_used )
        self.products = products  # dictionary ( product : Product )

