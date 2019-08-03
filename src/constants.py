import pygame
from glob import iglob
from os.path import basename

TILESIZE = 50
CONFPATH = 'conf.json'
TILE_SPRITES = {basename(i): pygame.transform.smoothscale(pygame.image.load(i).convert_alpha(), TILESIZE) for i in iglob("tiles/*")}
