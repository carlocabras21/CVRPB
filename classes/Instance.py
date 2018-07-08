import numpy as np
import sys

from Node import Node
from Route import Route
from utils.utils import compute_distance



class Instance(object):
    """
    This class represents a CVRPB instance.

    :param n_customers: An int, the number of customers involved
    :param n_vehicles: An int, the number of vehicles involved
    :param veichle_load: An int, the capacity of each vehicle

    :param depot_node: A Node object, the Depot's node

    :param linehaul_list: A list of Node objects, the customers of Linehaul type
    :param backhaul_list: A list of Node objects, the customers of Backhaul type

    :param distance_matrix: A numpy bi-dimensional array, the distance matrix for the distances between nodes
    :param main_routes: A list of Route objects, the list of main routes to optimize

    """
    n_customers = 0
    n_vehicles = 0
    vehicle_load = 0

    depot_node = Node() # in teoria dovrebbe farlo il costruttore

    linehaul_list = []
    backhaul_list = []

    distance_matrix = np.array([[]])
    main_routes = []


    def __init__(self):
        pass


    def showData(self):
        """
        This method simply prints informations about the instance itself.

        :return: nothing
        """
        print("Number of Customers %d" % self.n_customers)
        print("Number of Vehicles %d" % self.n_vehicles)
        print("Vehicle Load %d" % self.vehicle_load)
        print(self.depot_node)

        for node in self.backhaul_list:
            print(node)

        for node in self.linehaul_list:
            print(node)


    def compute_distance_matrix(self):
        """
        This method produces the distance matrix by computing the euclidean distance between each pair of nodes.

        :return: nothing, the distance matrix is an attribute of the istance itself
        """

        self.distance_matrix = np.zeros((self.n_customers + 1, self.n_customers + 1))

        customers = np.concatenate(([self.depot_node], self.linehaul_list, self.backhaul_list))

        for i in customers:
            for j in customers:
                self.distance_matrix[i.id, j.id] = compute_distance(i, j)


    def print_distance_matrix(self):
        """
        This function prints the distance matrix in a more readable way.

        :return: nothing
        """
        for i in range(0, self.n_customers + 1):
            for j in range(0, self.n_customers + 1):
                sys.stdout.write('%.1f' % self.distance_matrix[i, j] + " ")

            print("\n")



    def create_routes(self, nodes_list):
        """
        Given a list of Node objects, this method computes all the possible routes of nodes, so that the capacity
        constraint is verified and each node is visited only once.

        :param nodes_list: A list of Node objects, the list of linehauls or backhauls
        :return: a list of routes composed by Node objects
        """

        routes = []

        # While there are nodes in the list
        while nodes_list:
            curr_route = []
            curr_load = 0
            print("Route :) ")

            # For each node in the list
            for node in nodes_list:

                # check if it is possible to add a node to the current route
                if (curr_load + node.load) <= self.vehicle_load:

                    # if so, the node is added to the current route
                    curr_route.append(node)

                    # the current load is updated
                    curr_load += node.load

            # Each node in the current route is removed from the main list of nodes
            nodes_list = [x for x in nodes_list if x not in curr_route]

            for k in curr_route:
                print(k)

            # The current route is added to the routes list
            routes.append(curr_route)

        return routes

    def create_main_routes(self):
        """
        This method is the core of the Clustering Phase. It computes the main routes by chaining the linehauls
        backhauls routes in pairs.

        :return: nothing, the main routes list is an attribute of the instance itself
        """
        linehauls = self.linehaul_list
        backhauls = self.backhaul_list

        linehauls_routes = self.create_routes(linehauls)  # Computing routes of linehauls only
        backhauls_routes = self.create_routes(backhauls)  # Computing routes of backhauls only

        print(len(linehauls_routes))
        print(len(backhauls_routes))

        # Assuming that linehaul routes are greater that backhaul routes
        if len(backhauls_routes) > len(linehauls_routes):
            print("Errore, B > L routes :(")
            exit(1)

        # Linking linehaul and backhaul routes in pairs, as long as there are backhaul routes
        for i in range(len(backhauls_routes)):
            curr_route = Route()

            curr_route.depot_node = self.depot_node
            curr_route.linehauls = linehauls_routes[i]
            curr_route.backhauls = backhauls_routes[i]

            self.main_routes.append(curr_route)

        # If there are some remaining linehaul routes, main routes of only linehaul routes are created
        for i in range(len(backhauls_routes), len(linehauls_routes)):
            curr_route = Route()

            curr_route.depot_node = self.depot_node
            curr_route.linehauls = linehauls_routes[i]

            self.main_routes.append(curr_route)

        for route in self.main_routes:
            print("Main route")
            print(route)




