import gym
from gym import spaces
import random
import pygame
import numpy as np
from files.modoIA.ActionsManager import ActionsManager

class FNAF2Env(gym.Env):
    def __init__(self, App):
        super(FNAF2Env, self).__init__()
        self.app = App
        self.anim_map = App.ia.anim_map
        self.num_camera = App.ia.num_camera
        self.previous_action=-1
        self.last_camera_change_time = pygame.time.get_ticks()
        self.music_box_time=pygame.time.get_ticks()
        # Definir el espacio de acciones y observaciones
        self.action_space = spaces.Discrete(9)  # 9 acciones posibles

        # Obtén la forma de la superficie del juego
        # game_surface_shape = pygame.surfarray.array3d(App.surface).shape

        # Define el espacio de observación
        self.observation_space = spaces.Dict({
            'num_camera': spaces.Discrete(13),
            'anim_map': spaces.MultiDiscrete([len(App.ia.anim_map)] * 13),
            # 'game_surface': spaces.Box(low=0, high=255, shape=game_surface_shape, dtype=np.uint8)
        })
        self.anim_map_size = self.observation_space['num_camera'].n + sum(self.observation_space['anim_map'].nvec)
        # Inicializar variables de estado
        self.action_manager = ActionsManager(App.ia)

    def reset(self):
        # Reiniciar el entorno a un estado inicial
        self.app.ia.reset()
        return self._get_observation()

    def step(self, action):
        # Tomar una acción y avanzar un paso en el entorno

        # Mapear acciones a funciones específicas
        if action == 0:
            self.action_manager.observe_office()
        elif action == 1:
            self.action_manager.observe_monitor()
        elif action == 2:
            self.action_manager.defense_normal()
        elif action == 3:
            self.action_manager.defense_foxy()
        elif action == 4:
            self.action_manager.defensa_balloon_boy()
        elif action == 5:
            self.action_manager.defensa_puppet()
        elif action == 6:
            self.action_manager.turn_on_light()
        elif action == 7:
            self.action_manager.turn_off_light()
        elif action == 8:
            self.action_manager.change_camera()
        # Obtener la observación después de la acción
        observation = self._get_observation()
        
        # Calcular la recompensa
        reward = 0  # Inicializa la recompensa en 0

        if self.app.ia.game_over or self.app.ia.jumpscare:
            reward = -1  # Dar una recompensa negativa si el juego ha terminado

        if action == 1 and len(self.anim_map[0]) == 0:
            reward += 1 # Dar una recompensa positiva si se ejecuta la acción 1 y anim_map[0] está vacío
        else:
            reward -=1
        if action == 0 and len(self.anim_map[0]) > 0:
            reward +=1  # Dar una recompensa positiva si se ejecuta la acción 2 y anim_map[0] no está vacío
        else:
            reward -=1

        if self.previous_action == 1 and pygame.time.get_ticks() - self.last_camera_change_time >= 1500:
            if action==8:
                reward+=5
                self.last_camera_change_time= pygame.time.get_ticks()
        if self.previous_action==1:
            if action==1:
                reward -=1
        # Determinar si el episodio ha terminado
        if (action == 2 or action == 3 or action == 4) and len(self.anim_map[0]) == 0: 
            reward -= 1
        if (action == 2 or action == 3 or action == 4) and len(self.anim_map[0]) > 0: 
            reward += 1
            
        if pygame.time.get_ticks()- self.music_box_time>=3000:
            if action == 5:
                reward +=1

        done = self.app.ia.game_over

        # Información adicional (opcional)
        info = {}
        self.previous_action=action
        return observation, reward, done, info

    def render(self):
        # Método opcional para visualizar el entorno
        print(f"Estado actual: {self.num_camera}")

    def _get_observation(self):
        game_surface_array = pygame.surfarray.array3d(self.app.surface).shape
        # Obtener la observación actual del entorno
        return {
            'num_camera': self.app.ia.num_camera,
            'anim_map': self.app.ia.anim_map,
            # 'game_surface':spaces.Box(low=0, high=255, shape=game_surface_array, dtype=np.uint8)
        }
