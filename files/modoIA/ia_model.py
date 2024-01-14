import random
from IPython.display import clear_output
import numpy as np
import pygame
import joblib
import csv
import json
import hashlib
from files.modoIA.encoder import SetEncoder
class Trainer:
    def __init__(self, App):
        self.env = App.env
        self.App = App
        self.q_table = np.zeros([self.env.observation_size] + [self.env.action_space.n])
        # Hyperparameters
        self.alpha = 0.1
        self.gamma = 0.6
        self.epsilon = 0.1
        self.action_interval = 1000  # Intervalo de tiempo en milisegundos entre acciones
        self.last_action_time = pygame.time.get_ticks()

    def train_model(self):
        
        for i in range(1, 101):
            done = False
            state = self.env.reset()
            self.App.game.updater(self.App)
            pygame.display.flip()
            table_size = self.q_table.shape[0]  # Tamaño de la tabla Q
            # Convert the state dictionary to a JSON string
            state_str = json.dumps(state, sort_keys=True, cls=SetEncoder)
            # Hash the JSON string
            hashed_state = int(hashlib.sha256(state_str.encode()).hexdigest(), 16) % table_size

            epochs, penalties, reward, = 0, 0, 0
            
             # Agregar código para abrir o crear el archivo CSV
            csv_file = open('datos_entrenamiento.csv', mode='w', newline='')
            fieldnames = ['Episode', 'Reward', 'Penalties', 'State', 'Hashed_State','value']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            clear_output(wait=True)
            print("-------------------------------NUEVO EPISODIO-----------------------")
            try:
                while not done:
                    events = pygame.event.get()

                    self.App.game_fps = self.App.clock.tick(self.App.frames_per_second)
                    self.App.get_deltatime()
                   
                    self.App.game_events(events)
                    self.App.game.updater(self.App)
                    self.App.ia.draw_rects()
                  
                    pygame.display.flip()
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_action_time >= self.action_interval:
                        if random.uniform(0, 1) < self.epsilon:
                            action = self.env.action_space.sample()  # Explore action space
                        else:
                            action = np.argmax(self.q_table[hashed_state])  # Exploit learned values

                        next_state, reward, done, info = self.env.step(action)
                        pygame.display.set_caption(f"Episodio: {i} Accion:{action} Tiempo en oficina:{self.App.ia.action_manager.get_action_duration('observe_office')  }  Tiempo en monitor:{self.App.ia.action_manager.get_action_duration('observe_monitor')}   Tiempo foxy:{self.App.ia.action_manager.time_action_foxy}   Tiempo puppet:{self.App.ia.action_manager.get_action_duration('defensa_puppet')} RECOMPENSA : {reward} ")
                        old_value = self.q_table[hashed_state, action]
                        next_max = np.max(self.q_table[hashed_state])

                        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
                        self.q_table[hashed_state, action] = new_value
                        clock = pygame.time.Clock()
                    
                        #print(f"Observación (anim_map): {hashed_state['anim_map']}, Recompensa: {reward}, Terminado: {done}")
                       

                        if reward == -5:
                            penalties += 1
                        state_str = json.dumps(state, sort_keys=True, cls=SetEncoder)
   
                        writer.writerow({'Episode': i, 'Reward': reward, 'Penalties': penalties,
                                            'State': state_str, 'Hashed_State': hashed_state, "value":new_value})
                        state = next_state
                        epochs += 1
                        
                        # Hash the JSON string
                        hashed_state = int(hashlib.sha256(state_str.encode()).hexdigest(), 16) % table_size
                        # Actualizar el tiempo de la última acción
                        self.last_action_time = current_time

                    
            finally:
                    # Cerrar el archivo CSV al finalizar, incluso si ocurre una excepción
                    csv_file.close()
        print("Training finished.\n")
        model_filename = "modelo_entrenado.joblib"
        joblib.dump(self.q_table, model_filename)
        print(f"Modelo entrenado guardado en {model_filename}")
