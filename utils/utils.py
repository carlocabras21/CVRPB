from scipy.spatial import distance
import time

from classes.Node import Node
DEPOT_TYPE = 0
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
    threshold = 0.0001

    is_objective_function_improving = True

    # Finding the bext exchange for each route's node

    start = time.time()

    while is_objective_function_improving:

        exchange_indices = [0,1,2,3]
        exchange_type = "null"

        routes = []

        # Create routtttttttesssssss
        for route in instance.main_routes:
            routes.append([route.depot_node] + route.linehauls + route.backhauls + [route.depot_node])

        fo_prec = fo_curr

        #print(fo_prec)

        #print(range(1, len(routes[0]) - 1))
        #print(range(1, len(routes[1]) - 1))
        for i in range(len(routes)):
            for m in range(1, len(routes[i]) - 1):
                # labels

                fst_line_int = (routes[i][m].type == LINEHAUL_TYPE and routes[i][m + 1].type == LINEHAUL_TYPE) \
                               or (routes[i][m].type == LINEHAUL_TYPE and len(instance.main_routes[i].linehauls) == 1)

                fst_line_ext = routes[i][m].type == LINEHAUL_TYPE and \
                               (routes[i][m + 1].type == DEPOT_TYPE or routes[i][m + 1].type == BACKHAUL_TYPE) and \
                                not fst_line_int

                fst_back_int = routes[i][m].type == BACKHAUL_TYPE and routes[i][m - 1].type == BACKHAUL_TYPE

                fst_back_ext = routes[i][m].type == BACKHAUL_TYPE and routes[i][m - 1].type == LINEHAUL_TYPE

                if routes[i][m].type == BACKHAUL_TYPE and routes[i][m - 1].type == DEPOT_TYPE:
                    print("____________rotta sbagliata______________")

                if (fst_line_ext + fst_line_int + fst_back_ext + fst_back_int) != 1:
                    print("**************************** fst errore:")
                    print(fst_line_ext + fst_line_int + fst_back_ext + fst_back_int)
                    print(fst_line_ext, fst_line_int, fst_back_ext, fst_back_int)
                    print(instance.main_routes[i])

                #print(fst_line_int, fst_line_ext, fst_back_int, fst_back_ext)

                for j in range(len(routes)):
                    for n in range(1, len(routes[j]) - 1):

                        # labels

                        snd_line_int = (routes[j][n].type == LINEHAUL_TYPE and routes[j][n + 1].type == LINEHAUL_TYPE) \
                                       or (routes[j][n].type == LINEHAUL_TYPE and len(instance.main_routes[j].linehauls) == 1)

                        snd_line_ext = routes[j][n].type == LINEHAUL_TYPE and \
                                       (routes[j][n + 1].type == DEPOT_TYPE or routes[j][n + 1].type == BACKHAUL_TYPE) and \
                                        not snd_line_int

                        snd_back_int = routes[j][n].type == BACKHAUL_TYPE and routes[j][n - 1].type == BACKHAUL_TYPE

                        snd_back_ext = routes[j][n].type == BACKHAUL_TYPE and routes[j][n - 1].type == LINEHAUL_TYPE

                        if (fst_line_ext + fst_line_int + fst_back_ext + fst_back_int) != 1:
                            print("**************************** snd errore:")
                            print(fst_line_ext + fst_line_int + fst_back_ext + fst_back_int)
                            print(fst_line_ext, fst_line_int, fst_back_ext, fst_back_int)

                        #print(snd_line_int, snd_line_ext, snd_back_int, snd_back_ext)

                        # exchange
                        sub = [0,0,0,0]
                        add = [0,0,0,0]
                        #print(i,m,j,n)

                        if i == j: # Sono sulla stessa route
                            if n == m:
                                pass
                            else:
                                if n == m + 1: # i nodi da scambiare sono attaccati
                                    sub[0] = instance.distance_matrix[routes[i][m - 1].id, routes[i][m].id]
                                    sub[1] = instance.distance_matrix[routes[i][n - 1].id, routes[i][n].id]

                                    add[0] = instance.distance_matrix[routes[i][m - 1].id, routes[i][n].id]
                                    add[1] = instance.distance_matrix[routes[i][m].id, routes[i][n + 1].id]

                                if m == n + 1:
                                    sub[0] = instance.distance_matrix[routes[i][n - 1].id, routes[i][n].id]
                                    sub[1] = instance.distance_matrix[routes[i][m].id, routes[i][m + 1].id]

                                    add[0] = instance.distance_matrix[routes[i][n - 1].id, routes[i][m].id]
                                    add[1] = instance.distance_matrix[routes[i][n].id, routes[i][m + 1].id]
                        else:
                            sub[0] = instance.distance_matrix[routes[i][m - 1].id, routes[i][m].id]

                            sub[1] = instance.distance_matrix[routes[i][m].id, routes[i][m + 1].id]

                            sub[2] = instance.distance_matrix[routes[j][n - 1].id, routes[j][n].id]

                            sub[3] = instance.distance_matrix[routes[j][n].id, routes[j][n + 1].id]

                            add[0] = instance.distance_matrix[routes[i][m - 1].id, routes[j][n].id]

                            add[1] = instance.distance_matrix[routes[j][n].id, routes[i][m + 1].id]

                            add[2] = instance.distance_matrix[routes[j][n - 1].id, routes[i][m].id]

                            add[3] = instance.distance_matrix[routes[i][m].id, routes[j][n + 1].id]

                        fo_exchange = fo_prec - sum(sub) + sum(add)
                        #print(m,n)
                        #print(fo_exchange, fo_curr)
                        #print(fo_exchange)

                        if not (i == j and m == n):
                            # LL
                            if (fst_line_int and snd_line_int) or (fst_line_int and snd_line_ext) or (fst_line_ext and snd_line_int) or (fst_line_ext and snd_line_ext):
                                #print(fst_line_int, snd_line_int)
                                capacity_route_i = 0
                                capacity_route_j = 0

                                for node in instance.main_routes[i].linehauls:
                                    capacity_route_i += node.load

                                for node in instance.main_routes[j].linehauls:
                                    capacity_route_j += node.load

                                if (capacity_route_i - routes[exchange_indices[0]][exchange_indices[1]].load + routes[exchange_indices[2]][exchange_indices[3]].load <= instance.vehicle_load) and \
                                    (capacity_route_j - routes[exchange_indices[2]][exchange_indices[3]].load + routes[exchange_indices[0]][exchange_indices[1]].load <= instance.vehicle_load) and \
                                    (fo_exchange < fo_curr):

                                    fo_curr = fo_exchange

                                    exchange_indices[0] = i
                                    exchange_indices[1] = m - 1
                                    exchange_indices[2] = j
                                    exchange_indices[3] = n - 1

                                    print(exchange_indices)

                                    exchange_type = "LL"
                                    #print(exchange_type)

                            # BB
                            if (fst_back_int and snd_back_int) or (fst_back_int and snd_back_ext) or (fst_back_ext and snd_back_int) or (fst_back_ext and snd_back_ext):
                                capacity_route_i = 0
                                capacity_route_j = 0

                                for node in instance.main_routes[i].backhauls:
                                    capacity_route_i += node.load

                                for node in instance.main_routes[j].backhauls:
                                    capacity_route_j += node.load

                                if (capacity_route_i - routes[exchange_indices[0]][exchange_indices[1]].load +
                                    routes[exchange_indices[2]][exchange_indices[3]].load <= instance.vehicle_load) and \
                                        (capacity_route_j - routes[exchange_indices[2]][exchange_indices[3]].load +
                                         routes[exchange_indices[0]][exchange_indices[1]].load <= instance.vehicle_load) and \
                                        (fo_exchange < fo_curr):

                                    fo_curr = fo_exchange
                                    # salviamo gli indici

                                    exchange_indices[0] = i
                                    exchange_indices[1] = m - (len(instance.main_routes[i].linehauls) + 1)
                                    exchange_indices[2] = j
                                    exchange_indices[3] = n - (len(instance.main_routes[j].linehauls) + 1)

                                    exchange_type = "BB"
                                    #print(exchange_type)

                            # L -> B
                            if (fst_line_ext and snd_back_ext and i != j):
                                capacity_route_i = 0
                                capacity_route_j = 0

                                for node in instance.main_routes[i].linehauls:
                                    capacity_route_i += node.load

                                for node in instance.main_routes[j].backhauls:
                                    capacity_route_j += node.load

                                if (capacity_route_i - routes[exchange_indices[0]][exchange_indices[1]].load +
                                    routes[exchange_indices[2]][exchange_indices[3]].load <= instance.vehicle_load) and \
                                        (capacity_route_j - routes[exchange_indices[2]][exchange_indices[3]].load +
                                         routes[exchange_indices[0]][exchange_indices[1]].load <= instance.vehicle_load) and \
                                        (fo_exchange < fo_curr):
                                    fo_curr = fo_exchange
                                    # salviamo gli indici

                                    exchange_indices[0] = i
                                    exchange_indices[1] = m - 1
                                    exchange_indices[2] = j
                                    exchange_indices[3] = n - (len(instance.main_routes[j].linehauls) + 1)

                                    exchange_type = "LB"
                                    #print(exchange_type)

                            # B -> L
                            if (fst_back_ext and snd_line_ext and i != j):
                                capacity_route_i = 0
                                capacity_route_j = 0

                                for node in instance.main_routes[i].backhauls:
                                    capacity_route_i += node.load

                                for node in instance.main_routes[j].linehauls:
                                    capacity_route_j += node.load

                                if (capacity_route_i - routes[exchange_indices[0]][exchange_indices[1]].load +
                                    routes[exchange_indices[2]][exchange_indices[3]].load <= instance.vehicle_load) and \
                                        (capacity_route_j - routes[exchange_indices[2]][exchange_indices[3]].load +
                                         routes[exchange_indices[0]][exchange_indices[1]].load <= instance.vehicle_load) and \
                                        (fo_exchange < fo_curr):

                                    fo_curr = fo_exchange
                                    # salviamo gli indici

                                    exchange_indices[0] = i
                                    exchange_indices[1] = m - (len(instance.main_routes[i].linehauls) + 1)
                                    exchange_indices[2] = j
                                    exchange_indices[3] = n - 1

                                    exchange_type = "BL"
                                    #print(exchange_type)
        print("iter")
        #print(exchange_type)
        #print(exchange_indices)
        #print(fo_prec)
        #print(fo_curr)
        # Updating gain
        gain = (fo_prec - fo_curr) / fo_prec
        #print("gain " + str(gain))

        if exchange_type == "LL":
            print(exchange_type)
            print(instance.main_routes[exchange_indices[0]].linehauls[exchange_indices[1]])
            print(instance.main_routes[exchange_indices[2]].linehauls[exchange_indices[3]])
            supp_node = instance.main_routes[exchange_indices[0]].linehauls[exchange_indices[1]]
            instance.main_routes[exchange_indices[0]].linehauls[exchange_indices[1]] = instance.main_routes[exchange_indices[2]].linehauls[exchange_indices[3]]
            instance.main_routes[exchange_indices[2]].linehauls[exchange_indices[3]] = supp_node

        if exchange_type == "BB":
            print(exchange_type)
            print(instance.main_routes[exchange_indices[0]].backhauls[exchange_indices[1]])
            print(instance.main_routes[exchange_indices[2]].backhauls[exchange_indices[3]])

            supp_node = instance.main_routes[exchange_indices[0]].backhauls[exchange_indices[1]]
            instance.main_routes[exchange_indices[0]].backhauls[exchange_indices[1]] = instance.main_routes[exchange_indices[2]].backhauls[exchange_indices[3]]
            instance.main_routes[exchange_indices[2]].backhauls[exchange_indices[3]] = supp_node

        if exchange_type == "BL":
            print(exchange_type)
            print(instance.main_routes[exchange_indices[0]].backhauls[exchange_indices[1]])
            print(instance.main_routes[exchange_indices[2]].linehauls[exchange_indices[3]])

            # spostamento backhaul
            first_back = instance.main_routes[exchange_indices[0]].backhauls[exchange_indices[1]]
            instance.main_routes[exchange_indices[2]].backhauls = [first_back] + instance.main_routes[exchange_indices[2]].backhauls
            instance.main_routes[exchange_indices[0]].backhauls.remove(first_back)

            # spostamento linehaul
            last_line = instance.main_routes[exchange_indices[2]].linehauls[exchange_indices[3]]
            instance.main_routes[exchange_indices[0]].linehauls.append(last_line)
            instance.main_routes[exchange_indices[2]].linehauls.remove(last_line)

        if exchange_type == "LB":
            print(exchange_type)
            print(instance.main_routes[exchange_indices[0]].linehauls[exchange_indices[1]])
            print(instance.main_routes[exchange_indices[2]].backhauls[exchange_indices[3]])

            # spostamento linehaul
            last_line = instance.main_routes[exchange_indices[0]].linehauls[exchange_indices[1]]
            instance.main_routes[exchange_indices[2]].linehauls.append(last_line)
            instance.main_routes[exchange_indices[0]].linehauls.remove(last_line)

            # spostamento backhaul
            first_back = instance.main_routes[exchange_indices[2]].backhauls[exchange_indices[3]]
            instance.main_routes[exchange_indices[0]].backhauls = [first_back] + instance.main_routes[exchange_indices[0]].backhauls
            instance.main_routes[exchange_indices[2]].backhauls.remove(first_back)


        is_objective_function_improving = gain > threshold
        for route in instance.main_routes:
           print(route)

    print("\n" + str(fo_curr))



    print(objective_function(instance.distance_matrix, instance.main_routes))
    end = time.time() - start
    print("seconds %f" % end)
