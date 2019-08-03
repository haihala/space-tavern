from tile import Tile
from item import Item
from item_collection import ITEMS

import math
import pygame

class Room():
    def __init__(self, name="", fill_color=(0,0,0)):
        self.name = name
        self.tiles = []
        self.background = []
        self.items = [
                ITEMS["item_beer"]([6, 5])
        ]

        for x in range(-10, 10):
            for y in range(-6, 7):
                if math.sin(x) > 0 and abs(math.sin(y)) < (0.2 + abs(math.cos(x)/1.23)):
                    self.background.append(Tile([x,y], "wall_middle"))
                else:
                    self.background.append(Tile([x,y], "wall"))

        for x in range(-10, 10):
            for y in range(-6, 7):

                if ((x == -10 or x == 9) or (y == -6 or y == 6 or y == 0) and (not (y == 0 and abs(x) < 3))) and not (y <= 5 and y >= 3):
                    self.tiles.append(Tile([x,y], "floor"))
                elif (y <= 5 and y >= 3) and (x == -10 or x == 9):
                    self.tiles.append(ITEMS["item_door"]([x,y]))
                elif y == 0 and abs(x) < 3:
                    self.tiles.append(ITEMS["item_jump_pad"]([x,y]))

                if y == 6 or y == -6 or (y == 0 and abs(x) > 2) or (y == 2 and (x == -10 or x == 9)):
                    self.background.append(Tile([x,y+1], "floor_bottom"))
                if y == -6 or y == 6 or (y == 0 and abs(x) > 2):
                    self.background.append(Tile([x,y-1], "floor_top"))
                if (x == -10 or x == 9 or (y == 0 and x == -3)) and not (y <= 5 and y >= 3):
                    self.background.append(Tile([x+1,y], "floor_right"))
                if (x == -10 or x == 9 or (y == 0 and x == 3)) and not (y <= 5 and y >= 3):
                    self.background.append(Tile([x-1,y], "floor_left"))
                if ((x == -10 and y == -6) or (y == 0 and x == 3)) or (y == 6 and x == -10):
                    self.background.append(Tile([x-1,y-1], "floor_top_left"))
                if ((x == -10 and y == 6) or (y == 0 and x == 3)) or (y == 2 and (x == -10 or x == 9)):
                    self.background.append(Tile([x-1,y+1], "floor_bottom_left"))
                if ((x == 9 and y == -6) or (y == 0 and x == -3)) or (y == 6 and x == 9):
                    self.background.append(Tile([x+1,y-1], "floor_top_right"))
                if ((x == 9 and y == 6) or (y == 0 and x == -3)) or (y == 2 and (x == -10 or x == 9)):
                    self.background.append(Tile([x+1,y+1], "floor_bottom_right"))

        self.color = fill_color

    @property
    def colliders(self):
        return [i for i in self.items if i.collider] + self.tiles

    def draw(self, surface, camera=(0,0)):
        sprites = []
        for bg in self.background:
            sprites.append(bg.get_surf(surface, camera))

        for fg in self.tiles:
            sprites.append(fg.get_surf(surface, camera))

        for item in self.items:
            sprites.append(item.get_surf(surface, camera))

        surface.fill(self.color)
        surface.blits(sprites)
