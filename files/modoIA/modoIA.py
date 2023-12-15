import cv2 as cv
from ultralytics import YOLO
import pygame

class MODO_IA:
    def __init__(self, App):
        self.turn_to_left = False
        self.turn_to_right = False
        self.hallway = False
        self.right_vent = False
        self.left_vent = False
        self.open_monitor = True
        self.num_camera = 9
        self.cascade_freddy = cv.CascadeClassifier('cascade/cascade.xml')
        self.put_mask = False
        self.music_box = True
        self.observation_bool = True
        self.model = YOLO("runs/segment/train4/weights/best.pt")
        self.last_observation_time = pygame.time.get_ticks()
        self.detected_rect = None
        self.label = ""
        self.names=[]
    def observation(self, surface):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_observation_time >= 2000:
            self.names=[]
            pygame.image.save(surface, "frame.png")
            self.detection("frame.png")
            self.last_observation_time = current_time

        self.draw_detection_box(surface)
    def draw_detection_box(self, surface):
        if self.detected_rect is not None:
            for r in self.detected_rect:
                for i in range(len(r.boxes)):
                    class_id = int(r.boxes.cls[i].numpy())
                    confidence = r.boxes.conf[i].numpy()
                    class_name = self.model.names[class_id]

                    x_min, y_min, x_max, y_max = map(int, r.boxes.xyxy[i, :4].numpy())
                    print(f"x_min, y_min, x_max, y_max: {x_min, y_min, x_max, y_max}")
                    print(f"Class ID: {class_id}, Class Name: {class_name}, Confidence: {confidence}")

                    # Dibujar el rectángulo
                    pygame.draw.rect(surface, (255, 0, 0), (x_min, y_min, x_max - x_min, y_max - y_min), 2)

                    # Mostrar la etiqueta debajo del rectángulo
                    font = pygame.font.Font(None, 36)
                    label_text = font.render(f"{class_name} {confidence:.2f}", True, (255, 255, 255))
                    surface.blit(label_text, (x_min, y_max + 5))  # Ajusta la posición según tus preferencias
                    # boxes = item.boxes
                    # for box in boxes:
                    #     newbox=box.xyxy
                    #     class_id = newbox[-1]
                    #     conf = newbox[-2]
                    #     class_name = self.model.names[int(class_id)]
                    #     x_min, y_min, x_max, y_max =newbox[:4]
                    #     print(f"x_min, y_min, x_max, y_max: {x_min, y_min, x_max, y_max}")

                    #     # Mostrar la etiqueta debajo del rectángulo
                    #     font = pygame.font.Font(None, 36)
                    #     label_text = font.render(class_name, True, (255, 255, 255))
                    #     surface.blit(label_text, (x_min, y_max + 5))  # Ajusta la posición según tus preferencias
                    #     pygame.draw.rect(surface, (255, 0, 0), (x_min, y_min, x_max - x_min, y_max - y_min), 2)

    def detection(self, image_path):
        results = self.model.predict(image_path, conf=0.8,save=True,show_labels=True,show_conf=True,save_txt=True,save_crop=False,line_width=2)
        self.detected_rect = results

    # def observation(self,surface):
    #         current_time = pygame.time.get_ticks()
    #         if current_time - self.last_observation_time >= 2000:  # 5000 milliseconds = 5 seconds
    #             pygame.image.save(surface, "frame.png")
    #             self.detection("frame.png",surface)
    #         if current_time - self.last_observation_time >= 3000:
                
    #  Realiza la predicción con YOLO
       

        # Dibuja el cuadrado alrededor del objeto detectado
        

        # ... (código existente)

    

# tamaño_de_estado = (64, 64, 3)# Ajusta según las dimensiones reales después del preprocesamiento
# número_de_acciones = 9
# factor_de_descuento = 0.9
# número_de_episodios = 1000
# gym.register(
#         id='GameEnv-v0',
#         entry_point='files.modoIA.gameEnv:GameEnv',
#         max_episode_steps=300,)
# # Función para preprocesar imágenes
# def preprocess_image(image):
#     # Redimensionar la imagen a un tamaño específico
#     resized_image = cv.resize(image, (tamaño_de_estado[0], tamaño_de_estado[1]))

#     # Normalizar los valores de píxeles a un rango entre 0 y 1
#     normalized_image = resized_image / 255.0

#     return normalized_image


# # Crear el modelo de aprendizaje por refuerzo
# model = Sequential()
# model.add(Flatten(input_shape=tamaño_de_estado))
# model.add(Dense(64, activation='relu'))
# model.add(Dense(32, activation='relu'))
# model.add(Dense(número_de_acciones, activation='linear'))
# model.compile(optimizer='adam', loss='mse')
# # Crear instancia de la clase MODO_IA
# modo_ia = MODO_IA()

# # Configurar el entorno Gym (puedes necesitar instalar gym y box2d)
# env = gym.make('GameEnv-v0')

# # Bucle principal de entrenamiento
# for episodio in range(número_de_episodios):
#     estado = env.reset()
#     # estado = preprocess_image(estado)

#     while True:
#         # Tomar acción basada en el estado actual (salida del modelo)
#         accion = model.predict(np.reshape(estado, (1,64, 64, 3)))
#         # Mapear las salidas del modelo a las acciones de la clase MODO_IA
#         modo_ia.turn_to_left = bool(accion[0][0])
#         modo_ia.turn_to_right = bool(accion[0][1])
#         modo_ia.hallway = bool(accion[0][2])
#         modo_ia.right_vent = bool(accion[0][3])
#         modo_ia.left_vent = bool(accion[0][4])
#         modo_ia.open_monitor = bool(accion[0][5])
#         modo_ia.num_camera = int(accion[0][6])
#         modo_ia.put_mask = bool(accion[0][7])
#         modo_ia.music_box = bool(accion[0][8])

#         # Aplicar la acción al entorno y obtener el próximo estado y recompensa
#         próximo_estado, recompensa, hecho, _,_ = env.step(modo_ia)
#         # próximo_estado = preprocess_image(próximo_estado)

#         # Actualizar el modelo con la experiencia de aprendizaje por refuerzo
#         target = recompensa + factor_de_descuento * np.max(model.predict(np.reshape(próximo_estado, (1, 64,64,3))))
#         model.fit(np.reshape(estado,  (1, 64,64,3)),
#                    np.reshape(target, (1)), epochs=1, verbose=0)

#         # Actualizar el estado actual
#         estado = próximo_estado

#         # Salir del bucle si el episodio ha terminado
#         if hecho:
#             break

# # Guardar el modelo entrenado
# model.save('modelo_entrenado.h5')
