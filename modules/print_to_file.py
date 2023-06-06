import csv
from datetime import datetime

def print_to_csv(router_name, rp_container):
    """Prints registers' data to csv file: router_name, reg_addr,
    representation, expected value, decoded value, passed_the_test.
    :router_name: name of the router
    :rp_container: a list of RegisterParameters objects
    """
    with open(get_file_name(router_name), 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(["Tested device: " + router_name])
        writer.writerow(['Register address',
                         'Representation',
                         'Expected value',
                         'Decoded value',
                         'Passed the test'])
        
        for p in rp_container:
            writer.writerow([p.reg_addr - 1,
                             p.representation,
                             p.expected_decoded_result,
                             p.decoded_registers_value,
                             p.passed_the_test])

def get_file_name(router_name):
    """Composes a csv file name in a form: router_date_time.csv
    :router_name: name of the router
    :return: file name 
    """
    if len(router_name) < 5:
        raise("Router name indicated inproperly.")
    
    return "results/" + router_name + datetime.now().strftime("_%Y-%m-%d_%H.%M.%S") + ".csv"