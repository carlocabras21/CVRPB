from utils.file_handler import *
from utils.utils import *

# Main module
if __name__ == "__main__":

    # Loading instance
    instance = read_instance("A1")

    # Printing data
    # instance.showData()

    # Creating distance matrix
    instance.compute_distance_matrix()

    # instance.showData()
    # instance.print_distance_matrix()

    # Creating main routes
    instance.create_main_routes()

    # Computing objective function
    main_fo = objective_function(instance.distance_matrix, instance.main_routes)
    # print(main_fo)

    # Minimizing objective function with best exchange approach
    minimize_fo(instance)
