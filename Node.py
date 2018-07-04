class Node:

    type = 0 # node type: 0 depot, 1 linehaul, 2 bakchaul
    load = 0 # if node type 0 ......
    x = 0 # coord x
    y = 0 # coord y

    # Constructor
    def __init__(self, type, load, x, y):
        self.type = type
        self.load = load
        self.x = x
        self.y = y

