import sys

import numpy as np
import random as rnd
from classes.Node import Node
from classes.Route import Route
from utils.utils import compute_distance, LINEHAUL_TYPE, BACKHAUL_TYPE


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
    :param curr_routes: A list of Route objects, the list of current routes

    """
    n_customers = 0
    n_vehicles = 0
    vehicle_load = 0

    depot_node = Node()

    linehaul_list = []
    backhaul_list = []

    distance_matrix = np.array([[]])
    curr_routes = []


    def __init__(self):
        """
            Override of the __init__ method in order to instantiate a new Instance Object with new values.

            """
        self.n_customers = 0
        self.n_vehicles = 0
        self.vehicle_load = 0

        self.depot_node = Node()

        self.linehaul_list = []
        self.backhaul_list = []

        self.distance_matrix = np.array([[]])
        self.curr_routes = []


    def __str__(self):
        """
            This method simply prints informations about the instance itself.

            :return: output: a string, information about instance object
            """

        output = "Number of Customers: " + str(self.n_vehicles) + \
                 "\nNumber of Vehicles: " + str(self.n_vehicles) + \
                 "\nVehicle Load: " + str(self.vehicle_load) + \
                 "\n" + str(self.depot_node) + "\n"

        for back in self.backhaul_list:
            output += str(back) + "\n"

        for line in self.linehaul_list:
            output += str(line) + "\n"

        return output


    def show_current_routes(self):
        """
            This method show in a more meaningful representation the current routes.
            """
        for route in self.curr_routes:
            print(route)

    def compute_distance_matrix(self):
        """
            This method produces the distance matrix by computing the Euclidean distance between each pair of nodes.

            :return: nothing, the distance matrix is an attribute of the instance itself
            """

        # initialization of the matrix dimension
        self.distance_matrix = np.zeros((self.n_customers + 1, self.n_customers + 1))

        # linking customers
        customers = np.concatenate(([self.depot_node], self.linehaul_list, self.backhaul_list))

        # Euclidean Distance between each pair of nodes
        for i in customers:
            for j in customers:
                self.distance_matrix[i.id, j.id] = compute_distance(i, j)


    def create_feasible_routes(self, nodes_list):
        """
        Given a list of Node objects, this method returns a set of feasible routes, so that the capacity
        constraint is verified and each node is visited only once.
        :param nodes_list: A list of Node objects, the list of linehauls or backhauls
        :return: a list of routes composed by Node objects
        """

        routes = []

        # While there are nodes in the list
        while nodes_list:
            curr_route = []
            curr_load = 0

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

            # The current route is added to the routes list
            routes.append(curr_route)

        return routes


    def create_main_routes(self):
        """
        This method is the core of the Clustering Phase. It computes the main routes by chaining the linehauls
        backhauls routes in pairs.

        :return: nothing, the main routes list is an attribute of the instance itself
        """

        linehauls_routes = self.create_feasible_routes(self.linehaul_list)  # Computing feasible routes of linehauls only
        backhauls_routes = self.create_feasible_routes(self.backhaul_list)  # Computing feasible routes of backhauls only

        # If there are more backhauls routes then linehaul routes
        while len(backhauls_routes) > len(linehauls_routes):
            # Creating one more linehaul route by removing a node from the first route
            # that has at least two linehaul nodes

            # Find the index of the first route with at least 2 linehauls
            idx = 0
            while len(linehauls_routes[idx]) <= 1:
                idx += 1

            # takes the first node of this route and creates a list with only that node
            node = linehauls_routes[idx][0]

            # removes the node from its current list
            linehauls_routes[idx].remove(node)

            # creates the new linehaul route
            linehauls_routes.append([node])

        # Linking linehaul and backhaul routes in pairs, as long as there are backhaul routes
        for i in range(len(backhauls_routes)):
            self.curr_routes.append(
                Route(self.depot_node, linehauls_routes[i], backhauls_routes[i])
            )

        # If there are some remaining linehaul routes, only linehaul routes are created
        for i in range(len(backhauls_routes), len(linehauls_routes)):
            self.curr_routes.append(
                Route(self.depot_node, linehauls_routes[i], [])
            )

        # if the number of routes is less than number of vehicles
        while len(self.curr_routes) < self.n_vehicles:
            # finds a route with at least two linehauls and two backhauls
            idx = 0
            while (len(self.curr_routes[idx].linehauls) < 2) or (len(self.curr_routes[idx].backhauls) < 1):
                idx += 1

            # removes their first L/B node and creates the list
            line_node = self.curr_routes[idx].linehauls[0]
            back_node = self.curr_routes[idx].backhauls[0]

            self.curr_routes[idx].linehauls.remove(line_node)
            self.curr_routes[idx].backhauls.remove(back_node)

            self.curr_routes.append(
                Route(self.depot_node, [line_node], [back_node])
            )


    def get_unified_routes(self):
        """
            Concatenates the deposit, the linehauls, the backhauls and finally again the deposit
            in a single list.
            It's used in the exchange phase, when it's required to have the customers in a single list

            :return: a list of routes, i.e. a list of list of Nodes
            """
        unified_routes = []

        for route in self.curr_routes:
            unified_routes.append([route.depot_node] + route.linehauls + route.backhauls + [route.depot_node])

        return unified_routes


    def mix_routes_random(self):
        """
            Mixes the routes by performing legal exchanges (i.e that respect the capacity constraint)

            # excchange type:
            #   L/B: move a node from a route to another, without exchange with other nodes (i.e. a legal relocate move)
            #   LL (BB): legal exchange between linehauls (bakchauls) nodes
            #   BL (LB): legal exchange between a backhaul (linehaul) with a linehaul (backhaul)
            """
        moves = ["L", "B", "LL", "BB", "BL", "LB"]
        n_moves = 500

        for exchange in range(n_moves):
            # selects the exchange move randomly
            choose = rnd.randint(0, 5)

            # generates two random indices for the routes
            route1 = rnd.randint(0, len(self.curr_routes) - 1)
            route2 = rnd.randint(0, len(self.curr_routes) - 1)

            move = moves[choose]

            if len(move) == 2:
                self.random_legal_exchange(route1, route2, move) # LL or BB or BL or LB
            else:
                self.random_legal_relocate(route1, route2, move) # L or B

        # Final random permutation for the individual linehaul and backhaul lists of each route
        for route in self.curr_routes:
            rnd.shuffle(route.linehauls)
            rnd.shuffle(route.backhauls)


    def random_legal_relocate(self, route1, route2, relocate_type):
        """
            This method makes a relocate move given two routes and a node of one of them

            :param route1: the route from which we remove the node
            :param route2: the to which we add the node
            :param relocate_type: the type of the relocate move
            :return:
            """

        if route1 != route2:
            if relocate_type == "L":
                # move a Linehaul node from route1 to route2

                relocate = False  # True if the relocate happens, False otherwise
                attempts = 1  # relocate attempts

                while not relocate and (attempts <= (len(self.curr_routes[route1].linehauls))):
                    # repeat until the relocate move happens or until we finish the numer of attempts

                    # generates a random linehaul node index from route1
                    idx = rnd.randint(0, len(self.curr_routes[route1].linehauls) - 1)

                    # Check constraints
                    if (self.curr_routes[route2].linehauls_load() + self.curr_routes[route1].linehauls[idx].load <= self.vehicle_load) and \
                       (len(self.curr_routes[route1].linehauls) >= 2):

                        # appends the node to route2
                        self.curr_routes[route2].linehauls.append(self.curr_routes[route1].linehauls[idx])

                        # removes the node from route1
                        self.curr_routes[route1].linehauls.remove(self.curr_routes[route1].linehauls[idx])

                        relocate = True

                    attempts += 1
            else:
                # move a Backhaul node from route1 to route2

                relocate = False  # True if the relocate happens, False otherwise
                attempts = 1  # relocate attempts

                #If the route contains at least one backhaul
                if len(self.curr_routes[route1].backhauls) >= 1:

                    while not relocate and (attempts <= (len(self.curr_routes[route1].backhauls))):
                        # repeat until the relocate move happens or until we finish the numer of attempts

                        # generates a random backhaul index
                        idx = rnd.randint(0, len(self.curr_routes[route1].backhauls) - 1)

                        # Check constraints
                        if (self.curr_routes[route2].backhauls_load() + self.curr_routes[route1].backhauls[idx].load <= self.vehicle_load) and \
                           (len(self.curr_routes[route2].linehauls) >= 1):

                            backhaul_to_move = self.curr_routes[route1].backhauls[idx]

                            # appends the node to route2
                            self.curr_routes[route2].backhauls.append(backhaul_to_move)

                            # removes the node from route1
                            self.curr_routes[route1].backhauls.remove(self.curr_routes[route1].backhauls[idx])

                            relocate = True

                        attempts += 1

    def random_legal_exchange(self, route1, route2, exchange_type):
        """
            Computes an legal exchange between route1 and route2.

            :param route1: the route from which we remove the node
            :param route2: the to which we add the node
            :param exchange_type: the type of the exchange
            :return:
            """

        exchange = False  # True when an exchange happens, False otherwise
        attempts = 1  # number of exchange attempts

        if exchange_type == "LL":

            # repeat until there is an exchange or the number of attempts are over
            while not exchange and \
                  (attempts <= (len(self.curr_routes[route1].linehauls)) *(len(self.curr_routes[route2].linehauls))):

                # generates two random linehaul indices from the two routes
                idx1 = rnd.randint(0, len(self.curr_routes[route1].linehauls) - 1)
                idx2 = rnd.randint(0, len(self.curr_routes[route2].linehauls) - 1)

                # if they aren't the same node and the capacity constraint holds
                if not (idx1 == idx2 and self.curr_routes[route1] == self.curr_routes[route2]) and \
                    (self.curr_routes[route1].linehauls_load() -
                     self.curr_routes[route1].linehauls[idx1].load +
                     self.curr_routes[route2].linehauls[idx2].load <= self.vehicle_load) and \
                    (self.curr_routes[route2].linehauls_load() -
                     self.curr_routes[route2].linehauls[idx2].load +
                     self.curr_routes[route1].linehauls[idx1].load <= self.vehicle_load):

                    # Exchange LL
                    supp_node = self.curr_routes[route1].linehauls[idx1]
                    self.curr_routes[route1].linehauls[idx1] = self.curr_routes[route2].linehauls[idx2]
                    self.curr_routes[route2].linehauls[idx2] = supp_node

                    exchange = True

                attempts += 1

        if exchange_type == "BB":

            # repeat until there is an exchange or the number of attempts are over
            while not exchange and \
                  (attempts <= (len(self.curr_routes[route1].backhauls)) * (len(self.curr_routes[route2].backhauls))):

                # generates two random backhauls indices from the two routes
                idx1 = rnd.randint(0, len(self.curr_routes[route1].backhauls) - 1)
                idx2 = rnd.randint(0, len(self.curr_routes[route2].backhauls) - 1)

                # if they aren't the same node and the capacity constraint holds
                if not (idx1 == idx2 and self.curr_routes[route1] == self.curr_routes[route2]) and \
                    (self.curr_routes[route1].backhauls_load() -
                     self.curr_routes[route1].backhauls[idx1].load +
                     self.curr_routes[route2].backhauls[idx2].load <= self.vehicle_load) and \
                    (self.curr_routes[route2].backhauls_load() -
                     self.curr_routes[route2].backhauls[idx2].load +
                     self.curr_routes[route1].backhauls[idx1].load <= self.vehicle_load):

                    # exchange
                    supp_node = self.curr_routes[route1].backhauls[idx1]
                    self.curr_routes[route1].backhauls[idx1] = self.curr_routes[route2].backhauls[idx2]
                    self.curr_routes[route2].backhauls[idx2] = supp_node

                    exchange = True

                attempts += 1

        if exchange_type == "BL" and len(self.curr_routes[route1].backhauls) >= 1:
            # if there are at least 2 backhaul nodes in the first route

            # repeat until there is an exchange or the number of attempts are over
            while not exchange and \
                  (attempts <= (len(self.curr_routes[route1].backhauls)) * (len(self.curr_routes[route2].linehauls))):

                # generates a random backhaul index from route 1
                idx1 = rnd.randint(0, len(self.curr_routes[route1].backhauls) - 1)
                # generates a random linehaul index from route 2
                idx2 = rnd.randint(0, len(self.curr_routes[route2].linehauls) - 1)

                # if the capacity constraints holds and there are at least 2 linehauls in the second route
                # (to avoid only backhauls routes)
                if (self.curr_routes[route1].linehauls_load() +
                    self.curr_routes[route2].linehauls[idx2].load <= self.vehicle_load) and \
                   (self.curr_routes[route2].backhauls_load() +
                    self.curr_routes[route1].backhauls[idx1].load <= self.vehicle_load) and \
                   (len(self.curr_routes[route2].linehauls) >= 2):

                    # exchange
                    # gets the backhaul from the first route
                    supp_node = self.curr_routes[route1].backhauls[idx1]

                    # inserts it in the head of backhauls list of the second route
                    self.curr_routes[route2].backhauls = [supp_node] + self.curr_routes[route2].backhauls

                    # removes it from route 1
                    self.curr_routes[route1].backhauls.remove(supp_node)

                    # now the same but for the linehaul node

                    # gets the linehaul from the second route
                    supp_node = self.curr_routes[route2].linehauls[idx2]

                    # inserts it in the tail of linehauls list of the first node
                    self.curr_routes[route1].linehauls.append(supp_node)

                    # removes it from the second list
                    self.curr_routes[route2].linehauls.remove(supp_node)

                    exchange = True

                attempts += 1

        if exchange_type == "LB" and len(self.curr_routes[route2].backhauls) >= 1:
            # if there are at least 2 backhaul nodes in the second route

            # repeat until there is an exchange or the number of attempts are over
            while not exchange and \
                  (attempts <= (len(self.curr_routes[route1].linehauls)) * (len(self.curr_routes[route2].backhauls))):

                # generates a random linehaul index from route1
                idx1 = rnd.randint(0, len(self.curr_routes[route1].linehauls) - 1)
                # generates a random backhaul index from route2
                idx2 = rnd.randint(0, len(self.curr_routes[route2].backhauls) - 1)

                # if the capacity constraints holds and there are at least two linehauls in the first route
                if (self.curr_routes[route1].backhauls_load() +
                    self.curr_routes[route2].backhauls[idx2].load <= self.vehicle_load) and \
                   (self.curr_routes[route2].linehauls_load() +
                    self.curr_routes[route1].linehauls[idx1].load <= self.vehicle_load) and \
                   (len(self.curr_routes[route1].linehauls) >= 2):

                    # exchange
                    # gets the linehaul of the first route
                    supp_node = self.curr_routes[route1].linehauls[idx1]

                    # inserts it in the tail of backhauls list of the second route
                    self.curr_routes[route2].linehauls.append(supp_node)

                    # removes it from route 1
                    self.curr_routes[route1].linehauls.remove(supp_node)

                    # now the same but for the backhaul node

                    # gets the backhaul of the first route
                    supp_node = self.curr_routes[route2].backhauls[idx2]

                    # inserts it in the head of backhauls list of the first node
                    self.curr_routes[route1].backhauls = [supp_node] + self.curr_routes[route1].backhauls

                    # removes it from route 2
                    self.curr_routes[route2].backhauls.remove(supp_node)

                    exchange = True

                attempts += 1

    def check_constraints(self):
        for route in self.curr_routes:

            # capacity
            if route.linehauls_load() > self.vehicle_load or \
                            route.backhauls_load() > self.vehicle_load:
                print("capacity constraint violated")
                exit(1)

            # no routes with only backhauls
            if not route.linehauls and route.backhauls:
                print("no-routes-with-only-backhauls constraint violated")
                exit(2)

            # no nodes in wrong list
            for node in route.backhauls:
                if node.type == LINEHAUL_TYPE:
                    print("no-linehaul-node-in-backhauls-list constraint violated")
                    exit(3)
            for node in route.linehauls:
                if node.type == BACKHAUL_TYPE:
                    print("no-backhaul-node-in-linehauls-list constraint violated")
                    exit(4)
