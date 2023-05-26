import main
import csv
from prettytable import PrettyTable
from datetime import datetime
import rp_container

def print_to_csv():
    """Prints registers' data to csv file: router_name, reg_addr,
    representation, expected value, decoded value, passed_the_test.
    """
    with open(get_file_name(), 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(["Tested device: " + main.router_name])
        writer.writerow(['Register address',
                         'Representation',
                         'Expected value',
                         'Decoded value',
                         'Passed the test'])
        
        for p in rp_container.register_parameters:
            writer.writerow([p.reg_addr - 1,
                             p.representation,
                             p.expected_decoded_result,
                             p.decoded_registers_value,
                             p.passed_the_test])

def get_file_name():
    """Composes a csv file name in a form: router_date_time.csv
    :return: file name 
    """
    return main.router_name + datetime.now().strftime("_%Y-%m-%d_%H:%M:%S") + ".csv"

def print_to_terminal():
    """Prints required information to the terminal.
    A number of passed tests is marked in green; not passed - red.
    """
    CRED = '\033[91m'
    CEND = '\033[0m'
    CGREEN = '\033[92m'

    print_data_to_table()
    print("Device name: " + main.router_name)
    print("Passed tests: " + CGREEN + str(rp_container.count_passed_tests()) + CEND)
    print("Not passed tests: " + CRED + str(rp_container.count_not_passed_tests()) + CEND)
    print("Num of configurations: " + str(len(rp_container.register_parameters)))

def print_data_to_table():
    """Prints a list of RegisterParameters to table."""
    t = PrettyTable(['name', 'reg_addr', 'reg_num', 'type', 'decoded value', 'expected value', 'passed'])

    for p in rp_container.register_parameters:
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