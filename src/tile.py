from entity import Entity

class Tile(Entity):
    def __init__(self, position, sprite, **kwargs):
        super().__init__(position=position, sprite=sprite, **kwargs)

