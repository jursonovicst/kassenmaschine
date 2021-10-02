from mymfrc522 import MyMFRC522
import RPi.GPIO as GPIO

try:
    reader = MyMFRC522(pin_rst=25, pin_mode=GPIO.BCM)

    print(f"place card on the reader...")
    amount = 100.00
    reader.write(f"{amount:.2f}")
    print(f"write complete")
    id, text = reader.read()
    print(f"new balance of card {id} is {text}")
finally:
  GPIO.cleanup()