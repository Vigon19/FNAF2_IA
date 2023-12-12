from simple_image_download import simple_image_download as simp
response = simp.simple_image_download
keywords= ["toy bonnie","toy chica","mangle", "balloon boy","puppet","withered freddy","withered bonnie","withered chica"
           ,"withered foxy","golden freddy","shadow freddy","endo-02"]
for kw in keywords:
    response().download(kw,80)