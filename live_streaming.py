from picamera2 import Picamera2
import cv2
import time

# Initialiser la caméra
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())  # Mode aperçu
picam2.start()

print("Appuyez sur 'q' pour quitter.")

try:
    while True:
        # Capture une image depuis la caméra
        frame = picam2.capture_array()

        # Convertir l'image en format compatible OpenCV (BGR)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Afficher l'image en live
        cv2.imshow("Live Stream", frame)

        # Quitter avec la touche 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    picam2.stop()
    cv2.destroyAllWindows()
    print("Streaming arrêté.")
