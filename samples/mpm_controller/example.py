from mpm_controller import MPM
import pyvisa

# Initialize PyVISA resource manager
rm = pyvisa.ResourceManager()

# Open a connection to the MPM instrument via GPIB
instrument = rm.open_resource('GPIB0::11:INSTR')        # Replace with your instrument's GPIB address

# Create an instance of the MPM class
mpm = MPM(instrument)

# Print the instrument identification
print(mpm.idn)
