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
    return pygame.transform.scale(ret, (TILESIZE*width, TILESIZE*height))

def get(x, y):
    return pygame.transform.scale(ARRAY[x][y], (TILESIZE, TILESIZE))

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

    floor_top = get(7, 5)
    floor_middle = get(4, 4)
    floor_bottom = get(7, 7)
    floor_right = get(8, 6)
    floor_left = get(6, 6)
    floor_top_left = get(6, 5)
    floor_top_right = get(8, 5)
    floor_bottom_left = get(6, 7)
    floor_bottom_right = get(8, 7)
    floor = get(7, 6)

    projectile_gun = [get(i+7, 3) for i in range(2)]
    projectile_alien = [get(i+7, 4) for i in range(2)]

    player_idle = [get(i, 0) for i in range(2)]
    player_walk = [get(i, 1) for i in range(4)]   # Lista kuvia from x=0-3, y=1
    player_jump = [get(i+2, 0) for i in range(2)]
    player_fall = get(3, 0)

    base_alien = [get(i, 2) for i in range(2)]
    fly_alien = [get(i+2, 2) for i in range(2)]
    brain_alien = [get(i, 3) for i in range(2)]
    turret_alien = [get(i+2, 3) for i in range(2)]
    big_alien = [merge(i*2, 4, 2, 2) for i in range(2)]

    item_door = get(4, 3)
    item_shop = [get(i+4, 0) for i in range(2)]
    item_beer = get(8, 0)
    item_gun = [get(i+4, 2) for i in range(2)]
    item_jump_pad = [get(i+5, 3) for i in range(2)]


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

            "floor": floor,
            "floor_top": floor_top,
            "floor_middle": floor_middle,
            "floor_bottom": floor_bottom,
            "floor_right": floor_right,
            "floor_left": floor_left,
            "floor_top_left": floor_top_left,
            "floor_top_right": floor_top_right,
            "floor_bottom_left": floor_bottom_left,
            "floor_bottom_right": floor_bottom_right,

            "player_idle": player_idle,
            "player_walk": player_walk,
            "player_jump": player_jump,
            "player_fall": player_fall,

            "base_alien": base_alien,
            "fly_alien": fly_alien,
            "brain_alien": brain_alien,
            "turret_alien": turret_alien,
            "big_alien": big_alien,

            "item_door": door,
            "item_shop": shop,
            "item_gun": item_gun,
            "item_beer": item_beer,
            "item_jump_pad": item_jump_pad,
            }

SPRITES = get_sprites()
