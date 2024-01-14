import gym
from gym import spaces
import pygame
import numpy as np
from files.modoIA.ActionsManager import ActionsManager
import time
class FNAF2Env(gym.Env):
    def __init__(self, App):
        super(FNAF2Env, self).__init__()
        self.app = App
        self.anim_map = App.ia.anim_map
        self.num_camera = App.ia.num_camera
        self.change_camera=0
        self.previous_action=1
        # Definir el espacio de acciones y observaciones
        self.action_space = spaces.Discrete(7)  # 9 acciones posibles
        self.no_defense_puppet=pygame.time.get_ticks()
        # Obtén la forma de la superficie del juego
        # game_surface_shape = pygame.surfarray.array3d(App.surface).shape

        # Define el espacio de observación
        self.observation_space = spaces.Dict({
            'anim_map': spaces.MultiDiscrete([len(App.ia.anim_map)] * 13),
            'last_action': spaces.Discrete(self.action_space.n),
            'open_monitor': spaces.Discrete(2),  # Abierto (1) o cerrado (0)
            'num_camera': spaces.Discrete(13),   # Cámaras del 0 al 12
            'hallway': spaces.Discrete(2),       # Verdadero (1) o falso (0)
            'right_vent': spaces.Discrete(2),    # Verdadero (1) o falso (0)
            'left_vent': spaces.Discrete(2),     # Verdadero (1) o falso (0)
            'put_mask': spaces.Discrete(2),      # Verdadero (1) o falso (0)
            'jumpscare': spaces.Discrete(2),     # Verdadero (1) o falso (0)
            'in_office': spaces.Discrete(2),     # Verdadero (1) o falso (0)
            'flashlight': spaces.Discrete(2),    # Verdadero (1) o falso (0)
            'music_box': spaces.Discrete(2)      # Verdadero (1) o falso (0)
        })
        self.observation_size = (sum(self.observation_space['anim_map'].nvec) + 39)
        

    def reset(self):
        # Reiniciar el entorno a un estado inicial
        self.app.ia.reset()
        self.no_defense_puppet=pygame.time.get_ticks()
        self.app.ia.action_manager.time_action_foxy=0
        self.app.ia.action_manager.time_action_puppet=0
        self.app.ia.action_manager.time_defense=0
        return self._get_observation()

    def step(self, action):
        # Tomar una acción y avanzar un paso en el entorno

        # Mapear acciones a funciones específicas

        if action == 0:
            self.app.ia.action_manager.change_camera()
        elif action == 1:
            self.app.ia.action_manager.defense_normal()
        elif action == 2:
            self.app.ia.action_manager.defense_foxy()
        elif action == 3:
            self.app.ia.action_manager.defensa_balloon_boy()
        elif action == 4:
            self.app.ia.action_manager.defensa_puppet()
        elif action == 5:
            self.app.ia.action_manager.turn_left()
        elif action == 6:
            self.app.ia.action_manager.turn_right()
        # Obtener la observación después de la acción
        observation = self._get_observation()
        
        # Calcular la recompensa
        reward = 0  # Inicializa la recompensa en 0


                #DEFENSA
                 #ANIMATRONICO DETECTADO EN LA OFICINA (DENTRO, EN PASILLO O VENTILACIÓN)
                
        if len(self.app.ia.anim_map[0])>0:
                    print("---------------------ANIMATRONICO DETECTADO----------------")
                    #SI ES FOXY SE DEFIENDE CON ACCION 'DEFENSE_FOXY'
                    if 'withered_foxy' in self.app.ia.anim_map[0]:
                        print("---------------------FOXY----------------")
                        if self.app.ia.action_manager.time_action_foxy<5000:
                            if action == 2:
                                print("---------------------DEFENSA FOXY (+2)----------------")
                                reward += 6
                            else:
                                print("---------------------NO DEFENSA FOXY (-5)----------------")
                                reward -=2
                    #SI ES BALLOON_BOY SE DEFIENDE CON ACCION 'DEFENSE_FOXY'
                    if 'balloon_boy' in self.anim_map[0] :
                        print("---------------------BALLOON BOY----------------")
                        if action == 1:
                            print("---------------------DEFENSA BALLOON BOY (+2)----------------")
                            reward += 6
                        else:
                            print("---------------------NO DEFENSA BALLOON BOY (-5)----------------")
                            reward -=2
                    if 'withered_bonnie' in self.anim_map[0] :
                        print("---------------------BALLOON BOY----------------")
                        if action == 1:
                            print("---------------------DEFENSA BALLOON BOY (+2)----------------")
                            reward += 6
                        else:
                            print("---------------------NO DEFENSA BALLOON BOY (-5)----------------")
                            reward -=2
                    if 'withered_chica' in self.anim_map[0] :
                        print("---------------------BALLOON BOY----------------")
                        if action == 1:
                            print("---------------------DEFENSA BALLOON BOY (+2)----------------")
                            reward += 6
                        else:
                            print("---------------------NO DEFENSA BALLOON BOY (-5)----------------")
                            reward -=2
                    if 'withered_freddy' in self.anim_map[0] :
                        print("---------------------BALLOON BOY----------------")
                        if action == 1:
                            print("---------------------DEFENSA BALLOON BOY (+2)----------------")
                            reward += 6
                        else:
                            print("---------------------NO DEFENSA BALLOON BOY (-5)----------------")
                            reward -=2
                    if 'toy_freddy' in self.anim_map[0] :
                        print("---------------------BALLOON BOY----------------")
                        if action == 1:
                            print("---------------------DEFENSA BALLOON BOY (+2)----------------")
                            reward += 6
                        else:
                            print("---------------------NO DEFENSA BALLOON BOY (-5)----------------")
                            reward -=2
        elif len(self.app.ia.anim_map[5])>0:
                    if 'balloon_boy' in self.anim_map[5] :
                        print("---------------------BALLOON BOY----------------")
                        if action == 1:
                            print("---------------------DEFENSA BALLOON BOY (+2)----------------")
                            reward += 6
                        else:
                            print("---------------------NO DEFENSA BALLOON BOY (-5)----------------")
                            reward -=2
                    if 'toy_chica' in self.anim_map[5] :
                        print("---------------------TOY CHICA----------------")
                        if action == 1:
                            print("---------------------DEFENSA TOY CHICA (+2)----------------")
                            reward += 6
                        else:
                            print("---------------------NO DEFENSA TOY CHICA (-5)----------------")
                            reward -=2
        elif len(self.app.ia.anim_map[6])>0:
                    if 'toy_bonnie' in self.anim_map[6] :
                        print("---------------------TOY BONNIE----------------")
                        if action == 1:
                            print("---------------------DEFENSA TOY BONNIE (+2)----------------")
                            reward += 6
                        else:
                            print("---------------------NO DEFENSA TOY BONNIE (-5)----------------")
                            reward -=2
                    if 'mangle' in self.anim_map[6] :
                        print("---------------------TOY BONNIE----------------")
                        if action == 1:
                            print("---------------------DEFENSA TOY BONNIE (+2)----------------")
                            reward += 6
                        else:
                            print("---------------------NO DEFENSA TOY BONNIE (-5)----------------")
                            reward -=2
                #OBSERVACIÓN
        else:
                    
                    #MIRANDO CAMARAS
                    if action == 0:
                        print("-----------------MIRANDO CAMARAS---------------")
                        #MAS DE 12 SEGUNDOS
                        if (self.app.ia.action_manager.get_action_duration("observe_monitor") > 12000):
                                print("-----------------MÁS DE 12 SEGUNDOS---------------")
                                #CAJA DE MUSICA LE QUEDA TIEMPO
                                if pygame.time.get_ticks()- self.no_defense_puppet<=4000:
                                    print("-----------------PUPPET QUEDA TIEMPO---------------")
                                    #CAMBIO A OFICINA
                                    if action in [1,5,6]:
                                        print("-----------------CAMBIO A OFICINA (+3)---------------")
                                        reward+=3
                                    #SEGUIR EN CAMARAS
                                    elif action ==0:
                                        print("-----------------SEGUIR EN CAMARAS(-5)---------------")
                                        reward-=5
                                else:
                                    print("-----------------PUPPET NO QUEDA TIEMPO---------------")
                                    if action == 4:
                                        print("-----------------PROTEGER PUPPET (+3)---------------")
                                        reward+=3
                                    else:
                                        print("-----------------NO PROTEGER PUPPET (-5)---------------")
                                        reward-=5
                        #MENOS DE 12 SEGUNDOS
                        else:
                            print("---------------- MENOS DE 12 SEGUNDOS ---------------")
                            if action == 0:
                                print("----------------SEGUIR EN CAMARAS(+2) ---------------")
                                reward+=2
                    #EN OFICINA
                    if action in [5,6]:
                        #MAS DE 8 SEGUNDOS
                        if self.app.ia.action_manager.get_action_duration("observe_office") >= 8000:
                             print("---------------MÁS DE 8 SEGUNDOS----------------")
                             #CAJA DE MUSICA LE QUEDA TIEMPO
                             if pygame.time.get_ticks()- self.no_defense_puppet<=8000:
                                print("---------------PUPPET QUEDA TIEMPO----------------")
                                #CAMBIO A CAMARAS
                                if action == 0 :
                                      print("---------------CAMBIO A CAMARAS (+3)----------------")
                                      reward+=3
                                #SEGUIR EN OFICINA
                                elif action in [5,6]:
                                    print("----------------SIGUE EN OFICINA (-5)----------------")
                                    reward-=5
                             else:
                                print("---------------PUPPET SIN TIEMPO----------------")
                                if self.app.ia.action_manager.time_action_puppet<5000:
                                    if action == 4:
                                            print("---------------SALVAR PUPPET (+3)----------------")
                                            reward+=3
                                    else:
                                            print("---------------NO SALVAR PUPPET (-5)----------------")
                                            reward-=5
                        #MENOS DE 8 SEGUNDOS
                        else:
                            print("---------------MENOS DE 8 SEGUNDOS----------------")
                            if action in [5,6]:
                                reward+=2


            

        if self.app.ia.action_manager.time_action_puppet>=5000:
            print("-------------HAN PASADO SEGUNDOS PROTEGIENDO(-1)")   
            self.no_defense_puppet=pygame.time.get_ticks()
            self.app.ia.action_manager.reload_timer('defensa_puppet')
            self.app.ia.action_manager.time_action_puppet=0


        duration = self.app.ia.action_manager.time_action_foxy
        if duration is not None:
            if duration > 6000:
                        print("----------FOXY SUPERADO -----------")
                        if 'withered_foxy' in self.app.ia.anim_map[0]:
                            self.app.ia.anim_map[0].remove('withered_foxy')
                        self.app.ia.action_manager.reload_timer('defense_foxy')
                        self.app.ia.action_manager.time_action_foxy=0

        duration_defense = self.app.ia.action_manager.time_defense
        if duration_defense is not None:
             if duration_defense > 8000:
                        print("----------AMENAZADA SUPERADA -----------")
                        self.app.ia.anim_map[0].clear()
                        self.app.ia.anim_map[5].clear()
                        self.app.ia.anim_map[6].clear()
                        self.app.ia.action_manager.reload_timer('defensa_normal')
                        self.app.ia.action_manager.time_defense=0
           


        done = self.app.ia.game_over or self.app.objects.gameTimer.time==6

        # Información adicional (opcional)
        info = {}
        self.previous_action=action
        return observation, reward, done, info

    def render(self):
        # Método opcional para visualizar el entorno
        print(f"Estado actual: {self.num_camera}")

    def _get_observation(self):
        return {
            'anim_map': self.app.ia.anim_map,
            'last_action': self.previous_action,
            'open_monitor': int(self.app.ia.open_monitor),
            'num_camera': self.app.ia.num_camera,
            'hallway': int(self.app.ia.hallway),
            'right_vent': int(self.app.ia.right_vent),
            'left_vent': int(self.app.ia.left_vent),
            'put_mask': int(self.app.ia.put_mask),
            'jumpscare': int(self.app.ia.jumpscare),
            'in_office': int(self.app.ia.in_office),
            'flashlight': int(self.app.ia.flashlight),
            'music_box': int(self.app.ia.music_box)
        }