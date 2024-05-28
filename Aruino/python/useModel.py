import os
os.system("cls")
import pygame
from pygame import mixer
mixer.init()
mixer.music.load("./Audio/intro.wav")
mixer.music.play()
import serial
import time
import numpy as np
import tensorflow
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

#global variable
phi1 = 0
phi2 = 0
running = True
firstClick = True
try:
    arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
except:
    print('can not open port to connect with arduino, Please check your connection and try again')
    running = False
#endn define global variable
#define function using for connecting with arrduino
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
# Pygame for interface
pygame.init() 
window = pygame.display.set_mode((1040, 780)) 
pygame.display.set_caption("Using model") 
clock = pygame.time.Clock() 
try:
    image = pygame.image.load('./picture/img.jpg') 
    image = pygame.transform.scale(image, (1040, 780))
except:
    print('can find img for this position, The program will be close, Please check picture on Picture folder and try again')
    running = False
    image = pygame.image.load('./picture/imgNotFound.jpg')
    image = pygame.transform.scale(image, (1040, 780))
# End define pygame interface

#define and build model
model  = Sequential()
model.add (Dense(8, activation='relu', input_dim=2))
model.add (Dense(8, activation='relu'))
model.add (Dense(2))
try:
    model.load_weights('myweight.weights.h5')
except:
    print('can not load weight of model which has been tranned, This model have been create with random weight. It cant use for predict angle of servo. Program will be close, Please check file weight myweight.weights.h5 and try again')
    running = False

while running:
    window.blit(image, (0, 0)) 
    # loop through the list of Event 
    for event in pygame.event.get(): 
        # to end the event/loop 
        if event.type == pygame.QUIT: 
            print("Thanks for using this program")
            # it will deactivate the pygame library 
            pygame.quit() 
            quit() 
        # to display when screen update 
        pygame.display.flip() 
        if event.type == pygame.MOUSEBUTTONUP:
            if firstClick:
                mixer.music.load("./Audio/causion.wav")
                mixer.music.play()
                firstClick = False
            else:
                mixer.music.load("./Audio/activeWarming.wav")
                mixer.music.play()
                print("[On processing]")
                positionMouse = pygame.mouse.get_pos()
                state = []
                x = positionMouse[0] / 1040
                y = positionMouse[1] / 780
                state.append(x)
                state.append(y)
                state = np.array(state)
                state.resize((1,2))
                outModel = model.predict(state, verbose=1)
                phi1 = 90*outModel[0][0] + 90
                phi2 = 90*outModel[0][1] + 90
                phi1 = int(phi1)
                phi2 = int(phi2)
                print('Model predict angle of servo Phi1: {}, Phi2: {}'.format(phi1, phi2))
                sendArduino()
