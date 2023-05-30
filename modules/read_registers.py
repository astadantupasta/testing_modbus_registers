import main
from modules import printing_errors

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

    printing_errors.print_modbus_errors(parameter.get_reg_addr()-1)

    return registers

def read_all_registers(rp_container):
    """Reads registers of every parameter, saves the value and then decodes it.
    """
    if len(rp_container) == 0:
        raise Exception("modules/read_registers.py, read_all_registers(): rp_container is empty.")

    for parameter in rp_container:

        # Reading the registers from address 'reg_addr' to 'reg_addr + reg_nb'
        registers = read_holding_registers(parameter)

        if registers is not None:
            parameter.set_registers(registers)
            parameter.decode_registers() 