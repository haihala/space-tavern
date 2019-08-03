from tile import Tile

import pygame

class Room():
    def __init__(self, name="", tiles=[], background=[], fill_color=(0,0,0)):
        self.name = name
        self.tiles = []
        for x in range(-10, 10):
            for y in range(-6, 7):
                if (x == -10 or x == 9) or (y == -6 or y == 0 or y == 6):
                    self.tiles.append(Tile([x,y], "wall"))

        self.background = [Tile(*i) for i in background]
        self.color = fill_color

    def draw(self, surface, camera=(0,0)):
        sprites = []
        for bg in self.background:
            sprites.append(bg.get_surf(surface, camera))

        for fg in self.tiles:
            sprites.append(fg.get_surf(surface, camera))

        surface.fill(self.color)
        surface.blits(sprites)
