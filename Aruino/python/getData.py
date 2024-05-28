import serial
import pygame
import keyboard
import os
import time
import numpy as np
# Xây dựng một class Agent

phi1 = 0
phi2 = 0

def sendArduino():
    dataSend = phi1 * 1000 + phi2
    dataSend = str(dataSend)
    print(f'Current phi1: {phi1}')
    print(f'Current phi2: {phi2}')
    arduino.write(bytes(dataSend, 'utf-8'))
    time.sleep(0.1)
    data = arduino.readline()
    data = data.decode('utf-8')
    print(f'Phi send back from arduino: {data}')

#Main function -------------Start
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
os.system('cls')
mainData = []
try:
    mainData = np.load('dataSet.npy')
    print("Load old date set success")
except:
    print("Cant find old data set. Creating new dataset")
run = 1
while run:
    state = []
    x = float(input("Gia tri truc X: "))
    if x == -1:
        run = 0
    y = float(input("Gia tri truc Y: "))
    state.append(x)
    state.append(y)
    #=============================
    while 1:
        if keyboard.is_pressed('w'):
            phi2 = phi2 + 1
            sendArduino()
        elif keyboard.is_pressed('s'):
            phi2 = phi2 - 1
            sendArduino()
        elif keyboard.is_pressed('a'):
            phi1 = phi1 + 1
            sendArduino()
        elif keyboard.is_pressed('d'):
            phi1 = phi1 - 1
            sendArduino()
        elif keyboard.is_pressed('o'):
            sendArduino()
            break
    state.append((phi1 - 90) / 90)
    state.append((phi2 - 90) / 90)
    mainData.append(state)
    temp = int(input("Do you want continue colect dataset (1/0: continue/stop): "))
    if temp == 1:
        run = 1
    elif temp == 0:
        run = 0
mainData = np.array(mainData)
np.save('dataSet', mainData)
print("Your data set that you colect have been save with file name is dataSet.npy")
