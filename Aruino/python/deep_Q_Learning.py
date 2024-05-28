import serial
import keyboard
import os
import time
import random
import numpy as np
import tensorflow
from collections import deque

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

# Xây dựng một class Agent
class MyAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.phi1 = 90
        self.phi2 = 90
        # Khởi tạo replay buffer
        self.replay_buffer = deque(maxlen=50000)

        # Khởi tạo tham số của Agent
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.98
        self.learning_rate = 0.001
        self.update_targetnn_rate = 10

        self.main_network = self.get_nn()
        self.target_network = self.get_nn()

        # Update weight của mạng target = mạng main
        self.target_network.set_weights(self.main_network.get_weights())

    def get_nn(self):
        model  = Sequential()
        model.add (Dense(16, activation='relu', input_dim=self.state_size))
        model.add (Dense(16, activation='relu'))
        model.add (Dense(self.action_size))
        model.compile( loss="mse", optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def save_experience(self, state, action, reward, next_state, terminal):
        self.replay_buffer.append((state, action, reward, next_state, terminal))

    def get_batch_from_buffer(self, batch_size):
        exp_batch = random.sample(self.replay_buffer, batch_size)
        state_batch  = np.array([batch[0] for batch in exp_batch]).reshape(batch_size, self.state_size)
        action_batch = np.array([batch[1] for batch in exp_batch])
        reward_batch = [batch[2] for batch in exp_batch]
        next_state_batch = np.array([batch[3] for batch in exp_batch]).reshape(batch_size, self.state_size)
        terminal_batch = [batch[4] for batch in exp_batch]
        return state_batch, action_batch, reward_batch, next_state_batch, terminal_batch

    def train_main_network(self, batch_size):
        state_batch, action_batch, reward_batch, next_state_batch, terminal_batch = self.get_batch_from_buffer(batch_size)
        # Lấy Q value của state hiện tại
        q_values = self.main_network.predict(state_batch, verbose=0)
        # Lấy Max Q values của state S' (State chuyển từ S với action A)
        next_q_values = self.target_network.predict(next_state_batch, verbose=0)
        max_next_q = np.amax(next_q_values, axis=1)

        for i in range(batch_size):
            new_q_values = reward_batch[i] if terminal_batch[i] else reward_batch[i] + self.gamma * max_next_q[i]
            q_values[i][action_batch[i]] = new_q_values

        self.main_network.fit(state_batch, q_values, verbose=0)

    def make_decision(self, state):
        state = state.reshape((1, self.state_size))
        q_values = self.main_network.predict(state, verbose=0)
        print(q_values)
        action =  np.argmax(q_values[0])
        print(action)
        if action == 0:
            pass
        elif action == 1:
            if self.phi1 < 180:
                self.phi1 = self.phi1 + 1
        elif action == 2:
            if self.phi1 > 0:
                self.phi1 = self.phi1 - 1
        elif action == 3:
            if self.phi2 < 180:
                self.phi2 = self.phi2 + 1
        elif action == 4:
            if self.phi2 > 0:
                self.phi2 = self.phi2 - 1
        return action
    
    def sendArduino(self):
        dataSend = self.phi1 * 1000 + self.phi2
        dataSend = str(dataSend)
        print(f'Current phi1: {self.phi1}')
        print(f'Current phi2: {self.phi2}')
        arduino.write(bytes(dataSend, 'utf-8'))
        time.sleep(0.1)
        data = arduino.readline()
        data = data.decode('utf-8')
        print(f'Phi send back from arduino: {data}')

    def out_qvalue(self, state):
        state = state.reshape((1, self.state_size))
        return self.main_network.predict(state, verbose = 1)
    
    def summaryModel(self):
        self.main_network.summary()

#Main function -------------Start
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
os.system('cls')
sizeAction = 5
sizeState = 4
agent = MyAgent(sizeState, sizeAction)
agent.summaryModel()
n_episodes = 80
n_timesteps = 10
batch_size = 64
run = 1
while run:
    state = []
    x = float(input("Gia tri truc X: "))
    if x == -1:
        run = 0
    y = float(input("Gia tri truc Y: "))
    state.append(x)
    state.append(y)
    state.append((agent.phi1 - 90) / 90)
    state.append((agent.phi2 - 90) / 90)
    state = np.array(state)
    print(agent.out_qvalue(state))
    #=============================
    for ep in range(n_episodes):
        ep_rewards = 0
        n_timesteps = 100
        total_time_step = 0
        for t in range(n_timesteps):
            total_time_step += 1
            # Cập nhật lại target NN mỗi my_agent.update_targetnn_rate
            if total_time_step % agent.update_targetnn_rate == 0:
                # Có thể chọn cách khác = weight của targetnetwork = 0 * weight của targetnetwork  + 1  * weight của mainnetwork
                agent.target_network.set_weights(agent.main_network.get_weights())
            action = agent.make_decision(state)
            agent.sendArduino()
            next_state = []
            next_state.append(x)
            next_state.append(y)
            next_state.append(agent.phi1)
            next_state.append(agent.phi2)
            next_state = np.array(next_state)
            while (1):
                if keyboard.is_pressed('n'):
                    reward = -2
                    break
                elif keyboard.is_pressed('o'):
                    reward = 2
                    break
            terminal = 0
            agent.save_experience(state , action, reward, next_state, terminal)
            state = next_state
            ep_rewards += reward

            if len(agent.replay_buffer) > batch_size:
                agent.train_main_network(batch_size)


# Save weights
agent.main_network.save("train_agent.keras")
