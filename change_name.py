import os

def change_name():
    ruta_completa = 'comun_2/'  # Ruta completa de la carpeta

    # Verificar si la ruta existe
    if not os.path.exists(ruta_completa):
        print(f"La ruta '{ruta_completa}' no existe.")
        return

    # Obtener la lista de archivos en la carpeta
    archivos = os.listdir(ruta_completa)

    # Iterar sobre los archivos y cambiar sus nombres
    for i, archivo in enumerate(archivos, start=1):
        # Obtener la ruta completa del archivo original
        ruta_original = os.path.join(ruta_completa, archivo)

        # Obtener la extensión del archivo
        _, extension = os.path.splitext(archivo)

        # Construir el nuevo nombre del archivo con el formato 1, 2, 3, ...
        nuevo_nombre = f"{i}{extension}"

        # Obtener la ruta completa del nuevo archivo
        ruta_nueva = os.path.join(ruta_completa, nuevo_nombre)

        # Renombrar el archivo
        os.rename(ruta_original, ruta_nueva)

        print(f"Renombrado: {archivo} -> {nuevo_nombre}")

# Llamar a la función para realizar el cambio de nombres
change_name()