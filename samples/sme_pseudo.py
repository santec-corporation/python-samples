"""
SME pseudo script.
Script to perform SME mode scan using Santec's TSL and custom PD via GPIB communication.

Last Updated: Mon Jan 27, 2025 15:52
Dependencies: pyvisa, numpy, time
"""

import time
import pyvisa
import numpy as np


# Initialize global variables
TSL = None  # Tunable Laser Source
PD = None  # Photo diode


def initialize_instruments():
    """Detects a TSL instrument via GPIB and initializes it."""
    global TSL, PD
    rm = pyvisa.ResourceManager()
    tools = [resource for resource in rm.list_resources() if 'GPIB' in resource]  # Filter GPIB devices
    for tool in tools:
        try:
            buffer = rm.open_resource(tool)
            idn = buffer.query("*IDN?")
            if 'TSL' in idn:
                TSL = buffer  # Assign TSL instrument
                TSL.read_termination = "\r\n"
                TSL.write_termination = "\r\n"
        except Exception as e:
            print(f"Error while opening {tool}: {e}")

    PD = rm.open_resource('GPIB0::10::INSTR')       # Replace the gpib resource of your photo diode.


def configure_tsl(power, start_wavelength, stop_wavelength, speed, step_size):
    """Configures the TSL instrument with the given parameters."""
    TSL.write('*CLS')  # Clear status
    TSL.write('*RST')  # Reset device
    TSL.write('SYST:COMM:GPIB:DEL 2')  # Set GPIB delimiter
    TSL.write('SYST:COMM:COD 1')  # Enable SCPI commands

    if TSL.query('POW:STAT?') == '0':  # Check if output is off
        TSL.write('POW:STAT 1')  # Turn on output
        while int(TSL.query('*OPC?')) == 0:  # Wait for operation to complete
            time.sleep(1)

    TSL.write('POW:UNIT 0')  # Set power unit to dBm
    TSL.write('WAV:UNIT 0')  # Set wavelength unit to nm
    TSL.write('COHCtrl 0')  # Disable coherence control
    TSL.write('POW:ATT:AUT 0')  # Disable automatic attenuation
    TSL.write('POW:ATT 0')  # Set attenuator value to 0
    TSL.write('AM:STAT 0')  # Disable amplitude modulation
    TSL.write('PW:SHUT 0')  # Open internal shutter

    TSL.write(':TRIG:OUTP 3')  # Set trigger output to step mode
    TSL.write('TRIG:INP:EXT 0')  # Disable external trigger

    # Configure sweep parameters
    TSL.write(f'POW {power}')  # Set output power
    TSL.write(f'WAV:SWE:STAR {start_wavelength}')  # Set start wavelength
    TSL.write(f'WAV:SWE:STOP {stop_wavelength}')  # Set stop wavelength
    TSL.write(f'WAV:SWE:SPE {speed}')  # Set sweep speed
    # step_size = float(speed) / 20000
    TSL.write(f'TRIG:OUTP:STEP {step_size}')  # Set trigger step size


def configure_PD(start_wavelength, stop_wavelength, speed, step_size):
    """Configures the PD instrument with the given parameters."""
    step_size = float(speed) / 20000  # Calculate step size based on speed

    # Insert the commands of the respective operatio
    PD.write('')  # Set measurement unit to dBm
    PD.write('')  # Set TIA gain level
    PD.write('')  # Set wavelength sweep mode
    PD.write(f'')  # Configure sweep parameters
    PD.write(f'')  # Set sweep speed
    PD.write('')  # Enable external trigger


def perform_sweep(start_wavelength):
    """Executes the wavelength sweep and triggers measurement."""
    TSL.write(f'WAV {start_wavelength}')  # Set starting wavelength
    TSL.write('TRIG:INP:STAN 1')  # Enable trigger standby mode

    input("Press any key to start to the sweep process.")

    print("Starting the SME process....")

    # Start measurement on PD
    PD.write('')        # Start PD measuring

    TSL.write(':WAV:SWE 1')  # Start sweep
    status = int(TSL.query(':WAV:SWE?'))
    while status != 3:
        # tsl.write(':WAV:SWE 1')
        status = int(TSL.query(':WAV:SWE?'))
        time.sleep(0.5)
    TSL.write(':WAV:SWE:SOFT')

    # Wait for PD measurement to complete
    while PD.query("").split(',')[0] == '0':
        time.sleep(0.1)

    print("SME process done.")


def fetch_data():
    """Fetches and returns logged data from the PD."""
    try:
        # Prompt user for module and channel numbers
        user_input = input("Enter the module and channel number to fetch data from (e.g., 0,1): ")
        module_no, channel_no = map(int, user_input.split(','))

        # Query PD for logged data
        data = PD.query_binary_values(f"")  # Insert the command of the PD to fetch the measurement data
        return data

    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        return []



def main():
    """Main workflow to initialize, configure, and perform the sweep."""
    initialize_instruments()

    if not TSL or not PD:
        print("Error: Instruments not detected.")
        return

    # Collect user inputs
    power = input("Input output power: ")
    start_wavelength = input("Input start wavelength: ")
    stop_wavelength = input("Input stop wavelength: ")
    speed = input("Input scan speed: ")
    step = float(input("Input step wavelength: "))

    # Configure instruments
    configure_tsl(power, start_wavelength, stop_wavelength, speed, step)
    configure_PD(start_wavelength, stop_wavelength, speed, step)

    # Perform sweep and fetch data
    perform_sweep(start_wavelength)
    data = fetch_data()

    # Output data
    print("Measurement complete. \nData length:", len(data))


if __name__ == "__main__":
    main()
