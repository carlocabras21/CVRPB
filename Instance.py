from Node import Node
from Route import Route
import numpy as np
from utils.utils import compute_distance
import sys


class Instance(object):
    n_customers = 0
    n_vehicles = 0
    vehicle_load = 0

    depot_node = Node()

    linehaul_list = []
    backhaul_list = []

    distance_matrix = np.array([[]])

    main_routes = []

    def __init__(self):
        pass

    def showData(self):

        print("Number of Customers %d" % self.n_customers)
        print("Number of Vehicles %d" % self.n_vehicles)
        print("Vehicle Load %d" % self.vehicle_load)
        print(self.depot_node)

        for node in self.backhaul_list:
            print(node)

        for node in self.linehaul_list:
            print(node)

    def compute_distance_matrix(self):
        self.distance_matrix = np.zeros((self.n_customers + 1, self.n_customers + 1))

        customers = np.concatenate(([self.depot_node], self.linehaul_list, self.backhaul_list))

        for i in customers:
            for j in customers:
                self.distance_matrix[i.id, j.id] = compute_distance(i, j)

    def print_distance_matrix(self):
        for i in range(0, self.n_customers + 1):
            for j in range(0, self.n_customers + 1):
                sys.stdout.write('%.1f' % self.distance_matrix[i, j] + " ")

            print("\n")

    def create_main_routes(self):
        linehauls = self.linehaul_list
        backhauls = self.backhaul_list

        linehauls_routes = self.create_routes(linehauls) # liste soli linehauls
        backhauls_routes = self.create_routes(backhauls) # liste soli backhauls

        # creazione main route
        print(len(linehauls_routes))
        print(len(backhauls_routes))

        # caso grave
        if len(backhauls_routes) > len(linehauls_routes):
            print("Errore, B > L routes :(")
            exit(1)

        for i in range(len(backhauls_routes)):

            curr_route = Route()

            curr_route.depot_node = self.depot_node
            curr_route.linehauls = linehauls_routes[i]
            curr_route.backhauls = backhauls_routes[i]

            self.main_routes.append(curr_route)

        for i in range(len(backhauls_routes), len(linehauls_routes)):
            curr_route = Route()

            curr_route.depot_node = self.depot_node
            curr_route.linehauls = linehauls_routes[i]

            self.main_routes.append(curr_route)

        for route in self.main_routes:
            print("Route Main")
            print(route)


    # da cambiarererereerererere
    def create_routes(self, nodes_list):
        routes = []

        # finche ho nodi
        while nodes_list != []:
            curr_route = []
            curr_load = 0
            print("Route :) ")
            # prendo ogni nodo
            for node in nodes_list:

                # verifico il carico se posso aggiungerlo
                if (curr_load + node.load) <= self.vehicle_load:

                    # aggiungo il nodo
                    curr_route.append(node)

                    # aggiorno il carico
                    curr_load += node.load

            # rimuovo i nodi della curr route
            nodes_list = [x for x in nodes_list if x not in curr_route]

            for k in curr_route:
                print(k)

            routes.append(curr_route)

        return routes