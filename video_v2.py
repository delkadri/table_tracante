from picamera2 import Picamera2
from PIL import Image
import time
import os
import sys
import termios
import tty
import select

# Fonction pour détecter l'appui sur une touche sans bloquer
def is_key_pressed():
    dr, dw, de = select.select([sys.stdin], [], [], 0)
    if dr:
        return sys.stdin.read(1)
    return None

# Fonction pour vider le dossier photos
def clear_photos_folder(folder):
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Supprimer le fichiergo
            except Exception as e:
                print(f'Erreur en supprimant le fichier {file_path}: {e}')

# Initialiser la caméra
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()

# Dossier de sauvegarde des images
save_folder = "photos"

# Vider le dossier photos avant de commencer
clear_photos_folder(save_folder)

# Créer le dossier s'il n'existe pas
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

print("Appuyez sur 'q' pour arrêter la capture.")

photo_count = 1

try:
    while True:
        # Capture d'image
        frame = picam2.capture_array()

        # Convertir en image PIL et sauvegarder
        image = Image.fromarray(frame)
        image.save(os.path.join(save_folder, f"photo_{photo_count}.jpg"))

        print(f"Photo {photo_count} capturée")

        photo_count += 1

        # Vérifier si l'utilisateur appuie sur 'q' pour arrêter
        key = is_key_pressed()
        if key == 'q':
            break

        # Réduire le délai au minimum pour rendre la capture plus rapide
        time.sleep(0.1)  # Vous pouvez ajuster le délai si nécessaire

finally:
    picam2.stop()
    print("Capture arrêtée.")
