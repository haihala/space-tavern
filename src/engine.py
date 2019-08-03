from player import Player
from room import Room

import pygame

from time import sleep, time

class Engine():
    def __init__(self, conf):
        flags = (pygame.FULLSCREEN * int(conf["fullscreen"]))
        self.display = pygame.display.set_mode(conf["resolution"], flags)

        self.player = Player(conf["binds"])
        self.actors = [self.player] 
        self.rooms = {
                room["name"]: Room(**room)
                for room in conf["rooms"]
                }
        self.current_room = "ship"
        
        self.tick_target_duration = 1
        self.cam = [0,0]
        self.running = False
        self._collidables = None

    @property
    def room(self):
        return self.rooms[self.current_room]

    @property
    def collidables(self):
        if not self._collidables:
            self._collidables = [j for k in [i.colliders for i in self.actors] + [i.colliders for i in self.room.tiles] for j in k]
        return self._collidables

    def collides(self, target):
        return self.collidables.count(target) > 1

    def run(self):
        self.running = True
        while self.running:
            self._collidables = None
            for entity in self.actors:
                if entity == self.player:
                    self.player_tick(self.tick_target_duration)
                else:
                    entity.tick(self)
            for entity in self.actors:
                entity.grounded = any(self.collides([i[0], i[1]+1]) for i in entity.colliders)

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
                        if event.unicode in self.player.binds:
                            buffered = self.player.binds[event.unicode]

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

