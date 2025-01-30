# -*- coding: utf-8 -*-
"""
MPM instrument class.
Command mode: Legacy
Communication: GPIB | LAN (PyVISA)

Last Updated: Thu Jan 30, 2025 13:46
"""

from enum import Enum


class MPM:
    def __init__(self, instance):
        """
        Initializes the MPM class with an opened PyVISA resource.

        Parameters:
            instance: An open PyVISA resource representing the connected instrument.
        """
        self.instance = instance

        self._power_mode_for_each_channel = None

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

    def echo(self, value: int):
        """
        Define echo (For only RS-232 Communication)

        Parameters:
            0 : Disable
            1 : Enable
        """
        self.write(f'ECHO {value}')

    @property
    def idn(self) -> str:
        """
        Identification Query.
        Parameter: None

        Response: SANTEC,MPM-210H,00000000,Ver.2.0
        """
        return self.query('*IDN?')

    @property
    def error(self):
        """
        Check Error information.

        Response:
            <value>,<string>
            <value>: Error Code
            <string>: Summary of content for Error
        """
        error_value, error_message = self.query('ERR?').split(',')
        error_code = ErrorCode(int(error_value))
        return error_code, error_message

    @property
    def get_modules(self):
        """
        Check recognition of Module for MPM-210H.
        
        Response:
            <value0>, <value1>, <value2>, <value3>, <value4>
            value0: Module0
            value1: Module1
            value2: Module2
            value3: Module3
            value4: Module4
            0: Module is not recognized.
            1: Module is recognized.

        Example:
            IDIS?
            Response: 1,1,1,1,1
        """
        return self.query('IDIS?')

    def module_information(self, module: int):
        """
        Identification query of a module type.

        Parameters: <module >: 0,1,2,3,4

        Response:
            <value0>,<value1>,<value2>,<Value3>
            value0: Company (Santec)
            value1: Product code (MPM-211,MPM-212,MPM-
            213,MPM-215)
            value2: Serial number
            value3: Firmware version

        Example:
            MMVER? 0
            Response : Santec,MPM-211,00000000M211,Ver1.11
        """
        return self.query(f'MMVER? {module}')

    @property
    def gpib_address(self):
        """Get the current GPIB address."""
        return self.query('ADDR?')

    @gpib_address.setter
    def gpib_address(self, value: str):
        """
        Set the GPIB address.

        Parameters:
            <value>: GPIB address value, range 1 to 31
        """
        self.write(f'ADDR {value}')

    @property
    def gateway_address(self):
        """Get the current Gateway Address."""
        return self.query('GW?')

    @gateway_address.setter
    def gateway_address(self, address: str):
        """
        Set the Gateway address.

        Parameters:
            <address>: Gateway address in the format 'www.xxx.yyy.zzz'
        """
        self.write(f'GW {address}')

    @property
    def subnet_mask(self):
        """Get the current Subnet Mask."""
        return self.query('SUBNET?')

    @subnet_mask.setter
    def subnet_mask(self, address: str):
        """
        Set the Subnet Mask.

        Parameters:
            <address>: Subnet mask in the format 'www.xxx.yyy.zzz'
        """
        self.write(f'SUBNET {address}')

    @property
    def ip_address(self):
        """Get the current IP address."""
        return self.query('IP?')

    @ip_address.setter
    def ip_address(self, address: str):
        """
        Set the IP address.

        Parameters:
            <address>: IP address in the format www.xxx.yyy.zzz (0 ~ 255)
        """
        self.write(f'IP {address}')

    def perform_zeroing(self):
        """
        Before measuring optical power, run Zeroing to delete
        electrical DC offset. Please be careful with the incidence of light
        into Optic Port. When using the current meter module,
        the MPM-213, please remove the BNC cable from the
        MPM-213. This command action takes about 3 sec, so
        please run other commands at least 3 sec later.
        """
        self.write('ZERO')

    @property
    def input_trigger(self):
        """Get the current input trigger setting."""
        return self.query('TRIG?')

    @input_trigger.setter
    def input_trigger(self, value: int):
        """
        Set the input trigger.

        Parameters:
            value: 0 - Internal trigger, 1 - External trigger
        """
        self.write(f'TRIG {value}')

    @property
    def measurement_mode(self):
        """Get the current measurement mode."""
        return self.query('WMOD?')

    @measurement_mode.setter
    def measurement_mode(self, mode: str):
        """
        Set the measurement mode.

        Parameters:
            mode: One of the supported modes:
                - CONST1: Constant Wavelength, No Auto Gain, SME mode
                - SWEEP1: Sweep Wavelength, No Auto Gain, SME mode
                - CONST2: Constant Wavelength, Auto Gain, SME mode
                - SWEEP2: Sweep Wavelength, Auto Gain, SME mode
                - FREE-RUN: Constant Wavelength, No Auto Gain, First Hardware Trigger Start (CME mode)
        """
        if mode not in ["CONST1", "SWEEP1", "CONST2", "SWEEP2", "FREE-RUN"]:
            raise ValueError("Invalid mode. Supported modes: CONST1, SWEEP1, CONST2, SWEEP2, FREE-RUN")
        self.write(f'WMOD {mode}')

    @property
    def wavelength(self):
        """Get the current wavelength in Constant Wavelength Measurement Mode (CONST1, CONST2)."""
        return self.query('WAV?')

    @wavelength.setter
    def wavelength(self, value: float):
        """
        Set the wavelength for Constant Wavelength Measurement Mode (CONST1, CONST2).

        Parameters:
            value: Wavelength in nm (1250.000 ~ 1630.000)
        """
        if not 1250.000 <= value <= 1630.000:
            raise ValueError("Wavelength must be between 1250.000 and 1630.000 nm.")
        self.write(f'WAV {value}')

    @property
    def wavelength_for_each_channel(self):
        """Get the wavelength for a specific module and channel in Constant Wavelength Measurement Mode."""
        return self.query('DWAV?')

    @wavelength_for_each_channel.setter
    def wavelength_for_each_channel(self, values: tuple):
        """
        Set the wavelength for a specific module and channel in Constant Wavelength Measurement Mode.

        Parameters:
            values: A tuple containing the following values:
                - value1: Module number (0-5), where 5 sets all channels and modules to the same wavelength
                - value2: Channel number (1-4)
                - value3: Wavelength in nm (1250.000 ~ 1630.000)
        """
        value1, value2, value3 = values
        if not 0 <= value1 <= 5:
            raise ValueError("Module value must be between 0 and 5.")
        if not 1 <= value2 <= 4:
            raise ValueError("Channel value must be between 1 and 4.")
        if not 1250.000 <= value3 <= 1630.000:
            raise ValueError("Wavelength must be between 1250.000 and 1630.000 nm.")

        self.write(f'DWAV {value1},{value2},{value3}')

    @property
    def sweep_wavelength_and_step(self):
        """Get the current sweep wavelength settings (start, stop, step)."""
        return self.query('WSET?')

    @sweep_wavelength_and_step.setter
    def sweep_wavelength_and_step(self, values: tuple):
        """
        Set the sweep wavelength parameters.

        Parameters:
            values: A tuple containing the following values:
                - start: Start wavelength (1250 ~ 1630 nm)
                - stop: Stop wavelength (1250 ~ 1630 nm)
                - step: Step wavelength (0.001 ~ 10 nm)
        """
        start, stop, step = values
        if not 1250 <= start <= 1630:
            raise ValueError("Start wavelength must be between 1250 and 1630 nm.")
        if not 1250 <= stop <= 1630:
            raise ValueError("Stop wavelength must be between 1250 and 1630 nm.")
        if not 0.001 <= step <= 10:
            raise ValueError("Step wavelength must be between 0.001 and 10 nm.")
        if stop <= start:
            raise ValueError("Stop wavelength must be greater than start wavelength.")

        self.write(f'WSET {start},{stop},{step}')

    @property
    def sweep_speed(self):
        """Get the current wavelength sweep speed."""
        return self.query('SPE?')

    @sweep_speed.setter
    def sweep_speed(self, speed: float):
        """
        Set the wavelength sweep speed.

        Parameters:
            speed: Sweep speed in nm/sec (0.001 ~ 200).

        Raises:
            ValueError: If the speed is out of the valid range (0.001 to 200).
        """
        if not 0.001 <= speed <= 200:
            raise ValueError("Sweep speed must be between 0.001 and 200 nm/sec.")
        self.write(f'SPE {speed}')

    @property
    def dynamic_range(self):
        """Get the current TIA gain setting."""
        return self.query('LEV?')

    @dynamic_range.setter
    def dynamic_range(self, dynamic_range: int):
        """
        Set the TIA gain for measuring modes like CONST1, SWEEP1, FREERUN, and AUTO1.

        Parameters:
            range: 1 to 5 for MPM-215 or 1 to 4 for MPM-213.
        """
        if dynamic_range not in [1, 2, 3, 4, 5]:
            raise ValueError("Invalid range. Valid values are 1, 2, 3, 4, or 5.")
        self.write(f'LEV {dynamic_range}')

    @property
    def dynamic_range_set2(self):
        """Get TIA Gain for CONST1, SWEEP1, FREERUN, AUTO1 measuring mode for each channel."""

        def get_gain(value1, value2):
            return self.query(f'DLEV? {value1},{value2}')

        return get_gain

    @dynamic_range_set2.setter
    def dynamic_range_set2(self, values):
        """
        Set TIA Gain for CONST1, SWEEP1, FREERUN, AUTO1 measuring mode for each channel.

        Parameters:
            values: A tuple containing (value1: module, value2: channel, value3: gain)
            value1: Module 0, 1, 2, 3, 4, 5
            value2: Channel 1, 2, 3, 4
            value3: Gain 1, 2, 3, 4, 5
        """
        value1, value2, value3 = values
        if value3 not in [1, 2, 3, 4, 5]:
            raise ValueError("Invalid gain value. Valid values are 1, 2, 3, 4, or 5.")
        self.write(f'DLEV {value1},{value2},{value3}')

    @property
    def average_time(self):
        """Get the average time."""
        return self.query('AVG?')

    @average_time.setter
    def average_time(self, time):
        """
        Set the average time.

        Parameters:
            time: A value between 0.01 and 10000.00 (in ms).
        """
        if not (0.01 <= time <= 10000.00):
            raise ValueError("Invalid time value. It must be between 0.01 and 10000.00 ms.")
        self.write(f'AVG {time}')

    @property
    def average_time_set2(self):
        """Get the average time (set2)."""
        return self.query('FGSAVG?')

    @average_time_set2.setter
    def average_time_set2(self, value):
        """
        Set the average time (set2).

        Parameters:
            value: A value between 0.01 and 10000.00 (in ms).
        """
        if not (0.01 <= value <= 10000.00):
            raise ValueError("Invalid value. It must be between 0.01 and 10000.00 ms.")
        self.write(f'FGSAVG {value}')

    @property
    def power_unit(self):
        """Get the current measuring unit for optical power or electrical current."""
        return self.query('UNIT?')

    @power_unit.setter
    def power_unit(self, value):
        """
        Set the measuring unit for optical power or electrical current.

        Parameters:
            value: 0 for dBm/dBmA, 1 for mW/mA
        """
        if value not in [0, 1]:
            raise ValueError("Invalid value. It must be 0 (for dBm/dBmA) or 1 (for mW/mA).")
        self.write(f'UNIT {value}')

    @property
    def power_mode(self):
        """Get the current power mode (Auto or Manual)."""
        return self.query('AUTO?')

    @power_mode.setter
    def power_mode(self, value):
        """
        Set the power mode (Auto or Manual).

        Parameters:
            value: 0 for Manual range, 1 for Auto range
        """
        if value not in [0, 1]:
            raise ValueError("Invalid value. It must be 0 (Manual range) or 1 (Auto range).")
        self.write(f'AUTO {value}')

    @property
    def power_mode_for_each_channel(self):
        """Get the power mode (Auto or Manual) for a specific module."""
        return self._power_mode_for_each_channel

    @power_mode_for_each_channel.setter
    def power_mode_for_each_channel(self, value):
        """
        Set the power mode (Auto or Manual) for each channel.

        Parameters:
            value: A tuple (module, range_mode)
            module: Module number (0 to 5)
            range_mode: 0 for Manual range, 1 for Auto range
        """
        module, range_mode = value
        if range_mode not in [0, 1]:
            raise ValueError("Invalid value. It must be 0 (Manual range) or 1 (Auto range).")
        self.write(f'DAUTO {module},{range_mode}')
        self._power_mode_for_each_channel = range_mode

    def power_of_single_module(self, module):
        """
        Get the optical power or electrical current for each channel of the selected module.

        Syntax:
            READ? <module>

        Parameters:
            <module>: Module Number (0, 1, 2, 3, 4)

        Response:
            <module>: Module Number (0, 1, 2, 3, 4)
            Response: <value1>,<value2>,<value3>,<value4>
            value1: Optical power of port 1
            value2: Optical power of port 2
            value3: Optical power of port 3
            value4: Optical power of port 4

        Example:
            READ? 0
            Response: -20.123,-20.454,-20.764,-20.644
        """
        response = self.query(f'READ? {module}').split(',')
        return response

    def wavelength_to_be_calibrated(self, module, index):
        """
        Get the wavelength that should be calibrated for the given module and index.

        Parameters:
            <module>: Module Number (0, 1, 2, 3, 4)
            <index>: Wavelength set order (1, 2, 3... 18, 19, 20)

        Response:
            <value>: Wavelength in nm

        Example:
            CWAV? 0,1
            Response: 1250

        Returns:
            float: Wavelength in nm to be calibrated.
        """
        response = self.query(f'CWAV? {module},{index}')
        return float(response)

    def power_calibration_of_calibrated_wavelength(self, module, channel, index):
        """
        Get the power calibration value of the wavelength from the "CWAV?" command index.

        Parameters:
            <module>: Module Number (0, 1, 2, 3, 4)
            <channel>: Port number (1, 2, 3, 4)
            <index>: Wavelength set order (1, 2, 3...18, 19)

        Response:
            <value>: Optical power offset in dB (float)

        Example:
            CWAVPO? 0,1,1
            Response: 0.904640

        Returns:
            float: Optical power offset in dB.
        """
        response = self.query(f'CWAVPO? {module},{channel},{index}')
        return float(response)

    def start_measurement(self):
        """Command to start measuring."""
        self.write('MEAS')

    def stop_measurement(self):
        """Command to stop measuring."""
        self.write('STOP')

    @property
    def logging_status(self):
        """
        Gets the latest measuring status and logging points.

        Response:
            <value1>,<value2>
                <value1>: Status
                    0 – Measuring is still in process.
                    1 – Measurement completed.
                    -1 – The measurement is forcibly stopped.
                <value2>: Measured logging point

        Example Response: 1,100
        """
        status, count = self.instance.query('STAT?').split(',')
        return int(status), int(count)

    @property
    def logging_data_point(self):
        """Get the current measurement logging point in CONST1/CONST2/FREE-RUN measuring mode."""
        response = self.query('LOGN?')
        return int(response)

    @logging_data_point.setter
    def logging_data_point(self, value: int):
        """
        Set measurement logging point in CONST1/CONST2/FREE-RUN measuring mode.
        Refer to the 5.6.3 Measurement logging setting (LOGN).

        Syntax:
            LOGN <value>

        Parameters:
            value: 1 ~ 1,000,000

        Default value: 1

        Example: LOGN 100
        """
        if not (1 <= value <= 1000000):
            raise ValueError("Measurement data point must be between 1 and 1,000,000.")
        self.write(f'LOGN {value}')

    def get_logging_data(self, module_no: int, channel_no: int):
        """
        Read out the logging logg.
        This command is not available for RS-232 communication.

        Example:    LOGG? 0,1
        """
        try:
            return self.instance.query_binary_values(f'LOGG? {module_no},{channel_no}',
                                                     datatype='f',
                                                     is_big_endian=False,
                                                     expect_termination=False)
        except Exception as e:
            print(f"Error while fetching logging data (query_binary_values): {e}")

        try:
            self.instance.write(f'LOGG? {module_no},{channel_no}')
            return self.instance.read_raw()
        except Exception as e:
            print(f"Error while fetching logging data (read_raw): {e}")


class ErrorCode(Enum):
    NO_ERROR = 0
    INVALID_CHARACTER = -101
    INVALID_SEPARATOR = -103
    DATA_TYPE_ERROR = -104
    PARAMETER_NOT_ALLOWED = -108
    MISSING_PARAMETER = -109
    COMMAND_HEADER_ERROR = -110
    UNDEFINED_HEADER = -113
    SETTING_CONFLICT = -221
    DATA_OUT_OF_RANGE = -222
    PROGRAM_RUNNING = -284
    DEVICE_SPECIFIC_ERROR = -300
    NOT_MEASUREMENT_MODULE = -301
    QUEUE_OVERFLOW = -350
    QUEUE_EMPTY = -351
    UPP_COMM_HEADER_ERROR = 101
    UPP_COMM_RSP_NO = 103
    UPP_COMM_MODULE_MISMATCHED = 104
    TCPIP_COMM_ERROR = 110
    GPIB_TX_NOT_COMPLETED = 116
    GPIB_TX_TIMER_EXPIRED = 117
    MC_TRIG_ERROR = 120
    SEM_NOT_EXIST = 210

    @staticmethod
    def get_error_description(error_code):
        error_descriptions = {
            ErrorCode.NO_ERROR: "No error",
            ErrorCode.INVALID_CHARACTER: "Invalid character. This occurs when unacceptable characters are received for Command or Parameter. Unacceptable characters: '%', '&', '$', '#', '~'.",
            ErrorCode.INVALID_SEPARATOR: "Invalid separator. This occurs when an unacceptable character is received as a separator between the Command and the Parameter. Unacceptable characters: '`', ';'.",
            ErrorCode.DATA_TYPE_ERROR: "Data type error. This occurs when the Parameter is not an acceptable data type.",
            ErrorCode.PARAMETER_NOT_ALLOWED: "Parameter not allowed. This occurs when the number of parameters in the corresponding command is more or less than expected.",
            ErrorCode.MISSING_PARAMETER: "Missing parameter. This occurs when the number of characters in the Parameter is longer than 18.",
            ErrorCode.COMMAND_HEADER_ERROR: "Command header error. This occurs when the number of characters in the Command is longer than 13.",
            ErrorCode.UNDEFINED_HEADER: "Undefined Header. This occurs when an unsupported command is received.",
            ErrorCode.SETTING_CONFLICT: "Setting conflict. This occurs when one of the following setup commands (other than STOP or STAT?) was received before measurement using 'MEAS' command is completed: AVG, LEV, LOGN, AUTO, WAVE, WMOD, WSET, SPE, LOOP, UNIT.",
            ErrorCode.DATA_OUT_OF_RANGE: "Data out of range. This occurs when the parameter is outside the acceptable value.",
            ErrorCode.PROGRAM_RUNNING: "Program currently running. This occurs when the mainframe delivers new commands to the module before the process of delivering commands to the module and receiving responses is completed.",
            ErrorCode.DEVICE_SPECIFIC_ERROR: "Device specific error. This occurs when the GPIB Address number that you are trying to set exceeds 32.",
            ErrorCode.NOT_MEASUREMENT_MODULE: "Is not Measurement Module. This occurs when user attempts to deliver a command to a module (slot) that is not installed.",
            ErrorCode.QUEUE_OVERFLOW: "Queue overflow. This occurs when the Queue space used for communication between internal Tasks is full, and there is no space to store information.",
            ErrorCode.QUEUE_EMPTY: "Queue empty. This occurs when there is no message in the Queue space used for communication between internal Tasks.",
            ErrorCode.UPP_COMM_HEADER_ERROR: "uPP Comm. Header Error. This occurs when the Headers of the Packet used to send and receive data between the mainframe and the module are different.",
            ErrorCode.UPP_COMM_RSP_NO: "uPP Comm. Rsp No. This occurs when the mainframe sends data information to the module but does not receive a response.",
            ErrorCode.UPP_COMM_MODULE_MISMATCHED: "uPP Comm. Module Mismatched. This occurs when the mainframe receives information from a different module than the one that sent the data.",
            ErrorCode.TCPIP_COMM_ERROR: "TCPIP Comm. Error. This occurs when all data to be transferred is not sent in TCP/IP communication.",
            ErrorCode.GPIB_TX_NOT_COMPLETED: "GPIB Tx not completed. This occurs when no event is delivered to the internal GPIB Task used for GPIB communication.",
            ErrorCode.GPIB_TX_TIMER_EXPIRED: "GPIB Tx Timer Expired. This occurs when all data to be transferred is not sent in GPIB communication.",
            ErrorCode.MC_TRIG_ERROR: "MC Trig. Error. This occurs when the mainframe does not receive a measurement completion signal (H/W signal) from the module after the measurement command was delivered to the module.",
            ErrorCode.SEM_NOT_EXIST: "not exist SEM. This occurs when an unregistered message is delivered between internal tasks.",
        }
        return error_descriptions.get(error_code, "Unknown error")
