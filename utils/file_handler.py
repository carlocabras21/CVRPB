import os

from classes.Instance import Instance
from utils import creating_node


# File Handler, da spostare in utils ???

def read_instance(filename):
    """
    This method reads an instance file and creates an Instance object, populating it with all the necessary information.

    :param filename: a string, the name of the instance file
    :return: instance, an Istance object representing a CVRPB instance
    """
    if os.path.isfile("data/Instances/" + filename + ".txt"):
        fp = open("data/Instances/" + filename + ".txt")

        # Instantiating a new Instance object
        instance = Instance()

        # Retrieving data about the number of customers and vehicles
        instance.n_customers = int(fp.readline())
        fp.readline() # Skipping the default 1 row
        instance.n_vehicles = int(fp.readline())

        # Retriving the Depot node data
        depot_data = fp.readline().split()

        # Depot node
        depot_node = creating_node(int(depot_data[0]), int(depot_data[1]), 0, 0, 0)
        instance.depot_node = depot_node

        # setting up the vehicles load
        instance.vehicle_load = int(depot_data[3])

        # init_id
        id_counter = 1

        # For each line in the file
        for line in fp.readlines():

            # Customer data
            data = line.split()
            delivery = int(data[2])
            pickup = int(data[3])

            # Backhaul node
            if pickup != 0:
                # Creating a backhaul node
                backhaul = creating_node(int(data[0]), int(data[1]), pickup, 2, id_counter)

                # Adding it to list
                instance.backhaul_list.append(backhaul)

            else: # Linehaul node
                # Creating a linehaul node
                linehaul = creating_node(int(data[0]), int(data[1]), delivery, 1, id_counter)

                # Adding it to list
                instance.linehaul_list.append(linehaul)

            # updating id
            id_counter += 1

        return instance
