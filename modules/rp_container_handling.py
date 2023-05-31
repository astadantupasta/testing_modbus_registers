from register_parameters import RegisterParameters
from modules import ssh_connection_handling

def dict_to_list_of_objects(data, default_hostname="192.168.1.1", default_username="root", default_password="Admin123"):
    """Returns a list of RegisterParameters classes, 
    converted from dictionary.
    :data: dictionary which was read from the json file
    :return: list of RegisterParameters objects, hostname, username, password, router_name
    """
    register_parameters = []
    hostname = str(data['hostname']) if len(str(data['hostname'])) else default_hostname
    username = str(data['username']) if len(str(data['username'])) else default_username
    password = str(data['password']) if len(str(data['password'])) else default_password

    for dictionary in data['registerParameters']:
        register_parameters.append(RegisterParameters(dictionary))

    return register_parameters, hostname, username, password

def count_passed_tests(register_parameters):
    """Counts how many tests have been passed.
    :register_parameters: a list of RegisterParameters objects
    :return: number of passed tests
    """
    counter = 0
    for p in register_parameters:
        if p.passed_the_test is True:
            counter += 1
    return counter

def count_not_passed_tests(register_parameters):
    """Counts how many tests have not been passed.
    register_parameters: a list of RegisterParameters objects
    :return: number of tests that were not passed
    """
    return len(register_parameters) - count_passed_tests(register_parameters)

def set_expected_results(register_parameters):
    """Executes shell commands for every parameter and sets the rceived
    values to RegisterParameters objects.
    register_parameters: a list of RegisterParameters objects
    """

    for parameter in register_parameters:
        ssh_stdout = ssh_connection_handling.execute_command(parameter.router_command)
        parameter.set_expected_decoded_result(ssh_stdout)