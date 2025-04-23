from mpm_instrument import MPM
import pyvisa

# Initialize PyVISA resource manager
rm = pyvisa.ResourceManager()

# Open a connection to the MPM instrument via GPIB
instrument = rm.open_resource('GPIB0::16::INSTR')        # Replace with your instrument's GPIB address

# Create a connection of the MPM class
mpm = MPM(instrument)

# Print the instrument identification
print(mpm.get_idn())

# Print logging data length
print(len(mpm.get_logging_data(0,1)))
