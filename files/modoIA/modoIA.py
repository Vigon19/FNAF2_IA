from ultralytics import YOLO
import pygame
import random
from threading import Thread, Timer, Lock,Event
from files.modoIA.ActionsManager import ActionsManager
from files.modoIA.anim_utils import AnimUtils
import time
class MODO_IA:
    def __init__(self,App,log_rect):
        # Inicialización de variables de estado

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

        #en el monitor
        self.num_camera = 9
        self.flashlight=True
        self.music_box = True
        self.game_surface=App.surface
        self.model = YOLO("runs/segment/train4/weights/best.pt")
        self.last_observation_time = pygame.time.get_ticks()
        self.change_camera_time = pygame.time.get_ticks()
        self.open_monitor_time=pygame.time.get_ticks()
        
        self.current_time=pygame.time.get_ticks()
        self.label = ""
        self.names = []
        self.anims = []
        self.lock=Lock()
        self.detection_thread = Thread(target=self.run_detection, daemon=True)
        self.stop_detection = Event()
        self.start_detection_thread()
        self.log_rect=log_rect
        self.log=""
        self.game_over=False
        self.show_log_rect=True
        self.actions_manager = ActionsManager(self)
        self.canInteract=True
        self.results = []
        self.waiting_time=pygame.time.get_ticks()
        self.waiting_time_exceeded=False
    def write_log(self):
        font_large = pygame.font.Font("five-nights-at-freddys.ttf", 36)
        font_small = pygame.font.Font("five-nights-at-freddys.ttf", 36)

        main_text_surface = font_large.render(self.log, True, (0, 0, 0))
        num_camera_surface = font_small.render(f"{self.num_camera}", True, (0, 0, 0))

        main_text_x = 10
        main_text_y = (100 - main_text_surface.get_height()) // 2

        self.log_rect.fill((255, 255, 255, 200))

        if self.show_log_rect:
            self.log_rect.blit(main_text_surface, (main_text_x, main_text_y))

            num_camera_x = 600 - num_camera_surface.get_width() - 60
            num_camera_y = main_text_y - 20

            self.log_rect.blit(num_camera_surface, (num_camera_x, num_camera_y))

            self.game_surface.blit(self.log_rect, ((224), 0))

            icon_x = 600 - num_camera_surface.get_width() - 10
            icon_y = num_camera_y + num_camera_surface.get_height() + 10

            for icon_name in self.anim_map[self.num_camera]:
                icon_path = f"sprites/icons/{icon_name}.png"
                icon_surface = pygame.image.load(icon_path).convert_alpha()
                self.game_surface.blit(icon_surface, (icon_x, icon_y))
                icon_x += icon_surface.get_width() + 10
    # def observation(self):  
    #     self.current_time = pygame.time.get_ticks()
    
    #     if self.canInteract:
    #         with self.lock:
    #             if self.current_time - self.open_monitor_time <= 20000:
    #                 self.log="CAMBIO AL MONITOR"
    #                 # Está en el monitor
    #                 self.open_monitor = True
    #                 if self.current_time - self.music_box_time >=10000:
    #                     self.num_camera=11
    #                     self.music_box_time= self.current_time
                        
    #                 else:
    #                     if self.current_time - self.change_camera_time >= 4500:
    #                         # Cambiar de cámara cada 5 segundos en el monitor
    #                         self.num_camera = random.randint(1, 12)
                            
    #                         self.change_camera_time = self.current_time

    #             else:
    #                 self.log="CAMBIO AL HALL PRINCIPAL"
    #                 # Está en el hall
    #                 self.open_monitor = False
    #                 self.num_camera = 0
    #                 self.put_mask=True
    #                 self.hallway=True
    #                 self.put_mask=True
                    
    #                 if self.current_time - self.open_monitor_time >= 35000:
    #                     # Reiniciar el temporizador del hall al llegar al final de los 15 segundos
    #                     self.put_mask=False
    #                     self.open_monitor_time = self.current_time
    #     self.draw_rects()             

       
        self.write_log()
    def draw_rects(self):
        results =self.results.copy()
        if results is not None:
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
    # def observation(self):      
    #     self.current_time = pygame.time.get_ticks()
    #     if self.current_time - self.open_monitor_time <= 20000:
    #         self.log="CAMBIO AL MONITOR"
    #         # Está en el monitor
    #         self.open_monitor = True
    #         if self.current_time - self.music_box_time >=10000:
    #             self.num_camera=11
    #             self.music_box_time= self.current_time
    #             self.draw_detection_box()
    #         else:
    #             if self.current_time - self.change_camera_time >= 4000:
    #                 # Cambiar de cámara cada 5 segundos en el monitor
    #                 self.num_camera = random.randint(1, 12)
    #                 self.draw_detection_box()
    #                 self.change_camera_time = self.current_time

    #     else:
    #         self.log="CAMBIO AL HALL PRINCIPAL"
    #         # Está en el hall
    #         self.open_monitor = False
    #         self.num_camera = 0
    #         self.draw_detection_box()
    #         self.hallway=True
    #         if self.current_time - self.open_monitor_time <= 27000:
    #             # Girar a la izquierda durante los primeros 5 segundos en el hall
               
    #             self.turn_to_left = True
    #             self.turn_to_right = False
    #             self.left_vent = True
    #             self.right_vent = False

    #         elif self.current_time - self.open_monitor_time <= 31000:
    #             # Girar a la derecha durante los siguientes 5 segundos en el hall
    #             self.turn_to_left = False
    #             self.turn_to_right = True
    #             self.left_vent = False
    #             self.right_vent = True

    #         elif self.current_time - self.open_monitor_time <= 33000:
    #             self.turn_to_left = False
    #             self.turn_to_right = False
    #             self.left_vent = False
    #             self.right_vent = False
    #         elif self.current_time - self.open_monitor_time <= 35000:
    #             # Reiniciar el temporizador del hall al llegar al final de los 15 segundos
    #             self.open_monitor_time = self.current_time
                

    #     print(f"ANIM_MAP: {self.anim_map}")
    #     self.write_log()        
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
        print("DETECCIÓN")
        self.show_log_rect = False
        self.flashlight = True
        with self.lock:
            
            pygame.image.save(self.game_surface, "frame.png")
            
            self.results = self.model.predict("frame.png", conf=0.65)
            self.check_anim()
        self.show_log_rect = True
        self.flashlight = False
        time.sleep(0.7)
        
    def run_detection(self):
        while not self.stop_detection.is_set():
            self.detection()
            time.sleep(0.7)  # Intervalo de detección

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
    # def change_dict(dict):
    #     new_dict =dict.copy()
    #     for value in new_dict.values():
    #      if value == "toy_freddy": value = 1,
    #      if value == "toy_chica":value = 2,
    #      if value == "toy_bonnie":value = 3,
    #      if value == "withered_bonnie":value = 4,
    #      if value == "withered_chica":value = 5,
    #      if value == "withered_foxy":value = 6,
    #      if value == "withered_freddy":value = 7,
    #      if value == "balloon_boy":value = 8,
    #      if value == "mangle":value = 9,
    #      if value == "puppet":value = 10,
    #     return dict

