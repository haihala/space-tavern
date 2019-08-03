from constants import TILESIZE

def sign(x):
    if x != 0:
        return x/abs(x)
    return 0

class Entity():
    # Abstract
    def __init__(self, sprite, position=[0,0], weight=1, speed=1, width=1, height=1, fatigue=0):
        from pygame_objects import SPRITES
        self._sprite = SPRITES[sprite]
        self.weight = weight
        self.position = position
        self.speed = speed
        self.fatigue = fatigue
        self.width = width
        self.height = height

        self.grounded = False
        self.grounded_last_tick = False # Internal mechanic to slow down gravity and give hang time in the air.

    def move(self, engine, amount=1, target=None, direction=None):
        if target and direction:
            raise ValueError("Both, direction and target passed to move")
        for i in range(amount):
            if target and not direction:
                direction = [target[i]-self.position[i] for i in range(2)]

            delta = [i/(direction[0]**2+direction[1]**2) for i in direction]
            if abs(delta[0]) > abs(delta[1]):
                delta = [sign(delta[0]), 0]
            else:
                delta = [0, sign(delta[1])]

            if engine.project_collides(self, shift=delta):
                return amount-i

    def sprite(self, i=0):
        if type(self._sprite) is list:
            return self._sprite[i%len(self._sprite)]
        return self._sprite

    @property
    def colliders(self):
        return [[self.position[0]+i, self.position[1]+j] for i in range(self.width) for j in range(self.height)]

    def tick(self):
        self.fatigue = max(0, self.fatigue-1)
        return self.fatigue != 0

    def gravity(self, engine):
        if not self.grounded and not self.grounded_last_tick:
            self.move(engine, amount=self.weight, direction=[0,1])
        self.grounded_last_tick = self.grounded

    def get_surf(self, surface, camera, i=0):
        sprite = self.sprite(i)
        offset = [(self.position[i] - camera[i])*TILESIZE - 0.5*sprite.get_size()[i] for i in range(2)]
        position = [int(offset[i]+surface.get_size()[i]/2) for i in range(2)]

        return (sprite, position)
