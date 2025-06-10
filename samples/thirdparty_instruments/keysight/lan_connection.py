import pyvisa

# Initialize the PyVISA resource manager
rm = pyvisa.ResourceManager()

# Define instrument connection details
# This the VXI-11 LAN protocol Ethernet IP Address
instrument_ip_address = "192.168.1.170::inst()"     # Replace with the IP address of your instrument

# Create the LAN resource string for the instrument
instrument_lan_resource = f'TCPIP::{instrument_ip_address}::INSTR'

# Open a connection to the instrument
instrument = rm.open_resource(instrument_lan_resource)

# Set a timeout for communication (in milliseconds)
instrument.timeout = 5000

# Query the instrument for its identification string (IDN)
idn = instrument.query('*IDN?')
print(f"Instrument Identification: {idn}")
