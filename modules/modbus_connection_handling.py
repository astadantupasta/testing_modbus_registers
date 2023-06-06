from pyModbusTCP.client import ModbusClient
import time

def create_modbus_client(hostname, port, auto_open=False, auto_close=True):
    """Modbus client constructor.
    :hostname: hostname or server IP address
    :port: port
    :auto_open: should the connection be openned automatically
    :auto_close: should the connection be closed automatically
    :return: ModbusClient object
    """
    return ModbusClient(host=hostname, port=port, auto_open=auto_open ,auto_close=auto_close)

def connect_to_modbus_client(modbusClient, waiting_seconds=5, repetition_times=10):
    """Connects to the ModbusClient object. 
    In case of connection error, tries to connect indicated number of times,
    and waits between connection an indicated amount of seconds.
    :modbusClient: pyModbusTCP client object
    :waiting_seconds: number of seconds that are waited between unsuccessful connections
    :repetition_times: number of attempt to connect to the client until success
    """
    for i in range(repetition_times):
        modbusClient.open()

        if not modbus_client_is_active(modbusClient):
            print("Modbus connection error.")
            print("Reconnecting...")
            time.sleep(waiting_seconds)
        else:
            break
    
def print_modbus_connection_errors(modbusClient):
    """Checks if modbus connection is still open.
    In case of connection error, tries to reconnect.
    :modbusClient: pyModbusTCP client object
    """
    if not modbus_client_is_active(modbusClient):
        print("Modbus connection error.")
        connect_to_modbus_client(modbusClient)

def modbus_client_is_active(modbusClient):
    """Checks if connection to the Modbus client is open.
    :return: is connection active
    """
    return modbusClient.is_open

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