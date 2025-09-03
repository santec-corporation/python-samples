"""
Script to retrieve MPM logging data via LAN communication using PyVISA.
"""

import math
import pyvisa
from pyvisa import util  # Used for decoding binary block data (IEEE 488.2 format)
from tqdm import tqdm  # tqdm provides a nice progress bar for data transfers

# Create a VISA resource manager to handle communication with instruments
rm = pyvisa.ResourceManager()

# Define the LAN socket address of the instrument (IP, port)
lan_resource = "TCPIP0::192.168.1.161::5000::SOCKET"

# Open a socket connection to the instrument with the specified read termination character
mpm = rm.open_resource(lan_resource, read_termination="\r")

# Query the instrument for its identification string
idn = mpm.query('*IDN?')
print("IDN: ", idn)

# Query how many log entries are available on the device
count = int(mpm.query('LOGN?'))
print("Logn: ", count)

# Calculate the expected size of the binary data:
# - Each data point is 4 bytes
# - Add 2 bytes for IEEE block header (usually "#n" + n digits)
# - Add 1 for comma or extra header character
# - Add int(log10(count)) for digit count in data length
# - Add 1 as buffer or termination byte
expected_size = count * 4 + (2 + 1 + int(math.log10(count))) + 1

# Initialize a progress bar to show transfer progress
with tqdm(total=expected_size, unit='B', unit_scale=True) as progress:
    # Send command to begin binary data transfer
    mpm.write('LOGG? 0,1')

    # Read the raw bytes from the instrument
    response = mpm.read_bytes(count=expected_size, monitoring_interface=progress)

# Convert the binary response (in IEEE 488.2 block format) to a list of values
data = util.from_ieee_block(response)

# Print the number of data points retrieved
print(len(data))
