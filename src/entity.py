from constants import TILESIZE

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

    def sprite(self, i=0):
        if type(self._sprite) is list:
            return self._sprite[i%len(self._sprite)]
        return self._sprite

    @property
    def colliders(self):
        return [[self.position[0]+i, self.position[1]+j] for i in range(self.width) for j in range(self.height)]

    def tick(self, engine):
        self.fatigue = max(0, self.fatigue-1)
        collision_targets = [j for k in [i.colliders for i in engine.actors] + [i.colliders for i in engine.room.tiles] for j in k]

        for i in range(self.weight):
            newy = self.position[1] + 1
            if not any([self.position[0]+j, newy] in collision_targets for j in range(self.width)):
                self.position = [self.position[0], newy]

        return self.fatigue != 0

    def get_surf(self, surface, camera, i=0):
        sprite = self.sprite(i)
        offset = [(self.position[i] - camera[i])*TILESIZE - 0.5*sprite.get_size()[i] for i in range(2)]
        position = [int(offset[i]+surface.get_size()[i]/2) for i in range(2)]

        return (sprite, position)
