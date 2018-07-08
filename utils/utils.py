from scipy.spatial import distance
import time

from classes.Node import Node

LINEHAUL_TYPE = 1
BACKHAUL_TYPE = 2


def compute_distance(i, j):
    """
    This method computes the euclidean distance between two nodes (customers) i, j.

    :param i: A Node object, the first node
    :param j: A Node object, the second node
    :return: the euclidean distance between the two nodes
    """
    return distance.euclidean([i.x, i.y], [j.x, j.y])


def cost(dist_matrix, route):
    """
    This method computes a route's cost as a sum of the individual links between nodes.

    :param dist_matrix: A numpy bi-dimensional array, the distance matrix
    :param route: A Route object
    :return: cost, the route's cost
    """

    current_cost = 0
    full_route = [route.depot_node] + route.linehauls + route.backhauls + [route.depot_node]

    # 0 -> L -> ... -> L -> B -> ... -> B -> 0
    for i in range(len(full_route) - 1):
        # print(dist_matrix[full_route[i].id, full_route[i+1].id])
        current_cost += dist_matrix[full_route[i].id, full_route[i + 1].id]

    return current_cost


def objective_function(distance_matrix, routes):
    """
    This method computes the current value of the objective function.

    :param distance_matrix: A numpy bi-dimensional array, the distance matrix
    :param routes: A list of Route objects, the current set of routes
    :return: fo, the objective function's value
    """
    fo = 0

    # computing for each route the cost associated to each adjacent pair of route's nodes
    for route in routes:
        fo += cost(distance_matrix, route)

    return fo


def minimize_fo(instance):
    """
    This function minimizes the objective function's value by implementing the Bext Exchange approach.

    :param instance: An Instance object, the CVRPB instance
    :return: nothing
    """
    fo_curr = objective_function(instance.distance_matrix, instance.main_routes)
    threshold = 0.01

    is_objective_function_improving = True

    # Finding the bext exchange for each route's node

    start = time.time()

    while is_objective_function_improving:

        fo_prec = fo_curr

        # indice route primo nodo
        for i in range(len(instance.main_routes)):
            # indice nodo i-esima route primo nodo
            for m in range(1, len(instance.main_routes[i].linehauls)):
                # indice route secondo nodo
                for j in range(len(instance.main_routes)):
                    # indice nodo j-esima route secondo nodo
                    for n in range(1, len(instance.main_routes[i].linehauls)):
                        # cerca migliore scambio e salva le coordinate dello scambio (cioe' (route-i,nodo1) (route-j,
                        #  nodo2))
                        # print("")
                        pass

        # Updating gain
        gain = (fo_prec - fo_curr) / fo_prec
        is_objective_function_improving = gain > threshold

    end = time.time() - start
    print("seconds %f" % end)
