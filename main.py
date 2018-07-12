from utils.file_handler import *
from utils.utils import *

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


    # Dopo che ho una soluzione iniziale deterministica (main routes) devo effettuare degli scambi e/o permutazioni random
    # per esplorare lo spazio delle soluzioni dove applicare local search

    # supponiamo di fare 50 permutazioni
    for i in range(1):

        # Qua modifico curr routes che inizialmente e' formato dalle main routes
        instance.mix_routes_random()

        instance.print_main_routes()
        instance.print_curr_routes()


        '''
        # Computing objective function
        main_fo = objective_function(instance.distance_matrix, instance.main_routes)
        print("Main fo: " + str(main_fo))

        # Minimizing objective function with best exchange approach
        minimize_fo(instance)

        print("Final Routes")
        for route in instance.main_routes:
            print(route)

        final_fo = objective_function(instance.distance_matrix, instance.main_routes)
        print("\nFinal fo: " + str(final_fo))

        improvement = (main_fo - final_fo) / main_fo * 100
        print("improvement " + str(improvement)[:4] + "%")
        '''
