import cv2 as cv
import matplotlib.pyplot as plt
image_path="cascade_images/freddy/negative/3.jpg"
cascade_freddy= cv.CascadeClassifier('cascade/cascade.xml')
screenshot = cv.imread(image_path)
# Verificar si la carga de la imagen fue exitosa
if screenshot is None:
    print(f"No se pudo cargar la imagen desde {image_path}")

      # Realizar la detección
rectangles = cascade_freddy.detectMultiScale(screenshot)
for (x, y, w, h) in rectangles:
            cv.rectangle(screenshot, (x, y), (x+w, y+h), (0, 255, 0), 2)
plt.imshow(cv.cvtColor(screenshot, cv.COLOR_BGR2RGB))
plt.title('Detección de Objetos')
plt.show()