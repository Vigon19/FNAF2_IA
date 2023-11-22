import cv2
import gym
import numpy as np
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Flatten
from files.modoIA.gameEnv import GameEnv

class MODO_IA:
    def __init__(self):
        self.turn_to_left = False
        self.turn_to_right = False
        self.hallway = False
        self.right_vent = False
        self.left_vent = False
        self.open_monitor = True
        self.num_camera = 11
        self.put_mask = False
        self.music_box = True
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
#     resized_image = cv2.resize(image, (tamaño_de_estado[0], tamaño_de_estado[1]))

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
