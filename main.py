import re

from utils.file_handler import *
from utils.utils import *
from os import listdir
import time

# Main module
if __name__ == "__main__":
    #file_name = "A1.txt"
    file_name = "all"

    # se file_name e' "all", allora opera su tutte le istanze
    if file_name == "all":
        instance_names = [f for f in listdir("data/Instances/")]
        instance_names.remove("info.txt")
        instance_names.sort()
        #instance_names = instance_names[:]
        #print(instance_names)

    # altrimenti opera solo su quella istanza
    else:
        instance_names = [file_name]

    gaps = []
    times = []

    for instance_name in instance_names:

        iter = 0

        start = time.time()

        # Loading instance
        print("instance: " + instance_name)
        instance = load_instance(instance_name)

        n_iter = 0

        if instance_name.startswith(('A', 'B')):
            n_iter = instance.n_customers * 20
        elif instance_name.startswith(('C', 'D', 'E')):
            n_iter = instance.n_customers * 15
        elif instance_name.startswith(('F', 'G', 'H')):
            n_iter = instance.n_customers * 10
        elif instance_name.startswith(('I', 'J')):
            n_iter = instance.n_customers * 8
        elif instance_name.startswith(('K', 'L', 'M', 'N')):
            n_iter = instance.n_customers * 5

        # Printing data
        # instance.showData()

        # Creating distance matrix
        instance.compute_distance_matrix()

        # Creating main routes
        instance.create_main_routes()

        end_cp = time.time() - start

        print("\nConstruction phase time: %.2f" % end_cp)

        optimal_cost = load_solution(instance_name)

        # Dopo che ho una soluzione iniziale deterministica (main routes) devo effettuare degli scambi e/o permutazioni random
        # per esplorare lo spazio delle soluzioni dove applicare local search

        # parto dalle main routes!!! Le copio proprio, non faccio un riferimento
        # instance.current_routes = deepcopy(instance.main_routes)
        # print("Mains")
        # instance.print_main_routes()

        min_fo = objective_function(instance.distance_matrix, instance.main_routes)
        #print("fo di partenza : %f" % min_fo)
        init_fo = min_fo

        best_routes = instance.main_routes

        start = time.time()

        while iter <= n_iter:
            #print(iter)
            # Qua modifico curr routes che inizialmente e' formato dalle main routes
            instance.mix_routes_random()

            #instance.print_main_routes()

            # Minimizing objective function with best exchange approach
            minimize_fo(instance)

            final_fo = objective_function(instance.distance_matrix, instance.main_routes)

            if final_fo < min_fo:
                min_fo = final_fo
                best_routes = instance.main_routes

            iter += 1

        end_ls = time.time() - start

        print("\nLocal search time: %.2f" % end_ls)

        print("\nTotal time: %.2f" % (end_cp + end_ls))

        create_instance_solution(instance, instance_name[0:2], init_fo, min_fo, optimal_cost, end_cp, end_ls)

        gap = ((min_fo - optimal_cost) / optimal_cost) * 100
        print("**** GAP: %.2f " % gap + str("% ****\n"))
        gaps.append(gap)

        times.append((end_cp + end_ls))
        instance.print_main_routes()

    print("\nGAPS:")
    print(gaps)
    print("\nGAP Medio: " + str(sum(gaps) / len(gaps)))

    print("\nTEMPI:")
    print(times)
    print("\nTempo medio: " + str(sum(times) / len(times)))
