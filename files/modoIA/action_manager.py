import random
import pygame

class ActionsManager:
    def __init__(self, env_action,Lock):

            self.env_action = env_action
            self.env_action.action_timers = {"observe_office": None, "observe_monitor": None, "defense_normal": None, "defense_foxy": None,
                                "defensa_balloon_boy": None, "defensa_puppet": None
                                }
            self.env_action.time_action_foxy=0
            self.env_action.time_action_puppet=0
            self.env_action.time_defense=0
            self.lock=Lock
    
    def get_action_duration(self, action_name):
        if self.env_action.action_timers[action_name] is not None:
            return pygame.time.get_ticks() - self.env_action.action_timers[action_name]
        else:
            return 0
    def reload_timer(self,current_action):
        self.env_action.action_timers[current_action] = None
                        
    def pause_timers(self, current_action):
        for action_name in self.env_action.action_timers:
            if action_name != current_action:
                if self.env_action.action_timers[action_name] is not None :
                    if action_name == 'defense_foxy' :
                            self.env_action.time_action_foxy+= pygame.time.get_ticks() - self.env_action.action_timers['defense_foxy']
                    if action_name == 'defensa_puppet':
                            self.env_action.time_action_puppet+= pygame.time.get_ticks() - self.env_action.action_timers['defensa_puppet']
                    if action_name == 'defense_normal':
                            self.env_action.time_defense+= pygame.time.get_ticks() - self.env_action.action_timers['defense_normal']
                    
                    self.env_action.action_timers[action_name] = None

    def start_action_timer(self, action_name):
        if self.env_action.action_timers[action_name] is None:
            self.env_action.action_timers[action_name] = pygame.time.get_ticks()

    def turn_left(self):
     with self.lock:

        self.env_action.log="GIRAR IZQUIERDA"
        self.start_action_timer('observe_office')
        self.pause_timers('observe_office')
        # Lógica específica para observar en el pasillo
        self.env_action.put_mask = False
        self.env_action.open_monitor = False
        self.env_action.num_camera = 0
        self.env_action.turn_to_left=True
        self.env_action.turn_to_right=False 
        self.turn_on_light()

    def turn_right(self):
     with self.lock:
        self.env_action.log="GIRAR DERECHA"
        self.start_action_timer('observe_office')
        self.pause_timers('observe_office')
        # Lógica específica para observar en el pasillo
        self.env_action.put_mask = False
        self.env_action.open_monitor = False
        self.env_action.num_camera = 0
        self.env_action.turn_to_left=False
        self.env_action.turn_to_right=True 
        self.turn_on_light()
            
    def defense_normal(self):
     with self.lock:

        self.start_action_timer("defense_normal")
        self.pause_timers('defense_normal')
        self.env_action.log=f"DEFENSA NORMAL: {self.env_action.anim_map[0]}"
        # Lógica específica para la defensa normal
        self.env_action.num_camera = 0
        self.env_action.open_monitor = False
        self.env_action.put_mask = True
        self.turn_off_light()
    def defense_foxy(self):
     with self.lock:

        self.start_action_timer("defense_foxy")
        self.pause_timers('defense_foxy')
        self.env_action.log="DEFENSA DE FOXY"
        # Lógica específica para la defensa conra Foxy
        self.env_action.num_camera = 0
        self.env_action.center_camera()
        self.env_action.turn_to_left = False
        self.env_action.turn_to_right = False
        self.env_action.put_mask=False
        self.env_action.open_monitor = False
        self.turn_on_light()
      


    def defensa_puppet(self):
     with self.lock:

        self.start_action_timer("defensa_puppet")
        self.pause_timers('defensa_puppet')
        self.env_action.log="DEFENSA DE PUPPET"
        self.env_action.music_box = True
        self.env_action.put_mask = False
        self.env_action.open_monitor = True
        self.env_action.num_camera = 11
    def change_camera(self):
     with self.lock:

        self.start_action_timer("observe_monitor")
        self.pause_timers('observe_monitor')
        if(self.env_action.action_timers['observe_office'] is not None):
            self.env_action.action_timers['observe_office'] = None
        self.env_action.log="CAMBIAR CAMARA"
        self.env_action.put_mask = False
        self.env_action.open_monitor = True
        probabilidad = random.randint(1, 100)

        # Asignar la cámara en base a la probabilidad
        if probabilidad <= 30:
            self.env_action.num_camera = random.choice([5, 6])  # Elegir entre 5 y 6
        else:
            self.env_action.num_camera = random.randint(1, 12)
        self.turn_on_light()
    def turn_on_light(self):
        
            self.env_action.flashlight = True
            self.env_action.left_vent = True
            self.env_action.right_vent = True
            self.env_action.hallway = True
        
        
    def turn_off_light(self):
            self.env_action.left_vent = False
            self.env_action.right_vent_vent = False
            self.env_action.hallway = False
            self.env_action.flashlight = False

