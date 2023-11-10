import os
from math import floor
import posixpath
from typing import Callable, List, Tuple, TypeVar
from PIL import Image


I = TypeVar("I")
O = TypeVar("O")


BRIGHTNESS_PIXEL_TO_ASCII_MAP: (
    str
) = '`^",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'


def get_image(path: str):
    img = Image.open(path)
    print("Successfully loaded image!")
    print(f"Image size: {img.height} x {img.width}")
    return img


def img_to_pixel_matrix(img) -> List[List[Tuple[int, int, int]]]:
    return [[img.getpixel((x, y)) for x in range(img.width)] for y in range(img.height)]


def write_to_file(matrix: List[List], path_to_write: str) -> None:
    parent_dir: str = posixpath.join(*posixpath.split(path_to_write)[:-1])
    os.makedirs(parent_dir, exist_ok=True)
    
    with open(path_to_write, "w") as f:
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                f.write(matrix[row][col] * 3)
            f.write("\n")


def transform_matrix(
    matrix: List[List[I]], lambda_to_transform: Callable[[I], O]
) -> List[List[O]]:
    return [
        [lambda_to_transform(matrix[row][col]) for col in range(len(matrix[row]))]
        for row in range(len(matrix))
    ]


def pixel_to_brightness(pixel: Tuple[int, int, int]) -> int:
    return round(sum(pixel) / len(pixel))


def brightness_pixel_to_ascii(brightness_of_pixel: int) -> str:
    return BRIGHTNESS_PIXEL_TO_ASCII_MAP[
        floor(brightness_of_pixel / 256 * len(BRIGHTNESS_PIXEL_TO_ASCII_MAP))
    ]


if __name__ == "__main__":
    img = get_image("images/ascii-pineapple.jpg")

    print(
        "Resizing image to 200 x 200 dimension, so that ascii text will fit the screen"
    )
    img = img.resize(size=(200, 200))

    pixel_matrix: List[List[Tuple[int, int, int]]] = img_to_pixel_matrix(img)

    brightness_matrix: List[List[int]] = transform_matrix(
        pixel_matrix, pixel_to_brightness
    )

    ascii_matrix: List[List[str]] = transform_matrix(
        brightness_matrix, brightness_pixel_to_ascii
    )

    write_to_file(ascii_matrix, "output/ascii-pineapple.txt")
