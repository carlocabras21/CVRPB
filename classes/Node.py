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
        """
           Override of the __init__ method in order to instantiate a new Route Object with new values.

           :param coord_x: a float, represents the x coordinate
           :param coord_y: a float, represents the y coordinate
           :param load: a float, represents the load of the Node
           :param _type: a integer, represents the type of the Node (0 -> Deposit, 1 -> Linehaul, 2-> Backhaul)
           :param _id: a integer, represents the id of the Node
           """
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
        elif self.type == 1:
            return "%d - Linehaul (%d,%d) %d" % (self.id, self.x, self.y, self.load)
        elif self.type == 2:
            return "%d - Backhaul (%d,%d) %d" % (self.id, self.x, self.y, self.load)


    def set_attributes(self, coord_x, coord_y, load, _type, _id):
        """
            This function updates the attributes of a node

            :param coord_x: a float, represents the new x coordinate
            :param coord_y: a float, represents the new y coordinate
            :param load: a float, represents the new load of the Node
            :param _type: a integer, represents the new type of the Node (0 -> Deposit, 1 -> Linehaul, 2-> Backhaul)
            :param _id: a integer, represents the new id of the Node
            """
        self.x = coord_x
        self.y = coord_y
        self.load = load
        self.type = _type
        self.id = _id

