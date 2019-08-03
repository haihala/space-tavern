from constants import TILESIZE

import pygame

from random import randint

def get_array(path, size=16):
    sheet = pygame.image.load(path).convert_alpha()
    width, height = sheet.get_size()

    return list(zip(*[[sheet.subsurface(pygame.Rect(x*size, y*size, size, size)) for x in range(width//size)] for y in range(height//size)]))

def merge(array, x, y, width, height, size=16):
    ret = pygame.Surface((width*size, height*size))
    for i in range(width):
        for j in range(height):
            ret.blit(array[x+i][y+j], (i*size, j*size))
    return pygame.transform.smoothscale(ret, (TILESIZE*width, TILESIZE*height))

def get(x, y):
    return pygame.transform.smoothscale(array[x][y], (TILESIZE, TILESIZE))

def stitch (array):
    wall = get(6, 2)    # Kuva @x=6, y=2
    walk = [get(i, 1) for i in range(4)]   # Lista kuvia from x=0-3, y=1
    big = merge(2, 3, 5, 5)         # yksi iso kuva joka on 5 leveä, 5 korkea ja vasen ylänurkka on kohdassa x=2 y=3

    return {
            "wall": wall,
            }

SPRITES = stitch(get_array("resources/Test.png"))
