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
    return ret

def stitch (array):
    wall = pygame.transform.smoothscale(array[6][2], (TILESIZE, TILESIZE))

    return {
            "wall": wall,
            }

SPRITES = stitch(get_array("resources/Test.png"))
