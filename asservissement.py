import cv2
import numpy as np
import libcamera
from picamera2 import Picamera2


# Dimensions du chassis en cm
chassis_size = 45.0  # 45x45 cm
camera_height = 36.0  # hauteur de la caméra en cm

# Calcule les facteurs de conversion de pixels à centimètres
# Ces valeurs dépendront de la résolution de la caméra et de la distance du point rouge
# Ce sera une approximation car les valeurs exactes nécessitent des calculs de calibration plus complexes
pixels_per_cm = 10  # Hypothèse: 1 cm = 10 pixels (valeur approximative)

# Initialisation de la caméra
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())
picam2.start()

print("Détection en cours... Appuyez sur 'q' pour quitter.")

try:
    while True:
        # Capture une image depuis la caméra
        frame = picam2.capture_array()

        # Convertir l'image en format BGR pour OpenCV
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Convertir l'image en espace colorimétrique HSV pour une détection de couleur plus facile
        hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

        # Plage de couleurs pour détecter le rouge
        # Ces valeurs peuvent nécessiter des ajustements en fonction de la lumière et des conditions
        lower_red = np.array([0, 120, 70])
        upper_red = np.array([10, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)

        lower_red = np.array([170, 120, 70])
        upper_red = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, lower_red, upper_red)

        # Combiner les deux masques
        mask = mask1 | mask2

        # Trouver les contours du masque
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Si des contours sont trouvés, traiter le plus grand
        if contours:
            # Trouver le contour le plus grand (supposé être le point rouge)
            largest_contour = max(contours, key=cv2.contourArea)
            # Calculer le centre du contour
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

             # Calculer la position du point rouge en centimètres avec l'origine en bas à droite
                x_position_cm = (frame_bgr.shape[1] - cX) / pixels_per_cm  # Mesure par rapport au côté droit
                y_position_cm = (frame_bgr.shape[0] - cY) / pixels_per_cm  # Mesure par rapport au côté inférieur


                # Afficher la position du point rouge
                print(f"Position du point rouge: X = {x_position_cm:.2f} cm, Y = {y_position_cm:.2f} cm")

                # Dessiner un cercle autour du point détecté
                cv2.circle(frame_bgr, (cX, cY), 10, (0, 255, 0), -1)

        # Afficher l'image avec le point rouge détecté
        cv2.imshow("Live Stream", frame_bgr)

        # Quitter avec la touche 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    picam2.stop()
    cv2.destroyAllWindows()
    print("Capture et détection terminées.")
