# -*- coding: utf-8 -*-
"""
Script to retrieve TSL power data via LAN communication.
"""

import math
import pyvisa
from pyvisa import util
from tqdm import tqdm

rm = pyvisa.ResourceManager()

lan_resource = "TCPIP0::192.168.1.101::5000::SOCKET"
tsl = rm.open_resource(lan_resource, read_termination="\r")

idn = tsl.query('*IDN?')
print("IDN: ", idn)

count = int(tsl.query('READout:POINts?'))
print("LOGGING POINTS: ", count)

expected_size = count * 4 + (2 + 1 + int(math.log10(count)))

with tqdm(total=expected_size, unit='B', unit_scale=True) as progress:
    tsl.write(':READout:DATa:POWer?')
    response = tsl.read_bytes(count=expected_size, monitoring_interface=progress)

data = util.from_ieee_block(response)
# print(data)
print(len(data))
