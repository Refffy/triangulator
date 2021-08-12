from PIL import Image
from sys import argv


def process_tile(tile, y, r, g, b, block_y):
    for i in range(y+1000):
        for j in range(i, block_y):
            tile.putpixel((j, i), (r, g, b))
            tile.putpixel((i, j), ((r * 3) // 2, (g * 3) //2 , (b * 3) // 2))

    return tile


def triangulize(img, block_size):
    with Image.open(img) as img:
        w, h = img.size
        block_x, block_y = block_size

        for y in range(0, h, block_y):
            for x in range(0, w, block_x):
                box = (x, y, x + block_x, y + block_y)
                tiled_img = img.crop(box)

                r, g, b = img.getpixel((x, y))
                processed_tile = process_tile(tiled_img, y, r, g, b, block_y)
                img.paste(processed_tile, (x, y))

        img.show()


if __name__ == '__main__':
    block_size = int(argv[2]), int(argv[3])
    triangulize(argv[1], block_size)
