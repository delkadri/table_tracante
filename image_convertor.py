from svgpathtools import svg2paths2

# Charger le fichier SVG
file_path = "image.svg"  # Remplacez par le chemin de votre fichier SVG
paths, attributes, svg_attributes = svg2paths2(file_path)

for path in paths:  
    for segment in path:  
        # Points de début et de fin.
        start = segment.start
        end = segment.end

        # Extraire les coordonnées x et y
        x_start, y_start = start.real, start.imag
        x_end, y_end = end.real, end.imag
        print(f"Début : ({x_start}, {y_start}), Fin : ({x_end}, {y_end})")

        

