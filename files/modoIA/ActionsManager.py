import random
class ActionsManager:
    def __init__(self, mode_ia):
        self.mode_ia = mode_ia

    def observe_office(self):
        print("Observando en la oficina")
        # Lógica específica para observar en el pasillo
        
        self.mode_ia.put_mask=False
        self.mode_ia.open_monitor=False
        self.mode_ia.num_camera=0
        # if look_left:
        #     self.mode_ia.hallway = False
        #     self.mode_ia.left_vent=True
        #     self.mode_ia.turn_to_left = True
        # elif look_right:
        #     self.mode_ia.hallway = False
        #     self.mode_ia.right_vent=True
        #     self.mode_ia.turn_to_right = True

    def observe_monitor(self):
        print("Observando en el monitor")
        # Lógica específica para observar en el monitor

        if self.mode_ia.canInteract:
            self.mode_ia.put_mask=False
            self.mode_ia.open_monitor = True


    def defense_normal(self):
        
        print("Defensa normal")
        # Lógica específica para la defensa normal
        self.mode_ia.open_monitor=False
        self.mode_ia.put_mask=True

    def defense_foxy(self):
        
        print("Defensa de Foxy")
        # Lógica específica para la defensa contra Foxy
        self.mode_ia.turn_to_left = False
        self.mode_ia.turn_to_right = False
        self.mode_ia.right_vent=False
        self.mode_ia.left_vent=False
        self.mode_ia.open_monitor=False
        self.turn_on_light()

    def defensa_balloon_boy(self):
        
        print("Defensa de ballon_boy")
        self.mode_ia.right_vent=False
        self.mode_ia.left_vent=True
        self.mode_ia.open_monitor=False
        self.mode_ia.hallway=True
    def defensa_puppet(self):
        
        print("Defensa de puppet")
        self.mode_ia.put_mask=False
        self.mode_ia.open_monitor=True
        self.mode_ia.num_camera=11
        self.mode_ia.music_box=True

    def turn_on_light(self):
        if self.mode_ia.open_monitor is False:
            if self.mode_ia.turn_to_left:
                self.mode_ia.left_vent=True
            elif self.mode_ia.turn_to_left:
                self.mode_ia.right_vent_vent=True
            else: self.mode_ia.hallway=True
        else:
            self.mode_ia.flashlight=True
    def turn_off_light(self):
        if self.mode_ia.open_monitor is False:
            if self.mode_ia.turn_to_left:
                self.mode_ia.left_vent=False
            elif self.mode_ia.turn_to_left:
                self.mode_ia.right_vent_vent=False
            else: self.mode_ia.hallway=False
        else:
            self.mode_ia.flashlight=False
    def change_camera(self,App):

            self.mode_ia.num_camera = random.randint(1, 12)