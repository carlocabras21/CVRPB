# Import libraries
from utils.file_handler import *

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