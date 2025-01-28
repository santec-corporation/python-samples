from tsl_controller import TSL
import pyvisa

# Initialize PyVISA resource manager
rm = pyvisa.ResourceManager()

# Open a connection to the TSL instrument via GPIB
instrument = rm.open_resource('GPIB0::10:INSTR')        # Replace with your instrument's GPIB address

# Create an instance of the TSL class
tsl = TSL(instrument)

# Print the instrument identification
print(tsl.idn)
