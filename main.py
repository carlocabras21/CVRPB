import time

from os import listdir
from utils.file_handler import load_instance, load_lower_bound, create_instance_solution
from utils.utils import objective_function, minimize_fo

# Main
if __name__ == "__main__":
    file_name = "B1.txt"
    # file_name = "all"

    # check
    if file_name == "all":
        # computes all instances
        instance_names = [f for f in listdir("data/Instances/")]
        instance_names.remove("info.txt")
        instance_names.sort()  # from A to N
    else:
        # computes only one specific instance
        instance_names = [file_name]

    gaps = []
    times = []

    for instance_name in instance_names:

        n_iterations = 0  # number of Best Exchange iterations
        start = time.time()

        # loades the instance
        print("\nLoading Instance")
        instance = load_instance(instance_name)
        print(instance)

        # number of iterations based on instance name (i.e. based on number of customers)
        if instance_name.startswith(('A', 'B')):
            n_iterations = instance.n_customers * 20
        elif instance_name.startswith(('C', 'D', 'E')):
            n_iterations = instance.n_customers * 15
        elif instance_name.startswith(('F', 'G', 'H')):
            n_iterations = instance.n_customers * 10
        elif instance_name.startswith(('I', 'J')):
            n_iterations = instance.n_customers * 8
        elif instance_name.startswith(('K', 'L', 'M', 'N')):
            n_iterations = instance.n_customers * 5

        # Creates the distance matrix
        instance.compute_distance_matrix()

        # Creates the main routes
        print("\nCreating Main Routes")
        instance.create_main_routes()

        end_cp = time.time() - start

        # Loades the instance lower bound
        lower_bound = load_lower_bound(instance_name)

        # Computes the initial objective function
        init_objf = objective_function(instance.distance_matrix, instance.curr_routes)

        # Sets the current minimum objective function
        min_objf = init_objf

        # Sets the current best routes
        best_routes = instance.curr_routes

        start = time.time()

        print("\nComputing Best Exchange")

        for it in range(n_iterations):
            # Mixes the routes
            instance.mix_routes_random()

            # Minimizes objective function with best exchange approach
            minimize_fo(instance)

            # Computes the objective function of mixed routes
            mix_objf = objective_function(instance.distance_matrix, instance.curr_routes)

            # checks if it is improving
            if mix_objf < min_objf:
                min_objf = mix_objf
                best_routes = instance.curr_routes

        end_ls = time.time() - start

        gap = ((min_objf - lower_bound) / lower_bound) * 100

        print("\nGAP %.2f" % gap + "%")

        print("Total time %.2f" % (end_ls + end_cp) + "s")

        print("\nGenerating Output File")

        # Generates the output file
        create_instance_solution(instance, instance_name[0:2], min_objf, lower_bound, (gap / 100), end_cp, end_ls)
