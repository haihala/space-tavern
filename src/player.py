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

    def throw(self, engine):
        engine.place(self.forwards, self.inventory)
        self.inventory.velocity = [int(self.facing_right)*2-1, -2]
        self.inventory = None
        from pygame_objects import SOUNDS
        SOUNDS["item_throw"].play()

    def pickup(self, engine):
        targets = []
        for i in [[i+self.position[0], j+self.position[1]] for i in range(-1, 2) for j in range(-1, 2)]:
            targets += engine.collides(point=i, target="item")

        if targets:
            target = targets.pop()
            self.inventory = target
            engine.items = [i for i in engine.items if i is not target]     # Remove item from the world
            from pygame_objects import SOUNDS
            SOUNDS["item_pickup"].play()
            return True

    @property
    def forwards(self):
        return [self.position[i] + [2*int(self.facing_right)-1, 0][i] for i in range(2)]

    def tick(self, engine, action):
        IsIdle = self.fatigue == 0

        if super().tick():
            return None

        moved = False
        from pygame_objects import SPRITES, SOUNDS
        if action:
            self.fatigue += self.speed
            if action == "left":
                if self._sprite != SPRITES["player_walk"]:
                    self.sprite_offset = 0
                self._sprite = SPRITES["player_walk"]
                self.move(engine, direction=[-1, 0])
                SOUNDS["player_move"].play()
                moved = True
            elif action == "right":
                if self._sprite != SPRITES["player_walk"]:
                    self.sprite_offset = 0
                self._sprite = SPRITES["player_walk"]
                self.move(engine, direction=[1, 0])
                SOUNDS["player_move"].play()
                moved = True
            elif action == "down":
                self._sprite = SPRITES["player_idle"]
            elif action == "jump":
                self.jump(engine)
            elif action == "use":
                if self.inventory:
                    self.inventory.on_use(self.inventory, engine, self)
                self.fatigue = 0
            elif action == "pickup":
                if self.inventory:
                    self.throw(engine)
                else:
                    if not self.pickup(engine):
                        # Nothing to pick up, no fatigue
                        self.fatigue = 0
        elif IsIdle:
            self._sprite = SPRITES["player_idle"]
        else:
            self.sprite_offset = self.sprite_offset - 1
        if not moved:
            self.gravity(engine)
