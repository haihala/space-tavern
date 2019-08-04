from entity import Entity

class Enemy(Entity):
    def __init__(self, ai, sprite, position, weight, speed, **kwargs):
        super().__init__(sprite, position, weight, speed, **kwargs)
        self.ai = ai

    def tick(self, engine):
        if super().tick():
            self.handle_velocity()
            self.gravity(engine)
            return None
        self.ai(self, engine)
        self.upkeep(engine)
