#!/usr/bin/env python3
import math
import serial
import time
from svgpathtools import svg2paths2

# --------------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------------

SVG_FILE = "simple_line.svg"   # Chemin vers votre fichier SVG
SERIAL_PORT = "/dev/ttyACM0"   # Adapté à votre config (ex: /dev/ttyUSB0, COM3 sous Windows)
BAUD_RATE = 115200             # Doit correspondre au Serial.begin(...) côté Arduino

STEP_SIZE = 5.0  # Distance (en unités SVG) entre chaque "MOVE" partiel
                 # Plus petit => plus de points, plus précis, plus lent

# --------------------------------------------------------------------------------
# Fonctions principales
# --------------------------------------------------------------------------------

def main():
    # 1) Lire le fichier SVG et générer la liste de commandes
    instructions = svg_to_instructions(SVG_FILE, STEP_SIZE)

    # 2) Ouvrir la liaison série avec l’Arduino
    print(f"Ouverture du port {SERIAL_PORT} à {BAUD_RATE} bauds...")
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Laisser le temps à l’Arduino de redémarrer

    # 3) Envoyer chaque commande
    for cmd in instructions:
        print(f"Envoi : {cmd}")
        ser.write((cmd + "\n").encode('utf-8'))  # Envoie la ligne + \n

        # 4) Lire la réponse (si l'Arduino envoie "OK" ou autre chose)
        response = ser.readline().decode('utf-8').strip()
        if response:
            print(f"Réponse Arduino : {response}")
        else:
            print("Pas de réponse (timeout ou vide)")

    ser.close()
    print("Fermeture du port série.")

def svg_to_instructions(file_path, step_size):
    """
    Lit le fichier SVG via svgpathtools,
    et produit une suite de commandes : PEN_UP, PEN_DOWN, MOVE X=... Y=...
    en subdivisant chaque segment selon 'step_size'.
    Retourne une liste de chaînes.
    """
    instructions = []

    paths, attributes, svg_attributes = svg2paths2(file_path)

    current_x, current_y = 0.0, 0.0  # position actuelle de "l'outil"

    for path in paths:
        for segment in path:
            start = segment.start
            end = segment.end

            x_start, y_start = start.real, start.imag
            x_end,   y_end   = end.real,   end.imag

            # Aller au point de départ stylo levé si on n'y est pas déjà
            if (current_x != x_start) or (current_y != y_start):
                instructions.append("PEN_UP")
                instructions.append(f"MOVE X={x_start:.2f} Y={y_start:.2f}")
                current_x, current_y = x_start, y_start

            # PEN_DOWN pour tracer
            instructions.append("PEN_DOWN")

            # Calculer distance + subdivisions
            dx = x_end - x_start
            dy = y_end - y_start
            distance = math.hypot(dx, dy)

            steps = max(1, int(distance / step_size))

            # Déplacements intermédiaires
            for i in range(1, steps + 1):
                new_x = x_start + (dx / steps) * i
                new_y = y_start + (dy / steps) * i
                instructions.append(f"MOVE X={new_x:.2f} Y={new_y:.2f}")

            # Mettre à jour position
            current_x, current_y = x_end, y_end

        # Après un path, on relève le stylo
        instructions.append("PEN_UP")

    # Fin : on peut éventuellement ajouter un "END"
    instructions.append("END")

    return instructions

# --------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
