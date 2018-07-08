class Node(object):
    """
    This class represents a Node in the VRP context (Depot or true customer).

    :param x: A float, the x coordinate
    :param y: A float, the y coordinate
    :param load: An int, the quantity of good to be picked up or delivered.
    :param type: An int, the node type; 0 for Depot, 1 for Linehaul, 2 for Backhaul
    :param id: An int, the node's unique identifier
    """
    x = 0
    y = 0
    load = 0
    type = 0
    id = 0

    def __init__(self, coord_x=0, coord_y=0, load=0, _type=0, _id=0):
        self.x = coord_x
        self.y = coord_y

        self.load = load
        self.type = _type
        self.id = _id

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

    def set_attributes(self, coord_x, coord_y, load, _type, _id):
        """
            This function updates the parameters of a node

            :param coord_x: Integer x coordinate
            :param coord_y: Integer y coordinate
            :param load: Node load (delivery / pickup)
            :param _type: Node type (0: depot, 1: linehaul, 2:backhaul
            :param _id: Integer id
            :return: Node instance
        """

        self.x = coord_x
        self.y = coord_y

        self.load = load
        self.type = _type
        self.id = _id

