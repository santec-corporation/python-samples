# -*- coding: utf-8 -*-
"""
Script to retrieve TSL power data via GPIB communication.
"""

import math
import time
import pyvisa
from tqdm import tqdm

rm = pyvisa.ResourceManager()

gpib_resource = "GPIB0::3::INSTR"
tsl = rm.open_resource(gpib_resource)

idn = tsl.query('*IDN?')
print("IDN: ", idn)

count = int(tsl.query('READout:POINts?'))
print("LOGGING POINTS: ", count)

expected_size = count * 4 + (2 + 1 + int(math.log10(count)))

with tqdm(total=expected_size, unit='B', unit_scale=True) as progress:
    response = tsl.query_binary_values(':READout:DATa:POWer?',
                                       datatype='i',
                                       chunk_size=expected_size,
                                       monitoring_interface=progress)

print(response)
print(len(response))

