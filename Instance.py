from Node import Node
import numpy as np
import math
from scipy.spatial import distance
import sys

class Instance(object):

    n_customers = 0
    n_vehicles = 0
    vehicle_load = 0
    depot_node = Node()
    linehaul_list = []
    backhaul_list = []
    distance_matrix = np.array([[]])

    def __init__(self):
        pass

    def showData(self):

        print("Number of Customers %d" % self.n_customers)
        print("Number of Vehicles %d" % self.n_vehicles)
        print("Vehicle Load %d" % self.vehicle_load)
        print(self.depot_node)

        for node in self.backhaul_list:
            print(node)

        for node in self.linehaul_list:
            print(node)

    def compute_distance_matrix(self):
        self.distance_matrix = np.zeros((self.n_customers + 1, self.n_customers + 1))

        customers = np.concatenate(([self.depot_node], self.linehaul_list, self.backhaul_list))

        for i in customers:
            for j in customers:
                self.distance_matrix[i.id,j.id] = self.distance(i,j)

    def distance(self,i,j):
        return distance.euclidean([i.x, i.y],[j.x, j.y])

    def print_distance_matrix(self):
        for i in range(0,self.n_customers + 1):
            for j in range(0,self.n_customers + 1):
                sys.stdout.write('%.1f' % self.distance_matrix[i,j] + " ")

            print("\n")