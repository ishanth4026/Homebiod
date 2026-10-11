import serial
import time
import math
from PIL import Image, ImageDraw

# --- CONFIGURATION ---
COM_PORT = 'COM3' # Ensure this matches your port
WIDTH = 250
HEIGHT = 122

def generate_display_buffer():
    print("Drawing image...")
    # Create a new 1-bit image with a white background
    image = Image.new('1', (WIDTH, HEIGHT), color=1)
    draw = ImageDraw.Draw(image)

    # Draw graphics and text
    draw.rectangle([0, 0, WIDTH-1, HEIGHT-1], outline=0, width=3)
    draw.text((15, 15), "USB Bridge: ONLINE", fill=0)
    draw.text((15, 45), "No Wi-Fi Needed!", fill=0)
    draw.text((15, 75), "Amrita Firewall Bypassed.", fill=0)

    # Convert the image to a byte array (3,904 bytes)
    bytes_per_row = math.ceil(WIDTH / 8)
    buffer = bytearray(bytes_per_row * HEIGHT)

    # Initialize all bytes to 0xFF (White)
    for i in range(len(buffer)):
        buffer[i] = 0xFF

    # Map the Pillow pixels to the byte array
    pixels = image.load()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if pixels[x, y] == 0: # If pixel is black
                byte_index = (y * bytes_per_row) + (x // 8)
                bit_index = 7 - (x % 8)
                buffer[byte_index] &= ~(1 << bit_index)
                
    return buffer

# 1. Generate the image
buffer = generate_display_buffer()

# 2. Connect to the ESP32 gently (preventing S3 USB crash)
print(f"Connecting to {COM_PORT}...")
ser = serial.Serial()
ser.port = COM_PORT
ser.baudrate = 115200
ser.timeout = 1
ser.dtr = False # CRITICAL for ESP32-S3 native USB
ser.rts = False # CRITICAL for ESP32-S3 native USB
ser.open()

# 3. Wait for the ESP32 Lighthouse Beacon
print("Waiting for ESP32 beacon...")
ser.reset_input_buffer()

ready = False
while not ready:
    line = ser.readline().decode('utf-8', errors='ignore').strip()
    if line:
        print(f"ESP32: {line}")
    if "READY" in line:
        ready = True

# 4. Blast the command down the cable
print("Sending 'DRAW' command...")
ser.write(b'DRAW\n')

# 5. Send data 64 bytes at a time, pausing for 10ms between sips
print("Sending 3,904 bytes of image data in chunks...")
chunk_size = 64
for i in range(0, len(buffer), chunk_size):
    ser.write(buffer[i:i+chunk_size])
    time.sleep(0.01)

# 6. Listen for the debug confirmation
print("Listening for ESP32 response...")
for _ in range(100): # Listen for 10 seconds to allow the screen to physically draw
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        print(f"ESP32: {line}")
    time.sleep(0.1)

print("Done! Check the e-paper screen.")