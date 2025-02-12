#!/usr/bin/env python3

import serial
import time

# Modifiez si nécessaire :
SERIAL_PORT = "/dev/ttyACM0"   # Sur Linux, sinon "COM3" sous Windows
BAUD_RATE   = 115200

def main():
    # Liste de commandes à envoyer dans l'ordre
    commands = [
        "MOVE X=50 Y=80",   # 1er déplacement
        "PEN_DOWN",         # abaisser le stylo (Z)
        "MOVE X=50 Y=50",   # 2e déplacement
        "PEN_UP",           # remonter le stylo (Z)
        "END"               # fin
    ]

    # Ouvrir la liaison série
    print(f"Ouverture de {SERIAL_PORT} à {BAUD_RATE} bauds...")
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # la plupart des cartes Arduino se réinitialisent à l'ouverture

    for cmd in commands:
        print(f"Envoi de la commande : {cmd}")
        ser.write((cmd + "\n").encode('utf-8'))

        # Lire la réponse (ex: "OK")
        response = ser.readline().decode('utf-8').strip()
        if response:
            print(f"Réponse de l'Arduino : {response}")
        else:
            print("Pas de réponse (timeout)")

        # Petite pause si nécessaire (pas obligatoire)
        time.sleep(0.1)

    # Fermer la liaison
    ser.close()
    print("Fermeture de la liaison série.")

if __name__ == "__main__":
    main()
