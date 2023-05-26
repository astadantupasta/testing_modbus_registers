# Imports
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
import numpy as np

class RegisterParameters:
    """Keeps information about registers' parameters."""

    def __init__(self, required_value, reg_addr, reg_num, representation):
        """ Initiation of RegisterParameters object.

        :required_value: description of the value that needs to be found, e.g. System uptime
        :reg_addr: address number from which information has to be started reading
        :reg_num: number of registers that have to be read
        :represantation: indicates the type of 'required_value' value representation, 
        e.g. uint32, uint16, int32, float32, text
        """
        
        self.required_value = required_value
        self.reg_addr = reg_addr
        self.reg_num = reg_num
        self.representation = representation
        self.router_command = ""
        self.registers = []
        self.decoded_registers_value = None
        self.expected_decoded_result = None
        self.passed_the_test = False

    def __init__(self, dictionary):
        """ Initiation of RegisterParameters object from a dictionary.

        :dictionary: dictionary with reg_addr, reg_num, representation values
        """
        self.router_command = ""
        for key in dictionary:
            setattr(self, key, dictionary[key])

        self.registers = []
        self.decoded_registers_value = None
        self.expected_decoded_result = 0
        self.passed_the_test = False

    def get_required_value(self):
        return self.required_value
    
    def get_reg_addr(self):
        return self.reg_addr
    
    def get_reg_num(self):
        return self.reg_num
    
    def get_representation(self):
        return self.representation

    def set_registers(self, registers):
        self.registers = registers
    
    def set_expected_decoded_result(self, expected_decoded_result):
        """Sets 'expected_decoded_result' and reevaluates if the test was passed.

        :expected_decoded_result: the value that is received from a router executing a command.
        """
        if expected_decoded_result != "":
            match self.representation:
                case 'uint16':
                    self.expected_decoded_result = int(expected_decoded_result)
                case 'uint32':
                    self.expected_decoded_result = int(expected_decoded_result)
                case 'int32':
                    self.expected_decoded_result = int(expected_decoded_result)
                case 'float32':
                    self.expected_decoded_result = float(expected_decoded_result)
                case default:
                    self.expected_decoded_result = expected_decoded_result
        else: self.expected_decoded_result = expected_decoded_result
        self.set_passed_the_test()

    def set_passed_the_test(self):
        self.passed_the_test = (
            self.expected_decoded_result == self.decoded_registers_value
        )

    def print_registers(self):
        """Prints register's required_value, decoded_registers_value and 
        a list of registers in a form 'reg_addr: value'"""
        
        print(self.get_required_value())
        print("Decoded value: " + str(self.decoded_registers_value))
        
        try:
            i = 0
            for reg_address in range(self.reg_addr, (self.reg_addr + self.reg_num)):
                print(str(reg_address) + ": " + str(self.registers[i]))
                i += 1
        except IndexError as e:
            print("List of registers is empty: " + str(e))
        
        print()


    def decode_registers(self):
        """Decodes registers' integer values to desired self.representation"""
        match self.representation:
            case 'uint16':
                self.decoded_registers_value = self.registers[0]

            case 'uint32' | 'int32':
                if ((self.required_value != 'Mobile signal strength') & 
                    (self.required_value != 'Current WAN IP address')):
                    self.decoded_registers_value = self.registers[0] * 65536 + self.registers[1]

                elif self.required_value == 'Mobile signal strength':
                    # Value of the second register is converted to binary, inverted and then 1 added
                    self.decoded_registers_value = -abs(np.invert(
                        np.array(self.registers[1], dtype=np.uint16)) + 1)

                elif self.required_value == 'Current WAN IP address':
                    self.convert_registers_to_IP()

                else:
                    self.decoded_registers_value = "'required_value' or 'representation' variables of the object are not defined properly."

            case 'float32':
                decoder = BinaryPayloadDecoder.fromRegisters(self.registers, wordorder=Endian.Big)
                self.decoded_registers_value = decoder.decode_32bit_float()

            case 'text':
                list_decode = self.registers.copy()
                list_decode[:] = np.trim_zeros(list_decode)
                decoder = BinaryPayloadDecoder.fromRegisters(list_decode, wordorder=Endian.Big)
                self.decoded_registers_value = str(decoder.decode_string(16)).lstrip("'b").rstrip("'").rstrip('\\x00')

            case default:
                self.decoded_registers_value = "NOT DECODED. Object's variable 'representation' value is unrecognizable or empty."

    def convert_registers_to_IP(self):
        """Converts IP registers to IP address
        :list: a list with elements of two registers
        """
        list = self.registers.copy()

        if self.required_value != 'Current WAN IP address':
            raise Exception("Method 'convert_registers_to_IP': "
                            + "'required_value' has to be 'Current WAN IP address'.")

        if len(list) != 2: 
            raise Exception("Method 'convert_registers_to_IP': the list is not "+
                            "of 2 elements. Only 2 elements are needed.")

        # Converts registers to 16bit binary values, splits into two parts, 
        # converts 8bit binary values to integers
        byte1 = int('{0:016b}'.format(list[0])[:8], 2)
        byte2 = int('{0:016b}'.format(list[0])[8:], 2)
        byte3 = int('{0:016b}'.format(list[1])[:8], 2)
        byte4 = int('{0:016b}'.format(list[1])[8:], 2)

        self.decoded_registers_value = str(byte1) + '.' + str(byte2) + '.' + str(byte3) + '.' + str(byte4)

    