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
            Override of the __init__ method in order to instantiate a new Route Object with new values.

            :param: depot_node: a Node object, represents the deposit node
            :param linehauls: A list of Node objects, the linehaul nodes list
            :param backhauls: A list of Node objects, the backhaul nodes list
            """
        self.n_customers = 0
        self.n_vehicles = 0
        self.vehicle_load = 0

        self.depot_node = Node()

        self.linehaul_list = []
        self.backhaul_list = []

        self.distance_matrix = np.array([[]])
        self.curr_routes = []

    def show_data(self):
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
            # print("Route :) ")

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

            # for k in curr_route:
            #    print(k)

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

        '''
        print("n of initial linehauls routes: " + str(len(linehauls_routes)))
        print("n of initial backhauls routes: " + str(len(backhauls_routes)))
        print("n of vehicles: " + str(self.n_vehicles))
        print("max load: " + str(self.vehicle_load))
        '''

        # if we have more backhauls routes then linehaul routes, we create one more linehaul route
        # by removing a node from the first route that has at least two linehaul nodes
        while len(backhauls_routes) > len(linehauls_routes):
            print("creating one more linehaul route...")

            # finds first route with at least 2 linehaul nodes
            i = 0
            while len(linehauls_routes[i]) <= 1:
                i += 1

            # ... and it's in position i

            # takes the first node of the ith route and creates a list with only that node
            node = linehauls_routes[i][0]

            # removes the node from its current list
            linehauls_routes[i].remove(node)

            # creates the list
            linehauls_routes.append([node])

            # Linking linehaul and backhaul routes in pairs, as long as there are backhaul routes
        for i in range(len(backhauls_routes)):
            self.curr_routes.append(
                Route(self.depot_node, linehauls_routes[i], backhauls_routes[i])
            )

        # If there are some remaining linehaul routes, main routes of only linehaul routes are created
        for i in range(len(backhauls_routes), len(linehauls_routes)):
            self.curr_routes.append(
                Route(self.depot_node, linehauls_routes[i], [])
            )

        # if we have less routes than customers, we create routes until they are the same number
        # (with this method we can get more combination in the mixing phase)
        # the approach used is the same as the precedent creation-of-linehaul-route step
        while len(self.curr_routes) < self.n_vehicles:
            # finds a route with at least two linehauls and two backhauls
            i = 0
            while (len(self.curr_routes[i].linehauls) < 2) or (len(self.curr_routes[i].backhauls) < 1):
                i += 1

            # removes their first L/B node and creates the list

            line_node = self.curr_routes[i].linehauls[0]
            back_node = self.curr_routes[i].backhauls[0]

            self.curr_routes[i].linehauls.remove(line_node)
            self.curr_routes[i].backhauls.remove(back_node)

            self.curr_routes.append(
                Route(self.depot_node, [line_node], [back_node])
            )

    def get_unified_routes(self):
        """
        Concatenates the depot, the linehauls, the backhauls and finally again the depot
        in a single list.
        It's used in the exchange phase, when we need the routes in a single list,
        not separating linehauls from backhauls from the depot.

        :return: a list of routes, i.e. a list of list of Nodes
        """
        routes = []
        for route in self.curr_routes:
            routes.append([route.depot_node] + route.linehauls + route.backhauls + [route.depot_node])
        return routes

    # Tramite tale metodo partendo dalle current route le permuto in maniera casuale
    # sia internamente che non
    def mix_routes_random(self):
        """
        Mixes the routes by performing feasible exchange: we move a node from a route
        to another (and viceversa for the other node) if after the exchange all the
        constraints are respected.
        """

        # excchange type:
        #   L/B: move a node from a route to another, without exchange with other nodes
        #        (i.e. a relocate move)
        #   LL (BB): exchange between linehauls (bakchauls) nodes
        #   BL (LB): exchange between a backhaul (linehaul) with a linehaul (backhaul),
        #            only if it's legal
        types = ["L", "B", "LL", "BB", "BL", "LB"]

        for i in range(500):
            # selects the exchange type randomly
            choose = rnd.randint(0, 5)

            if choose >= 2:
                # we have to do an exchange between two nodes

                # generates two random indices for the routes
                r1 = rnd.randint(0, len(self.curr_routes) - 1)
                r2 = rnd.randint(0, len(self.curr_routes) - 1)

                # recover the exchange type
                exchange_type = types[choose]

                # do the exchange between r1 and r2
                self.random_legal_exchange(r1, r2, exchange_type)

            else:
                # we have to move a node

                # generates two random indices for the routes
                r1 = rnd.randint(0, len(self.curr_routes) - 1)
                r2 = rnd.randint(0, len(self.curr_routes) - 1)

                # recover the relocate type
                relocate_type = types[choose]

                # do the relocate between r1 and r2
                self.random_legal_relocate(r1, r2, relocate_type)

        # random permutation inside the linehauls or backhauls of a route,
        # no constraints violated
        for route in self.curr_routes:
            rnd.shuffle(route.linehauls)
            rnd.shuffle(route.backhauls)

    def random_legal_relocate(self, r1, r2, relocate_type):
        """
        Moves a node of type relocate_type from route r1 to route r2,
        within all the constraints
        :param r1: the route from which we remove the node
        :param r2: the to which we add the node
        :param relocate_type: the type of the node
        :return:
        """

        if r1 != r2:
            # we move the node only if the routes are different, i.e. the node goes
            # from one route to another

            if relocate_type == "L":
                # we have to move a Linehaul node from r1 to r2    

                relocate = False  # True if the relocate happens, False otherwise
                attempts = 1  # relocate attempts

                while not relocate and (attempts <= (len(self.curr_routes[r1].linehauls))):
                    # repeat until there is a relocate or until we finish the numer of attempts

                    # generates a random linehaul index
                    idx1 = rnd.randint(0, len(self.curr_routes[r1].linehauls) - 1)

                    if (self.curr_routes[r2].linehauls_load() + self.curr_routes[r1].linehauls[idx1].load <=
                            self.vehicle_load) and (len(self.curr_routes[r1].linehauls) >= 2):
                        # if the capacity constraint is respected

                        # appends the node to r2
                        self.curr_routes[r2].linehauls.append(self.curr_routes[r1].linehauls[idx1])

                        # removes the node from r1
                        self.curr_routes[r1].linehauls.remove(self.curr_routes[r1].linehauls[idx1])

                        relocate = True

                    attempts += 1
            else:  # B
                # we have to move a Backhaul node from r1 to r2   

                relocate = False  # True if the relocate happens, False otherwise
                attempts = 1  # relocate attempts

                if len(self.curr_routes[r1].backhauls) >= 1:
                    # if there are at least two bakchauls nodes; with the purpose of not removing
                    # the only backhaul node from route r1

                    while not relocate and (attempts <= (len(self.curr_routes[r1].backhauls))):
                        # repeat until there is a relocate or until we finish the numer of attempts

                        # generates a random backhaul index
                        idx1 = rnd.randint(0, len(self.curr_routes[r1].backhauls) - 1)

                        if (self.curr_routes[r2].backhauls_load() + self.curr_routes[r1].backhauls[
                            idx1].load <= self.vehicle_load) and \
                                (len(self.curr_routes[r2].linehauls) >= 1):
                            # if the capacity constraint is respected

                            backhaul_to_move = self.curr_routes[r1].backhauls[idx1]

                            # appends the node to r2
                            self.curr_routes[r2].backhauls.append(backhaul_to_move)

                            # removes the node from r1
                            self.curr_routes[r1].backhauls.remove(self.curr_routes[r1].backhauls[idx1])

                            relocate = True

                        attempts += 1

    def random_legal_exchange(self, r1, r2, exchange_type):
        """
        Computes an exchange between route r1 and route r2 of type exchange type,
        within all the constraints.

        For a detailed explanation of how an exchange is performed, see the
        "finale_exchange" and "minimize_fo" functions

        :param r1: the route from which we remove the node
        :param r2: the to which we add the node
        :param exchange_type: the type of the exchange
        :return:
        """

        exchange = False  # True when an exchange happens, False otherwise
        attempts = 1  # number of exchange attempts

        if exchange_type == "LL":
            # exchange between two linehaul nodes

            # repeat until there is an exchange or the number of attempts are over
            while not exchange and \
                    (attempts <= (len(self.curr_routes[r1].linehauls)) *
                                 (len(self.curr_routes[r2].linehauls))):

                # generates two random linehaul indices from zero to the numbers of linehauls
                # in each route minus 1
                idx1 = rnd.randint(0, len(self.curr_routes[r1].linehauls) - 1)
                idx2 = rnd.randint(0, len(self.curr_routes[r2].linehauls) - 1)

                # if they aren't the same node and the capacity constraint holds
                if not (idx1 == idx2 and self.curr_routes[r1] == self.curr_routes[r2]) and \
                    (self.curr_routes[r1].linehauls_load() -
                     self.curr_routes[r1].linehauls[idx1].load +
                     self.curr_routes[r2].linehauls[idx2].load <=
                     self.vehicle_load) and \
                    (self.curr_routes[r2].linehauls_load() -
                     self.curr_routes[r2].linehauls[idx2].load +
                     self.curr_routes[r1].linehauls[idx1].load <=
                     self.vehicle_load):
                    # exchange
                    supp_node = self.curr_routes[r1].linehauls[idx1]
                    self.curr_routes[r1].linehauls[idx1] = self.curr_routes[r2].linehauls[idx2]
                    self.curr_routes[r2].linehauls[idx2] = supp_node
                    exchange = True

                attempts += 1

        if exchange_type == "BB":
            # exchange between two backhaul nodes

            # repeat until there is an exchange or the number of attempts are over
            while not exchange and \
                    (attempts <= (len(self.curr_routes[r1].backhauls)) *
                                 (len(self.curr_routes[r2].backhauls))):

                # generates two random backhauls indices from zero to the numbers of backhauls
                # in each route minus 1
                idx1 = rnd.randint(0, len(self.curr_routes[r1].backhauls) - 1)
                idx2 = rnd.randint(0, len(self.curr_routes[r2].backhauls) - 1)

                # if they aren't the same node and the capacity constraint holds
                if not (idx1 == idx2 and self.curr_routes[r1] == self.curr_routes[r2]) and \
                    (self.curr_routes[r1].backhauls_load() -
                     self.curr_routes[r1].backhauls[idx1].load +
                     self.curr_routes[r2].backhauls[idx2].load <=
                     self.vehicle_load) and \
                    (self.curr_routes[r2].backhauls_load() -
                     self.curr_routes[r2].backhauls[idx2].load +
                     self.curr_routes[r1].backhauls[idx1].load <=
                     self.vehicle_load):

                    # exchange
                    supp_node = self.curr_routes[r1].backhauls[idx1]
                    self.curr_routes[r1].backhauls[idx1] = self.curr_routes[r2].backhauls[idx2]
                    self.curr_routes[r2].backhauls[idx2] = supp_node
                    exchange = True

                attempts += 1

        # exchange between the first backhaul of the first route and
        # the last linehaul of the second route
        if exchange_type == "BL" and len(self.curr_routes[r1].backhauls) >= 1:
            # if there are at least 2 backhaul nodes in the first route

            # repeat until there is an exchange or the number of attempts are over
            while not exchange and (
                        attempts <= (len(self.curr_routes[r1].backhauls)) *
                                    (len(self.curr_routes[r2].linehauls))):

                # generates a random backhaul index from zero to the numbers of backhauls -1
                idx1 = rnd.randint(0, len(self.curr_routes[r1].backhauls) - 1)
                # generates a random linehaul index from zero to the numbers of linehauls -1
                idx2 = rnd.randint(0, len(self.curr_routes[r2].linehauls) - 1)

                # if the capacity constraints holds and there are at least
                # 2 linehauls in the first route, with the purpose of not
                # deleting that linehaul route
                if (self.curr_routes[r1].linehauls_load() +
                    self.curr_routes[r2].linehauls[idx2].load <=
                    self.vehicle_load) and \
                   (self.curr_routes[r2].backhauls_load() +
                    self.curr_routes[r1].backhauls[idx1].load <=
                    self.vehicle_load) and \
                   (len(self.curr_routes[r2].linehauls) >= 2):

                    # exchange
                    # gets the last backhaul of the first route
                    supp_node = self.curr_routes[r1].backhauls[idx1]

                    # inserts it in the head of backhauls list of the second route
                    self.curr_routes[r2].backhauls = [supp_node] + self.curr_routes[r2].backhauls

                    # removes it from route 1
                    self.curr_routes[r1].backhauls.remove(supp_node)

                    # now the same but for the linehaul node

                    # gets the linehaul from the second route
                    supp_node = self.curr_routes[r2].linehauls[idx2]

                    # inserts it in the tail of linehauls list of the first node
                    self.curr_routes[r1].linehauls.append(supp_node)

                    # removes it from the second list
                    self.curr_routes[r2].linehauls.remove(supp_node)

                    exchange = True

                attempts += 1

        # exchange between the last linehaul of the first route and
        # the first backhaul of the second route
        if exchange_type == "LB" and len(self.curr_routes[r2].backhauls) >= 1:
            # if there are at least 2 backhaul nodes in the second route

            # repeat until there is an exchange or the number of attempts are over
            while not exchange and (
                        attempts <= (len(self.curr_routes[r1].linehauls)) *
                                    (len(self.curr_routes[r2].backhauls))):

                # generates a random linehaul index from zero to the numbers of linehauls -1
                idx1 = rnd.randint(0, len(self.curr_routes[r1].linehauls) - 1)
                # generates a random backhaul index from zero to the numbers of backhauls -1
                idx2 = rnd.randint(0, len(self.curr_routes[r2].backhauls) - 1)

                # if the capacity constraints holds and there are at least two linehauls
                # in the first route
                if (self.curr_routes[r1].backhauls_load() +
                    self.curr_routes[r2].backhauls[idx2].load <=
                    self.vehicle_load) and \
                   (self.curr_routes[r2].linehauls_load() +
                    self.curr_routes[r1].linehauls[idx1].load <=
                    self.vehicle_load) and \
                   (len(self.curr_routes[r1].linehauls) >= 2):

                    # exchange
                    # gets the last linehaul of the first route
                    supp_node = self.curr_routes[r1].linehauls[idx1]

                    # inserts it in the tail of backhauls list of the second route
                    self.curr_routes[r2].linehauls.append(supp_node)

                    # removes it from route 1
                    self.curr_routes[r1].linehauls.remove(supp_node)

                    # now the same but for the backhaul node

                    # gets the first backhaul of the first route
                    supp_node = self.curr_routes[r2].backhauls[idx2]

                    # inserts it in the head of backhauls list of the first node
                    self.curr_routes[r1].backhauls = [supp_node] + self.curr_routes[r1].backhauls

                    # removes it from route 2
                    self.curr_routes[r2].backhauls.remove(supp_node)

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
