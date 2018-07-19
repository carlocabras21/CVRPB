import os

from classes.Instance import Instance
from classes.Node import Node
from utils.utils import BACKHAUL_TYPE, LINEHAUL_TYPE, cost


def load_lower_bound(file_name):
    """
        This method reads an instance file and retrieving the optimal objective function cost.

        :param file_name: a string, the name of the instance file
        :return: float, optimal objective function value
        """
    # Check if instance file exists
    if os.path.isfile("data/Instances/" + file_name):
        fp = open("data/DetailedSols/RPA_Solutions/Detailed_Solution_" + file_name)

        # For each line
        for line in fp.readlines():
            # Split lines for space char
            splitted_lines = line.split(" ")

            # Check if the line is the one containing the total cost
            if len(splitted_lines) == 4 and splitted_lines[0] == 'Total' and splitted_lines[1] == 'Cost':
                return float(splitted_lines[3])
    else:
        print("Error, no instance file named " + file_name + "!")


def load_instance(file_name):
    """
        This method reads an instance file and creates an Instance object, populating it with all the necessary information.

        :param file_name: a string, the name of the instance file
        :return: instance, an Istance object representing a CVRPB instance
        """
    # Check if instance file exists
    if os.path.isfile("data/Instances/" + file_name):
        fp = open("data/Instances/" + file_name)

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

            # Coordinates
            x = int(data[0])
            y = int(data[1])

            # Load
            delivery = int(data[2])
            pickup = int(data[3])

            # Check node type
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
    else:
        print("Error, no instance file named " + file_name + "!")


def create_instance_solution(instance, file_name, min_objf, optimal_cost, gap, end_cp, end_ls):
    """
        This method creates an output file for an instance

        :param instance:  an Istance object representing a CVRPB instance
        :param file_name: a string, the name of the instance file
        :param min_objf: a float, the value of minimum objective function
        :param optimal_cost: a float, the value of optimal objective function (lower bound)
        :param gap: a float, the gap between the optimal and minimized objective function
        :param end_cp: a float, time for the creation of the main routes
        :param end_ls: a float, time to perform the local search
        """

    # Creating new file (overwrite if it exists)
    fp = open("data/Solutions/" + file_name + "_solution.txt", "w+")

    # Writing informations about problem details
    fp.write("PROBLEM DETAILS")
    fp.write("\nCustomers: %d\n" % instance.n_customers)
    fp.write("Linehaul Customers: %d\n" % len(instance.linehaul_list))
    fp.write("Backhaul Customers: %d\n" % len(instance.backhaul_list))
    fp.write("Capacity: %d\n" % instance.vehicle_load)

    # Writing informations about local search
    fp.write("\nLOCAL SEARCH WITH BEST EXCHANGE")
    fp.write("\nTotal cost: %f\n" % min_objf)
    fp.write("Lower Bound: %f\n" % optimal_cost)
    fp.write("GAP: %f\n" % gap)

    # Writing informations about timers
    fp.write("\nTIMING")
    fp.write("\nConstruction phase time: %f\n" % end_cp)
    fp.write("Local search time: %f\n" % end_ls)
    fp.write("Total time: %f\n" % (end_cp + end_ls))

    # Writing informations about final routes
    fp.write("\nSOLUTION")
    fp.write("\nRoutes: %d\n" % len(instance.main_routes))

    id_route = 0
    for route in instance.main_routes:

        # Informations about every route
        fp.write("\nROUTE: %d\n" % id_route)
        fp.write("Cost: %f\n" % (cost(instance.distance_matrix, route)))
        fp.write("Delivery load: %f\n" % route.linehauls_load())
        fp.write("Pick-Up load: %f\n" % route.backhauls_load())
        fp.write("Customers in Route: %d\n" % (len(route.linehauls) + len(route.backhauls)))

        # Customers visit order
        str_route = route.get_route_solution()
        fp.write("Vertex sequence:\n")
        fp.write(str_route + "\n")

        id_route += 1