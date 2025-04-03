import cv2
import numpy as np
import libcamera
from picamera2 import Picamera2

# Dimensions du chassis en cm
chassis_size = 45.0
camera_height = 36.0
pixels_per_cm = 10  # Hypothese

# Initialisation de la camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())
picam2.start()

print("Detection en cours... Appuyez sur 'q' pour quitter.")

# Initialisation des reperes
orange_ref = None
blue_ref = None

try:
    while True:
        frame = picam2.capture_array()
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # DeTECTION DU POINT ROUGE
        #lower_red1 = np.array([0, 120, 70])
        lower_red1 = np.array([0, 0, 170])
        #upper_red1 = np.array([10, 255, 255])
        upper_red1 = np.array([64, 64, 255])
        mask_red = cv2.inRange(frame_bgr, lower_red1, upper_red1)

        """lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
                                    **
        mask_red = mask_red1 | mask_red2"""

        # DeTECTION DU ORANGE
        lower_orange = np.array([170, 0, 0])
        upper_orange = np.array([255, 64, 64])
        mask_orange = cv2.inRange(frame_bgr, lower_orange, upper_orange)

        # DeTECTION DU BLEU
        lower_blue = np.array([170, 0, 0])
        upper_blue = np.array([255, 64, 64])
        mask_blue = cv2.inRange(frame_bgr, lower_blue, upper_blue)

        # TROUVER LES CENTRES DES POINTS
        def get_center(mask):
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                c = max(contours, key=cv2.contourArea)
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    return (cx, cy)
            return None

        red_center = get_center(mask_red)
        orange_ref = get_center(mask_orange) or orange_ref
        blue_ref = get_center(mask_blue) or blue_ref

        # AFFICHAGE DES POINTS
        if red_center:
            cv2.circle(frame_bgr, red_center, 10, (0, 255, 255), -1)
            x_cm = (frame_bgr.shape[1] - red_center[0]) / pixels_per_cm
            y_cm = (frame_bgr.shape[0] - red_center[1]) / pixels_per_cm
            print(f"Position du point rouge: X = {x_cm:.2f} cm, Y = {y_cm:.2f} cm")

        if orange_ref:
            cv2.circle(frame_bgr,orange_ref, 10, (0, 255, 0), -1)
        if blue_ref:
            cv2.circle(frame_bgr, blue_ref, 10, (255, 0, 0), -1)

        # VeRIFICATION SI LE POINT ROUGE EST DANS LE CADRE
        if red_center and orange_ref and blue_ref:
            x_min = min (orange_ref[0], blue_ref[0])
            x_max = max (orange_ref[0], blue_ref[0])
            y_min = min (orange_ref[1], blue_ref[1])
            y_max = max (orange_ref[1], blue_ref[1])

            rx, ry = red_center
            if not (x_min <= rx <= x_max and y_min <= ry <= y_max):
                print("?? Point rouge HORS DU CADRE !")

            # Dessiner le cadre
            cv2.rectangle(frame_bgr, (x_min, y_min), (x_max, y_max), (255, 255, 0), 2)

        # Afficher l'image
        cv2.imshow("Live Stream", frame_bgr)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    picam2.stop()
    cv2.destroyAllWindows()
    print("Capture et detection terminees.")
