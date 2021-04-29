from PIL import Image
import os
from sys import argv

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

if __name__=='__main__':
    main()
