# coding=utf-8
from scipy.spatial import distance
from Route import Route
import time

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

# effettua la minimizzazione della fo
def minimize_fo(instance):
    fo_curr = objective_function(instance.distance_matrix, instance.main_routes)
    soglia = 0.01
    gain = soglia+1

    # ricerca il miglior scambio per ogni nodo

    start = time.time()

    while(gain >= soglia):

        fo_prec = fo_curr

        # indice route primo nodo
        for i in range(len(instance.main_routes)):
            # indice nodo i-esima route primo nodo
            for m in range(1,len(instance.main_routes[i].linehauls)):
                # indice route secondo nodo
                for j in range(len(instance.main_routes)):
                    # indice nodo j-esima route secondo nodo
                    for n in range(1,len(instance.main_routes[i].linehauls)):
                        # cerca migliore scambio e salva le coordinate dello scambio (cioè (route-i,nodo1) (route-j,
                        # nodo2))
                        print("")
        # aggiorna il guadagno
        gain = (fo_prec - fo_curr) / fo_prec

    end = time.time() - start
    print("seconds %f" % end)
