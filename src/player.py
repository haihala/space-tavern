from entity import Entity
from item_collection import ITEMS

class Player(Entity):
    def __init__(self, binds):
        super().__init__(sprite="player_idle", health=3)
        self.binds = binds
        self.jump_height = 3
        self.inventory = None
        self.sprite_updated = True

    def jump(self, engine):
        if self.grounded:
            self.move(engine, amount=self.jump_height, direction=[0, -1])

    def throw(self, engine):
        if engine.place(self.forwards, self.inventory):
            self.inventory.velocity = [int(self.facing_right)*2-1, -2]
        elif engine.place(self.up, self.inventory):
            self.inventory.velocity = [0, -3]
        self.inventory = None
        from pygame_objects import SOUNDS
        SOUNDS["item_throw"].play()


    def pickup(self, engine):
        targets = []
        for i in [[i+self.position[0], j+self.position[1]] for i in range(-1, 2) for j in range(-1, 2)]:
            targets += engine.collides(point=i, target="pickup")

        if targets:
            target = targets.pop()
            if "item" in target.data:
                if engine.money >= target.data["cost"]:
                    if target.data["itemcount"] != 0:
                        self.inventory = ITEMS[target.data["item"]](self.position)
                        engine.money -= target.data["cost"]
                        if target.data["itemcount"] != None:
                            target.data["itemcount"] -= 1
                else:
                    return False
            else:
                self.inventory = target
                engine.entities = [i for i in engine.entities if i is not target]     # Remove item from the world
                from pygame_objects import SOUNDS
                SOUNDS["item_pickup"].play()
            return True

    def tick(self, engine, action):
        IsIdle = self.fatigue == 0
        if self.inventory:
            self.inventory.tick(engine)

        if super().tick(engine):
            return None

        moved = False
        from pygame_objects import SPRITES, SOUNDS
        if action:
            self.fatigue += self.speed
            if action == "left":
                if self._sprite != SPRITES["player_walk"]:
                    self.sprite_offset = 0
                self._sprite = SPRITES["player_walk"]
                SOUNDS["player_move"].play()
                engine.camera_shake(1)
                self.move(engine, direction=[-1, 0])
                moved = True
            elif action == "right":
                if self._sprite != SPRITES["player_walk"]:
                    self.sprite_offset = 0
                self._sprite = SPRITES["player_walk"]
                SOUNDS["player_move"].play()
                engine.camera_shake(1)
                self.move(engine, direction=[1, 0])
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
        self.handle_velocity(engine)

        if abs(self.position[0]) > engine.ship_width:
            engine.target_cam = [self.position[0], 0]
        else:
            engine.target_cam = [0, 0]
