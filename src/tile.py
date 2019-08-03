from constants import TILESIZE
from entity import Entity
from sprites import tile_sprites

class Tile(Entity):
    def __init__(self, position, spritename, hard):
        self.position = position
        self.sprite = tile_sprites[spritename]
        self.hard = hard        # Collidable?

    def tick(self):
        pass

    def get_surf(self, surface, camera):
        offset = [(self.position[i] - camera[i] - 0.5)*TILESIZE for i in range(2)]
        position = [offset[i]+surface.get_size()[i] for i in range(2)]

        return (self.sprite, self.position)


