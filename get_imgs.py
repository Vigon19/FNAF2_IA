from simple_image_download import simple_image_download as simp
#DESCARGAR IMAGENES DE INTERNET DE CADA ANIMATRÓNICO
response = simp.simple_image_download
keywords= ["toy bonnie","toy chica","mangle", "balloon boy","puppet","withered freddy","withered bonnie","withered chica"
           ,"withered foxy"]
for kw in keywords:
    response().download(kw,80)