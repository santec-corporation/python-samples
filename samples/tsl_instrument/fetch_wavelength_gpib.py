# -*- coding: utf-8 -*-
"""
Script to retrieve TSL wavelength data via LAN communication.
"""

import math
import pyvisa
from tqdm import tqdm

rm = pyvisa.ResourceManager()

gpib_resource = "GPIB0::1::INSTR"
tsl = rm.open_resource(gpib_resource)

idn = tsl.query('*IDN?')
print("IDN: ", idn)

count = int(tsl.query('READout:POINts?'))
print("LOGGING POINTS: ", count)

expected_size = count * 4 + (2 + 1 + int(math.log10(count)))

with tqdm(total=expected_size, unit='B', unit_scale=True) as progress:
    response = tsl.query_binary_values(':READout:DATa?',
                                       chunk_size=expected_size,
                                       monitoring_interface=progress)

print(len(response))
