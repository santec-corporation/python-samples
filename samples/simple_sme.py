"""
SME - Single Measurement mode operation.

Supported Instruments
TSL series and MPM series.

Supported Communication modes
GPIB and TCPIP.
"""

# Import the SME class
from sme_operation.sme_operation import SME


def main(tsl, mpm):
    """Main workflow to initialize, configure, and perform the sweep."""
    # Create an instance and initialize SME class
    sme = SME(tsl, mpm)

    # Collect user inputs
    power = float(input("\nInput output power: "))
    start_wavelength = float(input("Input start wavelength: "))
    stop_wavelength = float(input("Input stop wavelength: "))
    speed = float(input("Input scan speed: "))
    step = float(input("Input step wavelength: "))

    # Configure TSL and MPM parameters
    sme.configure_tsl(start_wavelength, stop_wavelength, step, power, speed)

    sme.configure_mpm(
        start_wavelength,
        stop_wavelength,
        step,
        speed,
        is_mpm_215=False,
    )  # Set is_mpm_215 to True if using MPM-215 module

    input("\nPress any key to start to the scan process.")

    # Perform sweep
    # Set display_logging_status True to print the MPM logging status
    sme.perform_scan(display_logging_status=False)


if __name__ == "__main__":
    # Import pyvisa
    import pyvisa

    # Create an instance of the Resource manager class
    rm = pyvisa.ResourceManager()
    # print(rm.list_resources())

    # Connect to the TSL and MPM instruments
    tsl_instrument = rm.open_resource("GPIB2::3::INSTR", read_termination = '\r\n')
    mpm_instrument = rm.open_resource("GPIB2::15::INSTR", read_termination = '\n')

    # Uncomment the below code to use TCPIP connection
    # tsl_instrument = rm.open_resource("TCPIP::192.168.1.152::5000::SOCKET",
    #                                   read_termination='\r',
    #                                   open_timeout=5000)
    # mpm_instrument = rm.open_resource("TCPIP::192.168.1.161::5000::SOCKET",
    #                                   read_termination='\r',
    #                                   open_timeout=5000)

    if not tsl_instrument or not mpm_instrument:
        raise Exception("Could not connect to TSL / MPM instrument(s).")

    print("Connected to the instruments:")
    print(tsl_instrument.query('*IDN?'))
    print(mpm_instrument.query('*IDN?'))

    # Execute the main function
    main(tsl_instrument, mpm_instrument)