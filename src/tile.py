from constants import TILESIZE, TILE_SPRITES
from entity import Entity

class Tile(Entity):
    def __init__(self, position, spritename):
        self.position = position
        self.sprite = TILE_SPRITES[spritename]

    def get_surf(self, surface, camera):
        offset = [(self.position[i] - camera[i] - 0.5)*TILESIZE for i in range(2)]
        position = [offset[i]+surface.get_size()[i] for i in range(2)]

        return (self.sprite, self.position)


