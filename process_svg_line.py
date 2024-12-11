from svgpathtools import svg2paths2

# Charger le fichier SVG
file_path = "simple_line.svg"  
paths, attributes, svg_attributes = svg2paths2(file_path)

# Dimensions du SVG et du châssis (en cm)
svg_width = 100  # Dimensions du SVG en unités SVG
svg_height = 100
chassis_width_cm = 50
chassis_height_cm = 50

def svg_to_cm(x_svg, y_svg):
    # Convertir les coordonnées SVG en centimètres
    x_cm = (x_svg / svg_width) * chassis_width_cm
    y_cm = (y_svg / svg_height) * chassis_height_cm
    return x_cm, y_cm

def extract_and_convert_line_coordinates(paths):
    for path in paths:
        for segment in path:
            # Obtenir les coordonnées de début et de fin de la ligne
            start = segment.start
            end = segment.end

            # Extraire les coordonnées x et y des points
            x_start, y_start = start.real, start.imag
            x_end, y_end = end.real, end.imag

            # Convertir les coordonnées en centimètres
            x_start_cm, y_start_cm = svg_to_cm(x_start, y_start)
            x_end_cm, y_end_cm = svg_to_cm(x_end, y_end)

            print(f"Point de départ (cm) : ({x_start_cm}, {y_start_cm})")
            print(f"Point de fin (cm) : ({x_end_cm}, {y_end_cm})")

# Appeler la fonction pour extraire et convertir les coordonnées
extract_and_convert_line_coordinates(paths)


"""from svgpathtools import svg2paths2
import serial
import time

# Charger le fichier SVG
file_path = "simple_line.svg"  # Remplacez par le chemin de votre fichier SVG
paths, attributes, svg_attributes = svg2paths2(file_path)

# Dimensions du SVG et du châssis (en cm)
svg_width = 100  # Dimensions du SVG en unités SVG
svg_height = 100
chassis_width_cm = 50
chassis_height_cm = 50

# Facteur de conversion cm -> pas (ajustez selon votre configuration)
steps_per_cm = 100  # Par exemple, 100 pas pour déplacer de 1 cm

def svg_to_cm(x_svg, y_svg):
    # Convertir les coordonnées SVG en centimètres
    x_cm = (x_svg / svg_width) * chassis_width_cm
    y_cm = (y_svg / svg_height) * chassis_height_cm
    return x_cm, y_cm

def cm_to_steps(x_cm, y_cm):
    # Convertir les centimètres en pas pour chaque axe
    x_steps = int(x_cm * steps_per_cm)
    y_steps = int(y_cm * steps_per_cm)
    return x_steps, y_steps

def send_coordinates_to_arduino(ser, x_steps, y_steps):
    # Construire la chaîne de coordonnées à envoyer
    coordinates = f"x={x_steps},y={y_steps}\n"
    # Envoyer les coordonnées à l'Arduino
    ser.write(coordinates.encode())
    print(f"Coordonnées envoyées : {coordinates}")

def extract_and_send_line_coordinates(paths):
    # Initialiser la communication série avec l'Arduino
    ser = serial.Serial('/dev/serial0', 9600, timeout=1)
    time.sleep(2)  # Temps d'attente pour s'assurer que la connexion est établie

    try:
        for path in paths:
            for segment in path:
                # Obtenir les coordonnées de début et de fin de la ligne
                start = segment.start
                end = segment.end

                # Extraire les coordonnées x et y des points
                x_start, y_start = start.real, start.imag
                x_end, y_end = end.real, end.imag

                # Convertir les coordonnées en centimètres
                x_start_cm, y_start_cm = svg_to_cm(x_start, y_start)
                x_end_cm, y_end_cm = svg_to_cm(x_end, y_end)

                # Convertir les centimètres en pas
                x_start_steps, y_start_steps = cm_to_steps(x_start_cm, y_start_cm)
                x_end_steps, y_end_steps = cm_to_steps(x_end_cm, y_end_cm)

                # Envoyer les positions de début et de fin à l'Arduino
                send_coordinates_to_arduino(ser, x_start_steps, y_start_steps)
                time.sleep(1)  # Pause pour que le moteur ait le temps de se déplacer
                send_coordinates_to_arduino(ser, x_end_steps, y_end_steps)
                time.sleep(1)  # Pause pour que le moteur ait le temps de se déplacer

    finally:
        ser.close()
        print("Transmission terminée.")

# Appeler la fonction pour extraire, convertir et envoyer les coordonnées
extract_and_send_line_coordinates(paths)"""
