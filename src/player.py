from entity import Entity

class Player(Entity):
    def __init__(self, binds):
        super().__init__(sprite="player_idle", speed=2)
        self.binds = binds
        self.jump_height = 3
        self.inventory = None

    def jump(self, engine):
        if self.grounded:
            self.move(engine, amount=self.jump_height, direction=[0, -1])

    def tick(self, engine, action):
        IsIdle = self.fatigue == 0

        if super().tick():
            return None

        moved = False
        from pygame_objects import SPRITES
        if action:
            self.fatigue += self.speed
            if action == "left":
                if self._sprite != SPRITES["player_walk"]:
                    self.sprite_offset = 0
                self._sprite = SPRITES["player_walk"]
                self.move(engine, direction=[-1, 0])
                moved = True
            elif action == "right":
                if self._sprite != SPRITES["player_walk"]:
                    self.sprite_offset = 0
                self._sprite = SPRITES["player_walk"]
                self.move(engine, direction=[1, 0])
                moved = True
            elif action == "jump":
                self.jump(engine)
            elif action == "down":
                self._sprite = SPRITES["player_idle"]
        elif IsIdle:
            self._sprite = SPRITES["player_idle"]
        else:
            self.sprite_offset = self.sprite_offset - 1

        if not moved:
            self.gravity(engine)
