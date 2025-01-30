<p align="right"> <a href="https://www.santec.com/jp/" target="_blank" rel="noreferrer"> <img src="https://www.santec.com/dcms_media/image/common_logo01.png" alt="santec" 
  width="200" height="35"/> </a> </p>

<h1 align="left"> Python Samples </h1>

This repository provides Python code samples for controlling Santec instruments,
including lasers, power meters, polarization controllers,
enabling seamless integration and automation.

---

### Connectivity & Data Acquisition
- **[gpib_connection.py](https://github.com/santec-corporation/python-samples/blob/main/samples/gpib_connection.py)**  
  Connect and control instruments via GPIB communication.  
- **[lan_connection.py](https://github.com/santec-corporation/python-samples/blob/main/samples/lan_connection.py)**  
  Connect and control instruments via Ethernet communication.  
- **[ni_daq_read_data.py](https://github.com/santec-corporation/python-samples/blob/main/samples/ni_daq_read_data.py)**  
  Read data from NI (National Instruments) DAQ hardware.

### SME & Pseudo Implementations
- **[simple_sme.py](https://github.com/santec-corporation/python-samples/blob/main/samples/simple_sme.py)**  
  Basic SME (Single MEasurement) mode operation. 
- **[sme_pseudo.py](https://github.com/santec-corporation/python-samples/blob/main/samples/sme_pseudo.py)**  
  Provides a pseudo-version of the SME functionality.  

### Instrument Classes

#### TSL Instrument
- **[tsl_instrument.py](https://github.com/santec-corporation/python-samples/blob/main/samples/tsl_instrument/tsl_instrument.py)**  
  Manages control operations for TSL instrument.  
- **[tsl_example.py](https://github.com/santec-corporation/python-samples/blob/main/samples/tsl_instrument/tsl_example.py)**  
  Example usage of the TSL instrument class.

#### MPM Instrument
- **[mpm_instrument.py](https://github.com/santec-corporation/python-samples/blob/main/samples/mpm_instrument/mpm_instrument.py)**  
  Manages control operations for MPM instrument.  
- **[mpm_example.py](https://github.com/santec-corporation/python-samples/blob/main/samples/mpm_instrument/mpm_example.py)**  
  Example usage of the MPM instrument class.

#### PCU Instrument
- **[pcu_instrument.py](https://github.com/santec-corporation/python-samples/blob/main/samples/pcu_instrument/pcu_instrument.py)**  
  Manages control operations for PCU instrument.  
- **[pcu_example.py](https://github.com/santec-corporation/python-samples/blob/main/samples/pcu_instrument/pcu_example.py)**  
  Example usage of the PCU instrument class.

---