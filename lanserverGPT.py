import threading
import RPi.GPIO as gpio
import time
import sys
import socket
import selectors
import types
import openai 
import json
import speech_recognition as sr
import sounddevice

r = sr.Recognizer()
mic = sr.Microphone()

openai.api_key = "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"
background = "sei un robot umanoide chiamato Emma, hai due amici, entrambi piu piccoli di te chiamati naomi e ettore, quando ti fanno una domanda cerca di rispondere brevemente"
messages = [{"role":"system","content":background}]
# 
# drago_bianco_pin = 17
# stendardo_centrale_pin = 27
# 
# gpio.setmode(gpio.BCM)
# gpio.setup(stendardo_centrale_pin, gpio.OUT)
# gpio.setup(drago_bianco_pin, gpio.OUT)
# 
# gpio.output(stendardo_centrale_pin, False)
# gpio.output(drago_bianco_pin, False)
# 
# # Running cleanup
# gpio.cleanup()
# 
# gpio.setmode(gpio.BCM)
# gpio.setup(stendardo_centrale_pin, gpio.OUT)
# gpio.setup(drago_bianco_pin, gpio.OUT)
# 
# 
# def start_stendardo_centrale():
#     for x in range(500):
#         try:
#             gpio.output(stendardo_centrale_pin, True)
#             time.sleep(0.02)
#             gpio.output(stendardo_centrale_pin, False)
#             time.sleep(0.02)
#         except KeyboardInterrupt as ki:
#             print('Closing Stendardo Centrale by KI')
#             break
#     gpio.output(17, False)
# 
# def start_drago_bianco(random_number):
#     while True:
#         try:
#             gpio.output(drago_bianco_pin, True)
#             time.sleep(0.02)
#             gpio.output(drago_bianco_pin, False)
#             time.sleep(0.02)
#         except KeyboardInterrupt as e:
#             print('Closing Drago Bianco by KI')
#             break
#     gpio.cleanup()

sel = selectors.DefaultSelector()
print(sys.argv)
host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # permette il riutilizzo del socket dopo la chiusura
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

connections = []

def accept_wrapper(sock):
    try:
        conn, addr = sock.accept()  # Should be ready to read
    except socket.error as e:
        print(f"Error accepting connection: {e}")
        return
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
    connections.append(conn)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    try:
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
#             if "drago bianco" in recv_data.decode():
#                 drago_bianco = threading.Thread(target=start_drago_bianco, args=(1,))
#                 drago_bianco.start()
#                 start_stendardo_centrale()
            if recv_data:
                data.outb += recv_data
                # Send message to all connected clients
#                 for conn in connections:
#                     if conn != sock:
#                         try:
#                             conn.sendall(recv_data)
#                         except socket.error as e:
#                             print(f"Error sending data to {conn.getpeername()}: {e}")
#                             connections.remove(conn)
#                             sel.unregister(conn)
#                             conn.close()
            else:
                print(f"Closing connection to {data.addr}")
                sel.unregister(sock)
                sock.close()
                connections.remove(sock)
        if mask & selectors.EVENT_WRITE:
            if data.outb.decode() == "ready":
                print(data.outb,type(data.outb))
                #userInput = input(">>>>")
                
                with mic as source:
                    r.adjust_for_ambient_noise(source)
                    print("parla")
                    audio = r.listen(source)
                    response = r.recognize_google(audio, language="it-IT")
                    print(response)
                    userInput = response
                
                messages.append({"role":"user","content":userInput})
                response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages)

                try:
                    sent = sock.send(bytes(response['choices'][0]['message']['content'], encoding = "utf-8"))  # Should be ready to write
                except socket.error as e:
                    print(f"Error sending data to {data.addr}: {e}")
                    sel.unregister(sock)
                    sock.close()
                    connections.remove(sock)
                else:
                    data.outb = data.outb[sent:]
    except socket.error as e:
        print(f"Error handling connection to {data.addr}: {e}")
        #sel.unregister(sock)
        #sock.close()
        #connections.remove(sock)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
except Exception as e:
    print(f"Caught exception: {e}")
finally:
    sel.close() 
