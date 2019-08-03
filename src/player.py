from entity import Entity

def sign(x):
    if x != 0:
        return x/abs(x)
    return 0

class Player(Entity):
    def __init__(self, binds):
        super().__init__(sprite="wall", speed=2)
        self.binds = binds
        self.jump_height = 3

    def jump():
        if self.grounded:
            move(direction=[0, -3])

    def tick(self, engine, action):
        if super().tick(engine):
            return None

        if action:
            self.fatigue += self.speed
            if action == "left":
                self.move(direction=[-1, 0])
            elif action == "right":
                self.move(direction=[1, 0])
            elif action == "jump":
                self.jump()
