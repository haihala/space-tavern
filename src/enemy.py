from entity import Entity

class Enemy(Entity):
    def __init__(self, ai, sprite, position, weight, speed, collision_damage=1, **kwargs):
        super().__init__(sprite, position, weight, speed, collision_damage=collision_damage, **kwargs)
        self.ai = ai

    def tick(self, engine):
        if super().tick(engine):
            self.handle_velocity(engine)
            self.gravity(engine)
            return None
        self.ai(self, engine)
        self.upkeep(engine)
