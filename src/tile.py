from constants import TILESIZE
from entity import Entity

class Tile(Entity):
    def __init__(self, position, spritename):
        super().__init__(position=position)
        from pygame_objects import TILE_SPRITES
        self.position = position
        self.sprite = TILE_SPRITES[spritename]

    def get_surf(self, surface, camera):
        offset = [(self.position[i] - camera[i] - 0.5)*TILESIZE for i in range(2)]
        position = [int(offset[i]+surface.get_size()[i]/2) for i in range(2)]

        return (self.sprite, position)


