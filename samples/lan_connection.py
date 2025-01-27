import pyvisa

# Initialize the PyVISA resource manager
rm = pyvisa.ResourceManager()

# Define instrument connection details
instrument_ip_address = '192.168.1.155'  # IP address of the instrument
instrument_port = '5000'  # Port number for the instrument

# Create the LAN resource string for the instrument
instrument_lan_resource = f'TCPIP::{instrument_ip_address}::{instrument_port}::SOCKET'

# Open a connection to the instrument
instrument = rm.open_resource(instrument_lan_resource,
                              read_termination='\r')     # Define the termination character for reading responses

# Set a timeout for communication (in milliseconds)
instrument.timeout = 5000

# Query the instrument for its identification string (IDN)
idn = instrument.query('*IDN?')
print(f"Instrument Identification: {idn}")
