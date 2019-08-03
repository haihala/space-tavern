from entity import Entity

class Player(Entity):
    def __init__(self):
        super().__init__()
        self.speed = 1
        self.buffered = None
        self.binds = {}

