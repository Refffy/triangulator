from PIL import Image, ImageOps
from sys import argv


def triangulize(img, block_size):
    with Image.open(img) as img:
        w, h = img.size
        block_x, block_y = block_size

        for x in range(0, w, block_x):
            for y in range(0, h, block_y):
                box = (y, x, y+block_x, x+block_y)

                tiled_img = img.crop(box)
                r, g, b = img.getpixel((x, y))

                for i in range(x+block_x):
                    for j in range(i, block_y):
                        tiled_img.putpixel((i, j), (r, g, b))
                        tiled_img.putpixel((j, i), ((r * 3) // 2, (g * 3) //2 , (b * 3) // 2))
                img.paste(tiled_img, (x, y))

        img.show()


if __name__ == '__main__':
    block_size = int(argv[2]), int(argv[3])
    triangulize(argv[1], block_size)
