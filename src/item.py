from entity import Entity

class Item(Entity):
    def __init__(self, position, sprite, can_pickup=True, collider=False, **kwargs):
        super().__init__(position=position, sprite=sprite, collider=collider, **kwargs)
        self.can_pickup = can_pickup

    def tick(self, engine):
        if super().tick(engine):
            return None

        self.handle_velocity(engine)
        self.gravity(engine)

