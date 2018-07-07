import os
from Instance import Instance
from Node import Node

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

        # Retriving the Depot node
        depot_data = fp.readline().split()
        instance.depot_node.x = int(depot_data[0])
        instance.depot_node.y = int(depot_data[1])
        instance.vehicle_load = int(depot_data[3])
        instance.depot_node.type = 0
        instance.depot_node.id = 0

        id_counter = 1

        # For each line in the file
        for line in fp.readlines():
            #print(line)

            # Customer data
            data = line.split()
            delivery = int(data[2])
            pickup = int(data[3])

            # Backhaul node
            if pickup != 0:
                # Creating a backhaul node
                backhaul = Node()
                backhaul.x = int(data[0])
                backhaul.y = int(data[1])
                backhaul.load = pickup
                backhaul.type = 2
                backhaul.id = id_counter

                # Adding it to list
                instance.backhaul_list.append(backhaul)
                id_counter += 1

            else: # Linehaul node
                # Creating a linehaul node
                linehaul = Node()
                linehaul.x = int(data[0])
                linehaul.y = int(data[1])
                linehaul.load = delivery
                linehaul.type = 1
                linehaul.id = id_counter

                # Adding it to list
                instance.linehaul_list.append(linehaul)
                id_counter += 1

        return instance
