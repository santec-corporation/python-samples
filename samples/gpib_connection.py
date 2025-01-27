import pyvisa

# Initialize the PyVISA resource manager
rm = pyvisa.ResourceManager()

# Define GPIB communication details
instrument_gpib_address = 'GPIB0::10::INSTR'  # Replace with the GPIB address of your instrument

# Open a connection to the instrument over GPIB
instrument = rm.open_resource(instrument_gpib_address,
                              read_termination='\r\n')    # Define the termination character for reading responses

# Set a timeout for communication (in milliseconds)
instrument.timeout = 5000

# Query the instrument for its identification string (IDN)
idn = instrument.query('*IDN?')
print(f"Instrument Identification: {idn}")
