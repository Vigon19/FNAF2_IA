import random
from IPython.display import clear_output
import numpy as np
import pygame
import joblib
import csv
import json
import hashlib
from files.modoIA.encoder import SetEncoder
from files.modoIA.draw_ia import DrawIa
from files.modoIA.env_RL  import envRL
class Trainer():
    def __init__(self,App):
        self.app=App
        self.env=App.ia.env
        self.q_table = np.zeros([self.env.observation_size] + [self.env.action_space.n])
        # Hyperparameters
        self.alpha = 0.1
        self.gamma = 0.6
        self.epsilon = 0.1
        self.action_interval = 1300  # Intervalo de tiempo en milisegundos entre acciones
        self.white_rect = pygame.Surface((App.surface.get_width(), 80), pygame.SRCALPHA)
        self.white_rect.fill((255, 255, 255,200))
        self.draw_ia = DrawIa(App.surface)
        self.last_action_time = pygame.time.get_ticks()
        

    def train_model(self,App):
        
        for i in range(1, 91):
            done = False
            state = self.env.reset()
            
            events = pygame.event.get()
            self.app.game_fps = self.app.clock.tick(self.app.frames_per_second)
            self.app.get_deltatime()       
            self.app.game_events(events)
            self.app.game.updater(self.app)
            self.draw_ia.write_log(self.white_rect)
            self.draw_ia.draw_rects(App)
            pygame.display.flip() #ACTUALIZAR FRAME
            table_size = self.q_table.shape[0]  # Tamaño de la tabla Q

            # Convert the state dictionary to a JSON string
            state_str = json.dumps(state, sort_keys=True, cls=SetEncoder)
            # Hash the JSON string
            hashed_state = int(hashlib.sha256(state_str.encode()).hexdigest(), 16) % table_size

            epochs, penalties, reward, = 0, 0, 0
            
            #Agregar código para abrir o crear el archivo CSV
            csv_file = open('datos_entrenamiento.csv', mode='w', newline='')
            fieldnames = ['Episode', 'Reward', 'Penalties', 'State', 'Hashed_State','value']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            clear_output(wait=True)
            print(f"-------------------------------EPISODIO NÚMERO {i}-----------------------")
            try:
                while not done:
                    #VARIABLE DEL JUEGO NECESARIAS
                    events = pygame.event.get()
                    self.app.game_fps = self.app.clock.tick(self.app.frames_per_second)
                    self.app.get_deltatime()       
                    self.app.game_events(events)
                    self.app.game.updater(self.app)

                    self.draw_ia.draw_rects()
                    self.draw_ia.write_log()
                    
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_action_time >= self.action_interval:

                        #Q-LEARNING
                        if random.uniform(0, 1) < self.epsilon:
                            action = self.env.action_space.sample()  # Explore action space
                        else:
                            action = np.argmax(self.q_table[hashed_state])  # Exploit learned values

                        #TOMA LA SIGUIENTE ACCION
                        next_state, reward, done, info = self.env.step(action)

                        
                        old_value = self.q_table[hashed_state, action]

                        #DECIDE SI USAR ESTA ACCION O UNA ACCION ANTERIOR
                        next_max = np.max(self.q_table[hashed_state])

                        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
                        self.q_table[hashed_state, action] = new_value
                        clock = pygame.time.Clock()
                    
                    
                        if reward == -5:
                            penalties += 1

                        #ESCRIBIMOS EN EL CSV LOS RESULTADOS
                        state_str = json.dumps(state, sort_keys=True, cls=SetEncoder)
   
                        writer.writerow({'Episode': i, 'Reward': reward, 'Penalties': penalties,
                                            'State': state_str, 'Hashed_State': hashed_state, "value":new_value})
                        state = next_state
                        epochs += 1
                        
                        # Hash the JSON string
                        hashed_state = int(hashlib.sha256(state_str.encode()).hexdigest(), 16) % table_size
                        # Actualizar el tiempo de la última acción
                        self.last_action_time = current_time

                    #ACTUALIZAR EL FRAME
                    pygame.display.flip()
                    
            finally:
                    # Cerrar el archivo CSV al finalizar, incluso si ocurre una excepción
                    csv_file.close()
        print("Training finished.\n")
        model_filename = "modelo_entrenado.joblib"
        joblib.dump(self.q_table, model_filename)
        print(f"Modelo entrenado guardado en {model_filename}")
