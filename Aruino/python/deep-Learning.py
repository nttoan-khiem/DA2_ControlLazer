import serial
import keyboard
import os
import time
import random
import numpy as np
import tensorflow
import matplotlib.pyplot as plt
from collections import deque

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

def get_nn(state_size, output_size):
    model  = Sequential()
    model.add (Dense(8, activation='relu', input_dim=state_size))
    model.add (Dense(8, activation='relu'))
    model.add (Dense(output_size))
    model.compile( loss="mse", optimizer=Adam(learning_rate=0.01))
    return model
try:
    DataSet = np.load('dataSet.npy')
except:
    print("Dont have data set, Please prepare dataset in program getData, try again !")
    DataSet = [[0,0,0,0],[1,1,1,1]]
    DataSet = np.array(DataSet)
inModel = DataSet[:, 0:2]
outModel = DataSet[:, 2:4]
myModel = get_nn(2,2)
myModel.summary()
try:
    myModel.load_weights('myweight.weights.h5')
except:
    print("can not find old weight, create new model with random weight. Or something wrong can not load old weight")
history = myModel.fit(inModel, outModel, epochs=200, batch_size = 20, validation_split = 0.2, verbose=1)
print('success')
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
myModel.save_weights('myweight.weights.h5')
