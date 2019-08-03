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

    def move(self, amount=1, target=None, direction=None):
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

            self.position = [self.position[0]+delta[0], self.position[1]+delta[1]]

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
