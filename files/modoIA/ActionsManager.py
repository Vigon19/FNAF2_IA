import random

class ActionsManager:
    def __init__(self, mode_ia):
        self.mode_ia = mode_ia

    def observe_hallway(self, look_left=False, look_right=False):
        print("Observando en el pasillo")
        # Lógica específica para observar en el pasillo
        self.mode_ia.put_mask=False
        self.mode_ia.open_monitor=False
        self.mode_ia.hallway = True
        if look_left:
            self.mode_ia.hallway = False
            self.mode_ia.left_vent=True
            self.mode_ia.turn_to_left = True
        elif look_right:
            self.mode_ia.hallway = False
            self.mode_ia.right_vent=True
            self.mode_ia.turn_to_right = True

    def observe_monitor(self, change_camera=False):
        print("Observando en el monitor")
        # Lógica específica para observar en el monitor
        self.mode_ia.put_mask=False
        self.mode_ia.open_monitor = True
        if change_camera:
            self.mode_ia.num_camera = random.randint(1, 12)


    def defense_normal(self):
        
        print("Defensa normal")
        # Lógica específica para la defensa normal
        self.mode_ia.open_monitor=False
        self.mode_ia.put_mask=True

    def defense_foxy(self):
        
        print("Defensa de Foxy")
        # Lógica específica para la defensa contra Foxy
        self.mode_ia.open_monitor=False
        self.mode_ia.hallway=True


