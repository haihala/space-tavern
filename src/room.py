from tile import Tile

import pygame

class Room():
    def __init__(self, name="", tiles=[], background=[], fill_color=(0,0,0)):
        self.name = name
        self.tiles = [Tile(*i) for i in tiles]
        self.background = [Tile(*i) for i in background]
        self.color = fill_color

    def draw(self, surface, camera=(0,0)):
        sprites = []
        for bg in self.background:
            sprites.append(bg.get_surf(surface, camera))

        for fg in self.tiles:
            sprites.append(fg.get_surf(surface, camera))

        surface.fill(self.color)
        print(sprites)
        surface.blits(sprites)


