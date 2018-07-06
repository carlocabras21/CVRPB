# Import libraries
from utils.file_handler import *
from utils.utils import cost
from utils.utils import objective_function

# Main
if __name__ == "__main__":

    # Loading instance
    instance = read_instance("A1")

    # Print data
    #instance.showData()

    # Create distance matrix
    instance.compute_distance_matrix()

    #instance.showData()
    #instance.print_distance_matrix()

    # Create main route
    instance.create_main_routes()

    # Calcolo funzione obiettivo
    main_fo = objective_function(instance.distance_matrix, instance.main_routes)
    #print(main_fo)

    # Dobbiamo minimizzarla -> best exchange
