from Node import Node


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

    def __init__(self):
        self.depot_node = Node()
        self.linehaul = []
        self.backhauls = []

    def __str__(self):
        """
        Override of the __str__ method in order to get a more meaningful representation of the Route Object.

        :return: a string representing the Route object D -> L -> ... -> L [-> B -> ... -> B] -> D.
        """

        final_str = ""
        final_str += " D" + str(self.depot_node.id)

        for l in self.linehauls:
            final_str += " L" + str(l.id) #+ " (" + str(l.load) + ") "

        for b in self.backhauls:
            final_str += " B" + str(b.id) #+ " (" + str(b.load) + ") "



        final_str += " D" + str(self.depot_node.id)

        final_str += " ----- LoadL " + str(self.linehauls_load())
        final_str += " ----- LoadB " + str(self.backhauls_load())
        final_str += " ----- LoadT " + str(self.total_load())

        return final_str


    def linehauls_load(self):
        load = 0
        for node in self.linehauls:
            load += node.load
        return load

    def backhauls_load(self):
        load = 0
        for node in self.backhauls:
            load += node.load
        return load

    def total_load(self):
        return self.linehauls_load() + self.backhauls_load()