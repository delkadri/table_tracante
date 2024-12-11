import serial
import time
import xml.etree.ElementTree as ET

def parse_svg_line():
    # Example SVG string representing a horizontal line
    svg_string = '''
    <svg width="100" height="100">
        <line x1="0" y1="0" x2="50" y2="0"/>
    </svg>
    '''
    
    # Parse SVG
    root = ET.fromstring(svg_string)
    line = root.find('line')
    
    # Extract coordinates
    x1 = float(line.get('x1', 0))
    y1 = float(line.get('y1', 0))
    x2 = float(line.get('x2', 0))
    y2 = float(line.get('y2', 0))
    
    return (x1, y1, x2, y2)

def convert_distance_to_steps(distance_mm):
    # Convert mm to steps
    # This depends on your mechanical setup
    # Example: if 1 revolution (3200 steps) = 40mm
    STEPS_PER_MM = 3200 / 40  # 80 steps per mm
    return int(distance_mm * STEPS_PER_MM)

def move_motor(ser, steps):
    # Send movement command
    if steps > 0:
        ser.write(b'F')  # Forward

        print(f"Moving forward {steps} steps")
    else:
        ser.write(b'B')  # Backward
        print(f"Moving backward {abs(steps)} steps")
    
    # Wait for confirmation
    while True:
        response = ser.readline().decode().strip()
        if response:
            print(f"Arduino says: {response}")
        if "complete" in response.lower():
            break

def draw_line():
    try:
        # Connect to Arduino
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        time.sleep(2)
        
        # Get line coordinates
        x1, y1, x2, y2 = parse_svg_line()
        print(f"Drawing line from ({x1},{y1}) to ({x2},{y2})")
        
        # Calculate distance
        distance = x2 - x1  # For horizontal line
        steps = convert_distance_to_steps(distance)
        
        # Move motor
        move_motor(ser, steps)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ser.close()

if __name__ == "__main__":
    draw_line()