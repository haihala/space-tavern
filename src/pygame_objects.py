from constants import TILESIZE

import pygame

from random import randint

def get_array(path, size=16):
    sheet = pygame.image.load(path).convert_alpha()
    width, height = sheet.get_size()

    return list(zip(*[[sheet.subsurface(pygame.Rect(x*size, y*size, size, size)) for x in range(width//size)] for y in range(height//size)]))

ARRAY = get_array("resources/Test.png")

def merge(x, y, width, height, size=16):
    ret = pygame.Surface((width*size, height*size))
    for i in range(width):
        for j in range(height):
            ret.blit(ARRAY[x+i][y+j], (i*size, j*size))
    return pygame.transform.smoothscale(ret, (TILESIZE*width, TILESIZE*height))

def get(x, y):
    return pygame.transform.smoothscale(ARRAY[x][y], (TILESIZE, TILESIZE))

def get_sprites():
    wall_top = get(6, 0)
    wall_middle = get(6, 1)
    wall_bottom = get(7, 2)
    wall_right = get(8, 1)
    wall_left = get(4, 1)
    wall_top_left = get(5, 1)
    wall_top_right = get(7, 1)
    wall_bottom_left = get(6, 2)
    wall_bottom_right = get(8, 2)
    wall = get(7, 0)

    player_idle = [get(i, 0) for i in range(1)]
    player_walk = [get(i, 1) for i in range(4)]   # Lista kuvia from x=0-3, y=1
    player_jump = [get(i+2, 0) for i in range(1)]
    player_fall = get(3, 0)

    return {
            "wall": wall,
            "wall_top": wall_top,
            "wall_middle": wall_middle,
            "wall_bottom": wall_bottom,
            "wall_right": wall_right,
            "wall_left": wall_left,
            "wall_top_left": wall_top_left,
            "wall_top_right": wall_top_right,
            "wall_bottom_left": wall_bottom_left,
            "wall_bottom_right": wall_bottom_right,

            "player_idle": player_idle,
            "player_walk": player_walk,
            "player_jump": player_jump,
            "player_fall": player_fall,

            }

SPRITES = get_sprites()
