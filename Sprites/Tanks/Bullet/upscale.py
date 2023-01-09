from os import listdir
from os.path import isfile, join
from PIL import Image

onlyfiles = [f for f in listdir() if isfile(join(f)) and f.endswith(".png")]
for el in onlyfiles:
    img = Image.open(el)
    pixels = img.load()
    new_image = Image.new("RGB", (img.width * 3, img.height * 3), (0, 0, 0))
    pixels_new = new_image.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            color = pixels[x, y]
            for i in range(x * 3, x * 3 + 3):
                for j in range(y * 3, y * 3 + 3):
                    pixels_new[i, j] = color
    new_image.save(el)
