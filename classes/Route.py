from classes.Node import Node


class Route(object):
    """
        This class represents a Route in the VRP context.

        :param depot_node: A Node object, the depot node
        :param linehauls: A list of Node objects, the linehaul nodes list
        :param backhauls: A list of Node objects, the backhaul nodes list
        """
    depot_node = Node()
    linehauls = []
    backhauls = []

    # Constructor
    def __init__(self, depot_node=Node(), linehauls=None, backhauls=None):
        """
            Override of the __init__ method in order to instantiate a new Route Object with new values.

            :param: depot_node: a Node object, represents the deposit node
            :param linehauls: A list of Node objects, the linehaul nodes list
            :param backhauls: A list of Node objects, the backhaul nodes list
            """
        # To avoid mutable objects
        if backhauls is None:
            backhauls = []

        if linehauls is None:
            linehauls = []

        self.depot_node = depot_node
        self.linehauls = linehauls
        self.backhauls = backhauls

    def __str__(self):
        """
        Override of the __str__ method in order to get a more meaningful representation of the Route Object.

        :return: a string representing the Route object D -> L -> ... -> L [-> B -> ... -> B] -> D.
        """

        # Linking Depot node
        output = " D" + str(self.depot_node.id)

        # Linking linehauls customers
        for l in self.linehauls:
            output += " L" + str(l.id)

        # Linking backhauls customers
        for b in self.backhauls:
            output += " B" + str(b.id)

        # Linking Depot node
        output += " D" + str(self.depot_node.id)

        # Uncomment here to linking loads
        '''
        output += " ----- LoadL " + str(self.linehauls_load())
        output += " ----- LoadB " + str(self.backhauls_load())
        output += " ----- LoadT " + str(self.total_load())
        '''

        return output

    def get_route_solution(self):
        """
        This method returns customers' ids in visit order for writing it in the solution file

        :return: a string, representing the Route object 0 -> L.id ... L.id -> B.id ... B.id -> 0.
        """
        # Linking depot node
        output = str(self.depot_node.id)

        # Linking Linehauls nodes
        for l in self.linehauls:
            output += " " + str(l.id)

        # Linking Backhauls nodes
        for b in self.backhauls:
            output += " " + str(b.id)

        # Linking depot node
        output += " " + str(self.depot_node.id)

        return output

    def linehauls_load(self):
        """
            This method computes the delivery load for the Linehauls of a route

            :return: a float, representing the Linehauls customers delivery load
            """
        delivery_load = 0

        for linehaul in self.linehauls:
            delivery_load += linehaul.load

        return delivery_load

    def backhauls_load(self):
        """
           This method computes the pick-up load for the Backhauls of a route

           :return: a float, representing the Backhauls customers pick-up load
           """
        pickup_load = 0

        for backhaul in self.backhauls:
            pickup_load += backhaul.load

        return pickup_load