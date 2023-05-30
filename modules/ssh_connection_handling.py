import paramiko

sshClient = paramiko.SSHClient()

def connect_to_router(hostname, username, password):
    """Connecto to the device using SSH protocol.
    :hostname: ip address of the device
    :username: username for the ssh connection
    :password: password for the ssh connection
    """
    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        sshClient.connect(hostname=hostname, username=username, password=password)
    except:
        print("Ssh connection refused.")
        exit()

def disconnect_from_router():
    sshClient.close()


def check_connected_router_name(router_name):
    """Checks if products's name is as indicated in variable 'router_name'.
    :router_name: name of the router
    """
    try:
        ssh_stdin, ssh_stdout, ssh_stderr = sshClient.exec_command("cat /etc/config/system | grep routername | awk '{print $NF}' | sed \"s/'//g\"")
        ssh_stdin.close()
        if ssh_stdout.read().decode('ascii').strip("\n") != router_name:
            raise Exception("Connected product is not as indicated in variable 'router_name'")
    except:
        print("Reading router name failed.")
        exit()

def check_modem():
    """Checks if product has a modem."""
    try:
        ssh_stdin, ssh_stdout, ssh_stderr = sshClient.exec_command("gsmctl -a")
        ssh_stdin.close()
        if ssh_stdout.read().decode('ascii').strip("\n") == "":
            raise Exception("The connected product does not have a modem.")
    except:
        print("Reading modem name failed.")
        exit()

def execute_command(command):
    """Executes command on the device.
    :command: command to execute
    :return: result of the command
    """
    try:
        ssh_stdin, ssh_stdout, ssh_stderr = sshClient.exec_command(command)
        ssh_stdin.close()
    except:
        print("Executing ssh command failed. Command: " + command)

    return ssh_stdout.read().decode('ascii').strip("\n")

def get_device_hostname():
    """Finds device hostname."""
    return execute_command("cat /proc/sys/kernel/hostname")