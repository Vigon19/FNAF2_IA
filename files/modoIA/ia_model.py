import random
from IPython.display import clear_output
import numpy as np
import pygame
import joblib

class Trainer:
    def __init__(self, App):
        self.env = App.env
        self.App = App
        # game_surface_shape = App.env.observation_space['game_surface'].shape
        self.q_table = np.zeros([self.env.anim_map_size] + [self.env.action_space.n])
        # Hyperparameters
        self.alpha = 0.1
        self.gamma = 0.6
        self.epsilon = 0.1
        self.action_interval = 1200  # Intervalo de tiempo en milisegundos entre acciones
        self.last_action_time = pygame.time.get_ticks()

    def train_model(self):
        for i in range(1, 100001):
            state = self.env.reset()
            table_size = self.q_table.shape[0]  # Tamaño de la tabla Q
            hashed_state = hash(tuple(state)) % table_size
            epochs, penalties, reward, = 0, 0, 0
            done = False

            while not done:
                self.App.game.updater(self.App)
                pygame.display.flip()

                current_time = pygame.time.get_ticks()
                if current_time - self.last_action_time >= self.action_interval:
                    # Realizar acción solo si ha pasado el intervalo de tiempo especificado
                    if random.uniform(0, 1) < self.epsilon:
                        action = self.env.action_space.sample()  # Explore action space
                    else:
                        action = np.argmax(self.q_table[hashed_state])  # Exploit learned values

                    next_state, reward, done, info = self.env.step(action)

                    old_value = self.q_table[hashed_state, action]
                    next_max = np.max(self.q_table[hashed_state])

                    new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
                    self.q_table[hashed_state, action] = new_value

                    print(f"Observación (anim_map): {state['anim_map']}, Recompensa: {reward}, Terminado: {done}")
                    if reward == -10:
                        penalties += 1

                    state = next_state
                    epochs += 1

                    # Actualizar el tiempo de la última acción
                    self.last_action_time = current_time

            if i % 100 == 0:
                clear_output(wait=True)
                print(f"Episode: {i}")

        print("Training finished.\n")
        model_filename = "modelo_entrenado.joblib"
        joblib.dump(self.q_table, model_filename)
        print(f"Modelo entrenado guardado en {model_filename}")
