from pcu_instrument import PCU
import pyvisa

# Initialize PyVISA resource manager
rm = pyvisa.ResourceManager()

# Open a connection to the PCU instrument via GPIB
instrument = rm.open_resource('GPIB0::5:INSTR')        # Replace with your instrument's GPIB address

# Create an instance of the PCU class
pcu = PCU(instrument)

# Print the instrument identification
print(pcu.idn)
