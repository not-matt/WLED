import serial
import serial.tools.list_ports
import json
import os

baudrate = 115200  # Set the baud rate to match your device

# Enumerate available ports
available_ports = list(serial.tools.list_ports.comports())

if not available_ports:
    print("No serial ports found. Please make sure your device is connected.")
    exit()

print("Available serial ports:")
for i, port in enumerate(available_ports):
    print(f"{i + 1}. {port.device}")

# Prompt for port selection
port_choice = input("Enter the number of the serial port you want to use: ")
port = available_ports[int(port_choice) - 1].device

# Open the serial port
ser = serial.Serial(port, baudrate)

# Check if the port is open
if ser.is_open:
    print(f"Serial port {port} opened successfully.")

# Function to send JSON data over serial
def send_json_data(data):
    json_data = json.dumps(data)  # Convert data to JSON string
    ser.write(json_data.encode('utf-8'))  # Send JSON string over serial
    ser.write(b'\n')  # Add a newline character as a delimiter

# Define the path to the "config" directory
config_dir = os.path.join(os.path.dirname(__file__), 'config')

# Load and send config.json
config_file_path = os.path.join(config_dir, 'cfg.json')
with open(config_file_path, 'r') as config_file:
    config_data = json.load(config_file)
    print("Sending config.json...")
    send_json_data(config_data)

# Load and send presets.json
presets_file_path = os.path.join(config_dir, 'presets.json')
with open(presets_file_path, 'r') as presets_file:
    presets_data = json.load(presets_file)
    print("Sending presets.json...")
    send_json_data(presets_data)

# Close the serial port when finished
ser.close()