# -*- coding: utf-8 -*-
"""
Script to retrieve TSL wavelength data via LAN communication.
"""

import math
import pyvisa
from pyvisa import util
from tqdm import tqdm

rm = pyvisa.ResourceManager()

lan_resource = "TCPIP0::192.168.1.152::5000::SOCKET"
tsl = rm.open_resource(lan_resource, read_termination="\r")
tsl.timeout = 4000

idn = tsl.query('*IDN?')
print("IDN: ", idn)

count = int(tsl.query(':READout:POINts?'))
print("LOGGING POINTS: ", count)

expected_size = count * 4 + (2 + 1 + int(math.log10(count)))

with tqdm(total=expected_size, unit='B', unit_scale=True) as progress:
    tsl.write(':READout:DATa?')
    response = tsl.read_bytes(count=expected_size, monitoring_interface=progress)

data = util.from_ieee_block(response, datatype='i')
print(data)
print(len(data))

rounded = [float(f"{num / 10000:.4f}") for num in data]
print(rounded)
