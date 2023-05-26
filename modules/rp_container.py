from register_parameters import RegisterParameters
import main
import paramiko

register_parameters = []

def dict_to_list_of_objects(data):
    """Returns a list of RegisterParameters classes, 
    converted from dictionary.

    :data: dictionary which was read from the json file
    """
    # List of all the RegisterParameters classes

    for dictionary in data['registerParameters']:
        register_parameters.append(RegisterParameters(dictionary))

def count_passed_tests():
    """Counts how many tests have been passed.
    :return: number of passed tests
    """
    counter = 0
    for p in register_parameters:
        if p.passed_the_test is True:
            counter += 1
    return counter

def count_not_passed_tests():
    """Counts how many tests have not been passed.
    :return: number of tests that were not passed
    """
    return len(register_parameters) - count_passed_tests()

def set_expected_results():
    """Executes shell commands for every parameter and sets the rceived
    values to RegisterParameters objects.
    """
    # Connect to router using ssh protocol
    main.sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    main.sshClient.connect(hostname="192.168.1.1", username="root", password="Admin123")

    # Execute commands and save the received results
    for parameter in register_parameters:
        ssh_stdin, ssh_stdout, ssh_stderr = main.sshClient.exec_command(parameter.router_command)
        ssh_stdin.close()
        parameter.set_expected_decoded_result(ssh_stdout.read().decode('ascii').strip("\n"))
    print(ssh_stdout.read().decode('ascii').strip("\n"))