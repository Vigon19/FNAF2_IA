from ultralytics import YOLO
import pygame
from threading import Thread, Lock,Event
from files.modoIA.anim_paths import AnimPaths
import numpy as np
import matplotlib.pyplot as plt
import time
import cv2
class Detection:
    def __init__(self,Lock,env_var,surface,anim_path):
        
        #MODELO DE DETECCION
        self.model = YOLO("modelo_deteccion.pt")
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
            self.fill_dictionary(current_anims)

    def detection(self):    
            with self.lock:
                frame_array = pygame.surfarray.array3d(self.game_surface)
                frame_array =frame_array.swapaxes(0,1)
                frame_array = cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR)
                frame_array = frame_array.astype(np.uint8)
                self.results = self.model.predict(frame_array, conf=0.67)
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

    def fill_dictionary(self,current_anims):
        if not any(self.env_var.anim_dict.values()):
                # Si no hay animatrónicos registrados en ninguna cámara, registrar los actuales en la cámara actual
                self.env_var.anim_dict[self.env_var.num_camera] = set(current_anims)
        else:
                # Si hay animatrónicos registrados, compara con los actuales y actualiza el anim_dict
                for anim_set in self.env_var.anim_dict.values():
                    common_anims = anim_set.intersection(current_anims)
                    if common_anims:
                        # Elimina los aniamtrónicos de su ubicación actual en el diccionario
                        anim_set.difference_update(common_anims)
                        # Agrega las aniamtrónicos al anim_dict[num_camera]
                        self.env_var.anim_dict[self.env_var.num_camera].update(common_anims)
                    else:
                        self.env_var.anim_dict[self.env_var.num_camera].update(current_anims)
    
