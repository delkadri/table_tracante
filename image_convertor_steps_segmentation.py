from svgpathtools import svg2paths2
import math

# Charger le fichier SVG
file_path = "simple_line.svg"  # Remplacez par le chemin de votre fichier SVG
paths, attributes, svg_attributes = svg2paths2(file_path)

# Taille d'un pas (distance en unités)
step_size = 5  

# Variable pour garder la position actuelle du moteur (initialement à l'origine)
current_x, current_y = 0, 0

for path in paths:
    for segment in path:
        start = segment.start
        end = segment.end

        # Extraire les coordonnées x et y
        x_start, y_start = start.real, start.imag
        x_end, y_end = end.real, end.imag

        # Si le moteur n'est pas déjà au point de départ, il doit y aller
        if (current_x != x_start or current_y != y_start):
            print("PEN_UP")
            print(f"MOVE X={x_start} Y={y_start}")
            current_x, current_y = x_start, y_start

        # Abaisser le stylo pour dessiner
        print("PEN_DOWN")

        # Calcul de la distance totale à parcourir
        dx = x_end - x_start
        dy = y_end - y_start
        distance = math.sqrt(dx**2 + dy**2)  # Distance entre les deux points

        # Calcul du nombre de pas
        steps = max(1, int(distance / step_size))  # Assure au moins 1 step

        # Déplacement en plusieurs petits pas
        for i in range(1, steps + 1):
            # Calculer la nouvelle position
            new_x = x_start + (dx / steps) * i
            new_y = y_start + (dy / steps) * i
            print(f"MOVE X={new_x:.2f} Y={new_y:.2f}")  # Limiter à 2 décimales

        # Mettre à jour la position actuelle
        current_x, current_y = x_end, y_end

    # Lever le stylo entre les segments si nécessaire
    print("PEN_UP")
