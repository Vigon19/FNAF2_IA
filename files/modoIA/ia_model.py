
"""Training the agent"""
import random
from IPython.display import clear_output
import numpy as np
import pygame
class Trainer:
    def __init__(self,App):
        self.env=App.env
        game_surface_shape = App.env.observation_space['game_surface'].shape
        self.q_table = np.zeros([self.env.anim_map_size] + list(game_surface_shape) + [self.env.action_space.n])
        # Hyperparameters
        self.alpha = 0.1
        self.gamma = 0.6
        self.epsilon = 0.1


    def train_model(self):
            for i in range(1, 100001):
                state = self.env.reset()
                table_size = self.q_table.shape[0]  # Tamaño de la tabla Q
                hashed_state = hash(tuple(state)) % table_size
                epochs, penalties, reward, = 0, 0, 0
                done = False
                
                while not done:
                    if random.uniform(0, 1) < self.epsilon:
                        action = self.env.action_space.sample() # Explore action space
                    else:
                        action = np.argmax(self.q_table[hashed_state]) # Exploit learned values

                    next_state, reward, done, info = self.env.step(action) 
                    
                    old_value = self.q_table[hashed_state, action]
                    next_max = np.max(self.q_table[hashed_state])
                    
                    new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
                    self.q_table[hashed_state, action] = new_value

                    if reward == -10:
                        penalties += 1

                    state = next_state
                    epochs += 1
                    
                if i % 100 == 0:
                    clear_output(wait=True)
                    print(f"Episode: {i}")

            print("Training finished.\n")
