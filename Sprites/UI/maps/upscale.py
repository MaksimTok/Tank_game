from os import listdir
from os.path import isfile, join
from PIL import Image

onlyfiles = [f for f in listdir() if isfile(join(f)) and f.endswith(".png")]
for el in onlyfiles:
    img = Image.open(el)
    pixels = img.load()
    new_image = Image.new("RGB", (img.width // 3, img.height // 3), (0, 0, 0))
    pixels_new = new_image.load()
    for x in range(0, img.size[0], 3):
        for y in range(0, img.size[1],3):
            color = pixels[x, y]
            pixels_new[x //3, y//3] = color
    new_image.save(el)
