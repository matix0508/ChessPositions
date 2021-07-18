from typing import Tuple

from PIL import Image
import os
from slice import Space, Board


def recognize_slice(filepath: str) -> Space:
    # TODO: recognize slice and save it in Space class
    return Space(0, 'k', 'b')


class FenApp:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.filepath = self.get_filepath()
        self.width, self.height = self.get_size()
        self.files = None
        self.board = None

    def get_size(self) -> Tuple[int, int]:
        with Image.open(self.filepath) as im:
            return im.width, im.height

    def get_filepath(self) -> str:
        return os.path.join(os.getcwd(), self.filename)

    def crop(self):
        with Image.open(self.filepath) as im:
            width, height = im.width, im.height
            for i in range(im.height // height):
                for j in range(im.width // width):
                    box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
                    yield im.crop(box)

    def save_crop(self) -> None:
        for k, piece_im in enumerate(self.crop()):
            img = Image.new("RGB", (self.height // 8, self.width // 8))
            img.paste(piece_im)
            path = os.path.join(os.getcwd(), 'current')
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join(path, f"slice{k}")
            img.save(path)
        self.files = os.listdir(os.path.join(os.getcwd(), 'current'))

    def recognize_slices(self):
        spaces = []
        for image in self.files:
            space = recognize_slice(os.path.join(os.getcwd(), image))
            spaces.append(space)
        self.board = Board(spaces)
        print(self.board)
