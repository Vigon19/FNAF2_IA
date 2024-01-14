import joblib
import numpy as np
import pygame
import json
import hashlib
from files.modoIA.encoder import SetEncoder
class TestModel:
    def __init__(self,App) :
       
     # Cargar el modelo entrenado
     self.modelo_entrenado = joblib.load("modelo_entrenado.joblib")
     self.app=App
     # Crear una instancia del entorno
     self.env = App.env  # Asegúrate de tener una instancia de App antes de crear el entorno
     self.last_action_time = pygame.time.get_ticks()
     self.action_interval = 2000  # Intervalo de tiempo en milisegundos entre acciones
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
                self.app.ia.draw_rects()
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
