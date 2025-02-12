import math
import serial
import time
from svgpathtools import svg2paths2

# -------------------
# Configuration Arduino
# -------------------
SERIAL_PORT = "/dev/ttyACM0"  # Modifier selon ton système (COM3 sous Windows)
BAUD_RATE = 115200
STEP_SIZE = 5  # Taille d'un pas en unités (distance minimale)

# -------------------
# Fonction pour envoyer une commande à l'Arduino
# -------------------
def send_to_arduino(command, ser):
    ser.write((command + "\n").encode('utf-8'))  # Envoi avec un saut de ligne
    #time.sleep(0.1)  # Laisser un peu de temps pour traiter
    response = ser.readline().decode('utf-8').strip()  # Lire la réponse
    return response

# -------------------
# Fonction principale
# -------------------
def main():
    # Charger le fichier SVG
    file_path = "simple_line.svg"  # Remplacer par le chemin de votre fichier SVG
    paths, attributes, svg_attributes = svg2paths2(file_path)

    # Initialiser la position actuelle du moteur (à l'origine)
    current_x, current_y = 0, 0

    # Initialiser la connexion série avec l'Arduino
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Laisser du temps pour l'initialisation de l'Arduino

    # Traiter chaque chemin dans le fichier SVG
    for path in paths:
        for segment in path:
            start = segment.start
            end = segment.end

            # Extraire les coordonnées x et y
            x_start, y_start = start.real, start.imag
            x_end, y_end = end.real, end.imag

            # Si le moteur n'est pas déjà au point de départ, déplacer le stylo
            if (current_x != x_start or current_y != y_start):
                """command = "PEN_UP"
                print(f"Envoi : {command}")
                print(send_to_arduino(command, ser))"""

                command = f"MOVE X={x_start:.2f} Y={y_start:.2f}"
                print(f"Envoi : {command}")
                print(send_to_arduino(command, ser))

                current_x, current_y = x_start, y_start

            # Abaisser le stylo pour dessiner
                """command = "PEN_DOWN"
                print(f"Envoi : {command}")
                print(send_to_arduino(command, ser))"""

            # Calcul de la distance totale à parcourir
            dx = x_end - x_start
            dy = y_end - y_start
            distance = math.sqrt(dx**2 + dy**2)

            # Calcul du nombre de pas nécessaires
            steps = max(1, int(distance / STEP_SIZE))  # Minimum 1 step

            # Déplacement en plusieurs petits pas
            for i in range(1, steps + 1):
                new_x = x_start + (dx / steps) * i
                new_y = y_start + (dy / steps) * i
                command = f"MOVE X={new_x:.2f} Y={new_y:.2f}"
                print(f"Envoi : {command}")
                print(send_to_arduino(command, ser))

            # Mettre à jour la position actuelle
            current_x, current_y = x_end, y_end

        # Lever le stylo après un segment
        """command = "PEN_UP"
        print(f"Envoi : {command}")
        print(send_to_arduino(command, ser))"""

    # Fermer la connexion série
    ser.close()

# -------------------
# Lancer le programme
# -------------------
if __name__ == "__main__":
    main()




