import serial
import time

# === CONFIGURATION ===
SERIAL_PORT = "/dev/ttyUSB0"   # Change-le si besoin, ex: "/dev/ttyACM0"
BAUD_RATE = 115200

# === CONNEXION SÉRIE ===
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

# === SÉQUENCE DE TRAÇAGE SIMPLE ===

# Lever le stylo au départ
send_command("PEN_UP")

# Aller au point de départ
send_command("MOVE X=50 Y=50")

# Abaisser le stylo
send_command("PEN_DOWN")

## Tracer une ligne droite
send_command("MOVE X=80 Y=50")

## Tracer une ligne droite
send_command("MOVE X=80 Y=80")

## Tracer une ligne droite
send_command("MOVE X=0 Y=0")


# Lever le stylo après le tracé
send_command("PEN_UP")

# Fin de dessin
send_command("END")

# Fermer le port série
ser.close()
print("✏️ Ligne tracée. Port série fermé.")
