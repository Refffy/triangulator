from PIL import Image
from tqdm import tqdm
from sys import argv


def triangulize(img, block_size):
    with Image.open(img) as img:
        w, h = img.size

        for y in tqdm(range(0, h, block_size), desc='Completed in'):
            for x in range(0, w, block_size):
                box = (x, y, x+block_size, y+block_size)

                tiled_img = img.crop(box)
                r, g, b = img.getpixel((x, y))

                for i in range(block_size):
                    for j in range(block_size):
                        tiled_img.putpixel((i, j), (r, g, b))
                        tiled_img.putpixel((j, i), ((r * 3) // 2, (g * 3) //2 , (b * 3) // 2))
                img.paste(tiled_img, (x, y))

        img.show()


if __name__ == '__main__':
    block_size = int(argv[2])
    triangulize(argv[1], block_size)
