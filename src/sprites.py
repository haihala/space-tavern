from constants import TILESIZE

import pygame
from glob import iglob
from os.path import basename

tile_sprites = {basename(i): pygame.transform.smoothscale(pygame.image.load(i).convert_alpha(), TILESIZE) for i in iglob("tiles/*")}
