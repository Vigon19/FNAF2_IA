import random
import pygame

class ActionsManager:
    def __init__(self, mode_ia):

            self.mode_ia = mode_ia
            self.action_timers = {"observe_office": None, "observe_monitor": None, "defense_normal": None, "defense_foxy": None,
                                "defensa_balloon_boy": None, "defensa_puppet": None
                                }
            self.time_action_foxy=0
            self.time_action_puppet=0
            self.time_defense=0
    def reset_action_duration(self):
        self.action_timers = {"observe_office": None, "observe_monitor": None, "defense_normal": None, "defense_foxy": None,
                         "defensa_balloon_boy": None, "defensa_puppet": None, }
        self.time_action_foxy=0
        self.time_action_puppet=0
        self.time_defense=0
    def get_action_duration(self, action_name):
        if self.action_timers[action_name] is not None:
            return pygame.time.get_ticks() - self.action_timers[action_name]
        else:
            return 0
    def reload_timer(self,current_action):
        self.action_timers[current_action] = None
                        
    def pause_timers(self, current_action):
        for action_name in self.action_timers:
            if action_name != current_action:
                if self.action_timers[action_name] is not None :
                    if action_name == 'defense_foxy' :
                            self.time_action_foxy+= pygame.time.get_ticks() - self.action_timers['defense_foxy']
                    if action_name == 'defensa_puppet':
                            self.time_action_puppet+= pygame.time.get_ticks() - self.action_timers['defensa_puppet']
                    if action_name == 'defense_normal':
                            self.time_action_puppet+= pygame.time.get_ticks() - self.action_timers['defense_normal']
                    
                    self.action_timers[action_name] = None

    def start_action_timer(self, action_name):
        if self.action_timers[action_name] is None:
            self.action_timers[action_name] = pygame.time.get_ticks()
    def observe_office(self):
     with self.mode_ia.lock:
        self.start_action_timer("observe_office")
        self.pause_timers("observe_office")

        print("Observando en la oficina")
        # Lógica específica para observar en el pasillo
        self.mode_ia.put_mask = False
        self.mode_ia.open_monitor = False
        self.mode_ia.num_camera = 0
        self.mode_ia.turn_to_left=False
        self.mode_ia.turn_to_right=False 

    
    def turn_left(self):
     with self.mode_ia.lock:

        print("girar izquierda")
        self.start_action_timer('observe_office')
        self.pause_timers('observe_office')
        # Lógica específica para observar en el pasillo
        self.mode_ia.put_mask = False
        self.mode_ia.open_monitor = False
        self.mode_ia.num_camera = 0
        self.mode_ia.turn_to_left=True
        self.mode_ia.turn_to_right=False 
        if self.get_action_duration('observe_office')%3==0:
            self.turn_on_light()
        else:
            self.turn_off_light()
    def turn_right(self):
     with self.mode_ia.lock:

        print("girar derecha")
        self.start_action_timer('observe_office')
        self.pause_timers('observe_office')
        # Lógica específica para observar en el pasillo
        self.mode_ia.put_mask = False
        self.mode_ia.open_monitor = False
        self.mode_ia.num_camera = 0
        self.mode_ia.turn_to_left=False
        self.mode_ia.turn_to_right=True 
        if self.get_action_duration('observe_office')%3==0:
            self.turn_on_light()
        else:
            self.turn_off_light()
  
    def defense_normal(self):
     with self.mode_ia.lock:

        self.start_action_timer("defense_normal")
        self.pause_timers('defense_normal')
        print("Defensa normal")
        # Lógica específica para la defensa normal
        self.mode_ia.num_camera = 0
        self.mode_ia.open_monitor = False
        self.mode_ia.put_mask = True
        if self.get_action_duration('defense_normal')<1000:
            self.turn_on_light()
        else:
            self.turn_off_light()
    def defense_foxy(self):
     with self.mode_ia.lock:

        self.start_action_timer("defense_foxy")
        self.pause_timers('defense_foxy')
        print("Defensa de Foxy")
        # Lógica específica para la defensa contra Foxy
        self.mode_ia.num_camera = 0
        self.mode_ia.center_camera()
        self.mode_ia.turn_to_left = False
        self.mode_ia.turn_to_right = False
        self.mode_ia.right_vent = False
        self.mode_ia.left_vent = False
        self.mode_ia.put_mask=False
        self.mode_ia.open_monitor = False
        self.turn_on_light()
      

    def defensa_balloon_boy(self):
     with self.mode_ia.lock:

        self.start_action_timer("defensa_balloon_boy")
        self.pause_timers('defensa_balloon_boy')
        print("Defensa de ballon_boy")
        self.mode_ia.open_monitor = False
        self.mode_ia.num_camera = 0
        self.mode_ia.put_mask = False
        self.mode_ia.turn_to_left = True
        self.mode_ia.turn_to_right = False
        self.mode_ia.right_vent = False
        self.mode_ia.left_vent = True

        if self.get_action_duration('defensa_balloon_boy')<2000:
            self.turn_on_light()
        else:
            self.turn_off_light()
    def defensa_puppet(self):
     with self.mode_ia.lock:

        self.start_action_timer("defensa_puppet")
        self.pause_timers('defensa_puppet')
        print("Defensa de puppet")
        self.mode_ia.music_box = True
        self.mode_ia.put_mask = False
        self.mode_ia.open_monitor = True
        self.mode_ia.num_camera = 11
        
        if self.get_action_duration('defensa_puppet')<1000:
            self.turn_on_light()
        else:
            self.turn_off_light()
    def change_camera(self):
     with self.mode_ia.lock:

        self.start_action_timer("observe_monitor")
        self.pause_timers('observe_monitor')
        if(self.action_timers['observe_office'] is not None):
            self.action_timers['observe_office'] = None
        print("CAMBIAR CAMARA")
        self.mode_ia.put_mask = False
        self.mode_ia.open_monitor = True
        probabilidad = random.randint(1, 100)

        # Asignar la cámara en base a la probabilidad
        if probabilidad <= 30:
            self.mode_ia.num_camera = random.choice([5, 6])  # Elegir entre 5 y 6
        else:
            self.mode_ia.num_camera = random.randint(1, 12)
        if self.mode_ia.num_camera in [5,6,7,11]:
            self.turn_on_light()
        else:
            self.turn_off_light()
    def turn_on_light(self):
        print("ENCENDER LUZ")
        self.mode_ia.left_vent = True
        self.mode_ia.right_vent_vent = True
        self.mode_ia.hallway = True
        self.mode_ia.flashlight = True
        
    def turn_off_light(self):
            print("APAGAR LUZ")
            self.mode_ia.left_vent = False
            self.mode_ia.right_vent_vent = False
            self.mode_ia.hallway = False
            self.mode_ia.flashlight = False

