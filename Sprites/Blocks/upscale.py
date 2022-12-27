from os import listdir
from os.path import isfile, join
from PIL import Image
onlyfiles = [f for f in listdir() if isfile(join(f)) and f.endswith(".png")]
for i in onlyfiles:
    img = Image.open(i)
    new_image = img.resize((45, 48))
    name = i.split('.')[0]+"0.1"+".png"
    new_image.save(name)
