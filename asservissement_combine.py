import cv2
import numpy as np
import math
from svgpathtools import svg2paths2
from picamera2 import Picamera2

# Charger le fichier SVG
file_path = "simple_line.svg"
paths, attributes, svg_attributes = svg2paths2(file_path)

# Paramètres
step_size = 5  # Distance d'un pas
pixels_per_cm = 10  # Approximation pour convertir pixels -> cm

# Initialisation de la caméra
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())
picam2.start()

# Position actuelle du moteur
current_x, current_y = 0, 0

def detect_red_point():
    """Capture une image et détecte la position du point rouge"""
    frame = picam2.capture_array()
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

    # Définition des seuils pour le rouge
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = mask1 | mask2
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # Convertir en cm
            x_cm = (frame.shape[1] - cX) / pixels_per_cm
            y_cm = (frame.shape[0] - cY) / pixels_per_cm
            return x_cm, y_cm

    return None  # Pas de point rouge détecté

try:
    for path in paths:
        for segment in path:
            start = segment.start
            end = segment.end
            x_start, y_start = start.real, start.imag
            x_end, y_end = end.real, end.imag

            if (current_x != x_start or current_y != y_start):
                print("PEN_UP")
                print(f"MOVE X={x_start} Y={y_start}")
                current_x, current_y = x_start, y_start

            print("PEN_DOWN")

            dx, dy = x_end - x_start, y_end - y_start
            distance = math.sqrt(dx**2 + dy**2)
            steps = max(1, int(distance / step_size))

            for i in range(1, steps + 1):
                new_x = x_start + (dx / steps) * i
                new_y = y_start + (dy / steps) * i

                # Vérifier la présence du point rouge
                while True:
                    detected_position = detect_red_point()
                    if detected_position:
                        detected_x, detected_y = detected_position
                        # Vérifier si le point rouge est proche de la position attendue
                        if abs(detected_x - new_x) < 1 and abs(detected_y - new_y) < 1:
                            print(f"GO! MOVE X={new_x:.2f} Y={new_y:.2f}")
                            break  # Passe à la prochaine position
                    cv2.waitKey(1)  # Laisser le temps à la caméra de capter l'image

                current_x, current_y = new_x, new_y

            print("PEN_UP")

finally:
    picam2.stop()
    cv2.destroyAllWindows()
    print("Processus terminé.")
