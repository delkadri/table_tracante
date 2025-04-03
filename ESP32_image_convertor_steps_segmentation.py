import serial
import time
import math
from svgpathtools import svg2paths2

# === CONFIGURATION ===
SVG_FILE = "triangle-svgrepo-com.svg"   # Ton fichier SVG
STEP_SIZE = 5                           # Taille approximative d'un segment (en mm)
SERIAL_PORT = "/dev/ttyUSB0"           # À adapter selon ton port ESP32
BAUD_RATE = 115200

# === OUVERTURE DU PORT SÉRIE ===
print("Connexion à l'ESP32...")
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Laisser le temps à l'ESP32 de redémarrer
print("Connexion établie !")

# === UTILITAIRE POUR ENVOYER UNE COMMANDE ET ATTENDRE OK ===
def send_command(cmd):
    ser.write((cmd + "\n").encode())
    print("→", cmd)
    while True:
        response = ser.readline().decode().strip()
        if response == "OK":
            break
        elif response:
            print("← ESP32:", response)

# === CHARGER ET PARSER LE SVG ===
paths, attributes, svg_attributes = svg2paths2(SVG_FILE)

# Position actuelle du stylo (mm)
current_x, current_y = 0, 0

for path in paths:
    for segment in path:
        start = segment.start
        end = segment.end

        x_start, y_start = start.real, start.imag
        x_end, y_end = end.real, end.imag

        # Si le stylo n'est pas déjà au point de départ
        if (current_x != x_start or current_y != y_start):
            send_command("PEN_UP")
            send_command(f"MOVE X={x_start:.2f} Y={y_start:.2f}")
            current_x, current_y = x_start, y_start

        send_command("PEN_DOWN")

        dx = x_end - x_start
        dy = y_end - y_start
        distance = math.sqrt(dx**2 + dy**2)
        steps = max(1, int(distance / STEP_SIZE))

        for i in range(1, steps + 1):
            new_x = x_start + (dx / steps) * i
            new_y = y_start + (dy / steps) * i
            send_command(f"MOVE X={new_x:.2f} Y={new_y:.2f}")

        current_x, current_y = x_end, y_end

    # Relever le stylo entre les segments
    send_command("PEN_UP")

# Fin du dessin
send_command("PEN_UP")
send_command("END")
ser.close()
print("✏️ Dessin terminé. Port série fermé.")
