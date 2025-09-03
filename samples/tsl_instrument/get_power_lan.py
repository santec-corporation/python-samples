"""
Script to retrieve TSL power data via LAN communication using PyVISA.
"""

import math
import pyvisa
from pyvisa import util  # For parsing IEEE 488.2 binary block data
from tqdm import tqdm  # For showing a progress bar during data transfer

# Create a VISA resource manager to manage instrument communication
rm = pyvisa.ResourceManager()

# Define the LAN socket address of the TSL instrument (IP address and port)
lan_resource = "TCPIP0::192.168.1.101::5000::SOCKET"

# Open a connection to the TSL instrument
# Specify "\r" (carriage return) as the read termination character
tsl = rm.open_resource(lan_resource, read_termination="\r")

# Query and display the identification string of the connected TSL instrument
idn = tsl.query('*IDN?')
print("IDN: ", idn)

# Query how many power data points are available for reading
count = int(tsl.query('READout:POINts?'))
print("LOGGING POINTS: ", count)

# Estimate the expected size of the binary response:
# - 4 bytes per data point
# - +2 for the IEEE block header ("#n")
# - +1 for possible delimiter or header character
# - +log10(count) for digit count in the data length
expected_size = count * 4 + (2 + 1 + int(math.log10(count)))

# Create a progress bar for monitoring the binary read
with tqdm(total=expected_size, unit='B', unit_scale=True) as progress:
    # Send the command to retrieve the binary power data
    tsl.write(':READout:DATa:POWer?')

    # Read the raw binary block from the instrument
    response = tsl.read_bytes(count=expected_size, monitoring_interface=progress)

# Decode the IEEE 488.2 binary block into a list of numerical values
data = util.from_ieee_block(response)

# Print the number of power values received
print(len(data))
