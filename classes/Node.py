class Node(object):
    """
    This class represents a Node in the VRP context (Depot or true customer).

    :param id: An int, the node's unique identifier
    :param type: An int, the node type; 0 for Depot, 1 for Linehaul, 2 for Backhaul
    :param load: An int, the quantity of good to be picked up or delivered.
    :param x: A float, the x coordinate
    :param y: A float, the y coordinate
    """
    id = 0
    type = 0
    load = 0
    x = 0
    y = 0

    def __init__(self):
        pass

    def __str__(self):
        """
        Override of the __str__ method in order to get a more meaningful representation of the Node Object.

        :return: A string representing the Node object based on the type.
        """
        if self.type == 0:
            return "%d - Depot (%d,%d)" % (self.id, self.x, self.y)
        if self.type == 1:
            return "%d - Linehaul (%d,%d) %d" % (self.id, self.x, self.y, self.load)
        if self.type == 2:
            return "%d - Backhaul (%d,%d) %d" % (self.id, self.x, self.y, self.load)

        return "Default"
