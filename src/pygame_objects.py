from constants import TILESIZE

from math import pi
import pygame
pygame.mixer.init(buffer=1)

def get_array(path, size=16):
    sheet = pygame.image.load(path).convert_alpha()
    width, height = sheet.get_size()

    return list(zip(*[[sheet.subsurface(pygame.Rect(x*size, y*size, size, size)) for x in range(width//size)] for y in range(height//size)]))

ARRAY = get_array("resources/Test.png")

def merge(x, y, width, height):
    ret = pygame.Surface((width*TILESIZE, height*TILESIZE), pygame.SRCALPHA).convert_alpha()
    for i in range(width):
        for j in range(height):
            ret.blit(get(x+i, y+j), (i*TILESIZE, j*TILESIZE))
    return ret.convert_alpha()

def get(x, y):
    return pygame.transform.scale(ARRAY[x][y], (TILESIZE, TILESIZE))

def get_sprites():
    return {
        "panorama_stars": [pygame.image.load("resources/Stars_Panorama1.png").convert(), pygame.image.load("resources/Stars_Panorama2.png").convert()],
        "panorama_planet": [pygame.image.load("resources/Land_Panorama.png").convert_alpha()],

        "wall_top": get(6, 0),
        "wall_middle": get(6, 1),
        "wall_bottom": get(7, 2),
        "wall_right": get(8, 1),
        "wall_left": get(4, 1),
        "wall_top_left": get(5, 1),
        "wall_top_right": get(7, 1),
        "wall_bottom_left": get(6, 2),
        "wall_bottom_right": get(8, 2),
        "wall": get(7, 0),

        "window_top": get(1, 6),
        "window_bottom": get(0, 7),
        "window_right": get(4, 6),
        "window_left": get(3, 6),
        "window_top_left": get(0, 6),
        "window_top_right": get(2, 6),
        "window_bottom_left": get(5, 6),
        "window_bottom_right": get(1, 7),
        "window": get(6, 4),

        "floor_top": get(7, 5),
        "floor_middle": get(4, 4),
        "floor_bottom": get(7, 7),
        "floor_right": get(8, 6),
        "floor_left": get(6, 6),
        "floor_top_left": get(6, 5),
        "floor_top_right": get(8, 5),
        "floor_bottom_left": get(6, 7),
        "floor_bottom_right": get(8, 7),
        "floor": get(7, 6),

        "ground_top": get(5, 4),

        "projectile_gun": [get(i+7, 3) for i in range(2)],
        "projectile_alien": [get(i+7, 4) for i in range(2)],
        "projectile_alien_down": [pygame.transform.rotate(get(i+7, 4), 90) for i in range(2)],

        "player_idle": [get(i, 0) for i in range(2)],
        "player_walk": [get(i, 1) for i in range(4)],   # Lista kuvia from x=0-3, y=1,
        "player_jump": [get(i+2, 0) for i in range(2)],
        "player_fall": get(3, 0),

        "alien_spawner": [get(i+4,5) for i in range(2)],
        "alien_spawner_big": [merge(2+i*2, 7, 2, 2) for i in range(2)],
        "alien_base": [get(i, 2) for i in range(2)],
        "alien_fly": [get(i+2, 2) for i in range(2)],
        "alien_brain": [get(i, 3) for i in range(2)],
        "alien_turret": [get(i+2, 3) for i in range(2)],
        "alien_big": [merge(i*2, 4, 2, 2) for i in range(2)],

        "door": get(4, 3),
        "item_shop": [get(i+4, 0) for i in range(2)],
        "item_beer": get(8, 0),
        "item_gun": [get(i+4, 2) for i in range(2)],
        "item_jump_pad": [get(i+5, 3) for i in range(2)],
    }

SPRITES = get_sprites()

def get_sounds():
    return  {
        "item_throw": pygame.mixer.Sound("resources/item_throw.wav"),
        "item_pickup": pygame.mixer.Sound("resources/item_pickup.wav"),
        "item_drop": pygame.mixer.Sound("resources/item_drop.wav"),

        "player_move": pygame.mixer.Sound("resources/player_move.wav"),

        "music_peace": pygame.mixer.Sound("resources/music_peace.wav"),
        "music_space": pygame.mixer.Sound("resources/music_space.wav")
    }

SOUNDS = get_sounds()
