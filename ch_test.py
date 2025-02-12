import serial
import time

# Adaptation du port selon ta config ; souvent /dev/ttyACM0 sur Linux
# ou COM3, COM4... sur Windows
SERIAL_PORT = "/dev/ttyACM0"  
BAUD_RATE   = 115200

def main():
    # 1) Ouvrir la liaison série
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    
    # 2) Attendre 2 secondes, le temps que l’Arduino se réinitialise
    time.sleep(2)

    # 3) La commande qu'on souhaite envoyer (une seule ligne)
    command = "MOVE X=100 Y=200"

    print(f"Envoi de la commande : {command}")
    # On ajoute un "\n" à la fin, pour que l’Arduino lise la ligne complète
    ser.write((command + "\n").encode('utf-8'))

    # 4) Lire la réponse de l’Arduino (s’il envoie "OK" ou autre)
    response = ser.readline().decode('utf-8').strip()
    print(f"Réponse de l'Arduino : {response}")

    # 5) Fermer la liaison
    ser.close()

if __name__ == "__main__":
    main()
