from Node import Node

class Route(object):

    depot_node = Node()
    linehauls = []
    backhauls = []

    def __init__(self):
        pass

    def __str__(self):

        final_str = ""
        final_str += " D" + str(self.depot_node.id)

        for l in self.linehauls:
            final_str += " L" + str(l.id)

        for b in self.backhauls:
            final_str += " B" + str(b.id)

        final_str += " D" + str(self.depot_node.id)

        return final_str
