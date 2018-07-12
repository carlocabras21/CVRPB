import numpy as np
import sys
import math
from Node import Node
from Route import Route
from utils.utils import *
import random as rnd


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

    #current_routes = []

    def __init__(self):
        self.n_customers = 0
        self.n_vehicles = 0
        self.vehicle_load = 0
        self.depot_node = Node()
        self.linehaul_list = []
        self.backhaul_list = []
        self.distance_matrix = np.array([[]])
        self.main_routes = []

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

        # SCAMBI AMMISSIBILI : cioe' scambi a random che peggiorano/migliorano la fo, ma non ci interessa, basta che permettano
        # di rispettare il vincolo di capacita'

        types = ["L", "B", "LL", "BB", "BL", "LB"]

        # Se la lunghezza di types e' 1 devo fare uno spostamento, altrimenti uno scambio

        for i in range(300):

            # SCAMBI LEGALI
            # Genero due indici random di due route esistenti tra quelle correnti
            r1 = rnd.randint(0, len(self.main_routes) - 1)
            r2 = rnd.randint(0, len(self.main_routes) - 1)
            choose = rnd.randint(2,5)
            #print(choose)

            exhange_type = types[choose]

            self.random_legal_exchange(r1, r2, exhange_type)

            '''
            # RIPOSIZIONAMENTI LEGALI SENZA SCAMBI, PROPRIO SPOSTAMENTI

            # Genero due indici random di due route esistenti tra quelle correnti
            r1 = rnd.randint(0, len(self.main_routes) - 1)
            r2 = rnd.randint(0, len(self.main_routes) - 1)
            choose = rnd.randint(0, 1)
            exhange_type = types[choose]
            '''

        '''
        # PERMUTAZIONE : DA SOLA NON BASTA! MI CONVIENE PRIMA FARE ALCUNI SCAMBI AMMISSIBILI RANDOM TRA LE ROTTE
        # per ogni rotta
        for route in self.main_routes:
            # la permuto internamente nella sua parte linehaul e backhaul distintamente
            rnd.shuffle(route.linehauls)
            rnd.shuffle(route.backhauls)
        '''


    def print_main_routes(self):
        print("Main Routes")
        for route in self.main_routes:
            print(route)
        print("\n")


    def random_legal_relocate(self, r1, r2, relocate_type):

        if r1 != r2:
            if relocate_type == "L":
                # L
                # Devo mettere un linehaul da la r1 alla r2 se rispetto il vincolo
                relocate = False  # False se non ho scambiato, True se effettuo uno scambio
                attempts = 1  # tentativi di scambio

                # Finche' non effettuo uno scambio o finche' non finisco i possibili tentativi
                while not relocate and (attempts <= (len(self.main_routes[r1].linehauls))):
                    # Genero un indice random di un linehaul
                    idx1 = rnd.randint(0, len(self.main_routes[r1].linehauls) - 1)

                    if self.main_routes[r2].linehauls_load() + self.main_routes[r1].linehauls[idx1].load <= self.vehicle_load:
                        # posso spostare
                        # appendo
                        self.main_routes[r2].linehauls.append(self.main_routes[r1].linehauls[idx1])
                        #elimino dalla vecchia
                        self.main_routes[r1].linehauls.remove(self.main_routes[r1].linehauls[idx1])

                        relocate = True

                    attempts += 1
            else:
                # B
                # Devo mettere un backhaul da la r1 alla r2 se rispetto il vincolo
                relocate = False  # False se non ho scambiato, True se effettuo uno scambio
                attempts = 1  # tentativi di scambio

                if len(self.main_routes[r1].backhauls) >= 1:
                    # Finche' non effettuo uno scambio o finche' non finisco i possibili tentativi
                    while not relocate and (attempts <= (len(self.main_routes[r1].backhauls))):
                        # Genero un indice random di un linehaul
                        idx1 = rnd.randint(0, len(self.main_routes[r1].backhauls) - 1)

                        if self.main_routes[r2].backhauls_load() + self.main_routes[r1].backhauls[idx1].load <= self.vehicle_load:
                            # posso spostare
                            # appendo
                            self.main_routes[r2].backhauls.append(self.main_routes[r1].backhauls[idx1])
                            # elimino dalla vecchia
                            self.main_routes[r1].backhauls.remove(self.main_routes[r1].backhauls[idx1])

                            relocate = True

                        attempts += 1

    def random_legal_exchange(self, r1, r2, exhange_type):
        #print(exhange_type)
        # exhange_type 1 : scambio due LL
        if exhange_type == "LL":
            exchange = False # False se non ho scambiato, True se effettuo uno scambio
            attempts = 1 # tentativi di scambio

            # Finche' non effettuo uno scambio o finche' non finisco i possibili tentativi
            while not exchange and (attempts <= (len(self.main_routes[r1].linehauls)) * (len(self.main_routes[r2].linehauls))):

                # Genero due indici random di due linehaul
                idx1 = rnd.randint(0, len(self.main_routes[r1].linehauls) - 1)
                idx2 = rnd.randint(0, len(self.main_routes[r2].linehauls) - 1)

                # In caso di stessa rotta evito che tenti di scambiare il nodo con se stesso
                if not (idx1 == idx2 and self.main_routes[r1] == self.main_routes[r2]):

                    # Controllo se lo scambio rispetta il vincolo di capacita'
                    if (self.main_routes[r1].linehauls_load() - self.main_routes[r1].linehauls[idx1].load + self.main_routes[r2].linehauls[idx2].load <= self.vehicle_load) and \
                       (self.main_routes[r2].linehauls_load() - self.main_routes[r2].linehauls[idx2].load + self.main_routes[r1].linehauls[idx1].load <= self.vehicle_load):

                        # SCAMBIO
                        supp_node = self.main_routes[r1].linehauls[idx1]
                        self.main_routes[r1].linehauls[idx1] = self.main_routes[r2].linehauls[idx2]
                        self.main_routes[r2].linehauls[idx2] = supp_node
                        exchange = True

                attempts += 1

        # exhange_type 2 : scambio due BB
        if exhange_type == "BB":
            exchange = False # False se non ho scambiato, True se effettuo uno scambio
            attempts = 1 # tentativi di scambio

            # Finche' non effettuo uno scambio o finche' non finisco i possibili tentativi
            while not exchange and (attempts <= (len(self.main_routes[r1].backhauls)) * (len(self.main_routes[r2].backhauls))):

                # Genero due indici random di due linehaul
                idx1 = rnd.randint(0, len(self.main_routes[r1].backhauls) - 1)
                idx2 = rnd.randint(0, len(self.main_routes[r2].backhauls) - 1)

                # In caso di stessa rotta evito che tenti di scambiare il nodo con se stesso
                if not (idx1 == idx2 and self.main_routes[r1] == self.main_routes[r2]):

                    # Controllo se lo scambio rispetta il vincolo di capacita'
                    if (self.main_routes[r1].backhauls_load() - self.main_routes[r1].backhauls[idx1].load + self.main_routes[r2].backhauls[idx2].load <= self.vehicle_load) and \
                       (self.main_routes[r2].backhauls_load() - self.main_routes[r2].backhauls[idx2].load + self.main_routes[r1].backhauls[idx1].load <= self.vehicle_load):

                        # SCAMBIO
                        supp_node = self.main_routes[r1].backhauls[idx1]
                        self.main_routes[r1].backhauls[idx1] = self.main_routes[r2].backhauls[idx2]
                        self.main_routes[r2].backhauls[idx2] = supp_node
                        exchange = True

                attempts += 1

        if exhange_type == "BL":
            # Devo scambiare un backhaul della prima route con un linehaul della seconda
            exchange = False  # False se non ho scambiato, True se effettuo uno scambio
            attempts = 1  # tentativi di scambio

            if len(self.main_routes[r1].backhauls) >= 1:
                # Finche' non effettuo uno scambio o finche' non finisco i possibili tentativi
                while not exchange and (attempts <= (len(self.main_routes[r1].backhauls)) * (len(self.main_routes[r2].linehauls))):
                    # Genero due indici random
                    idx1 = rnd.randint(0, len(self.main_routes[r1].backhauls) - 1)
                    idx2 = rnd.randint(0, len(self.main_routes[r2].linehauls) - 1)

                    # Controllo se lo scambio rispetta il vincolo di capacita'
                    if (self.main_routes[r1].linehauls_load() + self.main_routes[r2].linehauls[idx2].load <= self.vehicle_load) and \
                       (self.main_routes[r2].backhauls_load() + self.main_routes[r1].backhauls[idx1].load <= self.vehicle_load) and \
                       (len(self.main_routes[r2].linehauls) >= 2):

                        # SCAMBIO
                        # prendo il backhaul
                        supp_node = self.main_routes[r1].backhauls[idx1]

                        # lo metto in testa alla lista dei backhaul della route 2
                        self.main_routes[r2].backhauls = [supp_node] + self.main_routes[r2].backhauls

                        # elimino il backhaul dalla route 1
                        self.main_routes[r1].backhauls.remove(supp_node)

                        # prendo il linehaul
                        supp_node = self.main_routes[r2].linehauls[idx2]

                        # lo metto in coda alla lista dei linehaul della route 1
                        self.main_routes[r1].linehauls.append(supp_node)

                        # elimino il linehaul dalla route 2
                        self.main_routes[r2].linehauls.remove(supp_node)

                        exchange = True

                    attempts += 1



        if exhange_type == "LB":
            # Devo scambiare un linehaul della prima route con un backhaul della seconda
            exchange = False  # False se non ho scambiato, True se effettuo uno scambio
            attempts = 1  # tentativi di scambio

            if len(self.main_routes[r2].backhauls) >= 1:
                # Finche' non effettuo uno scambio o finche' non finisco i possibili tentativi
                while not exchange and (attempts <= (len(self.main_routes[r1].linehauls)) * (len(self.main_routes[r2].backhauls))):
                    # Genero due indici random
                    idx1 = rnd.randint(0, len(self.main_routes[r1].linehauls) - 1)
                    idx2 = rnd.randint(0, len(self.main_routes[r2].backhauls) - 1)

                    # Controllo se lo scambio rispetta il vincolo di capacita'
                    if (self.main_routes[r1].backhauls_load() + self.main_routes[r2].backhauls[idx2].load <= self.vehicle_load) and \
                       (self.main_routes[r2].linehauls_load() + self.main_routes[r1].linehauls[idx1].load <= self.vehicle_load) and \
                       (len(self.main_routes[r1].linehauls) >= 2):

                        # SCAMBIO
                        # prendo il linehaul
                        supp_node = self.main_routes[r1].linehauls[idx1]

                        # lo metto in coda alla lista dei linehauls della route 2
                        self.main_routes[r2].linehauls.append(supp_node)

                        # elimino il linehauls dalla route 1
                        self.main_routes[r1].linehauls.remove(supp_node)

                        # prendo il backhaul
                        supp_node = self.main_routes[r2].backhauls[idx2]

                        # lo metto in testa alla lista dei backhauls della route 1
                        self.main_routes[r1].backhauls = [supp_node] + self.main_routes[r1].backhauls

                        # elimino il backhauls dalla route 2
                        self.main_routes[r2].backhauls.remove(supp_node)

                        exchange = True

                    attempts += 1