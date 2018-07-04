class Instance:

    n_customers = 0
    n_vehicles = 0
    linehaul_list = []
    backhaul_list = []

    # Constructor
    def __init__(self, customers, vehicles, linehauls, backhauls):
        self.n_customers = customers
        self.n_vehicles = vehicles
        self.linehaul_list = linehauls
        self.backhaul_list = backhauls

