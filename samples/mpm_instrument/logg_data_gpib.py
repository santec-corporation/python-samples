# -*- coding: utf-8 -*-
"""
Script to retrieve MPM logging data via GPIB communication using PyVISA.
"""

import math
import pyvisa  # PyVISA is used for communicating with instruments over GPIB, USB, Serial, etc.
from tqdm import tqdm  # tqdm provides a progress bar for loops and data transfers

# Create a resource manager instance to handle VISA connections
rm = pyvisa.ResourceManager()

# Define the GPIB resource address of the instrument
gpib_resource = "GPIB0::16::INSTR"

# Open a connection to the instrument using the specified GPIB address
mpm = rm.open_resource(gpib_resource)

# Query and print the identification string of the connected instrument
idn = mpm.query('*IDN?')
print("IDN: ", idn)

# Query the number of log entries stored in the instrument
count = int(mpm.query('LOGN?'))
print("Logn: ", count)

# Calculate the expected size of the binary response:
# Each data point is 4 bytes, plus additional characters for message framing
# 2 = framing characters, 1 = comma or space, log10(count) = digits in the count (for formatting)
expected_size = count * 4 + (2 + 1 + int(math.log10(count)))

# Use a progress bar to monitor the binary data transfer
with tqdm(total=expected_size, unit='B', unit_scale=True) as progress:
    # Query the binary data using 'LOGG?' command and update the progress bar during transfer
    response = mpm.query_binary_values('LOGG? 0,1',
                                       data_points=expected_size,
                                       monitoring_interface=progress)

# Print the number of values received (this may help verify completeness)
print(len(response))
