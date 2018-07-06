import os
from Instance import Instance
from Node import Node

# File Handler

def read_instance(filename):
    if os.path.isfile("data/Instances/" + filename + ".txt"):
        fp = open("data/Instances/" + filename + ".txt")

        # init instance
        instance = Instance()
        # Customers
        instance.n_customers = int(fp.readline())

        fp.readline() # default 1

        # Vehicles
        instance.n_vehicles = int(fp.readline())

        # Depot node
        depot_data = fp.readline().split()
        instance.depot_node.x = int(depot_data[0])
        instance.depot_node.y = int(depot_data[1])
        instance.vehicle_load = int(depot_data[3])
        instance.depot_node.type = 0
        instance.depot_node.id = 0

        id_counter = 1

        for line in fp.readlines():
            #print(line)

            # Customer
            data = line.split()
            delivery = int(data[2])
            pickup = int(data[3])

            # Backhaul
            if pickup != 0:
                # Creating backhaul node
                backhaul = Node()
                backhaul.x = int(data[0])
                backhaul.y = int(data[1])
                backhaul.load = pickup
                backhaul.type = 2
                backhaul.id = id_counter

                # adding it to list
                instance.backhaul_list.append(backhaul)
                id_counter += 1
            else:
                # Linehaul
                # Creating backhaul node
                linehaul = Node()
                linehaul.x = int(data[0])
                linehaul.y = int(data[1])
                linehaul.load = delivery
                linehaul.type = 1
                linehaul.id = id_counter

                # adding it to list
                instance.linehaul_list.append(linehaul)
                id_counter += 1

        return instance
