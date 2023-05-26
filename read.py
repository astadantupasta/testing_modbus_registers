import main
import error_handling
import json
import rp_container

def read_data_from_json(file_name):
    """Read data from json file.

    :file_name: name of the json file
    :return: dictionary read from the json file
    """
    with open(file_name, "r") as read_file:
        data = json.load(read_file)
    return data

def read_holding_registers(parameter):
    """modbusClient reads holding registers from a router.
    Reads registers from address num 'reg_addr' to 'reg_addr + reg_nb'

    :parameter: RegisterParameters object of which registers have to be read
    :return: registers that were read
    """
    try: 
        registers = main.modbusClient.read_holding_registers(
            reg_addr=parameter.get_reg_addr(), 
            reg_nb=parameter.get_reg_num())
    except ValueError as e: 
            print(e)

    error_handling.print_modbus_errors()

    return registers

def read_all_registers():
    """Reads registers of every parameter, saves the value and then decodes it.
    """
    for parameter in rp_container.register_parameters:

        # Reading the registers from address 'reg_addr' to 'reg_addr + reg_nb'
        registers = read_holding_registers(parameter)

        if registers is not None:
            parameter.set_registers(registers)
            parameter.decode_registers() 