"""
Script to retrieve TSL wavelength data via LAN communication using PyVISA.
"""

import math
import pyvisa
from pyvisa import util  # For decoding IEEE 488.2 binary blocks
from tqdm import tqdm  # Progress bar during data transfer

# Initialize VISA resource manager
rm = pyvisa.ResourceManager()

# Define LAN socket resource for TSL (update IP and port if needed)
lan_resource = "TCPIP0::192.168.1.152::5000::SOCKET"

# Open connection to TSL over LAN
# Set read termination and timeout (in milliseconds)
tsl = rm.open_resource(lan_resource, read_termination="\r")
tsl.timeout = 4000

# Identify the instrument
idn = tsl.query('*IDN?')
print("IDN: ", idn)

# Query the number of wavelength data points available
count = int(tsl.query(':READout:POINts?'))
print("LOGGING POINTS: ", count)

# Estimate the expected byte size of the binary response:
# - Each point = 4 bytes (assuming 32-bit integers)
# - 2 bytes for IEEE header ('#n')
# - 1 byte for separator
# - log10(count) = digits in byte count of the payload
expected_size = count * 4 + (2 + 1 + int(math.log10(count)))

# Begin data transfer with a visual progress bar
with tqdm(total=expected_size, unit='B', unit_scale=True) as progress:
    # Send query command for wavelength data
    tsl.write(':READout:DATa?')

    # Read the raw binary block from the device
    response = tsl.read_bytes(count=expected_size, monitoring_interface=progress)

# Decode the IEEE 488.2 binary block into a list of integers
data = util.from_ieee_block(response, datatype='i')  # 'i' = signed 32-bit integer
# Print the number of data points received
print("Number of data points received:", len(data))

# Convert integers to floating-point nanometer values (assumed units: pico-meters × 10^4)
rounded = [float(f"{num / 10000:.4f}") for num in data]
print("Converted Wavelengths (nm):")
print(rounded)
