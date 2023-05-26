# Imports
from pyModbusTCP.client import ModbusClient
from register_parameters import RegisterParameters
import paramiko
from modules import print
from modules import read
from modules import error_handling
from modules import rp_container

# Name of the router which is to be tested
router_name = "RUTX11"

# Modbus Master and sshClint declaration
modbusClient = ModbusClient(host="192.168.1.1", port=502, auto_open=True, auto_close=True)
sshClient = paramiko.SSHClient()

def main():
    # Check if the connected device is as indicated and
    # if the device has a modem
    error_handling.check_connected_router_name()
    error_handling.check_modem()

    # Print any modbus errors
    error_handling.print_modbus_errors()  

    # Read data from a file and append to a list of RegisterParameters objects
    file_data = read.read_data_from_json("parameters.json")
    rp_container.dict_to_list_of_objects(file_data)

    # Read registers of given parameters, save and decode them
    read.read_all_registers()

    # Execute shell commands, thus get and save expected values 
    # (values that are save in the router)
    rp_container.set_expected_results()

    # Print results to terminal and to the csv file
    print.print_to_terminal()
    print.print_to_csv()


if __name__ == "__main__":
    main()