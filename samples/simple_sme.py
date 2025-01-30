# -*- coding: utf-8 -*-
"""
Simple SME.
Script to perform SME mode scan.
Instruments: Santec TSL and MPM
Command mode: Legacy
Communication: GPIB

Last Updated: Thu Jan 30, 2025 13:46
Dependencies: pyvisa, numpy, time
"""

import time
import pyvisa
import numpy as np

# Initialize global variables
TSL = None  # Tunable Laser Source
MPM = None  # Multi-Channel Power Meter


def initialize_instruments():
    """Detects instruments via GPIB and initializes TSL and MPM."""
    global TSL, MPM
    rm = pyvisa.ResourceManager()
    tools = [resource for resource in rm.list_resources() if 'GPIB' in resource]  # Filter GPIB devices
    for tool in tools:
        try:
            buffer = rm.open_resource(tool)
            idn = buffer.query("*IDN?")
            if 'TSL' in idn:
                TSL = buffer  # Assign TSL instrument
                TSL.read_termination = '\r\n'
            elif 'MPM' in idn:
                MPM = buffer  # Assign MPM instrument
                MPM.read_termination = '\n'
        except Exception as e:
            print(f"Error while opening {tool}: {e}")


def configure_tsl(power, start_wavelength, stop_wavelength, speed, step_size):
    """Configures the TSL instrument with the given parameters."""
    TSL.write('*CLS')  # Clear status
    TSL.write('*RST')  # Reset device
    TSL.write('SYST:COMM:GPIB:DEL 2')  # Set GPIB delimiter
    TSL.write('SYST:COMM:COD 0')  # Enable Legacy commands

    if TSL.query('POW:STAT?') == '0':  # Check if output is off
        TSL.write('POW:STAT 1')  # Turn on output
        while int(TSL.query('*OPC?')) == 0:  # Wait for operation to complete
            time.sleep(1)

    TSL.write('POW:UNIT 0')  # Set power unit to dBm
    TSL.write('WAV:UNIT 0')  # Set wavelength unit to nm
    TSL.write('COHCtrl 0')  # Disable coherence control
    TSL.write('POW:ATT:AUT 1')  # Auto power control mode
    # TSL.write('POW:ATT 0')  # Set attenuator value to 0
    TSL.write('AM:STAT 0')  # Disable amplitude modulation
    TSL.write(':POW:SHUT 0')  # Open the internal shutter

    TSL.write(':TRIG:OUTP 3')  # Set trigger output to step mode
    TSL.write('TRIG:INP:EXT 0')  # Disable external trigger

    # Configure sweep parameters
    TSL.write(f'POW {power}')  # Set output power
    TSL.write(f'WAV:SWE:STAR {start_wavelength}')  # Set start wavelength
    TSL.write(f'WAV:SWE:STOP {stop_wavelength}')  # Set stop wavelength
    TSL.write(f'WAV:SWE:SPE {speed}')  # Set sweep speed
    TSL.write(f'TRIG:OUTP:STEP {step_size}')  # Set trigger step size


def configure_mpm(start_wavelength, stop_wavelength, speed, step_size):
    """Configures the MPM instrument with the given parameters."""
    MPM.write('UNIT 0')  # Set measurement unit to dBm
    MPM.write('LEV 1')  # Set TIA gain level
    MPM.write('WMOD SWEEP1')  # Set wavelength sweep mode
    MPM.write('TRIG 1')  # Enable external trigger
    MPM.write(f'WSET {start_wavelength},{stop_wavelength},{step_size}')  # Configure sweep parameters
    MPM.write(f'SPE {speed}')  # Set sweep speed


def perform_sweep(start_wavelength):
    """Executes the wavelength sweep and triggers measurement."""
    TSL.write(f'WAV {start_wavelength}')  # Set starting wavelength
    TSL.write('TRIG:INP:STAN 1')  # Enable trigger standby mode
    TSL.write('WAV:SWE 1')  # Start sweep

    input("Press any key to start to the sweep process.")

    # Wait for sweep to complete
    while TSL.query('WAV:SWE?') != '3':
        time.sleep(0.1)

    print("Starting the SME process....")

    # Start measurement on MPM
    MPM.write('MEAS')

    # Issue software trigger to the TSL
    TSL.write('WAV:SWE:SOFT')

    # Wait for measurement to complete
    while MPM.query("STAT?").split(',')[0] == '0':
        print(MPM.query("STAT?"))
        time.sleep(0.1)

    print("SME process done.")


def fetch_data():
    """Fetches and returns logged data from the MPM."""
    try:
        # Prompt user for module and channel numbers
        user_input = input("Enter the module and channel number to fetch data from (e.g., 0,1): ")
        module_no, channel_no = map(int, user_input.split(','))

        # Query MPM for logged data
        data = MPM.query_binary_values(
            f"LOGG? {module_no},{channel_no}",
            datatype='f',
            expect_termination=False,
            is_big_endian=False
        )
        return data

    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        return []


def main():
    """Main workflow to initialize, configure, and perform the sweep."""
    initialize_instruments()

    if not TSL or not MPM:
        print("Error: Instruments not detected.")
        return

    # Collect user inputs
    power = input("Input output power: ")
    start_wavelength = input("Input start wavelength: ")
    stop_wavelength = input("Input stop wavelength: ")
    speed = input("Input scan speed: ")

    # Calculate step size
    calculated_step_size = float(speed) / 20000
    if calculated_step_size <= 0.001:
        calculated_step_size = 0.002
    elif calculated_step_size > 10.001:
        calculated_step_size = 10.000

    # Configure instruments
    configure_tsl(power, start_wavelength, stop_wavelength, speed, calculated_step_size)
    configure_mpm(start_wavelength, stop_wavelength, speed, calculated_step_size)

    # Perform sweep and fetch data
    perform_sweep(start_wavelength)
    data = fetch_data()

    # Output data
    print("Measurement complete. \nData:", data)


if __name__ == "__main__":
    main()
