from constants import TILESIZE

import pygame
from glob import iglob
from os.path import basename
TILE_SPRITES = {basename(i): pygame.transform.smoothscale(pygame.image.load(i).convert_alpha(), (TILESIZE, TILESIZE)) for i in iglob("resources/*.png")}
