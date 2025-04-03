from svgpathtools import svg2paths2

# Charger le fichier SVG
file_path = "triangle-svgrepo-com.svg"  # Remplacez par le chemin de votre fichier SVG
paths, attributes, svg_attributes = svg2paths2(file_path)

# Variable pour garder la position actuelle du moteur (initialement à l'origine)
current_x, current_y = 0, 0

for path in paths:  
    for segment in path:  
        # Points de début et de fin.
        start = segment.start
        end = segment.end

        # Extraire les coordonnées x et y
        x_start, y_start = start.real, start.imag
        x_end, y_end = end.real, end.imag

        # Si nécessaire, lever le stylo avant de commencer à bouger
        if (current_x != x_start or current_y != y_start):
            print(f"PEN_UP")  # Lever le stylo avant de déplacer
            print(f"MOVE X={x_start} Y={y_start}")  # Déplacer le moteur au point de départ
            current_x, current_y = x_start, y_start

        # Abaisser le stylo pour commencer à dessiner
        print(f"PEN_DOWN")
        print(f"MOVE X={x_end} Y={y_end}")  # Déplacer le moteur vers le point final
        current_x, current_y = x_end, y_end  # Mettre à jour la position actuelle

    # Vous pouvez ajouter ici un PEN_UP supplémentaire pour lever le stylo entre les segments si nécessaire
