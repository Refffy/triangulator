from PIL import Image
import numpy as np
from multiprocessing import Pool, cpu_count
import sys


def process_block(args):
    img_array, x, y, block_x, block_y, w, h = args
    end_x = min(x + block_x, w)
    end_y = min(y + block_y, h)

    block = img_array[y:end_y, x:end_x]

    r, g, b = img_array[y, x]
    top_triangle_color = np.array([r, g, b])
    bottom_triangle_color = np.clip((
        top_triangle_color * 1.8
    ).astype(int), 0, 255)

    mask = np.tri(block.shape[0], block.shape[1], dtype=bool)
    block[mask] = top_triangle_color
    block[~mask] = bottom_triangle_color

    return x, y, block


def triangulize(img_path, block_size):
    with Image.open(img_path) as img:
        img_array = np.array(img)
        h, w, _ = img_array.shape
        block_x, block_y = block_size

        args = (
            (img_array, x, y, block_x, block_y, w, h)
            for x in range(0, w, block_x)
            for y in range(0, h, block_y)
        )

        with Pool(processes=cpu_count()) as pool:
            results = pool.map(
                func=process_block, iterable=args, chunksize=max(
                    block_x*w, block_y*h)
            )

        for x, y, block in results:
            img_array[y:y+block.shape[0], x:x+block.shape[1]] = block

        Image.fromarray(img_array).show()


if __name__ == '__main__':
    block_size = (int(sys.argv[2]), int(sys.argv[3]))
    triangulize(sys.argv[1], block_size)
