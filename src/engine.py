from player import Player
from room import Room
from enemy import Enemy
from enemy_collection import ENEMIES

import pygame

from copy import copy
from time import sleep, time

class Engine():
    def __init__(self, conf, resolution):
        flags = (pygame.FULLSCREEN * int(conf["fullscreen"]))
        self.display = pygame.display.set_mode(resolution, flags)

        self.player = Player(conf["binds"])
        self.actors = [self.player, ENEMIES["alien_base"]([-5, -5])]
        self.room = Room()

        self.tick_target_duration = 1
        self.cam = [0,0]
        self.running = False

    @property
    def enemies(self):
        return [i for i in self.actors if type(i) is Enemy]

    def collides(self, entity=None, point=None, target="collider", exclude=[]):
        spaces = {
                "*": self.actors + self.room.items + self.room.tiles,
                "collider": self.actors + self.room.colliders,
                "enemy": self.enemies,
                "actor": self.actors,
                "tile": self.room.tiles,
                "item": self.room.items
                }
        search_space = spaces[target]

        if entity:
            return [i for i in search_space if i not in exclude and any(p in i.colliders for p in entity.colliders)]
        if point:
            return [i for i in search_space if i not in exclude and point in i.colliders]

    def project_collides(self, entity, shift, target="collider", exclude=[]):
        cp = copy(entity)
        cp.position = [cp.position[i]+shift[i] for i in range(2)]
        exclude.append(entity)
        return self.collides(cp, target=target, exclude=exclude)

    def place(self, spot, item):
        if not self.collides(point=spot, target="*"):
            item.position = spot
            self.room.items.append(item)

    def run(self):
        self.running = True
        engine = self
        while self.running:
            for item in self.room.items:
                item.tick(engine)

            for entity in self.actors:
                for item in self.collides(entity, target="item"):
                    if item.on_collision:
                        item.on_collision(self, target)
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
        while time()-start_time < slot and not buffered:
            self.render((time()-start_time)/slot)
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
        self.draw_background()
        self.draw_world()
        self.draw_hud(tick_time_left)
        pygame.display.flip()

    def draw_background(self):
        self.room.draw(self.display, self.cam)

    def draw_world(self):
        targets = []
        for entity in self.actors:
            targets.append(entity.get_surf(self.display, self.cam))
        self.display.blits(targets)

    def draw_hud(self, tick_portion_left):
        if self.player.fatigue:
            color = [255, 0, 0]
        else:
            color = [0, 255, 0]
        pygame.draw.rect(self.display, color, (0, 0, self.display.get_width()*(1-tick_portion_left), 50))
