from player import Player

import pygame

from time import sleep, time

class Engine():
    def __init__(self, conf):
        self.tick_target_duration = 0.25
        self.tick = 0

        pygame.init()
        self.player = Player()

    def run(self):
        self.running = True
        while self.running:
            tick_start_time = time()
            for i in range(self.player.speed):
               self.player_tick()
            self.enemy_tick()
            self.physics()
            self.render()
            sleep(self.tick_target_duration-(time()-tick_start_time))
            self.tick += 1

    def player_tick(self):
        # Get player input, do that.
        pass

    def enemy_tick(self):
        # Player_tick, but for enemies
        pass

    def physics(self):
        # Make things fall mostly
        pass
            
    def render(self):
        # Draw the world
        self.draw_background()
        self.draw_world()
        self.draw_hud()

    def draw_background(self):
        pass
    
    def draw_world(self):
        # Collideable objects, player, non-collidables in that order.
        pass

    def draw_hud(self):
        pass


