from item import Item
from tile import Tile
from projectile_collection import PROJECTILES

def drop(self, engine, user):
    self.position = user.forwards
    if engine.place(self):
        user.inventory = None
        from pygame_objects import SOUNDS
        SOUNDS["item_drop"].play()

def jump_pad_collision(self, engine, user):
    if type(user) is not Tile and self != user:
        user.move(engine, amount=engine.ship_height*2-3, direction=[0, -1])
        self.sprite_offset = 1

def gun_shoot(self, engine, user):
    if not self.fatigue:
        bullet = PROJECTILES["projectile_gun"](user.forwards)

        bullet.position = user.forwards
        if engine.place(bullet, target="tile"):
            bullet.velocity = [int(user.facing_right)*2-1, 0]
            bullet.facing_right = user.facing_right
            self.fatigue += self.speed

SHOP_CATALOG = {
        "gun": {
            "name": "item_gun",
            "count": 1,
            "cost": 20
            },
        "box": {
            "name": "item_beer",
            "count": None,
            "cost": 5
            }
        }

def create_collection():
    def item_beer(position, **kwargs):
        sprite = "item_beer"
        return Item(position, sprite, on_use=drop, collider=True, collision_damage=1, **kwargs)

    def item_jump_pad(position, **kwargs):
        sprite = "item_jump_pad"
        return Item(position, sprite, on_collision=jump_pad_collision, on_use=drop, weight=1, **kwargs)

    def item_gun(position, **kwargs):
        sprite = "item_gun"
        return Item(position, sprite, on_use=gun_shoot, speed=6, **kwargs)

    def item_shop(position, item, **kwargs):
        sprite = "item_shop"
        i = SHOP_CATALOG[item]
        return Item(position, sprite, data={"item": i["name"], "itemcount": i["count"], "cost": i["cost"]}, collider=False, **kwargs)

    return  {
            "item_beer": item_beer,
            "item_jump_pad": item_jump_pad,
            "item_gun": item_gun,
            "item_shop": item_shop
            }

ITEMS = create_collection()
