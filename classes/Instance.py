import numpy as np
import sys
import math
from Node import Node
from Route import Route
from utils.utils import *
from random import shuffle
from copy import deepcopy
from random import randint

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

    depot_node = Node()  # in teoria dovrebbe farlo il costruttore

    linehaul_list = []
    backhaul_list = []

    distance_matrix = np.array([[]])
    main_routes = []

    current_routes = []

    def __init__(self):
        pass

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

        # PERMUTATION
        '''
        for route in linehauls_routes:
            shuffle(route)

        for route in backhauls_routes:
            shuffle(route)
        '''

        print("n of linehauls routes: " + str(len(linehauls_routes)))
        print("n of backhauls routes: " + str(len(backhauls_routes)))
        print("n of vehicles: " + str(self.n_vehicles))
        print("max load: " + str(self.vehicle_load))


        # Assuming that linehaul routes are greater that backhaul routes
        while len(backhauls_routes) > len(linehauls_routes):
            i = 0
            while len(linehauls_routes[i]) <= 1:
                i += 1

            # In posizione i c'e' una rotta con almeno due nodi linehaul

            #prendo il primo nodo
            node = linehauls_routes[i][0]

            # lo rimuovo dalla lista corrente in cui sta
            linehauls_routes[i].remove(node)

            # creo una nuova lista con quel nodo
            linehauls_routes.append([node])

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


        while len(self.main_routes) < self.n_vehicles:
            # Dobbiamo cercare una rotta che ha almeno 2 L e un B
            i = 0
            while (len(self.main_routes[i].linehauls) < 2) or (len(self.main_routes[i].backhauls) < 1):
                i += 1

            line_node = self.main_routes[i].linehauls[0]
            back_node = self.main_routes[i].backhauls[0]

            self.main_routes[i].linehauls.remove(line_node)
            self.main_routes[i].backhauls.remove(back_node)

            curr_route = Route()

            curr_route.depot_node = self.depot_node
            curr_route.linehauls = [line_node]
            curr_route.backhauls = [back_node]

            self.main_routes.append(curr_route)

        #print("Main routes")
        #for route in self.main_routes:
        #    print(route)


    def get_unified_routes(self):
        routes = []
        for route in self.main_routes:
            routes.append([route.depot_node] + route.linehauls + route.backhauls + [route.depot_node])
        return routes


    # Tramite tale metodo partendo dalle current route le permuto in maniera casuale sia internamente che non
    def mix_routes_random(self):
        # parto dalle main routes!!! Le copio proprio, non faccio un riferimento
        self.current_routes = deepcopy(self.main_routes)


        # SCAMBI AMMISSIBILI : cioe' scambi a random che peggiorano/migliorano la fo, ma non ci interessa, basta che permettano
        # di rispettare il vincolo di capacita'

        # Genero due indici random di due route esistenti tra quelle correnti
        r1 = randint(0, len(self.current_routes) - 1)
        r2 = randint(0, len(self.current_routes) - 1)

        # Se vale 1 scambio linehauls altrimenti backhauls tra le rotte. Se non ci sono backhauls scambio linehauls o se
        # c'e' almeno un backhaul lo metto nell'altra rotta ecc. 3 scambio linehauls e backhauls tra loro da fare poi
        #choose = randint(1,2,3)
        choose = 1
        print(r1, r2, choose)
        self.legal_exchange(self.current_routes[r1], self.current_routes[r2], choose)

        '''
        # PERMUTAZIONE : DA SOLA NON BASTA! MI CONVIENE PRIMA FARE ALCUNI SCAMBI AMMISSIBILI RANDOM TRA LE ROTTE
        # per ogni rotta
        for route in self.current_routes:
            # la permuto internamente nella sua parte linehaul e backhaul distintamente
            shuffle(route.linehauls)
            shuffle(route.backhauls)
        '''

    def print_main_routes(self):
        print("Main Routes")
        for route in self.main_routes:
            print(route)

    def print_curr_routes(self):
        print("Current Routes")
        for route in self.current_routes:
            print(route)


    def legal_exchange(self, route1, route2, choose):

        # Choose 1 : scambio due LL
        if choose == 1:
            exchange = False # False se non ho scambiato, True se effettuo uno scambio
            attempts = 1 # tentativi di scambio

            # Finche' non effettuo uno scambio o finche' non finisco i possibili tentativi
            while not exchange and (attempts <= (len(route1.linehauls)) * (len(route2.linehauls))):

                # Genero due indici random di due linehaul
                idx1 = randint(0, len(route1.linehauls) - 1)
                idx2 = randint(0, len(route2.linehauls) - 1)

                # In caso di stessa rotta evito che tenti di scambiare il nodo con se stesso
                if idx1 != idx2:
                    print(exchange)
                    print("Tentativo : %d" % attempts)
                    print(route1.linehauls[idx1])
                    print(route2.linehauls[idx2])
                    print("\n")


                    # Controllo se lo scambio rispetta il vincolo di capacita'
                    if (route1.linehauls_load() - route1.linehauls[idx1].load + route2.linehauls[idx2].load <= self.vehicle_load) and \
                       (route2.linehauls_load() - route2.linehauls[idx2].load + route1.linehauls[idx1].load <= self.vehicle_load):

                        # SCAMBIO
                        supp_node = route1.linehauls[idx1]
                        route1.linehauls[idx1] = route2.linehauls[idx2]
                        route2.linehauls[idx2] = supp_node
                        exchange = True

                    attempts += 1
