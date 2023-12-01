from PIL import Image, ImageEnhance, ImageFilter
import os

def generar_datos_sinteticos(imagen_origen, cantidad_generada, directorio_destino,num):
    # Obtener la ruta completa de la imagen de origen
    ruta_completa = os.path.join('cascade_images/freddy/positive', imagen_origen)

    # Cargar la imagen original
    imagen = Image.open(ruta_completa)

    # Crear directorio de destino si no existe
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)

    # Aplicar transformaciones y guardar las imágenes generadas
    for i in range(cantidad_generada):
        angulo = 30 + i*10
        gamma = 1 +i
        imagen_generada = aplicar_transformaciones(imagen,angulo,gamma)
        nombre_archivo = f"{num}.png"
        ruta_destino = os.path.join(directorio_destino, nombre_archivo)
        imagen_generada.save(ruta_destino)
        num = num + 1

def aplicar_transformaciones(imagen,angulo,gamma):
    # Ejemplo: Rotar la imagen aleatoriamente
    imagen_rotada = imagen.rotate(angulo)  # Puedes ajustar el ángulo según tus necesidades

    # Ejemplo: Aplicar desenfoque
    imagen_desenfocada = imagen_rotada.filter(ImageFilter.BLUR)

    # Ejemplo: Cambiar el gamma
    factor_gamma = 1.5  # Puedes ajustar este valor según tus necesidades
    enhancer = ImageEnhance.Contrast(imagen_desenfocada)
    imagen_con_gamma = enhancer.enhance(gamma)

    return imagen_con_gamma

# Ejemplo de uso
cantidad_generada = 3  # Ajusta según tus necesidades
directorio_destino = "img_generada/"
num=34
for img in os.listdir('cascade_images/freddy/positive'):
    print("asd")
    generar_datos_sinteticos(img, cantidad_generada, directorio_destino,num)
    num+=1
