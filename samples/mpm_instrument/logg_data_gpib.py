# -*- coding: utf-8 -*-
"""
Script to retrieve MPM logging data via LAN communication.
"""

import math
import pyvisa
from tqdm import tqdm

rm = pyvisa.ResourceManager()

gpib_resource = "GPIB0::16::INSTR"
mpm = rm.open_resource(gpib_resource)

idn = mpm.query('*IDN?')
print("IDN: ", idn)

count = int(mpm.query('LOGN?'))
print("Logn: ", count)

expected_size = count * 4 + (2 + 1 + int(math.log10(count)))

with tqdm(total=expected_size, unit='B', unit_scale=True) as progress:
    response = mpm.query_binary_values('LOGG? 0,1', chunk_size=expected_size, monitoring_interface=progress)

print(len(response))
