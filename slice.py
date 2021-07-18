from typing import Optional, List, Tuple
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
    'q': 'queen',
    'p': 'pawn'
}
INV_PIECES = dict((v, k) for k, v in PIECES.items())


class Space:

    def __init__(self, id: Optional[int] = None, piece: Optional[str] = None, color: Optional[str] = None):
        self.id = id
        self.piece = piece
        self.color = color

    def row(self) -> int:
        return self.id // 8

    def col(self) -> int:
        return self.id % 8

    def get_FEN(self) -> str:
        if self.color == 'white':
            return INV_PIECES[self.piece].upper()
        elif self.color == 'black':
            return INV_PIECES[self.piece]

    def __repr__(self) -> str:
        if not self.piece and not self.color:
            return f'_'
        return f"{self.color} {self.piece} on {self.id} ({self.row()} row)"


def get_rows(table: List[Space]) -> List[List[Space]]:
    return [
        table[8 * i:8 * i + 8] for i in range(8)
    ]


class Board:
    def __init__(self, table: Optional[List]) -> None:
        self.rows = None
        if table:
            self.rows = get_rows(table)

    def get_piece(self, id: int) -> Space:
        row = id // 8
        col = id % 8
        return self.rows[row][col]

    def __repr__(self) -> str:
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


def get_piece(piece_str: str) -> Space:
    space = Space()
    if piece_str in LETTERS:
        space.color = 'black'
    if piece_str in LETTERS.upper():
        space.color = 'white'
    space.piece = PIECES[piece_str.lower()]
    return space


class App:

    def __init__(self, source: str, output: str) -> None:
        self.source_dir = source
        self.output_dir = output
        self.files = self.get_files()
        self.file_count = 0
        self.filename = None
        self.filepath = None
        self.board = None
        self.width, self.height = None, None

        self.setup()

    def setup(self):
        self.filename = self.get_next_file()
        self.filepath = self.get_filepath()
        self.board = self.get_board()
        self.width, self.height = self.get_size()

    def get_filepath(self):
        return os.path.join(self.source_dir, self.filename)

    def get_files(self) -> List[str]:
        return os.listdir(os.path.join(os.getcwd(), self.source_dir))

    def get_next_file(self) -> str:
        output = self.files[self.file_count]
        self.file_count += 1
        return output

    def get_size(self) -> Tuple[int, int]:
        with Image.open(self.filepath) as im:
            return im.width, im.height

    def get_board(self) -> Board:
        name = self.filename.replace('.jpeg', '')
        board = []
        for row in name.split('-'):
            for letter in row:
                if letter in NUMBERS:
                    for i in range(int(letter)):
                        board.append(Space())
                if letter in LETTERS or letter in LETTERS.upper():
                    # print(self.filename)
                    board.append(get_piece(letter))
        for i, item in enumerate(board):
            item.id = i

        return Board(board)

    def crop(self, height: int, width: int):
        with Image.open(self.filepath) as im:
            for i in range(im.height // height):
                for j in range(im.width // width):
                    box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
                    yield im.crop(box)

    def get_folder_name(self, id: int) -> str:
        piece = self.board.get_piece(id)
        if not piece.piece:
            return "empty"
        return f"{piece.color}{piece.piece.capitalize()}"

    def save_slice(self) -> None:

        width, height = self.width // 8, self.height // 8
        start_num = 0
        for k, piece_im in enumerate(self.crop(height, width), start_num):
            img = Image.new('RGB', (height, width), 255)
            img.paste(piece_im)
            folder = self.get_folder_name(k)
            folder = os.path.join(os.getcwd(), self.output_dir, folder)
            if not os.path.isdir(folder):
                os.makedirs(folder)
            idx = len(os.listdir(folder))
            path = os.path.join(folder, f"IMG-{idx}.png")
            img.save(path)

    def slice_everything(self) -> None:
        while self.file_count != len(self.files):
            self.save_slice()
            self.setup()


if __name__ == "__main__":
    app = App(argv[1], argv[2])
    app.slice_everything()
