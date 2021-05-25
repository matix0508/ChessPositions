from PIL import Image
import os
from sys import argv
LETTERS = 'qwertyuiopasdfghjklzxcvbnm'

PIECES = {
    'b': 'bishop',
    'r': 'rook',
    'k': 'king',
    'n': 'night',
    'q': 'queen'
}

INV_PIECES = dict((v, k) for k, v in PIECES.items())

NUMBERS = '12345678'

class Space:
    def __init__(self, id=None, piece=None, color=None):
        self.id = id
        self.piece = piece
        self.color = color

    def row(self):
        return self.id // 8

    def col(self):
        return self.id % 8

    def FEN(self):
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
        table[8*i:8*i+8] for i in range(8)
    ]



class Board:
    def __init__(self, table=None):
        self.rows = get_rows(table)
        # print(self.rows)

    def __repr__(self):
        output = ''
        if self.rows:
            for row in self.rows:
                for item in row:
                    if item.FEN():
                        output += item.FEN()
                    else:
                        if not output:
                            output += '1'
                        elif output[-1] in NUMBERS:
                            output = output[:-1] + str(int(output[-1])+1)
                        else:
                            output += '1'
                output += '-'
        output = output[:-1]
        return output



def crop(infile,height,width):
    im = Image.open(infile)

    for i in range(imgheight//height):
        for j in range(imgwidth//width):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)


def main():
    infile=argv[1]
    with Image.open(infile):
        width, height = im.size
        width /= 8
        height /= 8
    start_num=0
    for k,piece in enumerate(crop(infile,height,width),start_num):
        img=Image.new('RGB', (height,width), 255)
        img.paste(piece)
        if len(argv) > 2:
            dest = argv[2]
        else:
            dest = 'slices'
        path=os.path.join('slices2',f"IMG-{k}.png")
        img.save(path)

def get_piece(piece_str):
    space = Space()
    if piece_str in LETTERS:
        space.color = 'black'
    if piece_str in LETTERS.upper():
        space.color = 'white'
    space.piece = PIECES[piece_str.lower()]
    return space


def get_names(filename):
    filename = filename.replace('.jpeg', '')
    board = []
    for row in filename.split('-'):
        for letter in row:
            # print(letter)
            if letter in NUMBERS:
                for i in range(int(letter)):
                    board.append(Space())
                    # print("empty space")
            if letter in LETTERS or letter in LETTERS.upper():
                board.append(get_piece(letter))
                # print(get_piece(letter).piece)
    for i, item in enumerate(board):
        item.id = i
    # print(board)
    # print(Board(board))
    print(Board(board))


# if __name__=='__main__':
    # main()
