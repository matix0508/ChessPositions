from typing import Optional

from PIL import Image
import os
from sys import argv

LETTERS = 'qwertyuiopasdfghjklzxcvbnm'
NUMBERS = '12345678'
PIECES = {
    'b': 'bishop',
    'r': 'rook',
    'k': 'king',
    'n': 'night',
    'q': 'queen'
}
INV_PIECES = dict((v, k) for k, v in PIECES.items())


class Space:

    def __init__(self, id: Optional[int] = None, piece: Optional[str] = None, color: Optional[str] = None):
        self.id = id
        self.piece = piece
        self.color = color

    def row(self):
        return self.id // 8

    def col(self):
        return self.id % 8

    def get_FEN(self) -> str:
        if self.color == 'white':
            return INV_PIECES[self.piece].upper()
        elif self.color == 'black':
            return INV_PIECES[self.piece]

    def __repr__(self):
        if not self.piece and not self.color:
            return f'_'
        return f"{self.color} {self.piece} on {self.id} ({self.row()} row)"


def get_rows(table):
    if not table:
        return None
    return [
        table[8 * i:8 * i + 8] for i in range(8)
    ]


class Board:
    def __init__(self, table=None):
        self.rows = get_rows(table)

    def __repr__(self):
        output = ''
        if self.rows:
            for row in self.rows:
                for item in row:
                    if item.get_FEN():
                        output += item.get_FEN()
                    else:
                        if not output:
                            output += '1'
                        elif output[-1] in NUMBERS:
                            output = output[:-1] + str(int(output[-1]) + 1)
                        else:
                            output += '1'
                output += '-'
        output = output[:-1]
        return output


def crop(infile, height, width):
    im = Image.open(infile)

    for i in range(im.height // height):
        for j in range(im.width // width):
            box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
            yield im.crop(box)


def main():
    infile = argv[1]
    with Image.open(infile) as im:
        width, height = im.size
        width /= 8
        height /= 8
    start_num = 0
    for k, piece in enumerate(crop(infile, height, width), start_num):
        img = Image.new('RGB', (height, width), 255)
        img.paste(piece)
        if len(argv) > 2:
            dest = argv[2]
        else:
            dest = 'slices'
        path = os.path.join('slices2', f"IMG-{k}.png")
        img.save(path)


def get_piece(piece_str: str) -> Space:
    space = Space()
    if piece_str in LETTERS:
        space.color = 'black'
    if piece_str in LETTERS.upper():
        space.color = 'white'
    space.piece = PIECES[piece_str.lower()]
    return space


class App:

    def __init__(self, filename: str):
        self.filename = filename
        self.board = None

    def get_names(self):
        name = self.filename.replace('.jpeg', '')
        board = []
        for row in name.split('-'):
            for letter in row:
                if letter in NUMBERS:
                    for i in range(int(letter)):
                        board.append(Space())
                if letter in LETTERS or letter in LETTERS.upper():
                    board.append(get_piece(letter))
        for i, item in enumerate(board):
            item.id = i

        self.board = Board(board)
