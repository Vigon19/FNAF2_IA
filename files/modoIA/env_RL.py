import gym
from gym import spaces
import pygame

class envRL(gym.Env):
    def __init__(self, env_var,action_manager,time):
        super(envRL, self).__init__()
        self.env_var=env_var
        self.action_manager=action_manager
        self.anim_dict =env_var.anim_dict
        self.num_camera = env_var.num_camera
        self.time=time
        self.previous_action=1
        self.puppet_sin_tiempo=False
        self.action_space = spaces.Discrete(6)  # 6 acciones posibles
        self.no_defense_puppet=pygame.time.get_ticks()

        # Define el espacio de observación
        self.observation_space = spaces.Dict({
            'last_action': spaces.Discrete(self.action_space.n),
            'open_monitor': spaces.Discrete(2),  
            'num_camera': spaces.Discrete(13),   
            'hallway': spaces.Discrete(2),       
            'right_vent': spaces.Discrete(2),
            'left_vent': spaces.Discrete(2),     
            'put_mask': spaces.Discrete(2),      
            'jumpscare': spaces.Discrete(2),     
            'flashlight': spaces.Discrete(2),    
            'music_box': spaces.Discrete(2),
            'puppet_sin_tiempo': spaces.Discrete(2),
            'en_peligro': spaces.Discrete(2),
            'foxy_en_pasillo': spaces.Discrete(2),
           
        })
        self.observation_size = 41

    def reset(self):
        # Reiniciar el entorno a un estado inicial
        self.env_var.reset()
        self.no_defense_puppet=pygame.time.get_ticks()
        self.action_manager.time_action_foxy=0
        self.action_manager.time_action_puppet=0
        self.action_manager.time_defense=0
        return self._get_observation()

    def step(self, action):


        if action == 0:
            self.action_manager.change_camera()
        elif action == 1:
            self.action_manager.defense_normal()
        elif action == 2:
            self.action_manager.defense_foxy()
        elif action == 3:
            self.action_manager.defense_puppet()
        elif action == 4:
            self.action_manager.turn_left()
        elif action == 5:
            self.action_manager.turn_right()

        observation = self._get_observation()
        

        # Calcular la recompensa
        reward = 0  # Inicializa la recompensa en 0

        print(f"anim_dict: {self.env_var.anim_dict}")
        #DEFENSA  
        if len(self.env_var.anim_dict[0])>0 or len(self.env_var.anim_dict[5])>0 or len(self.env_var.anim_dict[6])>0 :
                     #ANIMATRONICO DETECTADO EN LA OFICINA (DENTRO, EN PASILLO O VENTILACIÓN)
                    print("---------------------ANIMATRONICO DETECTADO----------------")
                    print(f"---------------- {self.env_var.anim_dict[0]}---------")
                    #SI ES FOXY SE DEFIENDE CON ACCION 'DEFENSE_FOXY'
                    if 'withered_foxy' in self.env_var.anim_dict[0] and len(self.env_var.anim_dict[0])== 1 and len(self.env_var.anim_dict[5])==0 and len(self.env_var.anim_dict[5])==0:
                        print("---------------------FOXY----------------")
                        if self.action_manager.time_action_foxy<4500 or (self.action_manager.time_action_foxy== 0 and self.action_manager.get_action_duration('defense_foxy')<4500):
                            if action == 2:
                                print("---------------------DEFENSA FOXY (+6)----------------")
                                reward += 6
                            else:
                                print("---------------------NO DEFENSA FOXY (-5)----------------")
                                reward -=5
                    else:
                         ("---------------HAY MAS ANIMATRONICOS A PARTE DE FOXY----------------")
                         if action == 1:
                                print("---------------------DEFENSA CON MÁSCARA (+6)----------------")
                                reward += 6
                         else:
                                print("---------------------NO DEFENSA  CON MÁSCARA (-6)----------------")
                                reward -=5

        #OBSERVACIÓN
        else:
            #NO DEFENDER PUPPET
            if pygame.time.get_ticks()- self.no_defense_puppet<=10000:       
                    print("-------------------PUPPET CON TIEMPO----------------------")
                    self.puppet_sin_tiempo=False
                    #MIRANDO CAMARAS
                    if self.previous_action == 0:
                        print("-----------------MIRANDO CAMARAS---------------")
                        #MAS DE 12 SEGUNDOS
                        if (self.action_manager.get_action_duration("observe_monitor") >= 12000):
                                print("-----------------MÁS DE 12 SEGUNDOS---------------")
                                if action in [4,5]:
                                        print("-----------------CAMBIO A OFICINA (+3)---------------")
                                        reward+=3
                                    #SEGUIR EN CAMARAS
                                elif action ==0:
                                        print("-----------------SEGUIR EN CAMARAS(-5)---------------")
                                        reward-=5
                        
                        #MENOS DE 12 SEGUNDOS
                        else:
                            print("---------------- MENOS DE 12 SEGUNDOS ---------------")
                             #SEGUIR EN CAMARAS
                            if action == 0:
                                print("----------------SEGUIR EN CAMARAS(+2) ---------------")
                                reward+=3
                            #CAMBIAR
                            else:
                                print("-----------------CAMBIAR DE CAMARAS(-5)---------------")
                                reward-=5
                           
                    #EN OFICINA
                    elif self.previous_action in [4,5]:
                        #MAS DE 8 SEGUNDOS
                        if self.action_manager.get_action_duration("observe_office") >= 8000:
                            print("---------------MÁS DE 8 SEGUNDOS----------------")
                            #CAMBIO A CAMARAS
                            if action == 0 :
                                print("---------------CAMBIO A CAMARAS (+3)----------------")
                                reward+=3
                            #SEGUIR EN OFICINA
                            elif action in [4,5]:
                                    print("----------------SIGUE EN OFICINA (-5)----------------")
                                    reward-=5
                            
                        #MENOS DE 8 SEGUNDOS
                        else:
                          
                            if action in [4,5]:
                                print("--------------SEGUIR EN OFICINA (+2)")
                                reward+=3
                            #CAMBIO
                            elif action not in [4,5]:
                                print("----------------CAMBIAR DE OFICINA (-5)----------------")
                                reward-=5
                    elif self.previous_action not in [0,4,5]:
                         ("-------------------DEFENDIENDO CUANDO NO HACE FALTA-----------------------")
                         reward -=10
            #DEFENDER PUPPET                
            else:
                    self.puppet_sin_tiempo=True
                    print("---------------PUPPET SIN TIEMPO----------------")
                    if self.action_manager.time_action_puppet<3000 or (self.action_manager.time_action_puppet== 0 and self.action_manager.get_action_duration('defensa_puppet')<3000):
                            if action == 3:
                                    print("---------------SALVAR PUPPET (+3)----------------")
                                    reward+=3
                            else:
                                    print("---------------NO SALVAR PUPPET (-5)----------------")
                                    reward-=5                


            
        #COMPROBAR LOS TIEMPOS DE DEFENSA
                                    
        if self.action_manager.time_action_puppet>=3000 or (self.action_manager.time_action_puppet== 0 and self.action_manager.get_action_duration('defensa_puppet')>=3000):
            print("-------------PUPPET PROTEGIDO-------------")   
            self.puppet_sin_tiempo=False
            self.no_defense_puppet=pygame.time.get_ticks()
            self.action_manager.reload_timer('defensa_puppet')
            self.action_manager.time_action_puppet=0

        # SI LLEVA 6 SEGUNDOS DEFENDIENDO A FOXY, CONSIDERAMOS QUE YA LO HEMOS DEFENDIDO Y LO QUITAMOS DEL DICT DE ANIMATRONICOS
        duration = self.action_manager.time_action_foxy
        if duration is not None:
            if duration > 6000 or (duration==0 and self.action_manager.get_action_duration('defense_foxy')>6000):
                        print("----------FOXY SUPERADO -----------")
                        if 'withered_foxy' in self.env_var.anim_dict[0]:
                            self.env_var.anim_dict[0].remove('withered_foxy')
                        self.action_manager.reload_timer('defense_foxy')
                        self.action_manager.time_action_foxy=0

        # SI LLEVA 8 SEGUNDOS CON LA MÁSCARA, CONSIDERAMOS QUE LOS ENEMIGOS DE LA OFICINA Y VENTILACIONES Y POR ELLO LOS QUITAMOS DEL DICT

        duration_defense = self.action_manager.time_defense
        if duration_defense is not None:
             if duration_defense > 7000 or (duration_defense== 0 and self.action_manager.get_action_duration('defense_normal')>=7000):
                        print("----------AMENAZADA SUPERADA -----------")
                        self.env_var.anim_dict[0].clear()
                        self.env_var.anim_dict[5].clear()
                        self.env_var.anim_dict[6].clear()
                        self.action_manager.reload_timer('defense_normal')
                        self.action_manager.time_defense=0
           


        done = self.env_var.game_over or self.time==6

        info = {}
        self.previous_action=action
        return observation, reward, done, info

    def render(self):
        # Método opcional para visualizar el entorno
        print(f"Estado actual: {self.num_camera}")

    def _get_observation(self):
        return {
            'last_action': self.previous_action,
            'open_monitor': int(self.env_var.open_monitor),
            'num_camera': self.env_var.num_camera,
            'hallway': int(self.env_var.hallway),
            'right_vent': int(self.env_var.right_vent),
            'left_vent': int(self.env_var.left_vent),
            'put_mask': int(self.env_var.put_mask),
            'jumpscare': int(self.env_var.jumpscare),
            'flashlight': int(self.env_var.flashlight),
            'puppet_sin_tiempo':int(pygame.time.get_ticks()- self.no_defense_puppet<=10000),
            'en_peligro': int((len(self.env_var.anim_dict[0])>0 or len(self.env_var.anim_dict[5])>0 or len(self.env_var.anim_dict[6])>0)),
            'foxy_en_pasillo': int('withered_foxy' in self.env_var.anim_dict[0])
        }