"""
Script to retrieve TSL power data via GPIB communication using PyVISA.
"""

import math
import time
import pyvisa
from tqdm import tqdm  # For displaying a progress bar during binary data transfer

# Initialize the VISA resource manager
rm = pyvisa.ResourceManager()

# Define the GPIB address of the TSL instrument
gpib_resource = "GPIB0::3::INSTR"

# Open a connection to the TSL instrument over GPIB
tsl = rm.open_resource(gpib_resource)

# Query the instrument identification string
idn = tsl.query('*IDN?')
print("IDN: ", idn)

# Query how many power logging points are available
count = int(tsl.query('READout:POINts?'))
print("LOGGING POINTS: ", count)

# Estimate the expected size of the binary data transfer:
# - Each data point is 4 bytes (typically 32-bit integer or float)
# - +2 bytes for IEEE block header start (e.g., '#')
# - +1 byte for separator (optional)
# - +log10(count) for number of digits in the block length specifier
expected_size = count * 4 + (2 + 1 + int(math.log10(count)))

# Progress bar for monitoring data transfer
with tqdm(total=expected_size, unit='B', unit_scale=True) as progress:
    # Query the binary data from the instrument
    # - datatype='i': interpret data as 32-bit signed integers
    # - chunk_size: controls how many bytes to read at a time
    # - monitoring_interface: connects tqdm to the read progress
    response = tsl.query_binary_values(':READout:DATa:POWer?',
                                       datatype='i',
                                       chunk_size=expected_size,
                                       monitoring_interface=progress)

# Print the number of data points received
print(len(response))
