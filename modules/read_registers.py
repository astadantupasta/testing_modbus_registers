import main
from modules import modbus_connection_handling

def read_holding_registers(parameter, modbusClient):
    """modbusClient reads holding registers from a router.
    Reads registers from address num 'reg_addr' to 'reg_addr + reg_nb'

    :parameter: RegisterParameters object of which registers have to be read
    :modbusClient: modbus Master object
    :return: registers that were read
    """
    try: 
        registers = modbusClient.read_holding_registers(
            reg_addr=parameter.get_reg_addr(), 
            reg_nb=parameter.get_reg_num())
    except ValueError as e: 
            print(e)

    modbus_connection_handling.print_modbus_errors(modbusClient, parameter.get_reg_addr()-1)

    return registers

def read_all_registers(rp_container, modbusClient):
    """Reads registers of every parameter, saves the value and then decodes it.
    :rp_container: a list of RegisterParameters objects
    :modbusClient: modbus Master object
    """
    if len(rp_container) == 0:
        raise Exception("modules/read_registers.py, read_all_registers(): rp_container is empty.")

    # Check if modbus connection is still active
    modbus_connection_handling.print_modbus_connection_errors(modbusClient)

    for parameter in rp_container:

        # Reading the registers from address 'reg_addr' to 'reg_addr + reg_nb'
        registers = read_holding_registers(parameter, modbusClient)

        if registers is not None:
            parameter.set_registers(registers)
            parameter.decode_registers() 