class Node(object):

    type = 0 # node type: 0 depot, 1 linehaul, 2 bakchaul
    load = 0 # if node type 0 ......
    x = 0 # coord x
    y = 0 # coord y

    id = 0

    def __init__(self):
        pass

    def __str__(self):
        if self.type == 0:
            return "%d - Depot (%d,%d)" % (self.id,self.x, self.y)
        if self.type == 1:
            return "%d - Linehaul (%d,%d) %d" % (self.id, self.x, self.y, self.load)
        if self.type == 2:
            return "%d - Backhaul (%d,%d) %d" % (self.id, self.x, self.y, self.load)

        return "Default"