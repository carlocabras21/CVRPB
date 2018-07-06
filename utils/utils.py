from scipy.spatial import distance
from Route import Route

def compute_distance(i, j):
    return distance.euclidean([i.x, i.y], [j.x, j.y])

# calcola il costo della route
def cost(dist_matrix, route):

    cost = 0
    full_route = [route.depot_node] + route.linehauls + route.backhauls + [route.depot_node]

    # 0 -> L -> ... -> L -> B -> ... -> B -> 0
    for i in range(len(full_route)-1):
        #print(dist_matrix[full_route[i].id, full_route[i+1].id])
        cost += dist_matrix[full_route[i].id, full_route[i+1].id]

    return cost

# metodo che restituisce il valore della funzione obiettivo
def objective_function(distance_matrix, routes):
    fo = 0
    # per ogni route calcolo il costo del collegamento tra due nodi della route
    for route in routes:
        fo += cost(distance_matrix, route)

    return fo

