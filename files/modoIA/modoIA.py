from ultralytics import YOLO
import pygame
import random
from threading import Thread, Timer
class MODO_IA:
    def __init__(self,App,log_rect):
        # Inicialización de variables de estado
        self.turn_to_left = False
        self.turn_to_right = False
        self.hallway = False
        self.right_vent = False
        self.left_vent = False
        self.open_monitor = False
        self.anim_map = {i: set() for i in range(0, 13)}
        self.num_camera = 9
        self.game_surface=App.surface
        self.drawn_icons = set()
        self.put_mask = False
        self.flashlight=False
        self.music_box = True
        self.model = YOLO("runs/segment/train4/weights/best.pt")
        self.last_observation_time = pygame.time.get_ticks()
        self.change_camera_time = pygame.time.get_ticks()
        self.open_monitor_time=pygame.time.get_ticks()
        self.music_box_time=pygame.time.get_ticks()
        self.current_time=pygame.time.get_ticks()
        self.detected_rect = None
        self.label = ""
        self.names = []
        self.anims = []
        self.detection_thread = Thread(target=self.run_detection, daemon=True)
        self.detection_thread.start()
        self.log_rect=log_rect
        self.log=""
        self.show_log_rect=True

    def write_log(self):
        font_large = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 36)

        main_text_surface = font_large.render(self.log, True, (0, 0, 0))
        num_camera_surface = font_small.render(f"{self.num_camera}", True, (0, 0, 0))

        main_text_x = 10
        main_text_y = (100 - main_text_surface.get_height()) // 2

        self.log_rect.fill((255, 255, 255, 200))

        if self.show_log_rect:  # Actualizar solo si show_log_rect es True
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
    def observation(self): 
        print("OBSERVATIÓN")     
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.open_monitor_time <= 20000:
            self.log="CAMBIO AL MONITOR"
            # Está en el monitor
            self.open_monitor = True
            if self.current_time - self.music_box_time >=10000:
                self.num_camera=11
                self.music_box_time= self.current_time
                
            else:
                if self.current_time - self.change_camera_time >= 4500:
                    # Cambiar de cámara cada 5 segundos en el monitor
                    self.num_camera = random.randint(1, 12)
                    
                    self.change_camera_time = self.current_time

        else:
            self.log="CAMBIO AL HALL PRINCIPAL"
            # Está en el hall
            self.open_monitor = False
            self.num_camera = 0

            self.hallway=True
            if self.current_time - self.open_monitor_time <= 27000:
                # Girar a la izquierda durante los primeros 5 segundos en el hall
               
                self.turn_to_left = True
                self.turn_to_right = False
                self.left_vent = True
                self.right_vent = False

            elif self.current_time - self.open_monitor_time <= 31000:
                # Girar a la derecha durante los siguientes 5 segundos en el hall
                self.turn_to_left = False
                self.turn_to_right = True
                self.left_vent = False
                self.right_vent = True

            elif self.current_time - self.open_monitor_time <= 33000:
                self.turn_to_left = False
                self.turn_to_right = False
                self.left_vent = False
                self.right_vent = False
            elif self.current_time - self.open_monitor_time <= 35000:
                # Reiniciar el temporizador del hall al llegar al final de los 15 segundos
                self.open_monitor_time = self.current_time
                

       
        self.write_log()
        

    def check_anim(self,detect):
            current_anims = []
            for r in detect:
                for i in range(len(r.boxes)):
                    class_id = int(r.boxes.cls[i].numpy())
                    confidence = r.boxes.conf[i].numpy()
                    class_name = self.model.names[class_id]
                    current_anims.append(class_name)
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
            self.names = []
            self.flashlight = True
            pygame.image.save(self.game_surface, "frame.png")
            results = self.model.predict("frame.png", conf=0.65)
            self.check_anim(results)
            self.show_log_rect = True
            self.flashlight = False
    def run_detection(self):
        while True:
            # Realizar la detección
            self.detection()
            # intervalo de detección (1 segundo)
            timer = Timer(1, self.run_detection)
            timer.start()
            timer.join()
 