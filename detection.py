import cv2 
import numpy as np
import os

# Taille du châssis en cm
chassis_size_cm = 50
half_chassis_size_cm = chassis_size_cm / 2

# Dimensions de l'image capturée 
image_width = 2592
image_height = 1944

# Fonction pour convertir les pixels en centimètres
def pixels_to_cm(x, y):
    x_cm = (x / image_width) * chassis_size_cm
    y_cm = (y / image_height) * chassis_size_cm
    return x_cm, y_cm

# Fonction pour calculer la position par rapport au centre
def calculate_position_relative_to_center(x_cm, y_cm):
    # Centre du châssis en cm
    center_x_cm = half_chassis_size_cm
    center_y_cm = half_chassis_size_cm

    # Position relative par rapport au centre
    relative_x_cm = x_cm - center_x_cm
    relative_y_cm = center_y_cm - y_cm  # Inverser l'axe Y pour correspondre au repère standard
    return relative_x_cm, relative_y_cm

# Fonction pour détecter la couleur rouge dans l'image
def detect_stylo_rouge(img):
    # Conversion en espace de couleur HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Définir les seuils pour la couleur rouge en HSV
    lower_red = np.array([0, 120, 70])  # Rouge clair
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 120, 70])  # Rouge foncé
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    # Combiner les deux masques
    mask = mask1 + mask2

    # Trouver les contours du masque rouge
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Prendre le plus grand contour (le crayon rouge)
        largest_contour = max(contours, key=cv2.contourArea)

        # Obtenir les coordonnées x, y du contour
        x, y, w, h = cv2.boundingRect(largest_contour)
        return x + w // 2, y + h // 2  # Centre du crayon rouge
    else:
        return None, None

# Fonction pour parcourir toutes les photos et détecter le crayon rouge
def process_photos_in_folder(folder_path):
    photo_files = [f for f in os.listdir(folder_path) if f.endswith(".jpg") or f.endswith(".png")]
    
    for photo in photo_files:
        # Charger l'image
        img = cv2.imread(os.path.join(folder_path, photo))

        if img is None:
            print(f"Erreur de lecture de l'image : {photo}")
            continue

        # Détecter la position du crayon rouge
        x, y = detect_stylo_rouge(img)

        if x is not None and y is not None:
            # Convertir les coordonnées en centimètres
            x_cm, y_cm = pixels_to_cm(x, y)

            # Calculer la position relative au centre
            relative_x, relative_y = calculate_position_relative_to_center(x_cm, y_cm)

            # Afficher les résultats
            print(f"Image: {photo} -> Position du crayon rouge : ({x_cm:.2f} cm, {y_cm:.2f} cm), Relative au centre: ({relative_x:.2f} cm, {relative_y:.2f} cm)")
        else:
            print(f"Stylo rouge non détecté dans l'image : {photo}")

# Dossier contenant les photos
photos_folder = "photos"

# Traiter les photos dans le dossier
process_photos_in_folder(photos_folder)
