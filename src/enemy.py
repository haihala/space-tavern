from entity import Entity

class Enemy(Entity):
    def __init__(self, ai, sprite, position, **kwargs):
        super().__init__(sprite, position, **kwarks)
        self.ai = ai

    def tick(self, engine):
        if super().tick(engine):
            return None
        self.ai(engine)

        self.gravity(engine)
