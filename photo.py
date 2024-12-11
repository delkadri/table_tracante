from picamera2 import Picamera2
from time import sleep

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())

picam2.start()

try:
    sleep(2)
    picam2.capture_file("image.jpg")

finally:
    picam2.stop()