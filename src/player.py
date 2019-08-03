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

    def throw(self, engine):
        spot = [self.position[i] + [0, -1][i] for i in range(2)]
        engine.place(spot, self.inventory)
        self.inventory = None

    def pickup(self, engine):
        targets = []
        for i in [[i+self.position[0], j+self.position[1]] for i in range(-1, 2) for j in range(-1, 2)]:
            targets += engine.collides(point=i, types=["item"])

        if targets:
            target = targets.pop()
            self.inventory = target
            engine.items = [i for i in engine.items if i is not target]     # Remove item from the world
            return True

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
            elif action == "down":
                pass
            elif action == "jump":
                self.jump(engine)
            elif action == "use":
                if self.inventory:
                    self.inventory.on_use(engine, self)
            elif action == "pickup":
                if self.inventory:
                    self.throw(engine)
                else:
                    if not self.pickup(engine):
                        # Nothing to pick up, no fatigue
                        self.fatigue = 0

                
        if not moved:
            self.gravity(engine)
