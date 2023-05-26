import main
import paramiko

def print_modbus_errors():
    """Prints errors and exceptions recorded in Modbus modbusClient object's variables"""
    if main.modbusClient.last_except != 0:
        print(main.modbusClient.last_except_as_txt)
    if main.modbusClient.last_error != 0:
        print(main.modbusClient.last_error_as_txt) 

def check_connected_router_name():
    """Checks if products's name is as indicated in variable 'router_name'."""
    # Connect to router using ssh protocol
    main.sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    main.sshClient.connect(hostname="192.168.1.1", username="root", password="Admin123")

    ssh_stdin, ssh_stdout, ssh_stderr = main.sshClient.exec_command("cat /etc/config/system | grep routername | awk '{print $NF}' | sed \"s/'//g\"")
    ssh_stdin.close()
    if ssh_stdout.read().decode('ascii').strip("\n") != main.router_name:
        raise Exception("Connected product is not as indicated in variable 'router_name'")

def check_modem():
    """Checks if product has a modem."""
    # Connect to router using ssh protocol
    main.sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    main.sshClient.connect(hostname="192.168.1.1", username="root", password="Admin123")
    
    ssh_stdin, ssh_stdout, ssh_stderr = main.sshClient.exec_command("gsmctl -a")
    ssh_stdin.close()
    if ssh_stdout.read().decode('ascii').strip("\n") == "":
        raise Exception("The connected product does not have a modem.")