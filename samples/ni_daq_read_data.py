import nidaqmx
from nidaqmx.constants import TerminalConfiguration

# Define the DAQ device and channel names
device_name = "Dev1"       # Replace with the name of your DAQ device
channel_names = "ai0:1"    # Replace with the desired analog input channels (e.g., "ai0:1" for channels ai0 and ai1)

# Construct the physical channel string (e.g., "Dev1/ai0:1")
physical_channel = f"{device_name}/{channel_names}"

try:
    # Create a new DAQ task for acquiring analog voltage data
    with nidaqmx.Task() as task:
        # Add an analog input voltage channel to the task
        task.ai_channels.add_ai_voltage_chan(
            physical_channel,
            name_to_assign_to_channel='AnalogDaq',  # Logical name for the channel (optional)
            terminal_config=TerminalConfiguration.DIFF,  # Use differential terminal configuration
            min_val=-5.0,  # Minimum voltage range (in volts)
            max_val=5.0    # Maximum voltage range (in volts)
        )

        # Define the sample size (number of samples to read per channel)
        sample_size = 100

        # Read the specified number of samples from the channel(s)
        data = task.read(number_of_samples_per_channel=sample_size)

        # Output the acquired data
        print("Data acquired:")
        print(data)

except Exception as e:
    # Handle any errors that occur during setup or data acquisition
    print(f"An error occurred: {e}")
