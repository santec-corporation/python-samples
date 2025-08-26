#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SME Measurement Script
-----------------------
It performs a wavelength sweep and collects power measurement data.

NOTE: This works only with the MPM-215 module.

Units:
    - Wavelength: nanometers (nm)
    - Power: dBm

Requirements:
    - Python 3 (Linux recommended)
    - PyVISA installed (pip install pyvisa)
    - VISA backend (NI-VISA or pyvisa-py)

Connections:
    - Update the IP addresses of your TSL and MPM in the script if they are different.

Author:
    Santec Holdings Corporation

Date:
    2025-08-26
"""

import time
import math
import pyvisa
from pyvisa import util


def setup_laser(tsl, power, start_nm, stop_nm, speed, step_nm):
    """Configure the TSL."""
    # Reset and basic setup
    tsl.write('*CLS')
    tsl.write('*RST')
    tsl.write('SYST:COMM:GPIB:DEL 0')
    tsl.write('SYST:COMM:COD 0')

    # Turn on output if off
    if tsl.query('POW:STAT?').strip() == '0':
        tsl.write('POW:STAT 1')
        while tsl.query('*OPC?').strip() == '0':
            time.sleep(1)

    # Units and modes
    tsl.write('POW:UNIT 0')  # Power in dBm
    tsl.write('WAV:UNIT 0')  # Wavelength in nm
    tsl.write('POW:ATT:AUT 1')  # Auto power control
    tsl.write('POW:SHUT 0')  # Open shutter

    # Trigger and sweep
    tsl.write('TRIG:OUTP 3')  # Trigger per step
    tsl.write('TRIG:INP:EXT 0')  # No external trigger
    tsl.write('TRIG:INP:STAN 1')  # Standby mode
    tsl.write('WAV:SWE:MOD 1')  # One-way continuous sweep

    # Sweep parameters
    tsl.write(f'POW {power}')
    tsl.write(f'WAV:SWE:STAR {start_nm}')
    tsl.write(f'WAV:SWE:STOP {stop_nm}')
    tsl.write(f'WAV:SWE:SPE {speed}')
    tsl.write(f'TRIG:OUTP:STEP {step_nm}')
    tsl.write('TRIG:OUTP:SETT')
    tsl.write('TRIG:INP:ACT 0')
    tsl.write('TRIG:OUTP:ACT 0')


def setup_meter(mpm, start_nm, stop_nm, speed, step_nm, data_count):
    """Configure the MPM."""
    mpm.write('STOP')  # Stop any old measurement
    mpm.write('UNIT 0')  # dBm
    time.sleep(0.5)
    mpm.write('WMOD SWEEP2')  # Set the SWEEP2 measurement mode
    while True:
        if 'SWEEP2' in mpm.query('WMOD?'):
            break
        mpm.write('WMOD SWEEP2')
    print("Sweep mode: ", mpm.query('WMOD?'))
    mpm.write('TRIG 1')  # Enable external trigger
    mpm.write(f'WSET {start_nm},{stop_nm},{step_nm}')
    mpm.write(f'SPE {speed}')
    average_wavelength = (start_nm + stop_nm) / 2
    mpm.write(f'WAV {average_wavelength}')
    # mpm.write(f'LOGN {data_count}')    # Do not set when using SWEEP2/CONST2 measurement modes


def run_sweep(tsl, mpm, start_nm):
    """Start sweep and wait until finished."""
    tsl.write(f'WAV {start_nm}')
    input("Press Enter to start the sweep...")

    mpm.write('MEAS')
    tsl.write(':WAV:SWE 1')

    # Wait until laser starts sweeping
    while int(tsl.query(':WAV:SWE?')) != 3:
        time.sleep(0.2)

    tsl.write(':WAV:SWE:SOFT')  # Software trigger

    # Monitor meter status until done
    status = mpm.query('STAT?').split(',')
    while status[0] == '0':
        print("MPM Status:", status)
        time.sleep(0.2)
        status = mpm.query('STAT?').split(',')

    print("Sweep finished. Final status:", status)


def get_data(mpm):
    """Fetch measurement data."""
    count = int(mpm.query('LOGN?'))
    print("Data points:", count)

    # Expected binary size
    expected_size = count * 4 + (3 + int(math.log10(count)))

    # Ask user which channel to fetch
    module, channel = input("Enter module,channel (e.g. 0,1): ").split(',')
    mpm.write(f'LOGG? {module},{channel}')

    # Read binary block
    response = mpm.read_bytes(expected_size)
    values = util.from_ieee_block(response)

    return values


def main():
    rm = pyvisa.ResourceManager()

    # Connect to instruments (update IPs if different)
    tsl = rm.open_resource('TCPIP::192.168.1.100::5000::SOCKET', read_termination='\r')
    mpm = rm.open_resource('TCPIP::192.168.1.161::5000::SOCKET', read_termination='\r\n')
    tsl.timeout = mpm.timeout = 5000

    # Ask user for scan settings
    power = float(input("Output power (dBm): "))
    start_nm = float(input("Start wavelength (nm): "))
    stop_nm = float(input("Stop wavelength (nm): "))
    speed = float(input("Scan speed (nm/s): "))
    step_nm = float(input("Step size (nm): "))

    # Calculate and set the total data count
    data_count = int((stop_nm - start_nm) / step_nm + 1)

    # Configure instruments
    setup_laser(tsl, power, start_nm, stop_nm, speed, step_nm)
    setup_meter(mpm, start_nm, stop_nm, speed, step_nm, data_count)

    # Run sweep and fetch results
    run_sweep(tsl, mpm, start_nm)
    data = get_data(mpm)

    print("Measurement complete.")
    print("Total points:", len(data))
    # print(data)


if __name__ == "__main__":
    main()
