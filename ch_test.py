import serial
import time

# Adaptation du port selon ta config ; souvent /dev/ttyACM0
# (Si c'est un Arduino branché en USB)
SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE   = 115200

def main():
    # Ouvrir la liaison série
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Laisser un peu de temps à l'Arduino pour s'initialiser

    # La commande qu'on veut envoyer (une seule ligne)
    command = "MOVE X=1000 Y=200"

    print(f"Envoi de la commande : {command}")
    ser.write((command + "\n").encode('utf-8'))  # On envoie la ligne + un saut de ligne

    # Lire la réponse de l’Arduino (si le code Arduino envoie "OK" ou autre)
    response = ser.readline().decode('utf-8').strip()
    print(f"Réponse de l'Arduino : {response}")

    ser.close()

if __name__ == "__main__":
    main()
