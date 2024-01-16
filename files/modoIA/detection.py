from ultralytics import YOLO
import pygame
from threading import Thread, Lock,Event
from files.modoIA.anim_paths import AnimPaths

import time
class Detection:
    def __init__(self,Lock,env_var,surface,anim_path):
        
        #MODELO DE DETECCION
        self.model = YOLO("runs/segment/train4/weights/best.pt")
        self.results = []
        self.lock=Lock
        self.env_var=env_var
        self.game_surface=surface
        self.detection_thread = Thread(target=self.run_detection, daemon=True)
        self.stop_detection = Event()
        self.start_detection_thread()
        self.anim_path=anim_path
       
    
    def check_anim(self):
            current_anims = []
            if self.results is not None:
                for r in self.results:
                    for i in range(len(r.boxes)):
                        class_id = int(r.boxes.cls[i].numpy())
                        class_name = self.model.names[class_id]
                        if self.anim_path.check_location(class_name,self.env_var.num_camera):
                            current_anims.append(class_name)
                            
            if not any(self.env_var.anim_map.values()):
                # Si no hay animaciones registradas en ninguna cámara, registrar las actuales en la cámara actual
                self.env_var.anim_map[self.env_var.num_camera] = set(current_anims)
            else:
                # Si hay animaciones registradas, compara con las actuales y actualiza el anim_map
                for anim_set in self.env_var.anim_map.values():
                    common_anims = anim_set.intersection(current_anims)
                    if common_anims:
                        # Elimina las animaciones comunes de su ubicación actual
                        anim_set.difference_update(common_anims)
                        # Agrega las animaciones comunes al anim_map[num_camera]
                        self.env_var.anim_map[self.env_var.num_camera].update(common_anims)
                    else:
                        self.env_var.anim_map[self.env_var.num_camera].update(current_anims)

    def detection(self):
        with self.lock:
            pygame.image.save(self.game_surface, "frame.png")
            # Pasar la matriz NumPy directamente al modelo
            self.results = self.model.predict("frame.png", conf=0.65)

            # Realizar el resto de las operaciones necesarias
            self.check_anim()
            
    def run_detection(self):
        while not self.stop_detection.is_set():
            self.detection()
            time.sleep(0.1)

    def start_detection_thread(self):
        self.detection_thread.start()
    def stop_detection_thread(self):
        self.stop_detection.set()
        self.detection_thread.join()
  