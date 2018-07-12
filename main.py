from utils.file_handler import *
from utils.utils import *
from copy import deepcopy

# Main module
if __name__ == "__main__":

    # Loading instance
    file_name = "A1.txt"
    print("instance: " + file_name)
    instance = load_instance(file_name)

    # Printing data
    # instance.showData()

    # Creating distance matrix
    instance.compute_distance_matrix()

    # instance.showData()
    # instance.print_distance_matrix()

    # Creating main routes
    instance.create_main_routes()

    optimal_cost = load_solution(file_name)
    
    # Dopo che ho una soluzione iniziale deterministica (main routes) devo effettuare degli scambi e/o permutazioni random
    # per esplorare lo spazio delle soluzioni dove applicare local search

    # parto dalle main routes!!! Le copio proprio, non faccio un riferimento
    #instance.current_routes = deepcopy(instance.main_routes)
    print("Mains")
    instance.print_main_routes()

    min_fo = objective_function(instance.distance_matrix, instance.main_routes)
    print("fo di partenza : %f" % min_fo)
    '''
    # Minimizing objective function with best exchange approach
    minimize_fo(instance)

    final_fo = objective_function(instance.distance_matrix, instance.main_routes)

    print("Final fo;) %f " % final_fo)

    gap = ((final_fo - optimal_cost) / optimal_cost) * 100
    print("\n GAP: %.2f " % gap + str("%"))

'''
    best_routes = deepcopy(instance.main_routes)

    mains = deepcopy(instance.main_routes)

    for i in range(1):

        #print("i %d" % i)

        #instance.main_routes = mains

        # Qua modifico curr routes che inizialmente e' formato dalle main routes
        instance.mix_routes_random()
        #print("\nroutes dopo scambi:")
        instance.print_main_routes()

        #instance.print_main_routes()

        # Minimizing objective function with best exchange approach
        minimize_fo(instance)

        final_fo = objective_function(instance.distance_matrix, instance.main_routes)

        print(final_fo)

        if final_fo < min_fo:
            min_fo = final_fo
            best_routes = deepcopy(instance.main_routes)
    
    print("min;) %f " % min_fo)

    print("\nLast.")
    instance.print_main_routes()

    gap = ((min_fo - optimal_cost) / optimal_cost) * 100
    print("\n GAP: %.2f " % gap + str("%"))
