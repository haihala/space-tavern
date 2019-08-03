from entity import Entity

class Player(Entity):
    def __init__(self, binds):
        super().__init__(speed=2)
        self.buffered = None
        self.binds = binds

    def tick(self, engine, action):
        if super().tick(engine):
            return None
