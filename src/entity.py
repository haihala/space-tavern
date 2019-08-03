
class Entity():
    # Abstract
    def __init__(self, position=(0,0), weight=1, speed=1, fatigue=0):
        self.weight = weight
        self.position = position
        self.speed = speed
        self.fatigue = fatigue

    def tick(self, engine):
        self.fatigue = max(0, self.fatigue-1)+self.speed
        collision_targets = [i.position for i in engine.actors] + [i.position for i in engine.room.tiles]

        for i in range(self.weight):
            newpos = list(self.position[:])
            newpos[1] += 1
            if newpos not in collision_targets:
                self.position = newpos

        return self.fatigue != self.speed
