from entity import Entity

class Enemy(Entity):
    def __init__(self, ai, sprite, position, **kwargs):
        super().__init__(sprite, position, **kwargs)
        self.ai = ai

    def tick(self, engine):
        if super().tick():
            return None
        self.ai(self, engine)
        self.upkeep(engine)
