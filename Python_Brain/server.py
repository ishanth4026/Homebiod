import serial
import time

# Create the Walkie-Talkie
ser = serial.Serial()
ser.port = 'COM3'     # Change to your COM port
ser.baudrate = 115200 
ser.timeout = 2       # Give it 2 seconds to reply

# Disable accidental reboot signals
ser.dtr = False
ser.rts = False

print("1. Opening port...")
ser.open()
time.sleep(2) # CRITICAL: Wait 2 seconds for Windows to fully stabilize the Native USB connection

# Clear out any old garbage text sitting in the Windows USB buffer
ser.reset_input_buffer()

print("2. Port stable. Sending PING...")
ser.write(b"PING\n")

print("3. Listening for reply...")
reply = ser.readline().decode('utf-8', errors='ignore').strip()

if reply == "PONG":
    print("SUCCESS! Handshake complete. The board replied: PONG")
elif reply:
    print(f"FAIL: The board replied with something else: {reply}")
else:
    print("FAIL: Silence. The board did not reply.")