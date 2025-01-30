# -*- coding: utf-8 -*-
from pcu_information import ErrorCode


class PCU:
    def __init__(self, instance):
        """
        Initializes the PCU class with an opened PyVISA resource.

        Parameters:
            instance: An open PyVISA resource representing the connected instrument.
        """
        self.instance = instance

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

    @property
    def idn(self) -> str:
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

    @property
    def self_test_query(self):
        """
        Self-test Query.
        Initiates an instrument self-test and places the results in the
        output queue.
        """
        response = self.query('*TST?')
        return "No Error" if response == '0' else "Error"

    @property
    def operation_complete_query(self):
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

    @property
    def standard_event_enable_register(self):
        """Gets the Standard Event Enable Register (SEER)."""
        return int(self.query('*ESE?'))

    @standard_event_enable_register.setter
    def standard_event_enable_register(self, value: int):
        """
        Sets the Standard Event Enable Register (SEER).

        Parameter Setting value from 0 to 255
        """
        if 0 >= value >= 255:
            raise Exception(f"Value {value} out of range.")
        self.write(f'*ESE {value}')

    @property
    def standard_event_status_register(self):
        """Gets the Standard Event Status Register (SESR)."""
        return int(self.query('*ESR?'))

    @property
    def service_request_enable_register(self):
        """Gets the Service Request Enable Register (SRER)."""
        return int(self.query('*SRE?'))

    @service_request_enable_register.setter
    def service_request_enable_register(self, value: int):
        """
        Service Request Enable Register Setting
        The Service Request Enable Register (SRER).

        Parameter: Setting value from 0 to 255
        """
        if 0 >= value >= 255:
            raise Exception(f"Value {value} out of range.")
        self.query(f'*SRE {value}')

    @property
    def status_byte_register(self):
        """Gets the Status Byte Register (STBR)"""
        return int(self.query('*STB?'))

    @property
    def polarization(self) -> str:
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

    @polarization.setter
    def polarization(self, state: int):
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

    @property
    def power_unit(self) -> str:
        """Gets the power unit."""
        response = self.query(':POW:UNIT?')
        power_units = {
            '0': "dBm",
            '1': "mW"
        }
        return power_units.get(response, "Unknown Power Unit")

    @power_unit.setter
    def power_unit(self, unit: int):
        """
        Sets the power unit.

        Parameters:
            unit (str): The power unit to set.
                    0: dBm
                    1: mW
        """
        if state not in [0, 1]:
            raise Exception(f"Invalid unit value {unit}.")
        self.write(f':POW:UNIT {unit}')

    @property
    def monitor_power(self):
        """Gets the monitor power."""
        return float(self.query(':POW:LEVEL?'))

    def reboot_device(self):
        """Reboots the device."""
        self.write('SPEC:REB')

    @property
    def system_error(self) -> str:
        """Gets the system error with a detailed description."""
        response = self.query(':SYST:ERR?').strip()
        try:
            error_code = ErrorCode(response)
            return f"{response}: {ErrorCode.get_description(error_code)}"
        except ValueError:
            return f"{response}: Unknown error code"

    @property
    def firmware_version(self) -> str:
        """Gets the firmware version."""
        return self.query(':SYST:VERS?')

    @property
    def gpib_address(self) -> int:
        """Gets the GPIB address."""
        return int(self.query(':SYST:COMM:GPIB:ADDR?'))

    @gpib_address.setter
    def gpib_address(self, address: int):
        """
        Sets the GPIB address.

        Parameters:
            address (int): The GPIB address to set.
        """
        self.write(f':SYST:COMM:GPIB:ADDR {address}')

    @property
    def gpib_delimiter(self) -> str:
        """Gets the GPIB command delimiter."""
        response = self.query(':SYST:COMM:GPIB:DEL?')
        delimiter_dict = {
            '0': "CR",
            '1': "LF",
            '2': "CR+LF",
            '3': "None"
        }
        return delimiter_dict.get(response, "Unknown delimiter")

    @gpib_delimiter.setter
    def gpib_delimiter(self, delimiter: int):
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

    @property
    def ethernet_dhcp(self) -> str:
        """Gets the Ethernet DHCP state."""
        response = self.query(':SYST:COMM:ETH:DHCP?')
        dhcp_state_dict = {
            '0': "DHCP disable",
            '1': "DHCP enable"
        }
        return dhcp_state_dict.get(response, "Unknown DHCP state")

    @ethernet_dhcp.setter
    def ethernet_dhcp(self, state: int):
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

    @property
    def ip_address(self) -> str:
        """Gets the Ethernet IP address."""
        return self.query(':SYST:COMM:ETH:IPAD?')

    @ip_address.setter
    def ip_address(self, ip: str):
        """
        Sets the Ethernet IP address.

        Parameters:
            ip (str): The IP address to set.
        """
        self.write(f':SYST:COMM:ETH:IPAD {ip}')

    @property
    def subnet_mask(self) -> str:
        """Gets the Ethernet subnet mask."""
        return self.query('SYST:COMM:ETH:SMAS?')

    @subnet_mask.setter
    def subnet_mask(self, mask: str):
        """
        Sets the Ethernet subnet mask.

        Parameters:
            mask (str): The subnet mask to set.
        """
        self.write(f'SYST:COMM:ETH:SMAS {mask}')

    @property
    def gateway(self) -> str:
        """Gets the Ethernet gateway."""
        return self.query(':SYST:COMM:ETH:DGAT?')

    @gateway.setter
    def gateway(self, gateway: str):
        """
        Sets the Ethernet gateway.

        Parameters:
            gateway (str): The gateway to set.
        """
        self.write(f':SYST:COMM:ETH:DGAT {gateway}')

    @property
    def port_number(self) -> int:
        """Gets the Ethernet port."""
        return int(self.query(':SYST:COMM:ETH:PORT?'))

    @port_number.setter
    def port_number(self, port: int):
        """
        Sets the Ethernet port.

        Parameters:
            port (int): The port number to set.
        """
        if 0 >= port >= 65535:
            raise Exception(f"Value {port} out of range.")
        self.write(f':SYST:COMM:ETH:PORT {port}')

