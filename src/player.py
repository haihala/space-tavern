from entity import Entity

class Player(Entity):
    def __init__(self, binds):
        super().__init__(sprite="player_idle", speed=2)
        self.binds = binds
        self.jump_height = 3
        self.inventory = None

    def jump(self, engine):
        if self.grounded:
            self.move(engine, amount=self.jump_height, direction=[0, -1])

    def tick(self, engine, action):
        if super().tick():
            return None

        moved = False
        if action:
            self.fatigue += self.speed
            if action == "left":
                self.move(engine, direction=[-1, 0])
                moved = True
            elif action == "right":
                self.move(engine, direction=[1, 0])
                moved = True
            elif action == "jump":
                self.jump(engine)
                
        if not moved:
            self.gravity(engine)
