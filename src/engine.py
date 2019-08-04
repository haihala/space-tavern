from enemy import Enemy
from player import Player
from tile import Tile
from enemy_collection import ENEMIES
from item_collection import ITEMS

from constants import HELDSIZE, TILESIZE, LERP

import pygame
import math
import random

from copy import copy
from time import sleep, time

class Engine():
    def __init__(self, conf, resolution):
        flags = (pygame.FULLSCREEN * int(conf["fullscreen"]))
        self.display = pygame.display.set_mode(resolution, flags)

        self.money = 0
        self.in_space = True
        self.planet = 0

        self.player = Player(conf["binds"])
        self.actors = [self.player, ENEMIES["alien_base"]([-5, -5])]
        self.items = [
                ITEMS["item_beer"]([6, 5]),
                ITEMS["item_gun"]([7, 4])
        ]
        self.tiles = []
        self.background = []
        self.panorama = [
            Tile([0,0], "panorama_stars"),
            Tile([-self.display.get_width()/TILESIZE, 0], "panorama_stars")
        ]
        self.color = (0, 0, 0)

        self.tick_target_duration = 1
        self.cam = [0,0]
        self.target_cam = [0,0]
        self.running = False

        from pygame_objects import SOUNDS
        SOUNDS["music_peace"].set_volume(0.25)
        SOUNDS["music_peace"].play(-1)

        for x in range(-10, 10):
            for y in range(-6, 7):
                if abs(x) <= 6 and abs(y) >= 2 and abs(y) <= 4:
                    if abs(x) < 6 and (y == 2 or y == -4):
                        self.background.append(Tile([x,y], "window_top"))
                    elif abs(x) < 6 and (y == 4 or y == -2):
                        self.background.append(Tile([x,y], "window_bottom"))
                    elif x == -6 and abs(y) == 3:
                        self.background.append(Tile([x,y], "window_left"))
                    elif x == 6 and abs(y) == 3:
                        self.background.append(Tile([x,y], "window_right"))
                    elif x == -6 and (y == -4 or y == 2):
                        self.background.append(Tile([x,y], "window_top_left"))
                    elif x == 6 and (y == -4 or y == 2):
                        self.background.append(Tile([x,y], "window_top_right"))
                    elif x == -6 and (y == 4 or y == -2):
                        self.background.append(Tile([x,y], "window_bottom_left"))
                    elif x == 6 and (y == 4 or y == -2):
                        self.background.append(Tile([x,y], "window_bottom_right"))
                    else:
                        self.background.append(Tile([x,y], "window"))
                elif math.sin(x) > 0 and abs(math.sin(y)) < (0.2 + abs(math.cos(x)/1.23)):
                    self.background.append(Tile([x,y], "wall_middle"))
                else:
                    self.background.append(Tile([x,y], "wall"))

        for x in range(-10, 10):
            for y in range(-6, 7):

                if ((x == -10 or x == 9) or (y == -6 or y == 6 or y == 0) and (not (y == 0 and abs(x) < 3))) and not (y <= 5 and y >= 3):
                    self.tiles.append(Tile([x,y], "floor"))
                elif (y <= 5 and y >= 3) and (x == -10 or x == 9):
                    self.items.append(ITEMS["item_door"]([x,y]))
                elif y == 0 and abs(x) < 3:
                    self.items.append(ITEMS["item_jump_pad"]([x,y]))

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

    @property
    def enemies(self):
        return [i for i in self.actors if type(i) is Enemy]

    def update_surroundings(self, state):
        self.in_space = state
        if self.in_space:
            pass
        else:
            pass

    def collides(self, entity=None, point=None, target="collider", exclude=[]):
        spaces = {
                "*": self.actors + self.items + self.tiles,
                "collider": self.actors + self.tiles + [i for i in self.items if i.collider],
                "enemy": self.enemies,
                "player": [self.player],
                "actor": self.actors,
                "tile": self.tiles,
                "item": self.items
                }
        search_space = spaces[target]

        if entity:
            return [i for i in search_space if i not in exclude and any(p in i.colliders for p in entity.colliders)]
        if point:
            return [i for i in search_space if i not in exclude and point in i.colliders]

    def project_collides(self, entity, shift, target="collider", exclude=[]):
        cp = copy(entity)
        cp.position = [cp.position[i]+shift[i] for i in range(2)]
        exclude.append(cp)
        return self.collides(cp, target=target, exclude=exclude)

    def place(self, spot, item):
        if not self.collides(point=spot, target="*"):
            item.position = spot
            item.old_position = spot
            self.items.append(item)
            return True

    def camera_shake(self, amount):
        self.cam = [self.cam[i] + random.uniform(-amount, amount) for i in range(2)]

    def run(self):
        self.running = True
        engine = self
        while self.running:
            self.actors = [entity for entity in self.actors if not entity.dead]
            self.items = [item for item in  self.items if not item.dead]

            for item in self.items:
                item.tick(engine)

            for entity in self.actors:
                for item in self.collides(entity, target="item"):
                    if item.on_collision:
                        item.on_collision(item, self, entity)
                if entity == self.player:
                    self.player_tick(self.tick_target_duration)
                    start_time = time()
                    while time()-start_time < 0.25:
                        self.render(0)
                else:
                    entity.tick(self)

            for entity in self.actors:
                entity.grounded = self.project_collides(entity, [0,1])

    def quit(self):
        # Maybe save
        exit(0)

    def player_tick(self, slot):
        buffered = None
        start_time = time()
        true_slot = (slot/2 if self.player.fatigue else slot)
        while time()-start_time < true_slot and not buffered:
            self.render((time()-start_time)/true_slot)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if not self.player.fatigue:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            btn = 'up'
                        elif event.key == pygame.K_DOWN:
                            btn = 'down'
                        elif event.key == pygame.K_LEFT:
                            btn = 'left'
                        elif event.key == pygame.K_RIGHT:
                            btn = 'right'
                        else:
                            btn = event.unicode

                        if btn in self.player.binds:
                            buffered = self.player.binds[btn]
        self.player.tick(self, buffered)

    def render(self, tick_time_left):
        # Draw the world
        self.cam = [LERP(self.cam[i], self.target_cam[i], 0.1) for i in range(2)]
        self.draw_panorama()
        self.draw_background()
        self.draw_world()
        self.draw_hud(tick_time_left)
        pygame.display.flip()

    def draw_panorama(self):
        targets = []
        for p in self.panorama:
            p.position = [p.position[0]+0.01, p.position[1]]
            if p.position[0] > self.display.get_width()/TILESIZE:
                p.position = [-self.display.get_width()/TILESIZE, p.position[1]]
                p.old_position = p.position[:]
            if random.randint(0,100) > 99:
                p.sprite_offset = p.sprite_offset + 1
            sprite, position = p.get_surf(self.display, self.cam)
            targets.append((pygame.transform.scale(sprite, (self.display.get_width(), self.display.get_height())), position))

        self.display.fill(self.color)
        self.display.blits(targets)

    def draw_background(self):

        targets= []
        for bg in self.background:
            targets.append(bg.get_surf(self.display, self.cam))
        for fg in self.tiles:
            targets.append(fg.get_surf(self.display, self.cam))

        self.display.blits(targets)

    def draw_world(self):
        targets = []
        for entity in self.actors:
            sprite, position = entity.get_surf(self.display, self.cam)
            targets.append((sprite, position))
            if type(entity) is Player and entity.inventory:
                inventory_sprite, inventory_position = entity.inventory.get_surf(self.display, self.cam)

                offset = [HELDSIZE if entity.facing_right else -HELDSIZE, 0]

                targets.append((pygame.transform.scale(pygame.transform.flip(inventory_sprite, True, False) if entity.facing_right else inventory_sprite, (HELDSIZE, HELDSIZE)), [position[i] + offset[i] + TILESIZE/2 - HELDSIZE/2 for i in range(2)]))
        for item in self.items:
            targets.append(item.get_surf(self.display, self.cam))
        self.display.blits(targets)

    def draw_hud(self, tick_portion_left):
        if self.player.fatigue:
            color = [255, 0, 0]
        else:
            color = [0, 255, 0]
        pygame.draw.rect(self.display, color, (0, 0, self.display.get_width()*(1-tick_portion_left), 50))
