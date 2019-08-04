from item import Item
from tile import Tile
from projectile_collection import PROJECTILES

def drop(self, engine, user):
    if engine.place(user.forwards, self):
        user.inventory = None
        from pygame_objects import SOUNDS
        SOUNDS["item_drop"].play()

def jump_pad_collision(self, engine, user):
    if type(user) is not Tile and self != user:
        user.move(engine, amount=5, direction=[0, -1])

def gun_shoot(self, engine, user):
    if not self.fatigue:
        bullet = PROJECTILES["projectile_gun"](user.forwards)

        if engine.place(user.forwards, bullet): 
            bullet.velocity = [int(user.facing_right)*2-1, 0]
            self.fatigue += self.speed

def create_collection():
    def item_beer(position, **kwargs):
        sprite = "item_beer"
        return Item(position, sprite, on_use=drop, collider=True, collision_damage=1, **kwargs)

    def item_jump_pad(position, **kwargs):
        sprite = "item_jump_pad"
        return Item(position, sprite, on_collision=jump_pad_collision, on_use=drop, weight=1, **kwargs)

    def item_door(position, **kwargs):
        sprite = "item_door"
        return Item(position, sprite, collider=True, can_pickup=False, **kwargs)

    def item_gun(position, **kwargs):
        sprite = "item_gun"
        return Item(position, sprite, on_use=gun_shoot, speed=6, **kwargs)

    return  {
            "item_beer": item_beer,
            "item_jump_pad": item_jump_pad,
            "item_door": item_door,
            "item_gun": item_gun
            }

ITEMS = create_collection()
