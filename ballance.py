from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

try:
    reader = SimpleMFRC522()

    print(f"place card on the reader...")
    id, text = reader.read()
    print(f"balance of card {id}: {text}")
finally:
  GPIO.cleanup()