from constants import TILESIZE, LERP
from constants import GROUND_LEVEL

import pygame

def sign(x):
    if x != 0:
        return x/abs(x)
    return 0

class Entity():
    # Abstract
    def __init__(self, sprite="transparent", position=[0,0], weight=1, speed=2, width=1, height=1, fatigue=0, drag=0.7, health=None, on_collision=None, on_use=None, on_death=None, jump_height=0, collision_damage=0, collider=True, data={}, sprite_updated=False):
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
        self.drag = drag
        self.health = health
        self.on_collision = on_collision
        self.on_use = on_use
        self.on_death = on_death
        self.jump_height = jump_height
        self.collision_damage = collision_damage
        self.collider = collider
        self.data = data
        self.sprite_updated = sprite_updated

        self.velocity = [0, 0]
        self.dead = False
        self.grounded = False
        self.grounded_last_tick = False # Internal mechanic to slow down gravity and give hang time in the air.
        self.facing_right = False

    def move(self, engine, amount=1, target=None, direction=None):
        if not (self in engine.entities):
            return None

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

            colgroup = engine.project_collides(entity=self, shift=delta, exclude=[self])

            if colgroup:
                for ent in colgroup:
                    if ent.on_collision:
                        ent.on_collision(ent, engine, self)
                    elif (self.velocity != [0, 0] or "enemy" in str(type(self))) and "item" not in str(type(ent)):
                        ent.hurt(engine, self.collision_damage)
                    from tile import Tile
                    if self.on_collision and type(ent) != Tile:
                        self.on_collision(self, engine, ent)
                    elif (ent.velocity != [0, 0] or "enemy" in str(type(ent))) and "item" not in str(type(self)):
                        self.hurt(engine, ent.collision_damage)
                self.velocity = [0, 0]
                return amount-i
            else:
                self.position = [self.position[i] + delta[i] for i in range(2)]
        self.grounded = engine.project_collides(self, [0,1], exclude=[self])

    @property
    def up(self):
        return [self.position[i] + [0, -1][i] for i in range(2)]
    @property
    def down(self):
        return [self.position[i] + [0, self.height][i] for i in range(2)]
    @property
    def left(self):
        return [self.position[i] + [-1, 0][i] for i in range(2)]
    @property
    def right(self):
        return [self.position[i] + [self.width, 0][i] for i in range(2)]

    @property
    def back(self):
        if self.facing_right:
            return self.left
        else:
            return self.right

    @property
    def forwards(self):
        if not self.facing_right:
            return self.left
        else:
            return self.right

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

    def tick(self, engine):
        self.position = [self.position[0], min(self.position[1], GROUND_LEVEL)]
        self.fatigue = max(0, self.fatigue-1)
        self.sprite_offset = (self.sprite_offset+1 if self.sprite_updated else 0)
        active = self.fatigue != 0
        if type(self) is Entity:
            self.upkeep(engine, False)
            if self.velocity == [0, 0]:
                self.dead = True
        return active

    def upkeep(self, engine, fatigue=True):
        self.handle_velocity(engine)
        self.gravity(engine)
        if fatigue:
            self.fatigue += self.speed

    def handle_velocity(self, engine):
        if self.velocity != [0, 0]:
            x, y = self.velocity
            self.move(engine, amount=abs(int(y)), direction=[0, y])
            self.move(engine, amount=abs(int(x)), direction=[x, 0])
            if self.drag != 0:
                self.velocity = [
                        x if not self.grounded else max(0, x-sign(x)*self.drag)*sign(x),
                        max(0, y-sign(y)*self.drag)*sign(y)
                        ]
    def gravity(self, engine):
        if not self.grounded and not self.grounded_last_tick:
            self.move(engine, amount=self.weight, direction=[0,1])
        self.grounded_last_tick = self.grounded

    def get_surf(self, surface, camera):
        sprite = self.sprite()
        #self.old_position = [LERP(self.old_position[i], self.position[i], 0.1) for i in range(2)]
        offset = [(self.old_position[i] - camera[i] - 0.5)*TILESIZE for i in range(2)]
        position = [int(offset[i]+surface.get_size()[i]/2) for i in range(2)]

        return (sprite, position)

    def hurt(self, engine, amount):
        if self.health is None:
            return
        from pygame_objects import SOUNDS
        SOUNDS["player_damage"]

        self.health -= amount
        if self.health <= 0:

            SOUNDS["entity_die"].play()
            self.dead = True
