# -*- coding: utf-8 -*-
from tsl_information import AlertCode, CommandError


class TSL:
    def __init__(self, instance):
        """
        Initializes the TSL class with an opened PyVISA resource.

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
        self.query(f'*SRE {value}')

    @property
    def status_byte_register(self):
        """Gets the Status Byte Register (STBR)"""
        return int(self.query('*STB?'))

    @property
    def wavelength_unit(self):
        """Gets wavelength unit."""
        response = self.query(':WAV:UNIT?')
        return "nm" if response == '0' else "THz" if response == '1' else ""

    @wavelength_unit.setter
    def wavelength_unit(self, unit: int):
        """
        Sets wavelength unit.

        Parameter
            Unit:
                0: nm
                1: THz
        """
        self.write(f':WAV:UNIT {unit}')

    @property
    def wavelength(self):
        """Gets the wavelength value."""
        if self.wavelength_unit == 'THz':
            return self.query(':FREQ?')
        else:
            return self.query(':WAV?')

    @wavelength.setter
    def wavelength(self, value):
        """Sets the output wavelength."""
        if self.wavelength_unit == 'THz':
            self.write(f':FREQ {value}')
        else:
            self.write(f':WAV {value}')

    @property
    def fine_tuning(self):
        """Reads out Fine-Tuning value."""
        return float(self.query(':WAV:FIN?'))

    @fine_tuning.setter
    def fine_tuning(self, value: float):
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

    @property
    def coherence_control(self):
        """Reads out Coherence control status."""
        response = self.query(':COHC?')
        return "OFF" if response == '0' else "ON" if response == '1' else ""

    @coherence_control.setter
    def coherence_control(self, value: int):
        """
        Sets Coherence control status.

        Parameter
            0: Coherence control OFF
            1: Coherence control ON
        """
        self.write(f':COHC {value}')

    @property
    def optical_output_status(self):
        """Reads out optical output status."""
        response = self.query(':POW:STAT?')
        return "OFF" if response == '0' else "ON" if response == '1' else ""

    @optical_output_status.setter
    def optical_output_status(self, value: int):
        """
          Sets optical output status.

        Parameter
            0: optical output OFF
            1: optical output ON
        """
        self.write(f':POW:STAT {value}')

    @property
    def attenuator(self):
        """Reads out the attenuator value."""
        response = self.query(':POW:ATT?')
        return float(response)

    @attenuator.setter
    def attenuator(self, value: float):
        """
        Sets the attenuator value.

        Parameter:
            Range: 0 to 30 (dB)
            Step: 0.01 (dB)
        """
        self.write(f':POW:ATT {value}')

    @property
    def power_control_mode(self):
        """Reads out the setting of the power control."""
        response = self.query(':POW:ATT:AUT?')
        power_modes = {
            '0': "Manual mode",
            '1': "Auto mode"
        }
        return power_modes.get(response, "Unknown mode")

    @power_control_mode.setter
    def power_control_mode(self, value: int):
        """
        Sets the power control mode.

        Parameter:
            0: Manual mode
            1: Auto mode
        """
        self.write(f':POW:ATT:AUT {value}')

    @property
    def power(self):
        """Reads out optical output power level setting."""
        response = self.query(':POW?')
        return float(response)

    @power.setter
    def power(self, power: float):
        """
        Sets optical output power level.

        Parameter:
            Range: -15dBm to +13dBm
            Step: 0.01dB (0.01mW)

        @ Legacy <value> should be in decimal notation in “dBm” or “mW”.
        Units are defined by the command “:POWer:UNIT”.
        Character strings representing a unit cannot be accepted.

        SCPI <value> is accepted in decimal notation and exponential notation.
        When a unit character string is not specified, the default units are used.
        The default units are defined by the command “:POWer:UNIT”.
        """
        self.write(f':POW {power}')

    @property
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

    @property
    def internal_shutter_status(self):
        """Reads out the status of the internal shutter."""
        response = self.query(':POW:SHUT?')
        shutter_status = {
            '0': "Shutter Open",
            '1': "Shutter Close"
        }
        return shutter_status.get(response, "Unknown status")

    @internal_shutter_status.setter
    def internal_shutter_status(self, value: int):
        """
        Sets Open/Close status of the internal shutter.
        The function is the same as the Laser ON/OFF command “:POWer:STATe”
        (Note, the relationship between parameter and state is reversed).

        Parameter:
            0: Shutter Open
            1: Shutter Close
        """
        self.write(f':POW:SHUT {value}')

    @property
    def power_unit(self):
        """Reads out the unit of the power setting and display."""
        response = self.query(':POW:UNIT?')
        units = {
            '0': "dBm",
            '1': "mW"
        }
        return units.get(response, "Unknown unit")

    @power_unit.setter
    def power_unit(self, unit: int):
        """
        Changes the unit of the power setting and display.

        Parameter:
            0: dBm
            1: mW
        """
        self.write(f':POW:UNIT {unit}')

    @property
    def start_wavelength(self):
        """Reads out the sweep start wavelength."""
        if self.wavelength_unit == 'THz':
            return self.query(':FREQ:SWE:STAR?')
        else:
            return self.query(':WAV:SWE:STAR?')

    @start_wavelength.setter
    def start_wavelength(self, value):
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
        if self.wavelength_unit == 'THz':
            self.write(f':FREQ:SWE:STAR {value}')
        else:
            self.write(f':WAV:SWE:STAR {value}')

    @property
    def stop_wavelength(self):
        """Reads out the sweep stop wavelength."""
        if self.wavelength_unit == 'THz':
            return self.query(':FREQ:SWE:STOP?')
        else:
            return self.query(':WAV:SWE:STOP?')

    @stop_wavelength.setter
    def stop_wavelength(self, value):
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
        if self.wavelength_unit == 'THz':
            self.write(f':FREQ:SWE:STOP {value}')
        else:
            self.write(f':WAV:SWE:STOP {stop}')

    @property
    def minimum_sweep_wavelength(self):
        """Reads out the minimum wavelength in the configurable sweep range."""
        if self.wavelength_unit == 'THz':
            return self.query(':FREQ:SWE:RANG:MIN?')
        else:
            return self.query(':WAV:SWE:RANG:MIN?')

    @property
    def maximum_sweep_wavelength(self):
        """Reads out the maximum wavelength in the configurable sweep range."""
        if self.wavelength_unit == 'THz':
            return self.query(':FREQ:SWE:RANG:MAX?')
        else:
            return self.query(':WAV:SWE:RANG:MAX?')

    @property
    def sweep_mode(self):
        """Reads out the sweep mode."""
        response = int(self.query(':WAV:SWE:MOD?'))
        modes = {
            0: "Step sweep mode and One way",
            1: "Continuous sweep mode and One way",
            2: "Step sweep mode and Two way",
            3: "Continuous sweep mode and Two way"
        }
        return modes.get(response, "Unknown mode")

    @sweep_mode.setter
    def sweep_mode(self, mode: int):
        """
        Sets the sweep mode.

        Parameter
            0: Step sweep mode and One way
            1: Continuous sweep mode and One way
            2: Step sweep mode and Two way
            3: Continuous sweep mode and Two way
        """
        self.write(f':WAV:SWE:MOD {mode}')

    @property
    def sweep_speed(self):
        """Reads out sweep speed."""
        return float(self.query(':WAV:SWE:SPE?'))

    @sweep_speed.setter
    def sweep_speed(self, speed: int):
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

    @property
    def step_width(self):
        """Reads out the step of Step sweep mode."""
        if self.wavelength_unit == 'THz':
            return self.query(':FREQ:SWE:STEP?')
        else:
            return float(self.query(':WAV:SWE:STEP?'))

    @step_width.setter
    def step_width(self, step):
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
        if self.wavelength_unit == 'THz':
            self.write(f':FREQ:SWE:STEP {value}')
        else:
            self.write(f':WAV:SWE:STEP {step}')

    @property
    def sweep_dwell(self):
        """Reads out wait time between consequent steps in step sweep mode."""
        return float(self.query(':WAV:SWE:DWEL?'))

    @sweep_dwell.setter
    def sweep_dwell(self, value: float):
        """
        Sets wait time between consequent steps in step sweep mode.
        This wait time does not include time for wavelength tuning.

        Parameter
            Range: 0 to 999.9 sec
            Step: 0.1 sec
        """
        self.write(f':WAV:SWE:DWEL {value}')

    @property
    def sweep_cycles(self):
        """Reads out the setting sweep repetition times."""
        return int(self.query(':WAV:SWE:CYCL?'))

    @sweep_cycles.setter
    def sweep_cycles(self, cycle: int):
        """
        Sets the sweep repetition times.

        Parameter
            Range: 0 to 999
            Step: 1
        """
        self.write(f':WAV:SWE:CYCL {cycle}')

    @property
    def sweep_count(self):
        """Reads out the current number of completed sweeps."""
        return int(self.query(':WAV:SWE:COUN?'))

    @property
    def sweep_delay(self):
        """Reads out the setting wait time between consequent scans."""
        return float(self.query(':WAV:SWE:DEL?'))

    @sweep_delay.setter
    def sweep_delay(self, time: float):
        """
        Sets the wait time between consequent scans.

        Parameter
            Range: 0 to 999.9 sec
            Step: 0.1 sec
        """
        self.write(f':WAV:SWE:DEL {time}')

    @property
    def sweep_status(self):
        """Reads out the current sweep status."""
        response = self.query(':WAV:SWE?')
        statuses = {
            '0': "Stopped",
            '1': "Running",
            '3': "Standing by trigger",
            '4': "Preparation for sweep start"
        }
        return statuses.get(response, "Unknown status")

    @sweep_status.setter
    def sweep_status(self, status: int):
        """
        Sets sweep status.
        This command executes a single scan.

        Parameter
            0: Stop.
            1: Start.
        """
        self.write(f':WAV:SWE {status}')

    def repeat_scan(self):
        """Starts repeat scan."""
        self.query(':WAV:SWE:REP')

    @property
    def logging_count(self):
        """
        Reads out the number of logging data.

        Response
            0 to 500,000
        """
        return int(self.query(':READ:POIN?'))

    def wavelength_logging_data(self):
        """Reads out wavelength logging data."""
        try:
            return self.instance.query_binary_values('READ:DAT?')
        except Exception as e:
            print(f"Error while fetching wavelength logging data (query_binary_values): {e}")

        try:
            self.instance.write('READ:DAT?')
            return self.instance.read_raw()
        except Exception as e:
            print(f"Error while fetching wavelength logging data (read_raw): {e}")

    def power_logging_data(self):
        """Reads out power logging data."""
        try:
            return self.instance.query_binary_values(':READ:DAT:POW?')
        except Exception as e:
            print(f"Error while fetching power logging data (query_binary_values): {e}")

        try:
            self.instance.write(':READ:DAT:POW?')
            return self.instance.read_raw()
        except Exception as e:
            print(f"Error while fetching power logging data (read_raw): {e}")

    @property
    def modulation_function_status(self):
        """Reads out status of modulation function of the laser output."""
        response = self.query(':AM:STAT?')
        status = {
            '0': "Disable",
            '1': "Enable"
        }
        return status.get(response, "Unknown status")

    @modulation_function_status.setter
    def modulation_function_status(self, value: int):
        """
        Enables and disables the modulation function of the laser output.

        Parameter:
            0: Disable
            1: Enable
        """
        self.write(f':AM:STAT {value}')

    @property
    def modulation_source(self):
        """Reads out the modulation source."""
        response = self.query(':AM:SOUR?')
        modulation_sources = {
            '0': "Coherence control",
            '1': "Intensity modulation",
            '3': "Frequency modulation"
        }
        return modulation_sources.get(response, "Unknown source")

    @modulation_source.setter
    def modulation_source(self, value: int):
        """
        Sets modulation source.

        Parameter
            0: Coherence control
            1: Intensity modulation
            3: Frequency modulation
        """
        self.write(f':AM:SOUR {value}')

    @property
    def input_trigger(self):
        """Reads out the setting of external trigger input."""
        response = self.query(':TRIG:INP:EXT?')
        trigger_settings = {
            '0': "Disable",
            '1': "Enable"
        }
        return trigger_settings.get(response, "Unknown setting")

    @property
    def input_trigger_polarity(self):
        """Reads out input trigger polarity."""
        response = self.query(':TRIG:INP:ACT?')
        polarities = {
            '0': "High Active / Triggers at rising edge",
            '1': "Low Active / Triggers at falling edge"
        }
        return polarities.get(response, "Unknown polarity")

    @input_trigger_polarity.setter
    def input_trigger_polarity(self, value: int):
        """
        Sets input trigger polarity.

        Parameter
            0: High Active / Triggers at rising edge
            1: Low Active / Triggers at falling edge
        """
        self.write(f':TRIG:INP:ACT {value}')

    @property
    def trigger_signal_input_mode(self):
        """Reads out the trigger signal input standby mode."""
        response = self.query(':TRIG:INP:STAN?')
        input_modes = {
            '0': "Normal operation mode",
            '1': "Trigger standby mode"
        }
        return input_modes.get(response, "Unknown mode")

    @trigger_signal_input_mode.setter
    def trigger_signal_input_mode(self, signal: int):
        """
        Sets the device in trigger signal input standby mode.

        Parameter
            0: Normal operation mode
            1: Trigger standby mode
        """
        self.write(f':TRIG:INP:STAN {signal}')

    def software_trigger(self):
        """Issues a soft trigger. Executes sweep from trigger standby mode."""
        return self.write(':WAV:SWE:SOFT')

    @property
    def output_trigger_signal(self):
        """Reads out the timing setting of the trigger signal output."""
        response = self.query(':TRIG:OUTP?')
        trigger_states = {
            '0': "None",
            '1': "Stop",
            '2': "Start",
            '3': "Step"
        }
        return trigger_states.get(response, "Unknown state")

    @output_trigger_signal.setter
    def output_trigger_signal(self, signal: int):
        """
        Sets the timing of the trigger signal output.

        Parameter
            0: None
            1: Stop
            2: Start
            3: Step
        """
        self.write(f':TRIG:OUTP {signal}')

    @property
    def output_trigger_polarity(self):
        """Reads out output trigger polarity."""
        response = self.query(':TRIG:OUTP:ACT?')
        polarities = {
            '0': "High Active / Triggers at rising edge",
            '1': "Low Active / Triggers at falling edge"
        }
        return polarities.get(response, "Unknown polarity")

    @output_trigger_polarity.setter
    def output_trigger_polarity(self, value: int):
        """
        Sets output trigger polarity.

        Parameter
            0: High Active / Triggers at rising edge
            1: Low Active / Triggers at falling edge
        """
        self.write(f':TRIG:OUTP:ACT {value}')

    @property
    def trigger_step(self):
        """Reads out the interval of the trigger signal output."""
        return float(self.query(':TRIG:OUTP:STEP?'))

    @trigger_step.setter
    def trigger_step(self, value: float):
        """
        Sets the interval of the trigger signal output.

        Parameter
            Range：0.0001 〜 Maximum specified wavelength range (nm)
            Step：0.0001（nm）


            The minimum set trigger step depends on the setting sweep
            speed. Refer to “6-5. Trigger Setting” for details.

            Legacy <value> should be decimal notation in “nm”. Character strings
            representing a unit cannot be accepted.

            SCPI <value> is accepted in decimal notation and exponential
            notation. These numbers are followed by character strings
            representing a unit. When a unit character string is not
            specified, m（meter）is used as the default.
        """
        self.write(f':TRIG:OUTP:STEP {value}')

    @property
    def output_trigger_period_mode(self):
        """Reads out the output trigger period mode."""
        response = self.query(':TRIG:OUTP:SETT?')
        modes = {
            '0': "Output trigger is periodic in wavelength.",
            '1': "Output trigger is periodic in time."
        }
        return modes.get(response, "Unknown mode")

    @output_trigger_period_mode.setter
    def output_trigger_period_mode(self, value: int):
        """
        Sets the output trigger period mode.

        Parameter
            0: Sets the output trigger to be periodic in wavelength.
            1: Sets the output trigger to be periodic in time.
        """
        self.write(f':TRIG:OUTP:SETT {value}')

    @property
    def trigger_through_mode(self):
        """Reads out the trigger through mode."""
        response = self.query(':TRIG:THR?')
        if response is '0':
            return "OFF"
        elif response is '1':
            return "OFF"
        return ""

    @trigger_through_mode.setter
    def trigger_through_mode(self, value: int):
        """
        Sets the trigger through mode.

        Parameter
            0: OFF
            1: ON
        """
        self.write(f':TRIG:THR {value}')

    @property
    def error_info(self):
        """Reads out the error issued."""
        response = self.query(':SYST:ERR?').split()
        return CommandError[response].value if response in CommandError.__members__ else "Unknown Error"

    @property
    def gpib_address(self):
        """Reads out the GPIB address."""
        return int(self.query(':SYST:COMM:GPIB:ADDR?'))

    @gpib_address.setter
    def gpib_address(self, value: int):
        """
        Sets the GPIB address.

        Parameter
            Integer from 1 to 30
        """
        self.write(f':SYST:COMM:GPIB:ADDR {value}')

    @property
    def delimiter_gpib_communication(self):
        """Reads out the command delimiter for GPIB communication."""
        response = self.query(':SYST:COMM:GPIB:DEL?')
        if response is '0':
            return "CR"
        elif response is '1':
            return "LF"
        elif response is '2':
            return "CR+LF"
        elif response is '3':
            return "None"
        return ""

    @delimiter_gpib_communication.setter
    def delimiter_gpib_communication(self, value: int):
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

    @property
    def mac_address(self):
        """Reads out the MAC address."""
        return self.query(':SYST:COMM:ETH:MAC?')

    @property
    def ip_address(self):
        """Reads out the IP address."""
        return self.query(':SYST:COMM:ETH:IPAD?')

    @ip_address.setter
    def ip_address(self, value: str):
        """
        Sets the IP address.

        Parameter
            ***.***.***.*** (*** is integer from 0 to 255)
        """
        self.write(f':SYST:COMM:ETH:IPAD {value}')

    @property
    def subnet_mask(self):
        """Reads out the subnet mask."""
        return self.query(':SYST:COMM:ETH:SMAS?')

    @subnet_mask.setter
    def subnet_mask(self, value: str):
        """
        Sets the subnet mask.

        Parameter ***.***.***.*** (*** is integer from 0 to 255)
        """
        self.write(f':SYST:COMM:ETH:SMAS {value}')

    @property
    def default_gateway(self):
        """Reads out the default gateway."""
        return self.query(':SYST:COMM:ETH:DGAT?')

    @default_gateway.setter
    def default_gateway(self, value: str):
        """
        Sets the default gateway.

        Parameter
            ***.***.***.*** (*** is integer from 0 to 255)
        """
        self.write(f':SYST:COMM:ETH:DGAT {value}')

    @property
    def port_number(self):
        """Reads out the port number."""
        return int(self.query(':SYST:COMM:ETH:PORT?'))

    @port_number.setter
    def port_number(self, value: int):
        """
        Sets the port number.

        Parameter
            Integer from 0 to 65535
        """
        self.write(f':SYST:COMM:ETH:PORT {value}')

    @property
    def command_set(self):
        """Reads out the current set."""
        response = self.query(':SYST:COMM:COD?')
        if response == '0':
            return "Legacy"
        elif response == '1':
            return "SCPI"
        return ""

    @command_set.setter
    def command_set(self, value: int):
        """
        Sets the command set.

        Parameter
            0: Legacy
            1: SCPI
        """
        self.write(f':SYST:COMM:COD {value}')

    @property
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

    @property
    def display_brightness(self):
        """Reads out brightness of the display."""
        return int(self.query(':DISP:BRIG?'))

    @display_brightness.setter
    def display_brightness(self, value: int):
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

    @property
    def alert_information(self):
        """Reads out the current alert information."""
        response = self.query(':SYST:ALER?').split()
        return AlertCode[response].value if response in AlertCode.__members__ else "Unknown Error"

    @property
    def firmware_version(self):
        """Reads out the firmware version."""
        return self.query(':SYST:VERS?')

    @property
    def product_code(self):
        """Reads out the product code."""
        return self.query(':SYST:COD?')
