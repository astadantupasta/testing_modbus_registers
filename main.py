# Imports
from pyModbusTCP.client import ModbusClient
from modules import print_to_file
from modules import print_to_terminal
from modules import read_from_file
from modules import read_registers
from modules import printing_errors
from modules import rp_container_handling
from modules import ssh_connection_handling

# Declaration of RegisterParameters container
rp_container = []

def main():
    # Read data from a file and append to a list of RegisterParameters objects
    file_data = read_from_file.read_data_from_json("parameters.json")
    rp_container, hostname, username, password, router_name = rp_container_handling.dict_to_list_of_objects(file_data)
    modbusClient = ModbusClient(host=hostname, port=502, auto_open=True, auto_close=True)

    # Print any modbus errors
    printing_errors.print_modbus_errors(modbusClient)
    
    # Check if the connected device is as indicated and
    # if the device has a modem
    ssh_connection_handling.connect_to_router(hostname, username, password)
    ssh_connection_handling.check_connected_router_name(router_name)
    ssh_connection_handling.check_modem()

    # Read registers of given parameters, save and decode them
    read_registers.read_all_registers(rp_container, modbusClient)

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