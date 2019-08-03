from entity import Entity

class Player(Entity):
    def __init__(self, binds):
        super().__init__(sprite="player_idle", speed=2)
        self.binds = binds
        self.jump_height = 3

    def jump(self):
        if self.grounded:
            self.move(engine, amount=self.jump_height, direction=[0, -1])

    def tick(self, engine, action):
        if super().tick(engine):
            return None

        if action:
            self.fatigue += self.speed
            if action == "left":
                self.move(engine, direction=[-1, 0])
            elif action == "right":
                self.move(engine, direction=[1, 0])
            elif action == "jump":
                self.jump()
