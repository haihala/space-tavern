
class Entity():
    # Abstract
    def __init__(self, position=[0,0], weight=1, speed=1, width=1, height=1, fatigue=0):
        self.weight = weight
        self.position = position
        self.speed = speed
        self.fatigue = fatigue
        self.width = width
        self.height = height

    @property
    def colliders(self):
        return [[self.position[0]+i, self.position[1]+j] for i in range(self.width) for j in range(self.height)]

    def tick(self, engine):
        self.fatigue = max(0, self.fatigue-1)+self.speed
        collision_targets = [j for k in [i.colliders for i in engine.actors] + [i.colliders for i in engine.room.tiles] for j in k]
        print(collision_targets)

        for i in range(self.weight):
            newy = self.position[1] + 1
            if not any([self.position[0]+j, newy] in collision_targets for j in range(self.width)):
                self.position = [self.position[0], newy]

        return self.fatigue != self.speed
