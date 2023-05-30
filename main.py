# Imports
from pyModbusTCP.client import ModbusClient
from modules import print_to_file
from modules import print_to_terminal
from modules import read_from_file
from modules import read_registers
from modules import printing_errors
from modules import rp_container_handling
from modules import ssh_connection_handling

# Name of the router which is to be tested
router_name = "RUTX11"

# Modbus Master and sshClint declaration
modbusClient = ModbusClient(host="192.168.1.1", port=502, auto_open=True, auto_close=True)
rp_container = []

def main():
    # Print any modbus errors
    printing_errors.print_modbus_errors("")
    
    # Check if the connected device is as indicated and
    # if the device has a modem
    ssh_connection_handling.connect_to_router("192.168.1.1", "root", "Admin123")
    ssh_connection_handling.check_connected_router_name(router_name)
    ssh_connection_handling.check_modem()

    # Read data from a file and append to a list of RegisterParameters objects
    file_data = read_from_file.read_data_from_json("parameters.json")
    rp_container = rp_container_handling.dict_to_list_of_objects(file_data)

    # Read registers of given parameters, save and decode them
    read_registers.read_all_registers(rp_container)

    # Execute shell commands, thus get and save expected values 
    # (values that are save in the router)
    rp_container_handling.set_expected_results(rp_container)
    ssh_connection_handling.disconnect_from_router()

    # Print results to terminal and to the csv file
    print_to_terminal.print_to_terminal(router_name, rp_container)
    print_to_file.print_to_csv(router_name, rp_container)


if __name__ == "__main__":
    while True:
        main()