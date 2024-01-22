
class EnvironmentVariables:
    def __init__(self,App):
      
        #Tiempos
        self.action_timers = {"observe_office": None, "observe_monitor": None, "defense_normal": None, "defense_foxy": None,
                                "defensa_balloon_boy": None, "defensa_puppet": None}
        self.time_action_foxy=0
        self.time_action_puppet=0
        self.time_defense=0
        self.App=App
        
        #VARIABLES DE ENTORNO 
        
        #en pasillo
        self.turn_to_left = False
        self.turn_to_right = False
        self.hallway = False
        self.right_vent = False
        self.left_vent = False
        self.open_monitor = False
        self.put_mask = False
        

        #en el monitor
        self.num_camera = 9
        self.flashlight=False
        self.music_box = False

        #Dict de los animatronicos
        self.anim_dict = {i: set() for i in range(0, 13)}

        #LOG
        self.log=""
        #Game_over
        self.game_over=False
    def reset(self):
        self.turn_to_left = False
        self.turn_to_right = False
        self.hallway = False
        self.right_vent = False
        self.left_vent = False
        self.open_monitor = False
        self.put_mask = False
        self.jumpscare=False
        self.anim_dict = {i: set() for i in range(0, 13)}
        self.num_camera = 9
        self.flashlight=False
        self.music_box = True
        self.game_over=False
        self.reset_action_duration()

    #Centrar cámara para conseguir defendernos de foxy (iluminar pasillo)
    def center_camera(self):
        self.App.objects.office.position[0]=-240
      
    def reset_action_duration(self):
        self.action_timers = {"observe_office": None, "observe_monitor": None, "defense_normal": None, "defense_foxy": None,
                         "defensa_balloon_boy": None, "defensa_puppet": None, }
        self.time_action_foxy=0
        self.time_action_puppet=0
        self.time_defense=0