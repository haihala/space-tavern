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
        
        self.tick_target_duration = 0.25
        self.running = False

    @property
    def room(self):
        return self.rooms[self.current_room]

    def run(self):
        self.running = True
        while self.running:
            for entity in self.actors:
                print(entity.position)
                if entity == self.player:
                    self.player_tick()
                else:
                    entity.tick(self)
            self.render()

    def quit(self):
        # Maybe save
        exit(0)

    def player_tick(self):
        start_time = time()
        self.player.buffered = None
        while time() - start_time < self.tick_target_duration * 0.8:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.unicode in self.player.binds:
                        self.player.buffered = self.player.binds[event.unicode]
        self.player.tick(self, self.player.buffered)
            
    def render(self):
        # Draw the world
        self.draw_background()
        self.draw_world()
        self.draw_hud()
        pygame.display.flip()

    def draw_background(self):
        self.room.draw(self.display, (0, 0))
    
    def draw_world(self):
        # Collideable objects, player, non-collidables in that order.
        pass

    def draw_hud(self):
        pass


