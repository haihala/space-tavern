from constants import TILESIZE, LERP
import pygame

def sign(x):
    if x != 0:
        return x/abs(x)
    return 0

class Entity():
    # Abstract
    def __init__(self, sprite, position=[0,0], weight=1, speed=2, width=1, height=1, fatigue=0, drag=0.3):
        from pygame_objects import SPRITES
        self._sprite = SPRITES[sprite]
        self.sprite_offset = 0
        self.weight = weight
        self.position = position
        self.old_position = position[:]
        self.speed = speed-1
        self.fatigue = fatigue
        self.width = width
        self.height = height
        self.facing_right = False

        self.velocity = [0, 0]
        self.drag = drag
        self.grounded = False
        self.grounded_last_tick = False # Internal mechanic to slow down gravity and give hang time in the air.

    def move(self, engine, amount=1, target=None, direction=None):
        if target and direction:
            raise ValueError("Both, direction and target passed to move")
        for i in range(amount):
            if target and not direction:
                direction = [target[i]-self.position[i] for i in range(2)]

            if direction[0] > 0:
                self.facing_right = True
            elif direction[0] < 0:
                self.facing_right = False

            delta = [i/(direction[0]**2+direction[1]**2) for i in direction]
            if abs(delta[0]) > abs(delta[1]):
                delta = [sign(delta[0]), 0]
            else:
                delta = [0, sign(delta[1])]

            if engine.project_collides(self, delta):
                self.velocity = [0, 0]
                return amount-i
            else:
                self.position = [self.position[i] + delta[i] for i in range(2)]

    def sprite(self):
        if type(self._sprite) is list:
            if self.facing_right:
                return pygame.transform.flip(self._sprite[self.sprite_offset%len(self._sprite)], True, False)
            else:
                return self._sprite[self.sprite_offset%len(self._sprite)]
        return self._sprite

    @property
    def colliders(self):
        return [[self.position[0]+i, self.position[1]+j] for i in range(self.width) for j in range(self.height)]

    def tick(self):
        self.fatigue = max(0, self.fatigue-1)
        self.sprite_offset = self.sprite_offset+1
        return self.fatigue != 0

    def upkeep(self, engine):
        self.handle_velocity(engine)
        self.gravity(engine)
        self.fatigue += self.speed

    def handle_velocity(self, engine):
        if self.velocity != [0, 0]:
            x, y = self.velocity
            self.move(engine, amount=abs(int(y)), direction=[0, y])
            self.move(engine, amount=abs(int(x)), direction=[x, 0])
            self.velocity = [
                    x,
                    max(0, abs(y-sign(y)*self.drag))*sign(y)
                    ]
            if self.velocity[1] == 0:
                self.velocity = [0, 0]
    def gravity(self, engine):
        if not self.grounded and not self.grounded_last_tick:
            self.move(engine, amount=self.weight, direction=[0,1])
        self.grounded_last_tick = self.grounded

    def get_surf(self, surface, camera):
        sprite = self.sprite()
        self.old_position = [LERP(self.old_position[i], self.position[i], 0.1) for i in range(2)]
        offset = [(self.old_position[i] - camera[i])*TILESIZE - 0.5*sprite.get_size()[i] for i in range(2)]
        position = [int(offset[i]+surface.get_size()[i]/2) for i in range(2)]

        return (sprite, position)
