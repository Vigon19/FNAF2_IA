from ultralytics import YOLO
import pygame
from multiprocessing import Process, Queue
import os
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
        self.child_queue = Queue()
        self.anim_map_queue = Queue()
        self.logs_queue = Queue()
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
    def init_map_process(self):
        # Inicializar Pygame y configurar la pantalla del mapa
        pygame.init()
        self.screen = pygame.display.set_mode((416,600))  #(416, 450)
        pygame.display.set_caption("IA CONTROL")

        map_image = pygame.image.load("sprites/cameras/utils/Map.png")
        self.screen.blit(map_image, (0, 0))
        pygame.display.flip()

        font = pygame.font.Font(None, 24)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            # Manejar eventos solo cuando sea necesario
            if not self.anim_map_queue.empty():
                current_anim = self.anim_map_queue.get()
                print(f"CURRENT ANIM ENVIADO {current_anim}")
                self.check_map(current_anim, self.screen)
            if not self.logs_queue.empty():
                log = self.logs_queue.get()
                self.draw_log(rect_position=(0, 312), log=log, font=font)

            pygame.display.update()
        pygame.quit()
    def draw_log(self, rect_position, log, font,screen):
        # Dibujar un rectángulo en la posición especificada
        pygame.draw.rect(screen, (255, 255, 255), (rect_position[0], rect_position[1], 600, 100))

        # Dibujar el texto del log dentro del rectángulo
        text_surface = font.render(log, True, (0, 0, 0))
        screen.blit(text_surface, (rect_position[0] + 10, rect_position[1] + 10))
    def observation(self):      
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.open_monitor_time <= 20000:
            self.log="CAMBIO AL MONITOR"
            # Está en el monitor
            self.open_monitor = True
            if self.current_time - self.music_box_time >=10000:
                self.num_camera=11
                self.music_box_time= self.current_time
                
            else:
                if self.current_time - self.change_camera_time >= 4000:
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
                

        print(f"ANIM_MAP: {self.anim_map}")
        self.write_log()
        

    def draw_detection_box(self):
        if self.detected_rect is not None:
            current_anims = []
            for r in self.detected_rect:
                for i in range(len(r.boxes)):
                    class_id = int(r.boxes.cls[i].numpy())
                    confidence = r.boxes.conf[i].numpy()
                    class_name = self.model.names[class_id]
                    current_anims.append(class_name)
                    # x_min, y_min, x_max, y_max = map(int, r.boxes.xyxy[i, :4].numpy())

                    # pygame.draw.rect(self.game_surface, (255, 0, 0), (x_min, y_min, x_max - x_min, y_max - y_min), 2)

                    # font = pygame.font.Font(None, 36)
                    # label_text = font.render(f"{class_name} {confidence:.2f}", True, (255, 255, 255))
                    # self.game_surface.blit(label_text, (x_min, y_max + 5))
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
        self.show_log_rect = False  # Ocultar log_rect antes de tomar el frame.png
        self.names = []
        self.flashlight = True
        pygame.image.save(self.game_surface, "frame.png")
        self.show_log_rect = True  # Mostrar log_rect después de tomar el frame.png
        results = self.model.predict("frame.png", conf=0.65)
        self.flashlight = False
        self.detected_rect = results
    def run_detection(self):
        while True:
            # Realizar la detección
            self.detection()
            # Ajustar el intervalo según sea necesario (1.5 segundos en este ejemplo)
            timer = Timer(0.8, self.run_detection)
            timer.start()
            timer.join()
    def check_map(self, current_anim, screen):
        # Limpiar los iconos dibujados anteriormente
        self.drawn_icons = set()

        for camera, anims in current_anim.items():
            anim_space = 0
            x_min_zone, y_min_zone, _, _ = self.mapZones(camera)

            # Volver a cargar el mapa para restaurar la imagen original
            map_image = pygame.image.load("sprites/cameras/utils/Map.png")
            screen.blit(map_image, (0, 0))

            for class_name in anims:
                icon_path = f"sprites/icons/{class_name}.png"
                if os.path.exists(icon_path):
                    icon_img = pygame.image.load(icon_path)
                    screen.blit(icon_img, (x_min_zone + anim_space, y_min_zone))
                    anim_space += 30
                    # Agregar el icono al conjunto de iconos dibujados
                    self.drawn_icons.add(icon_path)
    def mapZones(self,camera):
        if camera == 0: 
            x_min, y_min = 75, 4
            width, height = 80, 40
            return x_min, y_min, width, height
        if camera == 1: 
            x_min, y_min = 4, 90
            width, height = 80, 40
            return x_min, y_min, width, height
        if camera == 2: 
            x_min, y_min = 165, 90
            width, height = 80, 40
            return x_min, y_min, width, height
        if camera == 3: 
            x_min, y_min = 2, 157
            width, height = 80, 40
            return x_min, y_min, width, height
        if camera == 4: 
            x_min, y_min = 167, 156
            width, height = 80, 40
            return x_min, y_min, width, height
        if camera == 5: 
            x_min, y_min = 25, 16
            width, height = 80, 40
            return x_min, y_min, width, height
        if camera == 6: 
            x_min, y_min = 179, 16
            width, height = 80, 40
            return x_min, y_min, width, height
        if camera == 7: 
            x_min, y_min = 150, 230
            width, height = 80, 40
            return x_min, y_min, width, height
        if camera == 8: 
            x_min, y_min = 24, 244
            width, height = 80, 40
            return x_min, y_min, width, height    
        if camera == 9: 
            x_min, y_min = 290, 15
            width, height = 80, 40
            return x_min, y_min, width, height    
        if camera == 10: 
            x_min, y_min = 264, 145
            width, height = 80, 40
            return x_min, y_min, width, height    
        if camera == 11: 
            x_min, y_min = 356, 200
            width, height = 80, 40
            return x_min, y_min, width, height    
        if camera == 12: 
            x_min, y_min = 313, 57
            width, height = 80, 40
            return x_min, y_min, width, height