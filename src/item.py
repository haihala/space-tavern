from entity import Entity

class Item(Entity):
    def __init__(self, position, sprite, on_collision=None, on_use=None, can_pickup=True, collider=False, **kwargs):
        super().__init__(position=position, sprite=sprite, **kwargs)
        self.can_pickup = can_pickup
        self.collider = collider
        self.on_collision = on_collision
        self.on_use = on_use

    def tick(self, engine):
        if super().tick():
            return None

        self.gravity(engine)
