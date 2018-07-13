from utils.file_handler import *
from utils.utils import *
from os import listdir
from copy import deepcopy
from copy import deepcopy

# Main module
if __name__ == "__main__":
    #file_name = "B1.txt"
    file_name = "all"

    # se file_name e' "all", allora opera su tutte le istanze
    if file_name == "all":
        instance_names = [f for f in listdir("data/Instances/")]
        instance_names.remove("info.txt")
        instance_names.sort()
        # instance_names = instance_names[:15] # fino a D4
        print(instance_names)

    # altrimenti opera solo su quella istanza
    else:
        instance_names = [file_name]

    gaps = []

    for instance_name in instance_names:
        # Loading instance
        print("instance: " + instance_name)
        instance = load_instance(instance_name)

        # Printing data
        # instance.showData()

        # Creating distance matrix
        instance.compute_distance_matrix()

        # instance.showData()
        # instance.print_distance_matrix()

        # Creating main routes
        instance.create_main_routes()

        optimal_cost = load_solution(instance_name)

        # Dopo che ho una soluzione iniziale deterministica (main routes) devo effettuare degli scambi e/o permutazioni random
        # per esplorare lo spazio delle soluzioni dove applicare local search

        # parto dalle main routes!!! Le copio proprio, non faccio un riferimento
        # instance.current_routes = deepcopy(instance.main_routes)
        # print("Mains")
        # instance.print_main_routes()

        min_fo = objective_function(instance.distance_matrix, instance.main_routes)
        print("fo di partenza : %f" % min_fo)
        init_fo = min_fo

        best_routes = deepcopy(instance.main_routes)

        mains = deepcopy(instance.main_routes)

        for i in range(50):

            # print("i %d" % i)

            # instance.main_routes = mains

            # Qua modifico curr routes che inizialmente e' formato dalle main routes
            instance.mix_routes_random()
            # print("\nroutes dopo scambi:")
            # instance.print_main_routes()

            # instance.print_main_routes()

            # Minimizing objective function with best exchange approach
            minimize_fo(instance)

            final_fo = objective_function(instance.distance_matrix, instance.main_routes)

            # print(final_fo)

            if final_fo < min_fo:
                min_fo = final_fo
                best_routes = deepcopy(instance.main_routes)

        print("min_fo %f " % min_fo)

        print("\nLast.")
        instance.print_main_routes()

        gain = (init_fo - min_fo) / init_fo * 100
        print("Gain: %.2f " % gain + str("%\n"))

        gap = ((min_fo - optimal_cost) / optimal_cost) * 100
        print("**** GAP: %.2f " % gap + str("% ****\n"))

        gaps.append(gap)

    print "gaps:"
    print gaps
    print "\ngap medio: " + str(sum(gaps)/len(gaps))
