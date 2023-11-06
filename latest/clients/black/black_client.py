import bluetooth
import threading
import RPi.GPIO as gpio
import time
import sys

dragon_pin = 17
flag_pin = 27
dragon_thread = 0
dragon_stop = False

gpio.setmode(gpio.BCM)
gpio.setup(flag_pin, gpio.OUT)
gpio.setup(dragon_pin, gpio.OUT)

gpio.output(flag_pin, False)
gpio.output(dragon_pin, False)

# Running cleanup
gpio.cleanup()

gpio.setmode(gpio.BCM)
gpio.setup(flag_pin, gpio.OUT)
gpio.setup(dragon_pin, gpio.OUT)


def stop_all():
    dragon_stop = True
    gpio.output(flag_pin, False)
    gpio.output(dragon_pin, False)
    print('Stopping...')


def start_flag():
    for x in range(115):
        try:
            gpio.output(flag_pin, True)
            time.sleep(0.02)
            gpio.output(flag_pin, False)
            time.sleep(0.02)
        except KeyboardInterrupt as ki:
            print('Closing Flag by KI')
            break
    gpio.output(flag_pin, False)

def start_dragon(random_number):
    while not dragon_stop:
        try:
            gpio.output(dragon_pin, True)
            time.sleep(0.02)
            gpio.output(dragon_pin, False)
            time.sleep(0.02)
        except KeyboardInterrupt as e:
            print('Closing Drago Bianco by KI')
            break
    gpio.cleanup()
    print('Dragon thread stopped')

# Bluetooth socket
server_address = 'DC:A6:32:55:81:AB'
port = 1


def receive_data(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        data = data.decode()
        print(data)
        if "riavvia" in data:
            stop_all()
        elif "drago nero" in data:
            dragon_thread = threading.Thread(target=start_dragon, args=(1,))
            dragon_thread.start()
            start_flag()


client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
client_socket.connect((server_address, port))

# Create a separate thread for receiving data
receive_thread = threading.Thread(target=receive_data, args=(client_socket,))
receive_thread.start()

while True:
    message = input('')
    if message == 'quit':
        break
    client_socket.send(message)

client_socket.close()
receive_thread.join()
