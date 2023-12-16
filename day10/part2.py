import numpy as np
from PIL import Image

image = Image.open('input_convert_final.png')
img_arr = np.asarray(image)

print(img_arr)
print(img_arr.shape)

height = img_arr.shape[1]

count = 0
for row in img_arr:
    print()
    for pix in row:
        if pix.any():
            print('B', end='')
        else:
            count += 1
            print(' ', end='')
print(count)