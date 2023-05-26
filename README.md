# Modbus registers testing
## Short description of the task
The aim of the automated test is to test all Modbus registers and check their values correctness.
The results are printed to the terminal as well as to the CSV file. All information about Modbus registers is stored in a JSON configuration file.

The test reads the registers, decodes them, checks if the decoded values correspond with the expected values (expected values are read from the device using the ssh protocol), and calculates simple statistics for the test.

## Python library dependencies

One needs to install `pyModbusTCP`, `pymodbus`, `paramiko`, `prettytable`, `numpy` packages.
Installation can be done using 
```
pip3 install *package_name*
```
command.

## Configuration file
All information about modbus registers is stored in a JSON configuration file `parameters.json`.
Meaning of the parameters:
1. `required_value` describes the meaning of the decoded registers' value.
2. `reg_addr` indicates the register address number, from which registers have to be started reading.
3. `reg_num` indicates the number of registers that have to be read starting from the `reg_addr`th register.
4. `representation` contains either *uint32*, *uint16*, *int32*, *float32* or *text* values and describes the type of the value that registers hold.
5. `router_command` indicates the command that has to be executed in order to get the real parameter value (value that is stored in a device).

More information on the Modbus protocol and parameters [here](https://wiki.teltonika-networks.com/view/Monitoring_via_Modbus).

## Build
1. Extract the zip file of this project, open it in Visual Studeio Code.
2. Locate the variable `router_name` in a file `main.py` and change the value to the name of the tested device.
3. Execute command `python3 main.py`.






