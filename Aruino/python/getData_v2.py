import serial
import pygame
import os
import time
import numpy as np
# Pygame for interface
pygame.init() 
# setting frame/window/surface with some dimensions 
window = pygame.display.set_mode((1040, 780)) 
# to set title of pygame window 
pygame.display.set_caption("Get_dataSet") 
clock = pygame.time.Clock() 
# creating image object 
try:
    image = pygame.image.load('./picture/img.jpg') 
    image = pygame.transform.scale(image, (1040, 780))
except:
    print('can find img for this position')
    image = pygame.image.load('./picture/imgNotFound.jpg')
    image = pygame.transform.scale(image, (1040, 780))
# to display size of image 
print("size of image is (width,height):", image.get_size()) 
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
    mainData = np.array(mainData).tolist()
    print("Load old date set success")
except:
    print("Cant find old data set. Creating new dataset")

# loop to run window continuously 
while True: 
    window.blit(image, (0, 0)) 
    # loop through the list of Event 
    for event in pygame.event.get(): 
        # to end the event/loop 
        if event.type == pygame.QUIT: 
            mainData = np.array(mainData)
            np.save('dataSet', mainData)
            print("Your data set that you colect have been save with file name is dataSet.npy")
            # it will deactivate the pygame library 
            pygame.quit() 
            quit() 
        # to display when screen update 
        pygame.display.flip() 
        if event.type == pygame.MOUSEBUTTONUP:
            positionMouse = pygame.mouse.get_pos()
            state = []
            x = positionMouse[0] / 1040
            y = positionMouse[1] / 780
            state.append(x)
            state.append(y)
            state.append((phi1 - 90) / 90)
            state.append((phi2 - 90) / 90)
            mainData.append(state)
            print('dataSet have been saved: {}', state)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                phi2 = phi2 + 1
                sendArduino()
            if event.key == pygame.K_s:
                phi2 = phi2 - 1
                sendArduino()
            if event.key == pygame.K_a:
                phi1 = phi1 + 1
                sendArduino()
            if event.key == pygame.K_d:
                phi1 = phi1 - 1
                sendArduino()
# Xây dựng một class Agent