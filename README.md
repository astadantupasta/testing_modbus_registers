# Modbus registers testing
## Short description of the task
The aim of the automated test is to test all Modbus registers and check their values correctness.
The results are printed to the terminal as well as to the CSV file. All information about Modbus registers is stored in a JSON configuration file.

The test takes the name of the router as a flag using the command line, reads the registers of the indicated router, decodes them, checks if the decoded values correspond with the expected values (expected values are read from the device using the ssh protocol), and calculates simple statistics for the test.

## Python library dependencies

One needs to install `pyModbusTCP`, `pymodbus`, `paramiko`, `prettytable`, `numpy` packages.
Installation can be done using 
```
pip3 install *package_name*
```
command.

## Configuration file
All information about tested device and modbus registers is stored in a JSON configuration file `parameters.json`.

First of all, all the configurations are categorised according to the name of the device (e.g., `RUTX11`, `RUT956` and etc.). Every device has its `hostname`, `username`, `password` and `registerParameters`. The first three configurations (hostname, username, and password) have to be set correctly before starting the test. If these configurations are not set at all (left empty), then the default values are used (*192.168.1.1*, *root*, *Admin123* accordingly).

Every device has a different set of `registerParameters`. Meanings of their values:
1. `required_value` describes the meaning of the decoded registers' value.
2. `reg_addr` indicates the register address number, from which registers have to be started reading.
3. `reg_num` indicates the number of registers that have to be read starting from the `reg_addr`th register.
4. `representation` contains either *uint32*, *uint16*, *int32*, *float32* or *text* values and describes the type of the value that registers hold.
5. `router_command` indicates the command that has to be executed in order to get the real parameter value (value that is stored in a device).

More information on the Modbus protocol and parameters [here](https://wiki.teltonika-networks.com/view/Monitoring_via_Modbus).

An example of the configuration file:
![configs_example](https://github.com/astadantupasta/testing_modbus_registers/assets/79766133/c0f7bc92-aa56-4f09-a11a-779096baa834)

## Build
1. Extract the zip file of this project, open it in Visual Studio Code.
2. Make sure that the configurations for connection are written correctly in the configuration file *parameters.json*: locate the name of the router you are about to test, change *hostname*, *username*, *password* to the correct ones.
3. Execute the command `python3 main.py -n *router_name*`, where *router_name* is the name of the router, e.g., *RUTX11*, *RUT956*.






