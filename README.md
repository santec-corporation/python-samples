<p align="right"> <a href="https://www.santec.com/jp/" target="_blank" rel="noreferrer"> <img src="https://www.santec.com/dcms_media/image/common_logo01.png" alt="santec" 
  width="200" height="35"/> </a> </p>

<h1 align="left"> Python Samples </h1>

This repository provides Python code samples for controlling Santec instruments, including lasers and power meters,
enabling seamless integration and automation.

---

### Connectivity & Data Acquisition
- **[gpib_connection.py](https://github.com/santec-corporation/python-samples/blob/main/samples/gpib_connection.py)**  
  Establishes and manages GPIB communication.  
- **[lan_connection.py](https://github.com/santec-corporation/python-samples/blob/main/samples/lan_connection.py)**  
  Facilitates network-based device communication.  
- **[ni_daq_read_data.py](https://github.com/santec-corporation/python-samples/blob/main/samples/ni_daq_read_data.py)**  
  Read data from NI (National Instruments) DAQ hardware.

### SME & Pseudo Implementations
- **[simple_sme.py](https://github.com/santec-corporation/python-samples/blob/main/samples/simple_sme.py)**  
  Basic SME (Single MEasurement) mode operation. 
- **[sme_pseudo.py](https://github.com/santec-corporation/python-samples/blob/main/samples/sme_pseudo.py)**  
  Provides a pseudo-version of the SME functionality.  

### Instrument Controller

#### TSL Controller
- **[tsl_controller.py](https://github.com/santec-corporation/python-samples/blob/main/samples/tsl_controller/tsl_controller.py)**  
  Manages control operations for TSL instrument.  
- **[tsl_information.py](https://github.com/santec-corporation/python-samples/blob/main/samples/tsl_controller/tsl_information.py)**  
  TSL instrument error code information and related. 
- 
#### MPM Controller
- **[mpm_controller.py](https://github.com/santec-corporation/python-samples/blob/main/samples/mpm_controller/mpm_controller.py)**  
  Manages control operations for MPM instrument.  
- **[mpm_information.py](https://github.com/santec-corporation/python-samples/blob/main/samples/mpm_controller/mpm_information.py)**  
  MPM instrument error code information and related.

#### PCU Controller
- **[pcu_controller.py](https://github.com/santec-corporation/python-samples/blob/main/samples/pcu_controller/pcu_controller.py)**  
  Manages control operations for PCU instrument.  
- **[pcu_information.py](https://github.com/santec-corporation/python-samples/blob/main/samples/pcu_controller/pcu_information.py)**  
  PCU instrument error code information and related.

---