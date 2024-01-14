from ultralytics import YOLO
import pygame
from threading import Thread, Timer, Lock,Event
from files.modoIA.anim_utils import AnimUtils
from files.modoIA.ActionsManager import ActionsManager
import time
class MODO_IA:
    def __init__(self,App):
        # Inicialización de variables de estado
        self.lock=Lock()

        #en pasillo
        self.turn_to_left = False
        self.turn_to_right = False
        self.hallway = False
        self.right_vent = False
        self.left_vent = False
        self.open_monitor = False
        self.put_mask = False
        self.jumpscare=False
        self.in_office=False
        self.anim_utils =AnimUtils()
        #Dict de los animatronicos
        self.anim_map = {i: set() for i in range(0, 13)}
        self.action_manager = ActionsManager(self)
        #en el monitor
        self.num_camera = 9
        self.flashlight=True
        self.music_box = True
        self.game_surface=App.surface
        self.office=App.objects.office
        self.model = YOLO("runs/segment/train4/weights/best.pt")
        self.last_observation_time = pygame.time.get_ticks()
        self.change_camera_time = pygame.time.get_ticks()
        self.open_monitor_time=pygame.time.get_ticks()
        
        self.current_time=pygame.time.get_ticks()
        self.label = ""
        self.names = []
        self.anims = []
        self.assets=App.assets
        self.dimentions=App.dimentions
        self.detection_thread = Thread(target=self.run_detection, daemon=True)
        self.stop_detection = Event()
        self.start_detection_thread()

        self.log=""
        self.game_over=False
        self.show_log_rect=True
        self.canInteract=True
        self.results = []
        self.waiting_time=pygame.time.get_ticks()
        self.waiting_time_exceeded=False
    
    def draw_rects(self):
        if self.results is not None:
            for r in self.results: 
             for i in range(len(r.boxes)):
                    
                            class_id = int(r.boxes.cls[i].numpy())
                            confidence = r.boxes.conf[i].numpy()
                            class_name = self.model.names[class_id]
                            x_min, y_min, x_max, y_max = map(int, r.boxes.xyxy[i, :4].numpy())
                            if self.anim_utils.check_location(class_name,self.num_camera):
                                pygame.draw.rect(self.game_surface, (255, 0, 0), (x_min, y_min, x_max - x_min, y_max - y_min), 5)

                                font = pygame.font.Font("five-nights-at-freddys.ttf", 36)
                                label_text = font.render(f"{class_name} {confidence:.2f}", True, (255, 255, 255))
                                self.game_surface.blit(label_text, (x_min, y_max + 5))
    def check_anim(self):
            current_anims = []
            if self.results is not None:
                for r in self.results:
                    for i in range(len(r.boxes)):
                        class_id = int(r.boxes.cls[i].numpy())
                        confidence = r.boxes.conf[i].numpy()
                        class_name = self.model.names[class_id]
                        if self.anim_utils.check_location(class_name,self.num_camera):
                            current_anims.append(class_name)
                            # current_anims=self.change_dict(current_anims)
            if not any(self.anim_map.values()):
                # Si no hay animaciones registradas en ninguna cámara, registrar las actuales en la cámara actual
                self.anim_map[self.num_camera] = set(current_anims)
            else:
                # Si hay animaciones registradas, compara con las actuales y actualiza el anim_map
                for anim_set in self.anim_map.values():
                    common_anims = anim_set.intersection(current_anims)
                    if common_anims:
                        # Elimina las animaciones comunes de su ubicación actual
                        anim_set.difference_update(common_anims)
                        # Agrega las animaciones comunes al anim_map[num_camera]
                        self.anim_map[self.num_camera].update(common_anims)
                    else:
                        self.anim_map[self.num_camera].update(current_anims)
    def detection(self):
        with self.lock:
            pygame.image.save(self.game_surface, "frame.png")
                
            self.results = self.model.predict("frame.png", conf=0.65)
            
            self.check_anim()
        
  
    def run_detection(self):
        while not self.stop_detection.is_set():
            self.detection()
            time.sleep(0.05)  # Intervalo de detección

    def start_detection_thread(self):
        self.detection_thread.start()
    def stop_detection_thread(self):
        self.stop_detection.set()
        self.detection_thread.join()
    def reset(self):
        self.turn_to_left = False
        self.turn_to_right = False
        self.hallway = False
        self.right_vent = False
        self.left_vent = False
        self.open_monitor = False
        self.put_mask = False
        self.jumpscare=False
        self.in_office=False
        self.anim_map = {i: set() for i in range(0, 13)}
        self.num_camera = 9
        self.flashlight=False
        self.music_box = True
        self.game_over=False
        self.action_manager.reset_action_duration()
    def center_camera(self):
        self.office.position[0]=-240
        #-abs(self.assets.office1.get_width() - self.dimentions.dimentions[0])
    