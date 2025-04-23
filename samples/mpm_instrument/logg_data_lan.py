# -*- coding: utf-8 -*-
"""
Script to retrieve MPM logging data via LAN communication.
"""

import math
import pyvisa
from pyvisa import util
from tqdm import tqdm

rm = pyvisa.ResourceManager()

lan_resource = "TCPIP0::192.168.1.161::5000::SOCKET"
mpm = rm.open_resource(lan_resource, read_termination="\r")

idn = mpm.query('*IDN?')
print("IDN: ", idn)

count = int(mpm.query('LOGN?'))
print("Logn: ", count)

expected_size = count * 4 + (2 + 1 + int(math.log10(count))) + 1

with tqdm(total=expected_size, unit='B', unit_scale=True) as progress:
    mpm.write('LOGG? 0,1')
    response = mpm.read_bytes(count=expected_size, monitoring_interface=progress)

data = util.from_ieee_block(response)
print(len(data))
