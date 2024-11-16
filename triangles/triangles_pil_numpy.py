from PIL import Image
import numpy as np
from tqdm import tqdm
import sys


def triangulize(img_path, block_size):
    with Image.open(img_path) as img:
        img_array = np.array(img)
        h, w, _ = img_array.shape

        for y in tqdm(range(0, h, block_size), desc='Completed in'):
            for x in range(0, w, block_size):
                end_x = min(x + block_size, w)
                end_y = min(y + block_size, h)

                block = img_array[y:end_y, x:end_x]

                r, g, b = block[0, 0, :]

                mask = np.tri(block.shape[0], block.shape[1], dtype=bool)

                top_triangle_color = np.array([r, g, b])
                bottom_triangle_color = ((top_triangle_color * 1.8).astype(int)).clip(0, 255)

                block[mask] = top_triangle_color
                block[~mask] = bottom_triangle_color

                img_array[y:end_y, x:end_x] = block

        Image.fromarray(img_array).show()


if __name__ == '__main__':
    img_path = sys.argv[1]
    block_size = int(sys.argv[2])
    triangulize(img_path, block_size)
