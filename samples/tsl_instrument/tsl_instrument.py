"""
TSL instrument class.
Command mode: Legacy
Communication: GPIB | LAN (PyVISA)

Last Updated: Tue Feb 04, 2025 11:00
"""

from enum import Enum


class TSL:
    def __init__(self, connection):
        """
        Initializes the TSL class with an opened PyVISA resource.

        Parameters:
            connection: An open PyVISA resource representing the connected instrument.
        """
        self.connection = connection

    def query(self, command):
        """
        Sends a query command to the instrument and returns the response.

        Parameters:
            command (str): The command to query the instrument.

        Returns:
            str: The response from the instrument.
        """
        return self.connection.query(command)

    def write(self, command):
        """
        Sends a write command to the instrument.

        Parameters:
            command (str): The command to send to the instrument.
        """
        self.connection.write(command)

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

    def get_wavelength_unit(self):
        """Gets wavelength unit."""
        response = self.query(':WAV:UNIT?')
        return "nm" if '0' in response else "THz" if '1' in response else ""

    def set_wavelength_unit(self, unit: int):
        """
        Sets wavelength unit.

        Parameter
            Unit:
                0: nm
                1: THz
        """
        self.write(f':WAV:UNIT {unit}')

    def get_wavelength(self):
        """Gets the wavelength value."""
        if self.get_wavelength_unit() == 'THz':
            return self.query(':FREQ?')
        else:
            return self.query(':WAV?')

    def set_wavelength(self, value):
        """Sets the output wavelength."""
        if self.get_wavelength_unit() == 'THz':
            self.write(f':FREQ {value}')
        else:
            self.write(f':WAV {value}')

    def get_fine_tuning(self):
        """Reads out Fine-Tuning value."""
        return float(self.query(':WAV:FIN?'))

    def set_fine_tuning(self, value: float):
        """
        Sets Fine-Tuning value.

        Parameter
            Range: -100.00 to +100.00
            Step: 0.01
        """
        self.write(f':WAV:FIN {value}')

    def disable_fine_tuning(self):
        """Terminates Fine-Tuning operation."""
        self.query(':WAV:FIN:DIS')

    def get_coherence_control(self):
        """Reads out Coherence control status."""
        response = self.query(':COHC?')
        return "OFF" if response == '0' else "ON" if response == '1' else ""

    def set_coherence_control(self, value: int):
        """
        Sets Coherence control status.

        Parameter
            0: Coherence control OFF
            1: Coherence control ON
        """
        self.write(f':COHC {value}')

    def get_optical_output_status(self):
        """Reads out optical output status."""
        response = self.query(':POW:STAT?')
        return "OFF" if response == '0' else "ON" if response == '1' else ""

    def set_optical_output_status(self, value: int):
        """
        Sets optical output status.

        Parameter
            0: Optical output OFF
            1: Optical output ON
        """
        self.write(f':POW:STAT {value}')

    def get_attenuator(self):
        """Reads out the attenuator value."""
        response = self.query(':POW:ATT?')
        return float(response)

    def set_attenuator(self, value: float):
        """
        Sets the attenuator value.

        Parameter:
            Range: 0 to 30 (dB)
            Step: 0.01 (dB)
        """
        self.write(f':POW:ATT {value}')

    def get_power_control_mode(self):
        """Reads out the setting of the power control."""
        response = self.query(':POW:ATT:AUT?')
        power_modes = {
            '0': "Manual mode",
            '1': "Auto mode"
        }
        return power_modes.get(response, "Unknown mode")

    def set_power_control_mode(self, value: int):
        """
        Sets the power control mode.

        Parameter:
            0: Manual mode
            1: Auto mode
        """
        self.write(f':POW:ATT:AUT {value}')

    def get_power(self):
        """Reads out optical output power level setting."""
        response = self.query(':POW?')
        return float(response)

    def set_power(self, power: float):
        """
        Sets optical output power level.

        Parameter:
            Range: -15dBm to +13dBm
            Step: 0.01dB (0.01mW)

        Legacy <value> should be in decimal notation in “dBm” or “mW”.
        Units are defined by the command “:POWer:UNIT”.
        Character strings representing a unit cannot be accepted.

        SCPI <value> is accepted in decimal notation and exponential notation.
        When a unit character string is not specified, the default units are used.
        The default units are defined by the command “:POWer:UNIT”.
        """
        self.write(f':POW {power}')

    def power_monitor(self):
        """
        Reads out monitored optical power. The value is measured by
        the built-in power monitor.

        Response
            Range: -15dBm to peak power
            Step: 0.01dB (0.01mW)
            Units are defined by the command “:POWer:UNIT”.
        """
        return float(self.query(':POW:ACT?'))

    def get_internal_shutter_status(self):
        """Reads out the status of the internal shutter."""
        response = self.query(':POW:SHUT?')
        shutter_status = {
            '0': "Shutter Open",
            '1': "Shutter Close"
        }
        return shutter_status.get(response, "Unknown status")

    def set_internal_shutter_status(self, value: int):
        """
        Sets Open/Close status of the internal shutter.
        The function is the same as the Laser ON/OFF command “:POWer:STATe”
        (Note, the relationship between parameter and state is reversed).

        Parameter:
            0: Shutter Open
            1: Shutter Close
        """
        self.write(f':POW:SHUT {value}')

    def get_power_unit(self):
        """Reads out the unit of the power setting and display."""
        response = self.query(':POW:UNIT?')
        units = {
            '0': "dBm",
            '1': "mW"
        }
        return units.get(response, "Unknown unit")

    def set_power_unit(self, unit: int):
        """
        Changes the unit of the power setting and display.

        Parameter:
            0: dBm
            1: mW
        """
        self.write(f':POW:UNIT {unit}')

    def get_start_wavelength(self):
        """Reads out the sweep start wavelength."""
        if self.get_wavelength_unit() == 'THz':
            return self.query(':FREQ:SWE:STAR?')
        else:
            return self.query(':WAV:SWE:STAR?')

    def set_start_wavelength(self, value):
        """
        Sets the sweep start wavelength.

        Parameter
            Range: Specified wavelength range

            If value in nm,
            Step: 0.1 pm

            Legacy <value> should be decimal notation in “nm”
            Character strings representing a unit cannot be accepted.

            SCPI <value> is accepted in decimal notation and exponential
            notation. These numbers are followed by character strings
            representing a unit. When a unit character string is not
            specified, m（meter）is used as the default.

            If value in THz,
             Step: 10MHz

            Legacy <value> should be decimal notation in “THz”
            Character strings representing a unit cannot be accepted.

            SCPI <value> is accepted in decimal notation and exponential
            notation. These numbers are followed by character strings
            representing a unit. When a unit character string is not
            specified, Hz（Hertz）is used as the default.
        """
        if not self.minimum_sweep_wavelength <= value <= self.maximum_sweep_wavelength:
            raise Exception(f"Value {value} out of range.")

        if self.get_wavelength_unit() == 'THz':
            self.write(f':FREQ:SWE:STAR {value}')
        else:
            self.write(f':WAV:SWE:STAR {value}')

    def get_stop_wavelength(self):
        """Reads out the sweep stop wavelength."""
        if self.get_wavelength_unit() == 'THz':
            return self.query(':FREQ:SWE:STOP?')
        else:
            return self.query(':WAV:SWE:STOP?')

    def set_stop_wavelength(self, value):
        """
        Sets the sweep stop wavelength.

        Parameter
            Range: Specified wavelength range

            If value in nm,
            Step: 0.1 pm

            Legacy <value> should be decimal notation in “nm”.
            Character strings representing a unit cannot be accepted.

            SCPI <value> is accepted in decimal notation and exponential
            notation. These numbers are followed by character strings
            representing a unit. When a unit character string is not
            specified, m（meter）is used as the default.

            If value in THz,
             Step: 10MHz

            Legacy <value> should be decimal notation in “THz”.
            Character strings representing a unit cannot be accepted.

            SCPI <value> is accepted in decimal notation and exponential
            notation. These numbers are followed by character strings
            representing a unit. When a unit character string is not
            specified, Hz（Hertz）is used as the default.
        """
        if not self.minimum_sweep_wavelength <= value <= self.maximum_sweep_wavelength:
            raise Exception(f"Value {value} out of range.")

        if self.get_wavelength_unit() == 'THz':
            self.write(f':FREQ:SWE:STOP {value}')
        else:
            self.write(f':WAV:SWE:STOP {value}')

    def minimum_sweep_wavelength(self):
        """Reads out the minimum wavelength in the configurable sweep range."""
        if self.wavelength_unit == 'THz':
            return float(self.query(':FREQ:SWE:RANG:MIN?'))
        else:
            return float(self.query(':WAV:SWE:RANG:MIN?'))

    def maximum_sweep_wavelength(self):
        """Reads out the maximum wavelength in the configurable sweep range."""
        if self.wavelength_unit == 'THz':
            return float(self.query(':FREQ:SWE:RANG:MAX?'))
        else:
            return float(self.query(':WAV:SWE:RANG:MAX?'))

    def get_sweep_mode(self):
        """Reads out the sweep mode."""
        response = int(self.query(':WAV:SWE:MOD?'))
        modes = {
            0: "Step sweep mode and One way",
            1: "Continuous sweep mode and One way",
            2: "Step sweep mode and Two way",
            3: "Continuous sweep mode and Two way"
        }
        return modes.get(response, "Unknown mode")

    def set_sweep_mode(self, mode: int):
        """
        Sets the sweep mode.

        Parameter
            0: Step sweep mode and One way
            1: Continuous sweep mode and One way
            2: Step sweep mode and Two way
            3: Continuous sweep mode and Two way
        """
        self.write(f':WAV:SWE:MOD {mode}')

    def get_sweep_speed(self):
        """Reads out sweep speed."""
        return float(self.query(':WAV:SWE:SPE?'))

    def set_sweep_speed(self, speed: int):
        """
        Sets the sweep speed.

        Parameter
            Range: 1 to 200 nm/s
            Selection (TSL-570): 1,2,5,10,20,50,100,200 (nm/s)
            Legacy <value> should be decimal notation in “nm/s”
            Character strings representing a unit cannot be accepted.

            SCPI <value> should be decimal notation in “nm/s”
            Character strings representing a unit cannot be accepted.
        """
        self.write(f':WAV:SWE:SPE {speed}')

    def get_step_width(self):
        """Reads out the step of Step sweep mode."""
        if self.get_wavelength_unit() == 'THz':
            return self.query(':FREQ:SWE:STEP?')
        else:
            return float(self.query(':WAV:SWE:STEP?'))

    def set_step_width(self, step):
        """
        Sets the step for Step sweep mode.

        Parameter
            If value in nm,
            Range: 0.1pm to specified wavelength span.
            Step: 0.1 pm

            Legacy <value> should be decimal notation in “nm”
            Character strings representing a unit cannot be accepted.

            SCPI <value> is accepted in decimal notation and exponential
            notation. These numbers are followed by character strings
            representing a unit. When a unit character string is not
            specified, meters are used as the default units.

            If value in THz,
            Range: 20MHz to specified wavelength span.
            Step: 10 MHz

            Legacy <value> should be decimal notation in “THz”
            Character strings representing a unit cannot be accepted.

            SCPI <value> is accepted in decimal notation and exponential
            notation. These numbers are followed by character strings
            representing a unit. When a unit character string is not
            specified, “Hz” is used as the default units.
        """
        if self.get_wavelength_unit() == 'THz':
            self.write(f':FREQ:SWE:STEP {step}')
        else:
            self.write(f':WAV:SWE:STEP {step}')

    def get_sweep_dwell(self):
        """Reads out wait time between consequent steps in step sweep mode."""
        return float(self.query(':WAV:SWE:DWEL?'))

    def set_sweep_dwell(self, value: float):
        """
        Sets wait time between consequent steps in step sweep mode.
        This wait time does not include time for wavelength tuning.

        Parameter
            Range: 0 to 999.9 sec
            Step: 0.1 sec
        """
        self.write(f':WAV:SWE:DWEL {value}')

    def get_sweep_cycles(self):
        """Reads out the setting sweep repetition times."""
        return int(self.query(':WAV:SWE:CYCL?'))

    def set_sweep_cycles(self, cycle: int):
        """
        Sets the sweep repetition times.

        Parameter
            Range: 0 to 999
            Step: 1
        """
        self.write(f':WAV:SWE:CYCL {cycle}')

    def get_sweep_count(self):
        """Reads out the current number of completed sweeps."""
        return int(self.query(':WAV:SWE:COUN?'))

    def get_sweep_delay(self):
        """Reads out the setting wait time between consequent scans."""
        return float(self.query(':WAV:SWE:DEL?'))

    def set_sweep_delay(self, time: float):
        """
        Sets the wait time between consequent scans.

        Parameter
            Range: 0 to 999.9 sec
            Step: 0.1 sec
        """
        self.write(f':WAV:SWE:DEL {time}')

    def get_sweep_status(self):
        """Reads out the current sweep status."""
        response = self.query(':WAV:SWE?')
        statuses = {
            '0': "Stopped",
            '1': "Running",
            '3': "Standing by trigger",
            '4': "Preparation for sweep start"
        }
        return statuses.get(response, "Unknown status")

    def set_sweep_status(self, status: int):
        """
        Sets sweep status.
        This command executes a single scan.

        Parameter
            0: Stop.
            1: Start.
        """
        self.write(f':WAV:SWE {status}')

    def start_sweep(self):
        """Starts the TSL sweep operation."""
        self.set_sweep_status(1)

    def stop_sweep(self):
        """Stops the TSL sweep operation."""
        self.set_sweep_status(0)

    def repeat_scan(self):
        """Starts repeat scan."""
        self.query(':WAV:SWE:REP')

    def get_logging_count(self):
        """
        Reads out the number of logging data.

        Response
            0 to 500,000
        """
        return int(self.query(':READ:POIN?'))

    def get_wavelength_logging_data(self):
        """Reads out wavelength logging data."""
        try:
            return self.connection.query_binary_values('READ:DAT?',
                                                       datatype='f',
                                                       is_big_endian=False,
                                                       expect_termination=False)
        except Exception as e:
            print(f"Error while fetching wavelength logging data (query_binary_values): {e}")

    def get_power_logging_data(self):
        """Reads out power logging data."""
        try:
            return self.connection.query_binary_values(':READ:DAT:POW?',
                                                       datatype='f',
                                                       is_big_endian=False,
                                                       expect_termination=False)
        except Exception as e:
            print(f"Error while fetching power logging data (query_binary_values): {e}")

    def get_modulation_function_status(self):
        """Reads out status of modulation function of the laser output."""
        response = self.query(':AM:STAT?')
        status = {
            '0': "Disable",
            '1': "Enable"
        }
        return status.get(response, "Unknown status")

    def set_modulation_function_status(self, value: int):
        """
        Enables and disables the modulation function of the laser output.

        Parameter:
            0: Disable
            1: Enable
        """
        self.write(f':AM:STAT {value}')

    def get_modulation_source(self):
        """Reads out the modulation source."""
        response = self.query(':AM:SOUR?')
        modulation_sources = {
            '0': "Coherence control",
            '1': "Intensity modulation",
            '3': "Frequency modulation"
        }
        return modulation_sources.get(response, "Unknown source")

    def set_modulation_source(self, value: int):
        """
        Sets modulation source.

        Parameter
            0: Coherence control
            1: Intensity modulation
            3: Frequency modulation
        """
        self.write(f':AM:SOUR {value}')

    def get_input_trigger(self):
        """Reads out the setting of external trigger input."""
        response = self.query(':TRIG:INP:EXT?')
        trigger_settings = {
            '0': "Disable",
            '1': "Enable"
        }
        return trigger_settings.get(response, "Unknown setting")

    def set_input_trigger(self, value: int):
        """
        Sets the external trigger input.

        Parameter
            0: Disable
            1: Enable
        """
        self.write(f':TRIG:INP:EXT {value}')

    def get_input_trigger_polarity(self):
        """Reads out input trigger polarity."""
        response = self.query(':TRIG:INP:ACT?')
        polarities = {
            '0': "High Active / Triggers at rising edge",
            '1': "Low Active / Triggers at falling edge"
        }
        return polarities.get(response, "Unknown polarity")

    def set_input_trigger_polarity(self, value: int):
        """
        Sets input trigger polarity.

        Parameter
            0: High Active / Triggers at rising edge
            1: Low Active / Triggers at falling edge
        """
        self.write(f':TRIG:INP:ACT {value}')

    def get_trigger_signal_input_mode(self):
        """Reads out the trigger signal input standby mode."""
        response = self.query(':TRIG:INP:STAN?')
        input_modes = {
            '0': "Normal operation mode",
            '1': "Trigger standby mode"
        }
        return input_modes.get(response, "Unknown mode")

    def set_trigger_signal_input_mode(self, signal: int):
        """
        Sets the device in trigger signal input standby mode.

        Parameter
            0: Normal operation mode
            1: Trigger standby mode
        """
        self.write(f':TRIG:INP:STAN {signal}')

    def software_trigger(self):
        """Issues a software trigger. Executes sweep from trigger standby mode."""
        return self.write(':WAV:SWE:SOFT')

    def get_output_trigger_signal(self):
        """Reads out the timing setting of the trigger signal output."""
        response = self.query(':TRIG:OUTP?')
        trigger_states = {
            '0': "None",
            '1': "Stop",
            '2': "Start",
            '3': "Step"
        }
        return trigger_states.get(response, "Unknown state")

    def set_output_trigger_signal(self, signal: int):
        """
        Sets the timing of the trigger signal output.

        Parameter
            0: None
            1: Stop
            2: Start
            3: Step
        """
        self.write(f':TRIG:OUTP {signal}')

    def get_output_trigger_polarity(self):
        """Reads out output trigger polarity."""
        response = self.query(':TRIG:OUTP:ACT?')
        polarities = {
            '0': "High Active / Triggers at rising edge",
            '1': "Low Active / Triggers at falling edge"
        }
        return polarities.get(response, "Unknown polarity")

    def set_output_trigger_polarity(self, value: int):
        """
        Sets output trigger polarity.

        Parameter
            0: High Active / Triggers at rising edge
            1: Low Active / Triggers at falling edge
        """
        self.write(f':TRIG:OUTP:ACT {value}')

    def get_trigger_step(self):
        """Reads out the interval of the trigger signal output."""
        return float(self.query(':TRIG:OUTP:STEP?'))

    def set_trigger_step(self, value: float):
        """
        Sets the interval of the trigger signal output.

        Parameter
            Range: 0.0001 to Maximum specified wavelength range (nm)
            Step: 0.0001 (nm)

            The minimum set trigger step depends on the setting sweep
            speed. Refer to “6-5. Trigger Setting” for details.

            Legacy <value> should be decimal notation in “nm”. Character strings
            representing a unit cannot be accepted.

            SCPI <value> is accepted in decimal notation and exponential
            notation. These numbers are followed by character strings
            representing a unit. When a unit character string is not
            specified, m (meter) is used as the default.
        """
        self.write(f':TRIG:OUTP:STEP {value}')

    def get_output_trigger_period_mode(self):
        """Reads out the output trigger period mode."""
        response = self.query(':TRIG:OUTP:SETT?')
        modes = {
            '0': "Output trigger is periodic in wavelength.",
            '1': "Output trigger is periodic in time."
        }
        return modes.get(response, "Unknown mode")

    def set_output_trigger_period_mode(self, value: int):
        """
        Sets the output trigger period mode.

        Parameter
            0: Sets the output trigger to be periodic in wavelength.
            1: Sets the output trigger to be periodic in time.
        """
        self.write(f':TRIG:OUTP:SETT {value}')

    def get_trigger_through_mode(self):
        """Reads out the trigger through mode."""
        response = self.query(':TRIG:THR?')
        if response == '0':
            return "OFF"
        elif response == '1':
            return "ON"
        return ""

    def set_trigger_through_mode(self, value: int):
        """
        Sets the trigger through mode.

        Parameter
            0: OFF
            1: ON
        """
        self.write(f':TRIG:THR {value}')

    # TODO: Rework the Error information method
    # def get_error_info(self):
    #     """Reads out the error issued."""
    #     response = self.query(':SYST:ERR?').split()
    #     return CommandError[response].value if response in CommandError.__members__ else "Unknown Error"

    def get_gpib_address(self):
        """Reads out the GPIB address."""
        return int(self.query(':SYST:COMM:GPIB:ADDR?'))

    def set_gpib_address(self, value: int):
        """
        Sets the GPIB address.

        Parameter
            Integer from 1 to 30
        """
        self.write(f':SYST:COMM:GPIB:ADDR {value}')

    def get_gpib_delimiter(self):
        """Reads out the command delimiter for GPIB communication."""
        response = self.query(':SYST:COMM:GPIB:DEL?')
        if response == '0':
            return "CR"
        elif response == '1':
            return "LF"
        elif response == '2':
            return "CR+LF"
        elif response == '3':
            return "None"
        return ""

    def set_gpib_delimiter(self, value: int):
        """
        Sets the command delimiter for GPIB communication. EOI is
        always sent.

        Parameter
            0: CR
            1: LF
            2: CR+LF
            3: None
        """
        self.write(f':SYST:COMM:GPIB:DEL {value}')

    def get_mac_address(self):
        """Reads out the MAC address."""
        return self.query(':SYST:COMM:ETH:MAC?')

    def get_ip_address(self):
        """Reads out the IP address."""
        return self.query(':SYST:COMM:ETH:IPAD?')

    def set_ip_address(self, value: str):
        """
        Sets the IP address.

        Parameter
            ***.***.***.*** (*** is integer from 0 to 255)
        """
        self.write(f':SYST:COMM:ETH:IPAD {value}')

    def get_subnet_mask(self):
        """Reads out the subnet mask."""
        return self.query(':SYST:COMM:ETH:SMAS?')

    def set_subnet_mask(self, value: str):
        """
        Sets the subnet mask.

        Parameter ***.***.***.*** (*** is integer from 0 to 255)
        """
        self.write(f':SYST:COMM:ETH:SMAS {value}')

    def get_default_gateway(self):
        """Reads out the default gateway."""
        return self.query(':SYST:COMM:ETH:DGAT?')

    def set_default_gateway(self, value: str):
        """
        Sets the default gateway.

        Parameter
            ***.***.***.*** (*** is integer from 0 to 255)
        """
        self.write(f':SYST:COMM:ETH:DGAT {value}')

    def get_port_number(self):
        """Reads out the port number."""
        return int(self.query(':SYST:COMM:ETH:PORT?'))

    def set_port_number(self, value: int):
        """
        Sets the port number.

        Parameter
            Integer from 0 to 65535
        """
        self.write(f':SYST:COMM:ETH:PORT {value}')

    def get_command_set(self):
        """Reads out the current set."""
        response = self.query(':SYST:COMM:COD?')
        if response == '0':
            return "Legacy"
        elif response == '1':
            return "SCPI"
        return ""

    def set_command_set(self, value: int):
        """
        Sets the command set.

        Parameter
            0: Legacy
            1: SCPI
        """
        self.write(f':SYST:COMM:COD {value}')

    def external_interlock(self):
        """
        Reads out the status of external interlock.

        Response
            0: Unlocked
            1: External interlocked
        """
        response = self.query(':SYST:LOCK?')
        if response == '0':
            return "Unlocked"
        elif response == '1':
            return "External interlocked"
        return ""

    def get_display_brightness(self):
        """Reads out brightness of the display."""
        return int(self.query(':DISP:BRIG?'))

    def set_display_brightness(self, value: int):
        """
        Sets brightness of the display.

        Parameters:
            Brightness level from 0 to 100.
        """
        if not 0 <= value <= 100:
            raise ValueError("Brightness value must be between 0 and 100.")

        self.write(f':DISP:BRIG {value}')

    def shutdown(self):
        """Shuts down the device."""
        self.write(':SPEC:SHUT')

    def reboot(self):
        """Restarts the device."""
        self.write(':SPEC:REB')

    # TODO: Rework the Alert information method
    # def get_alert_information(self):
    #     """Reads out the current alert information."""
    #     response = self.query(':SYST:ALER?').split()
    #     return AlertCode[response].value if response in AlertCode.__members__ else "Unknown Error"

    def get_firmware_version(self):
        """Reads out the firmware version."""
        return self.query(':SYST:VERS?')

    def get_product_code(self):
        """Reads out the product code."""
        return self.query(':SYST:COD?')


class AlertCode(Enum):
    No00 = "Power supply Error1"
    No02 = "Power supply Error2"
    No03 = "Power supply Error3"
    No04 = "Power setting error (Unconfigurable power)"
    No05 = "Wavelength Error"
    No06 = "Attenuator Error"
    No07 = "Interlock detection"
    No20 = "Temperature control Error1"
    No21 = "Temperature control Error2"
    No22 = "Temperature control Error3"
    No23 = "Temperature control Error4"
    No24 = "Sensor Error1"
    No25 = "Shutter Error"
    No26 = "Sensor Error2"
    No27 = "Connection Error"
    No30 = "Exhaust Fan Error"


class CommandError(Enum):
    NoError = "No error"
    SyntaxError = "Syntax error"
    InvalidSeparator = "Invalid separator"
    ParameterNotAllowed = "Parameter not allowed"
    MissingParameter = "Missing parameter"
    UndefinedHeader = "Undefined header"
    CharacterDataNotAllowed = "Character data not allowed"
    ExecutionError = "Execution error"
    DataOutOfRange = "Data out of range"
    QueryInterrupted = "Query INTERRUPTED"
