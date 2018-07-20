from scipy.spatial import distance

# Types of the nodes
DEPOT_TYPE = 0
LINEHAUL_TYPE = 1
BACKHAUL_TYPE = 2


def compute_distance(i, j):
    """
        This method computes the Euclidean distance between two nodes (customers) i, j.

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

    # generates a route as a list of nodes, so that the cost is easily computable
    full_route = [route.depot_node] + route.linehauls + route.backhauls + [route.depot_node]

    # route is like: D -> L -> ... -> L -> B -> ... -> B -> D
    for i in range(len(full_route) - 1):
        current_cost += dist_matrix[full_route[i].id, full_route[i + 1].id]

    return current_cost


def objective_function(distance_matrix, routes):
    """
        This method computes the current value of the objective function.

        :param distance_matrix: A numpy bi-dimensional array, the distance matrix
        :param routes: A list of Route objects, the current set of routes
        :return: objf, the objective function's value
        """
    objf = 0

    # computes for each route the cost associated to each adjacent pair of route's nodes
    for route in routes:
        objf += cost(distance_matrix, route)

    return objf


def compute_objf_exchange(distance_matrix, routes, i, m, j, n, objf_prec):
    """
        Computes the objective function after the exchange without actually doing it:
        the exchange is between the first node (m-th of i-th route) and the second
        node (n-th of j-th route). To simulate the exchange, is subtracted the cost
        associated with the previous and the next link of each node (e.g. remove the cost from m-1 to m and the one
        from m to m+1) from the current objective function and we add the costs
        from the previous and the next link of the other node.

        route i: D -> ... ->  (m-1) -> (m) -> (m+1) -> ... -> D
        route j: D -> ... ->  (n-1) -> (n) -> (n+1) -> ... -> D

        1) subtract the (m-1) -> (m), (m) -> (m+1), (n-1) -> (n), (n) -> (n+1) costs
            from the objective function value

        have a situation like this, imagine that m and n are free nodes:

        route i: D -> ... ->  (m-1)    (m)    (m+1) -> ... -> D
        route j: D -> ... ->  (n-1)    (n)    (n+1) -> ... -> D

        2) add the "crossed" costs:
            add the (m-1) -> (n), (n) -> (m+1), (n-1) -> (m), (m) -> (n+1) costs
            to the objective function value

        the value of the objective function like if the nodes are like this
        (look carefully how m and n are switched):

        route i: D -> ... ->  (m-1) -> (n) -> (m+1) -> ... -> D
        route j: D -> ... ->  (n-1) -> (m) -> (n+1) -> ... -> D

        remember: the exchange is "never" happened, because of this formula can
        avoid to recompute all the objective function, where the variation is only
        local in the exchange.

        _____

        This approach is valid only if the routes are different. If the routes are
        the same, this is valid if the nodes to be exchanged are not adjacent.
        If they are adjacent, a different method is used:

        route: D -> ... ->  (m-1) -> (m) -> (n) -> (n+1) -> ... -> D

        1) subtract the  (m-1) -> (m), (n) -> (n+1) costs from the objective function

        switch m and n, they are like this:

        route: D -> ... ->  (m-1) -> (n) -> (m) -> (n+1) -> ... -> D

        2) add the "crossed" costs:
            add the (m-1) -> (n), (m) -> (n+1) costs to the objective function value

        The (m) -> (n) cost is never subtracted and the (n) -> (m) cost is never added
        because they are the same and thus the operations are useless.

        This is valid if n follows m in the route, i.e. n = m + 1.
        Conversely, if m follows m like this:

        route: D -> ... ->  (n-1) -> (n) -> (m) -> (m+1) -> ... -> D

        the operations are the same but with different indices.


        :param distance_matrix: the distance matrix of the instance
        :param routes: the routes as list of list of nodes
        :param i: first route index
        :param m: node index in the first route
        :param j: second route index
        :param n: node index in the second route
        :param objf_prec: the value of the objective function before the exchange
        :return: the value of the objective function after the exchange
        """

    # lists of values to be subtracted:
    # e.g. for general case, when the routes are different
    # sub[0] = cost of: (m-1) ->  (m)
    # sub[1] = cost of: (m)   -> (m+1)
    # sub[2] = cost of: (n-1) ->  (n)
    # sub[3] = cost of: (n)   -> (n+1)
    sub = [0, 0, 0, 0]

    # lists of values to be added:
    # e.g. for general case, when the routes are different
    # add[0] = cost of: (m-1) ->  (n)
    # add[1] = cost of: (n)   -> (m+1)
    # add[2] = cost of: (n-1) ->  (m)
    # add[3] = cost of: (m)   -> (n+1)
    add = [0, 0, 0, 0]

    if i == j:
        # the routes are the same
        if n == m:
            # they are the same node, do nothing
            pass
        else:
            if n == m + 1:
                # n follows m in the same route
                sub[0] = distance_matrix[routes[i][m - 1].id, routes[i][m].id]
                sub[1] = distance_matrix[routes[i][n].id, routes[i][n + 1].id]

                add[0] = distance_matrix[routes[i][m - 1].id, routes[i][n].id]
                add[1] = distance_matrix[routes[i][m].id, routes[i][n + 1].id]

            if m == n + 1:  # m follows n in the same route
                sub[0] = distance_matrix[routes[i][n - 1].id, routes[i][n].id]
                sub[1] = distance_matrix[routes[i][m].id, routes[i][m + 1].id]

                add[0] = distance_matrix[routes[i][n - 1].id, routes[i][m].id]
                add[1] = distance_matrix[routes[i][n].id, routes[i][m + 1].id]
    else:
        # the routes are different
        sub[0] = distance_matrix[routes[i][m - 1].id, routes[i][m].id]

        sub[1] = distance_matrix[routes[i][m].id, routes[i][m + 1].id]

        sub[2] = distance_matrix[routes[j][n - 1].id, routes[j][n].id]

        sub[3] = distance_matrix[routes[j][n].id, routes[j][n + 1].id]

        add[0] = distance_matrix[routes[i][m - 1].id, routes[j][n].id]

        add[1] = distance_matrix[routes[j][n].id, routes[i][m + 1].id]

        add[2] = distance_matrix[routes[j][n - 1].id, routes[i][m].id]

        add[3] = distance_matrix[routes[i][m].id, routes[j][n + 1].id]

    # Simulates the exchange
    return objf_prec - sum(sub) + sum(add)


def best_exchange(main_routes, exchange_indices, exchange_type):
    """
        Computes the exchange between the nodes with coordinates stored in exchange_indices:
        exchange_indices[0] = first route index
        exchange_indices[1] = node index of first route
        exchange_indices[2] = second route index
        exchange_indices[3] = node index of second route
    
        in exchange_type we have the different combinations of exchange:
        "LL": exchange between two linehaul nodes, just do a normal switch
        "BB": exchange between two backhaul nodes, just do a normal switch
        "BL": exchange between the first backhaul of first route and the
              last linehaul of the second route, like this:
    
            before:
            route 1: D -> L -> ... -> L  -> B* -> B -> ... -> B -> D
            route 2: D -> L -> ... -> L* -> B  -> B -> ... -> B -> D
    
            after:
            route 1: D -> L -> ... -> L -> L* -> B -> ... -> B -> D
            route 2: D -> L -> ... -> L -> B* -> B -> ... -> B -> D
    
            (where the star indicates the node to be exchanged)
    
            The steps are:
                - remove the backhaul from the first route and add it in
                    the head of backhauls of the second route
                - remove the linehaul from the second route and add it in
                    the tail of linehauls of the second route
    
        "LB": exchange between the last linehaul of first route and the
                first backhaul of the second route, like this:
    
        before:
        route 1: D -> L -> ... L* -> B  -> B -> ... -> B -> D
        route 2: D -> L -> ... L  -> B* -> B -> ... -> B -> D
    
        after:
        route 1: D -> L -> ... L -> B* -> B -> ... -> B -> D
        route 2: D -> L -> ... L -> L* -> B -> ... -> B -> D
    
        (where the star indicates the node to be exchanged)
    
        The steps are the same as before but with routes switched
    
        :param main_routes: the list of routes, i.e. a list of list of nodes
        :param exchange_indices: the list of indices from which we take routes and nodes
        :param exchange_type: the type of the exchange
        :return:
        """
    
    idx_route1 = exchange_indices[0]
    idx_node1 = exchange_indices[1]
    idx_route2 = exchange_indices[2]
    idx_node2 = exchange_indices[3]
    
    if exchange_type == "LL":
        # just a simple switch with a support variable
        supp_node = main_routes[idx_route1].linehauls[idx_node1]

        main_routes[idx_route1].linehauls[idx_node1] = \
            main_routes[idx_route2].linehauls[idx_node2]

        main_routes[idx_route2].linehauls[idx_node2] = supp_node

    elif exchange_type == "BB":
        # just a simple switch with a support variable
        supp_node = main_routes[idx_route1].backhauls[idx_node1]

        main_routes[idx_route1].backhauls[idx_node1] = \
            main_routes[idx_route2].backhauls[idx_node2]

        main_routes[idx_route2].backhauls[idx_node2] = supp_node

    elif exchange_type == "BL":
        # backhaul moving
        first_back = main_routes[idx_route1].backhauls[idx_node1]

        main_routes[idx_route2].backhauls = \
            [first_back] + main_routes[idx_route2].backhauls

        main_routes[idx_route1].backhauls.remove(first_back)

        # linehaul moving
        last_line = main_routes[idx_route2].linehauls[idx_node2]

        main_routes[idx_route1].linehauls.append(last_line)

        main_routes[idx_route2].linehauls.remove(last_line)

    elif exchange_type == "LB":
        # linehaul moving
        last_line = main_routes[idx_route1].linehauls[idx_node1]

        main_routes[idx_route2].linehauls.append(last_line)

        main_routes[idx_route1].linehauls.remove(last_line)

        # backhaul moving
        first_back = main_routes[idx_route2].backhauls[idx_node2]

        main_routes[idx_route1].backhauls = \
            [first_back] + main_routes[idx_route1].backhauls

        main_routes[idx_route2].backhauls.remove(first_back)


def minimize_fo(instance):
    """
        This function minimizes the objective function's value by implementing the Bext Exchange approach.

        main cycle:
            For each node in each route, this method checks if after exchanging it with another
            nodes the objective function improves. If so, it saves the coordinates of the exchange
            (i.e. indices of routes and nodes in the routes) and updates the value of the objective
            function if it's less than the previous minimum.
            Each exchange must respect all the model constraints.
            After executing all possible comparisons for possible exchanges, best exchange for
            that node is done and is repeated for all the others.

        Repeat this "main cycle" while the objective function is improving, that is its
        value is descending.

        Briefly:
        while the objective function is improving:
            for each node in each route:
                best exchange

        So, an exchange is possible if it respects the capacity constraint and:
        1) the first node is a linehaul and the second node is a linehaul
        2) the first node is a backhaul and the second node is a backhaul
        3) the first node is the last linehaul of the first route and
            the second node is the first backhaul of the second route,
            so that the linehaul moves to the second route and
            the backhaul moves to the first route.
            This is possibile only if the first route has more than one
            linehaul, otherwise if the exchange happens, the first route
            will have no linehauls, thus violating the constraint.
        4) the first node is the first backhaul of the first route and
            the second node is the last linehaul of the second route.
            This is possibile only if the second route has more than one
            linehaul, otherwise if the exchange happens, the second route
            will have no linehauls, thus violating the constraint.

        (in this way the precedence constraint L -> B is respected)

        For a detailed explanation of these exchanges, see the
        "best_exchange" function.

        :param instance: An Instance object, the CVRPB instance
        :return: nothing
        """

    objf_curr = objective_function(instance.distance_matrix, instance.curr_routes)

    is_objective_function_improving = True

    # Finding the bext exchange for each route's node

    while is_objective_function_improving:

        # gets a copy of the routes ( D L -- L B -- B D)
        # in the format of list of list of nodes
        routes = instance.get_unified_routes()

        # updates the objective function to be "beaten up"
        objf_ext = objf_curr

        # BEST EXCHANGE
        # For each route
        for i in range(len(routes)):
            for m in range(1, len(routes[i]) - 1):
                # indices big enough to make sure that if they aren't correctly setted
                # and we use them, we get an error
                exchange_indices = [9999999999, 9999999999, 9999999999, 9999999999]
                exchange_type = "null"

                # gets a copy of the routes ( D L -- L B -- B D)
                # in the format of list of list of nodes
                routes = instance.get_unified_routes()

                # updates the objective function to be "beaten up"
                objf_prec = objf_curr

                # first node type
                type_node_m = routes[i][m].type

                if routes[i][m].type == BACKHAUL_TYPE and routes[i][m - 1].type == DEPOT_TYPE:
                    print("WRONG ROUTE:")
                    print(str(instance.curr_routes[i]))
                    exit(2)

                # For each route
                for j in range(len(routes)):
                    for n in range(1, len(routes[j]) - 1):

                        # second node type
                        type_node_n = routes[j][n].type

                        # calculation of the possible objective function deriving from the exchange
                        objf_exchange = compute_objf_exchange(instance.distance_matrix, routes, i, m, j, n, objf_prec)

                        if objf_exchange < objf_curr:
                            # the new objective function is better than the one before
                            if not (i == j and m == n):
                                # they are different nodes

                                # L <-> L exchange
                                if type_node_m == LINEHAUL_TYPE and type_node_n == LINEHAUL_TYPE:
                                    # capacity constraint
                                    if (instance.curr_routes[i].linehauls_load() -
                                         routes[i][m].load + routes[j][n].load <= instance.vehicle_load) and \
                                        (instance.curr_routes[j].linehauls_load() -
                                         routes[j][n].load + routes[i][m].load <= instance.vehicle_load):

                                        # saves the current best objective functions
                                        objf_curr = objf_exchange

                                        # saves the current indices of best exchange
                                        exchange_indices = [i, m - 1, j, n - 1]

                                        # saves the exchange type
                                        exchange_type = "LL"

                                # B <-> B exchange
                                elif type_node_m == BACKHAUL_TYPE and type_node_n == BACKHAUL_TYPE:

                                    # capacity constraint
                                    if (instance.curr_routes[i].backhauls_load() -
                                         routes[i][m].load + routes[j][n].load <= instance.vehicle_load) and \
                                        (instance.curr_routes[j].backhauls_load() -
                                         routes[j][n].load + routes[i][m].load <= instance.vehicle_load):

                                        # saves the current best objective functions
                                        objf_curr = objf_exchange

                                        # saves the current indices of best exchange
                                        exchange_indices = [i, m - (len(instance.curr_routes[i].linehauls) + 1),
                                                            j, n - (len(instance.curr_routes[j].linehauls) + 1)]

                                        # saves the exchange type
                                        exchange_type = "BB"

                                # L <-> B exchange
                                elif type_node_m == LINEHAUL_TYPE and type_node_n == BACKHAUL_TYPE:

                                    # check if the linehauls list of the first route has at least two
                                    # elements and if the linehaul node is followed by a backhaul or
                                    # by a depot and if the backhaul node is preceded by a linehaul;
                                    # also they must be in different routes
                                    if i != j and len(instance.curr_routes[i].linehauls) >= 2 and \
                                            (routes[i][m + 1].type == BACKHAUL_TYPE or
                                             routes[i][m + 1].type == DEPOT_TYPE) and \
                                            (routes[j][n - 1].type == LINEHAUL_TYPE):

                                        # capacity constraint
                                        if (instance.curr_routes[j].linehauls_load() +
                                             routes[i][m].load <= instance.vehicle_load) and \
                                            (instance.curr_routes[i].backhauls_load() +
                                             routes[j][n].load <= instance.vehicle_load):

                                            # saves the current best objective functions
                                            objf_curr = objf_exchange

                                            # saves the current indices of best exchange
                                            exchange_indices = [i, m - 1, j, n - (len(instance.curr_routes[j].linehauls) + 1)]

                                            # saves the exchange type
                                            exchange_type = "LB"

                                # B <-> L exchange
                                elif type_node_m == BACKHAUL_TYPE and type_node_n == LINEHAUL_TYPE:

                                    # check if the linehauls list of the second route has at least two
                                    # elements and if the linehaul node is followed by a backhaul or
                                    # by a depot and if the backhaul node is preceded by a linehaul;
                                    # also they must be in different routes
                                    if i != j and len(instance.curr_routes[j].linehauls) >= 2 and \
                                            (routes[j][n + 1].type == BACKHAUL_TYPE or
                                             routes[j][n + 1].type == DEPOT_TYPE) and \
                                            (routes[i][m - 1].type == LINEHAUL_TYPE):

                                        # capacity constraint
                                        if (instance.curr_routes[j].backhauls_load() +
                                             routes[i][m].load <= instance.vehicle_load) and \
                                            (instance.curr_routes[i].linehauls_load() +
                                             routes[j][n].load <= instance.vehicle_load):

                                            # saves the current best objective functions
                                            objf_curr = objf_exchange

                                            # saves the current indices of best exchange
                                            exchange_indices = [i, m - (len(instance.curr_routes[i].linehauls) + 1), j, n - 1]

                                            # saves the exchange type
                                            exchange_type = "BL"

                # Do the best exchange
                best_exchange(instance.curr_routes, exchange_indices, exchange_type)

                # check if all the constraints hold
                instance.check_constraints()

        # Compute gain
        gain = objf_ext - objf_curr

        # Check gain
        is_objective_function_improving = gain > 0
