import os

from classes.Instance import *
from utils import *


def load_lower_bound(filename):
    if os.path.isfile("data/Instances/" + filename):
        fp = open("data/DetailedSols/RPA_Solutions/Detailed_Solution_" + filename)

        for line in fp.readlines():
            # print(line.split())
            splitted = line.split()
            if len(splitted) == 4 and splitted[0] == 'Total' and splitted[1] == 'Cost':
                return float(splitted[3])


# File Handler, da spostare in utils ???

def load_instance(filename):
    """
    This method reads an instance file and creates an Instance object, populating it with all the necessary information.

    :param filename: a string, the name of the instance file
    :return: instance, an Istance object representing a CVRPB instance
    """
    if os.path.isfile("data/Instances/" + filename):
        fp = open("data/Instances/" + filename)

        # Instantiating a new Instance object
        instance = Instance()

        # Retrieving data about the number of customers and vehicles
        instance.n_customers = int(fp.readline())
        fp.readline()  # Skipping the default 1 row
        instance.n_vehicles = int(fp.readline())

        # Retrives the Depot node data
        depot_data = fp.readline().split()

        # Depot node
        instance.depot_node = Node(int(depot_data[0]), int(depot_data[1]), 0, 0, 0)

        # sets the vehicles load
        instance.vehicle_load = int(depot_data[3])

        # intializes the id counter
        id_counter = 1

        # For each line in the file
        for line in fp.readlines():

            # Customer data
            data = line.split()

            x = int(data[0])
            y = int(data[1])
            delivery = int(data[2])
            pickup = int(data[3])

            if pickup != 0:  # Backhaul node
                # Creates a backhaul node and adds it to the list
                instance.backhaul_list.append(
                    Node(x, y, pickup, BACKHAUL_TYPE, id_counter)
                )

            else:  # Linehaul node
                # Creates a linehaul node and adds it to the list
                instance.linehaul_list.append(
                    Node(x, y, delivery, LINEHAUL_TYPE, id_counter)
                )

            # updating id
            id_counter += 1

        return instance

def create_instance_solution(instance, file_name, min_fo, optimal_cost, gap, end_cp, end_ls):
    fp = open("data/Solutions/" + file_name + "_solution.txt", "w+")

    fp.write("PROBLEM DETAILS")
    fp.write("\nCustomers: %d\n" % instance.n_customers)
    fp.write("Linehaul Customers: %d\n" % len(instance.linehaul_list))
    fp.write("Backhaul Customers: %d\n" % len(instance.backhaul_list))
    fp.write("Capacity: %d\n" % instance.vehicle_load)

    fp.write("\nLOCAL SEARCH WITH BEST EXCHANGE")
    fp.write("\nTotal cost: %f\n" % min_fo)
    fp.write("Lower Bound: %f\n" % optimal_cost)
    fp.write("GAP: %f\n" % gap)

    fp.write("\nTIMING")
    fp.write("\nConstruction phase time: %f\n" % end_cp)
    fp.write("Local search time: %f\n" % end_ls)
    fp.write("Total time: %f\n" % (end_cp + end_ls))

    fp.write("\nSOLUTION")
    fp.write("\nRoutes: %d\n" % len(instance.main_routes))

    id_route = 0
    for route in instance.main_routes:
        fp.write("\nROUTE: %d\n" % id_route)
        fp.write("Cost: %f\n" % (cost(instance.distance_matrix, route)))
        fp.write("Delivery load: %f\n" % route.linehauls_load())
        fp.write("Pick-Up load: %f\n" % route.backhauls_load())
        fp.write("Customers in Route: %d\n" % (len(route.linehauls) + len(route.backhauls)))

        str_route = route.get_route_solution()
        fp.write("Vertex sequence:\n")
        fp.write(str_route + "\n")

        id_route += 1