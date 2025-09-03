"""
Program to perform MPM read power operation via GPIB.
"""

import time
import pyvisa

rm = pyvisa.ResourceManager()

mpm_resource_name = 'GPIB0::16::INSTR'

mpm = rm.open_resource(mpm_resource_name,
                       read_termination="\n")

print(mpm.query("*IDN?"))

# Clear and reset the MPM
mpm.write("*RST")
mpm.write("*CLS")

measurement_mode = "FREERUN"
mpm.write(f"WMOD {measurement_mode}")

module_number = int(input("\nEnter the module to read from: "))
delay_time = float(input("\nEnter the delay time (in seconds) between each read operation: "))

input("\nPress Enter to start the measurement")
print("Hit Ctrl + C to stop the measurement\n")

try:
    while True:
        response = mpm.query(f'READ? {module_number}')

        print(f"\rRead response : {response}", end="")

        time.sleep(delay_time)

except KeyboardInterrupt:
    pass
