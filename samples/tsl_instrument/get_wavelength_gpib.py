# -*- coding: utf-8 -*-
"""
Script to retrieve TSL wavelength data via GPIB communication using PyVISA.
"""

import math
import pyvisa
from tqdm import tqdm  # For progress display during data transfer

# Create a VISA resource manager
rm = pyvisa.ResourceManager()

# Define the GPIB resource address of the TSL instrument
gpib_resource = "GPIB0::3::INSTR"

# Open the connection to the TSL device over GPIB
tsl = rm.open_resource(gpib_resource)

# Query the instrument's identification string
idn = tsl.query('*IDN?')
print("IDN: ", idn)

# Query the number of wavelength data points available
count = int(tsl.query('READout:POINts?'))
print("LOGGING POINTS: ", count)

# Estimate the size of the incoming IEEE 488.2 binary block:
# - 4 bytes per data point
# - 2 bytes for the block header start
# - 1 byte for separator (optional)
# - digits for the length specifier (log10(count))
expected_size = count * 4 + (2 + 1 + int(math.log10(count)))

# Read the binary data with a progress bar
with tqdm(total=expected_size, unit='B', unit_scale=True) as progress:
    response = tsl.query_binary_values(':READout:DATa?',
                                       datatype='i',  # 'i' = 32-bit signed integer
                                       chunk_size=expected_size,
                                       monitoring_interface=progress)

# Print the number of data points received
print("Number of values received:", len(response))

# Convert integers to float (assume a conversion factor = 1e-4 for pico-meters → nanometers)
rounded = [float(f"{num / 10000:.4f}") for num in response]
print("Converted Wavelengths (nm):")
print(rounded)
