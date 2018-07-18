from scipy.spatial import distance


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


def compute_fo_exchange(distance_matrix, routes, i, m, j, n, fo_prec):
    sub = [0, 0, 0, 0]
    add = [0, 0, 0, 0]

    if i == j:  # Sono sulla stessa route
        if n == m:
            pass
        else:
            if n == m + 1:  # i nodi da scambiare sono attaccati
                sub[0] = distance_matrix[routes[i][m - 1].id, routes[i][m].id]
                sub[1] = distance_matrix[routes[i][n].id, routes[i][n + 1].id]

                add[0] = distance_matrix[routes[i][m - 1].id, routes[i][n].id]
                add[1] = distance_matrix[routes[i][m].id, routes[i][n + 1].id]

            if m == n + 1:
                sub[0] = distance_matrix[routes[i][n - 1].id, routes[i][n].id]
                sub[1] = distance_matrix[routes[i][m].id, routes[i][m + 1].id]

                add[0] = distance_matrix[routes[i][n - 1].id, routes[i][m].id]
                add[1] = distance_matrix[routes[i][n].id, routes[i][m + 1].id]
    else:
        sub[0] = distance_matrix[routes[i][m - 1].id, routes[i][m].id]

        sub[1] = distance_matrix[routes[i][m].id, routes[i][m + 1].id]

        sub[2] = distance_matrix[routes[j][n - 1].id, routes[j][n].id]

        sub[3] = distance_matrix[routes[j][n].id, routes[j][n + 1].id]

        add[0] = distance_matrix[routes[i][m - 1].id, routes[j][n].id]

        add[1] = distance_matrix[routes[j][n].id, routes[i][m + 1].id]

        add[2] = distance_matrix[routes[j][n - 1].id, routes[i][m].id]

        add[3] = distance_matrix[routes[i][m].id, routes[j][n + 1].id]

    return fo_prec - sum(sub) + sum(add)


def final_exchange(main_routes, exchange_indices, exchange_type):
    if exchange_type == "LL":

        supp_node = main_routes[exchange_indices[0]].linehauls[exchange_indices[1]]

        main_routes[exchange_indices[0]].linehauls[exchange_indices[1]] = \
            main_routes[exchange_indices[2]].linehauls[exchange_indices[3]]

        main_routes[exchange_indices[2]].linehauls[exchange_indices[3]] = supp_node
        # n_exch += 1

    elif exchange_type == "BB":

        supp_node = main_routes[exchange_indices[0]].backhauls[exchange_indices[1]]

        main_routes[exchange_indices[0]].backhauls[exchange_indices[1]] = \
            main_routes[exchange_indices[2]].backhauls[exchange_indices[3]]

        main_routes[exchange_indices[2]].backhauls[exchange_indices[3]] = supp_node
        # n_exch += 1

    elif exchange_type == "BL":

        # spostamento backhaul
        first_back = main_routes[exchange_indices[0]].backhauls[exchange_indices[1]]

        main_routes[exchange_indices[2]].backhauls = \
            [first_back] + main_routes[exchange_indices[2]].backhauls

        main_routes[exchange_indices[0]].backhauls.remove(first_back)

        # spostamento linehaul
        last_line = main_routes[exchange_indices[2]].linehauls[exchange_indices[3]]

        main_routes[exchange_indices[0]].linehauls.append(last_line)

        main_routes[exchange_indices[2]].linehauls.remove(last_line)
        # n_exch += 1

    elif exchange_type == "LB":

        # spostamento linehaul
        last_line = main_routes[exchange_indices[0]].linehauls[exchange_indices[1]]

        main_routes[exchange_indices[2]].linehauls.append(last_line)

        main_routes[exchange_indices[0]].linehauls.remove(last_line)

        # spostamento backhaul
        first_back = main_routes[exchange_indices[2]].backhauls[exchange_indices[3]]

        main_routes[exchange_indices[0]].backhauls = \
            [first_back] + main_routes[exchange_indices[0]].backhauls

        main_routes[exchange_indices[2]].backhauls.remove(first_back)
        # n_exch += 1


def minimize_fo(instance):
    """
    This function minimizes the objective function's value by implementing the Bext Exchange approach.

    :param instance: An Instance object, the CVRPB instance
    :return: nothing
    """

    fo_curr = objective_function(instance.distance_matrix, instance.main_routes)

    is_objective_function_improving = True

    # Finding the bext exchange for each route's node

    # n_exch = 0

    while is_objective_function_improving:

        # Prendo una copia delle route correnti unificate ( D L -- L B -- B D)
        routes = instance.get_unified_routes()

        # Aggiorno la fo "da battere"
        fo_ext = fo_curr

        # BEST EXCHANGE

        for i in range(len(routes)):
            for m in range(1, len(routes[i]) - 1):

                # indici abbastanza grandi da fare in modo che se non sono assegnati diano errore
                exchange_indices = [9999999999,
                                    9999999999,
                                    9999999999,
                                    9999999999]
                exchange_type = "null"

                # Prendo una copia delle route correnti unificate ( D L -- L B -- B D)
                routes = instance.get_unified_routes()

                # Aggiorno la fo "da battere"
                fo_prec = fo_curr

                # Tipo del primo nodo
                type_node_m = routes[i][m].type

                if routes[i][m].type == BACKHAUL_TYPE and routes[i][m - 1].type == DEPOT_TYPE:
                    print("WRONG ROUTE:")
                    print(str(instance.main_routes[i]))
                    exit(2)

                for j in range(len(routes)):
                    for n in range(1, len(routes[j]) - 1):

                        # Tipo secondo nodo
                        type_node_n = routes[j][n].type

                        # EXCHANGE TIME

                        fo_exchange = compute_fo_exchange(instance.distance_matrix, routes, i, m, j, n, fo_prec)

                        if fo_exchange < fo_curr:

                            if not (i == j and m == n):  # se il nodo non e' lo stesso

                                # Controlliamo quale tipo di scambio dev'essere eseguito

                                # L <-> L
                                if type_node_m == LINEHAUL_TYPE and type_node_n == LINEHAUL_TYPE:

                                    # Controllo il vincolo di capacita'
                                    if (instance.main_routes[i].linehauls_load() - routes[i][m].load + routes[j][
                                        n].load <= instance.vehicle_load) and \
                                            (instance.main_routes[j].linehauls_load() - routes[j][n].load + routes[i][
                                                m].load <= instance.vehicle_load):
                                        fo_curr = fo_exchange

                                        exchange_indices = [i, m - 1, j, n - 1]
                                        exchange_type = "LL"

                                # B <-> B
                                elif type_node_m == BACKHAUL_TYPE and type_node_n == BACKHAUL_TYPE:
                                    # Controllo il vincolo di capacita'
                                    if (instance.main_routes[i].backhauls_load() - routes[i][m].load + routes[j][
                                        n].load <= instance.vehicle_load) and \
                                            (instance.main_routes[j].backhauls_load() - routes[j][n].load + routes[i][
                                                m].load <= instance.vehicle_load):
                                        fo_curr = fo_exchange

                                        # salviamo gli indici
                                        exchange_indices = [i, m - (len(instance.main_routes[i].linehauls) + 1),
                                                            j, n - (len(instance.main_routes[j].linehauls) + 1)]
                                        exchange_type = "BB"

                                # L <-> B
                                elif type_node_m == LINEHAUL_TYPE and type_node_n == BACKHAUL_TYPE:
                                    # Controlliamo che la lista della prima rotta (dove c'e' L) abbia almeno 2 L
                                    # e L sia seguito da B o D e B sia preceduto da L, e siano su una diversa rotta
                                    if i != j and len(instance.main_routes[i].linehauls) >= 2 and \
                                            (routes[i][m + 1].type == BACKHAUL_TYPE or routes[i][
                                                    m + 1].type == DEPOT_TYPE) and \
                                            (routes[j][n - 1].type == LINEHAUL_TYPE):

                                        # Verifica vincolo di capacita'
                                        if (instance.main_routes[j].linehauls_load() + routes[i][
                                            m].load <= instance.vehicle_load) and \
                                                (instance.main_routes[i].backhauls_load() + routes[j][
                                                    n].load <= instance.vehicle_load):
                                            fo_curr = fo_exchange

                                            # salviamo gli indici
                                            exchange_indices = [i, m - 1, j,
                                                                n - (len(instance.main_routes[j].linehauls) + 1)]
                                            exchange_type = "LB"

                                # B <-> L
                                elif type_node_m == BACKHAUL_TYPE and type_node_n == LINEHAUL_TYPE:
                                    # Controlliamo che la lista della seconda rotta (dove c'e' L) abbia almeno 2 L
                                    # e L sia seguito da B o D e B sia preceduto da L, e siano su una diversa rotta
                                    if i != j and len(instance.main_routes[j].linehauls) >= 2 and \
                                            (routes[j][n + 1].type == BACKHAUL_TYPE or routes[j][
                                                    n + 1].type == DEPOT_TYPE) and \
                                            (routes[i][m - 1].type == LINEHAUL_TYPE):

                                        # capacita'
                                        if (instance.main_routes[j].backhauls_load() + routes[i][
                                            m].load <= instance.vehicle_load) and \
                                                (instance.main_routes[i].linehauls_load() + routes[j][
                                                    n].load <= instance.vehicle_load):
                                            fo_curr = fo_exchange

                                            # salviamo gli indici
                                            exchange_indices = [i, m - (len(instance.main_routes[i].linehauls) + 1),
                                                                j, n - 1]
                                            exchange_type = "BL"

                final_exchange(instance.main_routes, exchange_indices, exchange_type)

                instance.check_constraints()

                # if int(fo_curr) != int(objective_function(instance.distance_matrix, instance.main_routes)):
                #   print("ERRORE: fo: " + str(objective_function(instance.distance_matrix, instance.main_routes)))

        gain = fo_ext - fo_curr
        is_objective_function_improving = gain > 0
