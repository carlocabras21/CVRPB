import os

from classes.Instance import *
from utils import *


def load_solution(filename):
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
