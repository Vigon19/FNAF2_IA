
from files.modoIA.detection import Detection
from files.modoIA.env_variables import EnvironmentVariables
from files.modoIA.env_RL import envRL
from files.modoIA.action_manager import ActionsManager
from files.modoIA.draw_ia import DrawIa
from files.modoIA.encoder import SetEncoder
from files.modoIA.anim_paths import AnimPaths
import numpy as np
import pygame
import random
from IPython.display import clear_output
import joblib
import csv
import json
import hashlib
from threading import Lock
class ModoIa:
    def __init__(self,App) :
        self.lock =Lock()
        self.anim_path=AnimPaths()
        self.env_var=EnvironmentVariables(App.objects.office.position[0])
        self.action_manager=ActionsManager(self.env_var,self.lock)
        
        
        self.env= envRL(self.env_var,self.action_manager,App.objects.gameTimer.time)
        self.draw_ia = DrawIa(App.surface)
        self.detection = Detection(self.lock,self.env_var,App.surface,self.anim_path)

        self.q_table = np.zeros([self.env.observation_size] + [self.env.action_space.n])
        # Hyperparameters
        self.alpha = 0.1
        self.gamma = 0.6
        self.epsilon = 0.1
        self.action_interval = 1300  # Intervalo de tiempo en milisegundos entre acciones
        self.white_rect = pygame.Surface((App.surface.get_width(), 80), pygame.SRCALPHA)
        self.white_rect.fill((255, 255, 255,200))
        
        self.last_action_time = pygame.time.get_ticks()
    def train_model(self,App):
        
        for i in range(1, 91):
            done = False
            state = self.env.reset()
            
            events = pygame.event.get()
            App.game_fps = App.clock.tick(App.frames_per_second)
            App.get_deltatime()       
            App.game_events(events)
            App.game.updater(App)
            self.draw_ia.write_log(self.white_rect,App.ia.env_var.log)
            self.draw_ia.draw_rects(self)
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
                    App.game_fps = App.clock.tick(App.frames_per_second)
                    App.get_deltatime()       
                    App.game_events(events)
                    App.game.updater(App)

                    self.draw_ia.write_log(self.white_rect,App.ia.env_var.log)
                    self.draw_ia.draw_rects(self)
                    
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
    def run_model(self):
        # Iniciar el bucle principal para usar el modelo
        for _ in range(10):  # Cambia 10 por el número de pasos que deseas ejecutar
            state = self.env.reset()
            self.app.game.updater(self.app)
            pygame.display.flip()
            size= np.zeros([self.env.observation_size] + [self.env.action_space.n]).shape[0] 
            # Convert the state dictionary to a JSON string
            state_str = json.dumps(state, sort_keys=True, cls=SetEncoder)
            # Hash the JSON string
            hashed_state = int(hashlib.sha256(state_str.encode()).hexdigest(), 16) % size

            
            done = False

            while not done:
                # Usa el modelo para tomar decisiones
                events = pygame.event.get()
                self.app.game_fps = self.app.clock.tick(self.app.frames_per_second)
                self.app.get_deltatime()
                self.app.game_events(events)
                self.app.game.updater(self.app)
                self.draw_ia.draw_rects(self)
                self.draw_ia.write_log(self.white_rect)
                pygame.display.flip()
                current_time = pygame.time.get_ticks()
                if current_time - self.last_action_time >= self.action_interval:
                    action = np.argmax(self.modelo_entrenado[hashed_state])
                    next_state, reward, done, _ = self.env.step(action)
                    state=next_state
                   # Convert the state dictionary to a JSON string
                    state_str = json.dumps(state, sort_keys=True, cls=SetEncoder)
                    # Hash the JSON string
                    hashed_state = int(hashlib.sha256(state_str.encode()).hexdigest(), 16) % size
            
                    # Realizar cualquier otra cosa que necesites con la salida del modelo
                    print(f"Acción: {action}, Recompensa: {reward}, Terminado: {done}")
                    self.last_action_time = current_time