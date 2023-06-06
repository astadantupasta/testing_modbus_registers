import paramiko
import time

sshClient = paramiko.SSHClient()
this_hostname = ""
this_username = ""
this_password = ""

def connect_to_router(hostname, username, password, waiting_seconds=5, repetition_times=10):
    """Connect to the device using SSH protocol.
    In case of connection error, code is stopped for waiting_seconds
    seconds repetition_times times
    :hostname: ip address of the device
    :username: username for the ssh connection
    :password: password for the ssh connection
    :waiting_seconds: number of seconds that the code has to be stopped
    for until the next attempt to execute the command
    :repetition_times: number of repetitions until the code is exited
    """
    this_hostname = hostname
    this_username = username
    this_password = password

    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for i in range(repetition_times):
        try:
            sshClient.connect(hostname=hostname, username=username, password=password)
            break
        except ConnectionError as e:
            print("Ssh connection error." + str(e))
            print("reconnecting...")
            time.sleep(waiting_seconds)
        except Exception as e:
            print("Ssh connection error occured: " + str(e))
            print("reconnecting...")
            time.sleep(waiting_seconds)

def disconnect_from_router():
    if sshClient.get_transport() is not None:
        sshClient.close()

def execute_command(command, waiting_seconds=5, repetition_times=10):
    """Executes command on the device. In case of connection error, 
    code is stopped for waiting_seconds seconds repetition_times times
    :command: command to execute
    :waiting_seconds: number of seconds that the code has to be stopped
    for until the next attempt to execute the command
    :repetition_times: number of repetitions until the code is exited
    :return: result of the command
    """
    for i in range(repetition_times):
        try:
            ssh_stdin, ssh_stdout, ssh_stderr = sshClient.exec_command(command)
            ssh_stdin.close()
            break
        except:
            print("Executing ssh command failed. Command: " + command)
            print("reexecuting...")
            connect_to_router(this_hostname, this_username, this_password)
            time.sleep(waiting_seconds)

    return ssh_stdout.read().decode('ascii').strip("\n")

def check_connected_router_name(router_name):
    """Checks if products's name is as indicated in variable 'router_name'.
    :router_name: name of the router
    """
    ssh_stdout = execute_command("cat /etc/config/system | grep routername | awk '{print $NF}' | sed \"s/'//g\"")
    if ssh_stdout != router_name:
        raise Exception("Connected product is not as indicated in variable 'router_name'")

def check_modem():
    """Checks if product has a modem."""
    ssh_stdout = execute_command("gsmctl -a")
    if ssh_stdout == "":
        raise Exception("The connected product does not have a modem.")

def get_device_hostname():
    """Finds device hostname."""
    return execute_command("cat /proc/sys/kernel/hostname")