import main

def print_modbus_errors(modbusClient, reg_addr=""):
    """Prints errors and exceptions recorded in Modbus modbusClient object's variables.
    :reg_addr: address of the register for which errors are being printed.
    :modbusClient: modbus Master object
    """
    if modbusClient.last_except != 0:
        print("reg_addr: " + str(reg_addr))
        print(modbusClient.last_except_as_txt)
    if modbusClient.last_error != 0:
        print(modbusClient.last_error_as_txt) 
        print()