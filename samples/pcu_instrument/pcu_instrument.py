# -*- coding: utf-8 -*-
"""
PCU instrument class.
Command mode: Legacy
Communication: GPIB | LAN (PyVISA)

Last Updated: Tue Feb 04, 2025 11:00
"""

from enum import Enum


class PCU:
    def __init__(self, connection):
        """
        Initializes the PCU class with an opened PyVISA resource.

        Parameters:
            connection: An open PyVISA resource representing the connected instrument.
        """
        self.instance = connection

    def query(self, command):
        """
        Sends a query command to the instrument and returns the response.

        Parameters:
            command (str): The command to query the instrument.

        Returns:
            str: The response from the instrument.
        """
        return self.instance.query(command)

    def write(self, command):
        """
        Sends a write command to the instrument.

        Parameters:
            command (str): The command to send to the instrument.
        """
        self.instance.write(command)

    def get_idn(self) -> str:
        """
        Identification Query.
        Parameter: None

        Response: SANTEC,TSL-570,21020001,0001.0000.0001
        """
        return self.query('*IDN?')

    def device_reset(self):
        """
        Device Reset
        Aborts standby operation.
        Clears the following items.
        ・Command input queue
        ・Error queue
        """
        self.write('*RST')

    def get_self_test_query(self):
        """
        Self-test Query.
        Initiates an instrument self-test and places the results in the
        output queue.
        """
        response = self.query('*TST?')
        return "No Error" if response == '0' else "Error"

    def get_operation_complete_query(self):
        """
        Operation Complete Query.
        Places 1 in the output queue when all operation processing is completed.
        """
        response = self.query('*OPC?')
        return "In operation" if response == '0' else "Operation completed" if response == '1' else ""

    def clear_status(self):
        """
        Clear Status
        Clears all event registers and queues and reflects the summary
        in the Status Byte Register.
        Clears the following items.
        ・Status Byte Register
        ・Standard Event Status Register
        ・Error Queue
        """
        self.write('*CLS')

    def get_standard_event_enable_register(self):
        """Gets the Standard Event Enable Register (SEER)."""
        return int(self.query('*ESE?'))

    def set_standard_event_enable_register(self, value: int):
        """
        Sets the Standard Event Enable Register (SEER).

        Parameter Setting value from 0 to 255
        """
        self.write(f'*ESE {value}')

    def get_standard_event_status_register(self):
        """Gets the Standard Event Status Register (SESR)."""
        return int(self.query('*ESR?'))

    def get_service_request_enable_register(self):
        """Gets the Service Request Enable Register (SRER)."""
        return int(self.query('*SRE?'))

    def set_service_request_enable_register(self, value: int):
        """
        Service Request Enable Register Setting
        The Service Request Enable Register (SRER).

        Parameter: Setting value from 0 to 255
        """
        self.query(f'*SRE {value}')

    def get_status_byte_register(self):
        """Gets the Status Byte Register (STBR)"""
        return int(self.query('*STB?'))

    def get_polarization(self) -> str:
        """Gets the polarization state."""
        response = self.query(':POL?')
        polarization_states = {
            '1': "Vertical Linear Polarization",
            '2': "Horizontal Linear Polarization",
            '3': "+45° Linear Polarization",
            '4': "-45° Linear Polarization",
            '5': "Right Hand Circular Polarization",
            '6': "Left Hand Circular Polarization"
        }
        return polarization_states.get(response, "Unknown Polarization State")

    def set_polarization(self, state: int):
        """
        Sets the polarization state.

        Parameters:
            state (int): The polarization state to set.
                    1: Vertical Linear Polarization
                    2: Horizontal Linear Polarization
                    3: +45°Linear Polarization
                    4: -45°Linear Polarization
                    5: Right Hand Circular Polarization
                    6: Left Hand Circular Polarization
        """
        if state not in [1, 2, 3, 4, 5, 6]:
            raise Exception(f"Invalid polarization state value {state}.")
        self.write(f':POL {state}')

    def get_power_unit(self) -> str:
        """Gets the power unit."""
        response = self.query(':POW:UNIT?')
        power_units = {
            '0': "dBm",
            '1': "mW"
        }
        return power_units.get(response, "Unknown Power Unit")

    def set_power_unit(self, unit: int):
        """
        Sets the power unit.

        Parameters:
            unit (str): The power unit to set.
                    0: dBm
                    1: mW
        """
        if unit not in [0, 1]:
            raise Exception(f"Invalid unit value {unit}.")
        self.write(f':POW:UNIT {unit}')

    def get_monitor_power(self):
        """Gets the monitor power."""
        return float(self.query(':POW:LEVEL?'))

    def reboot_device(self):
        """Reboots the device."""
        self.write('SPEC:REB')

    def get_system_error(self) -> str:
        """Gets the system error with a detailed description."""
        response = self.query(':SYST:ERR?').strip()
        try:
            error_code = ErrorCode(response)
            return f"{response}: {ErrorCode.get_description(error_code)}"
        except ValueError:
            return f"{response}: Unknown error code"

    def get_firmware_version(self) -> str:
        """Gets the firmware version."""
        return self.query(':SYST:VERS?')

    def get_gpib_address(self) -> int:
        """Gets the GPIB address."""
        return int(self.query(':SYST:COMM:GPIB:ADDR?'))

    def set_gpib_address(self, address: int):
        """
        Sets the GPIB address.

        Parameters:
            address (int): The GPIB address to set.
        """
        self.write(f':SYST:COMM:GPIB:ADDR {address}')

    def get_gpib_delimiter(self) -> str:
        """Gets the GPIB command delimiter."""
        response = self.query(':SYST:COMM:GPIB:DEL?')
        delimiter_dict = {
            '0': "CR",
            '1': "LF",
            '2': "CR+LF",
            '3': "None"
        }
        return delimiter_dict.get(response, "Unknown delimiter")

    def set_gpib_delimiter(self, delimiter: int):
        """
        Sets the GPIB command delimiter.

        Parameters:
            delimiter (str): The GPIB delimiter to set.
                        0: CR
                        1: LF
                        2: CR+LF
                        3: None
        """
        self.write(f':SYST:COMM:GPIB:DEL {delimiter}')

    def get_ethernet_dhcp(self) -> str:
        """Gets the Ethernet DHCP state."""
        response = self.query(':SYST:COMM:ETH:DHCP?')
        dhcp_state_dict = {
            '0': "DHCP disable",
            '1': "DHCP enable"
        }
        return dhcp_state_dict.get(response, "Unknown DHCP state")

    def set_ethernet_dhcp(self, state: int):
        """
        Sets the Ethernet DHCP state.

        Parameters:
            state (str): The DHCP state to set.
                    0: DHCP disable
                    1: DHCP enable
        """
        if state not in [0, 1]:
            raise Exception(f"Invalid state value {state}.")
        self.write(f':SYST:COMM:ETH:DHCP {state}')

    def get_ip_address(self) -> str:
        """Gets the Ethernet IP address."""
        return self.query(':SYST:COMM:ETH:IPAD?')

    def set_ip_address(self, ip: str):
        """
        Sets the Ethernet IP address.

        Parameters:
            ip (str): The IP address to set.
        """
        self.write(f':SYST:COMM:ETH:IPAD {ip}')

    def get_subnet_mask(self) -> str:
        """Gets the Ethernet subnet mask."""
        return self.query('SYST:COMM:ETH:SMAS?')

    def set_subnet_mask(self, mask: str):
        """
        Sets the Ethernet subnet mask.

        Parameters:
            mask (str): The subnet mask to set.
        """
        self.write(f'SYST:COMM:ETH:SMAS {mask}')

    def get_gateway(self) -> str:
        """Gets the Ethernet gateway."""
        return self.query(':SYST:COMM:ETH:DGAT?')

    def set_gateway(self, gateway: str):
        """
        Sets the Ethernet gateway.

        Parameters:
            gateway (str): The gateway to set.
        """
        self.write(f':SYST:COMM:ETH:DGAT {gateway}')

    def get_port_number(self) -> int:
        """Gets the Ethernet port."""
        return int(self.query(':SYST:COMM:ETH:PORT?'))

    def set_port_number(self, port: int):
        """
        Sets the Ethernet port.

        Parameters:
            port (int): The port number to set.
        """
        if not (0 <= port <= 65535):
            raise Exception(f"Value {port} out of range.")
        self.write(f':SYST:COMM:ETH:PORT {port}')


class ErrorCode(Enum):
    NO_ERROR = "0"
    SYNTAX_ERROR = "-102"
    INVALID_SEPARATOR = "-103"
    PARAMETER_NOT_ALLOWED = "-108"
    MISSING_PARAMETER = "-109"
    UNDEFINED_HEADER = "-113"
    INVALID_SUFFIX = "-131"
    CHARACTER_DATA_NOT_ALLOWED = "-148"
    EXECUTION_ERROR = "-200"
    DATA_OUT_OF_RANGE = "-222"
    ILLEGAL_PARAMETER_VALUE = "-224"
    QUERY_INTERRUPTED = "-410"

    @staticmethod
    def get_description(error_code) -> str:
        error_descriptions = {
            ErrorCode.NO_ERROR: "No error occurred during the operation.",
            ErrorCode.SYNTAX_ERROR: "The command contains an invalid syntax or unrecognized format.",
            ErrorCode.INVALID_SEPARATOR: "A separator in the command is missing or incorrect.",
            ErrorCode.PARAMETER_NOT_ALLOWED: "The command contains an unexpected or unsupported parameter.",
            ErrorCode.MISSING_PARAMETER: "Required parameter(s) are missing from the command.",
            ErrorCode.UNDEFINED_HEADER: "The command header is syntactically correct but not supported by the device.",
            ErrorCode.INVALID_SUFFIX: "A suffix in the command is invalid or incorrectly formatted.",
            ErrorCode.CHARACTER_DATA_NOT_ALLOWED: "Character data was received where it is not permitted.",
            ErrorCode.EXECUTION_ERROR: "The device is in a state that prevents execution of the command.",
            ErrorCode.DATA_OUT_OF_RANGE: "A parameter value is outside the permissible range.",
            ErrorCode.ILLEGAL_PARAMETER_VALUE: "A specific value expected by the command is invalid.",
            ErrorCode.QUERY_INTERRUPTED: "The query was interrupted due to an unexpected condition.",
        }
        return error_descriptions.get(ErrorCode(error_code), f"Unknown Error Code: {error_code}")
