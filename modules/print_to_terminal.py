from prettytable import PrettyTable
from modules import rp_container_handling

def print_to_terminal(router_name, rp_container):
    """Prints required information to the terminal.
    A number of passed tests is marked in green; not passed - red.
    :router_name: name of the router
    :rp_container: a list of RegisterParameters objects
    """
    CRED = '\033[91m'
    CEND = '\033[0m'
    CGREEN = '\033[92m'

    print_data_to_table(rp_container)
    print("Device name: " + router_name)
    print("Passed tests: " + CGREEN + str(rp_container_handling.count_passed_tests(rp_container)) + CEND)
    print("Not passed tests: " + CRED + str(rp_container_handling.count_not_passed_tests(rp_container)) + CEND)
    print("Num of configurations: " + str(len(rp_container)))

def print_data_to_table(rp_container):
    """Prints a list of RegisterParameters to table.
    :rp_container: a list of RegisterParameters objects
    """
    t = PrettyTable(['name', 'reg_addr', 'reg_num', 'type', 'decoded value', 'expected value', 'passed'])

    if len(rp_container) == 0:
        raise Exception("modules/print_to_terminal.py., print_data_to_table(): rp_container is empty.")

    for p in rp_container:
        t.add_row([p.required_value,
                   p.reg_addr - 1, 
                   p.reg_num, 
                   p.representation, 
                   p.decoded_registers_value, 
                   p.expected_decoded_result, 
                   p.passed_the_test])
    t.align['name'] = 'l'
    t.align['type'] = 'l'
    t.align['passed'] = 'l'
    print(t)