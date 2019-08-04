from item import Item
from tile import Tile
from projectile_collection import PROJECTILES

from random import choice

def drop(self, engine, user):
    self.position = user.forwards
    self.old_position = user.forwards
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

def stop_time(self, engine, user):
    user.inventory = None
    for i in engine.entities:
        if i is not user:
            i.fatigue += 20

def speed_up(self, engine, user):
    user.inventory = None
    user.speed = max(1, user.speed-1)

def heal(self, engine, user):
    user.inventory = None
    user.health += 2
    from pygame_objects import SOUNDS
    SOUNDS["player_heal"].play()

def explode(self, engine, user):

    from pygame_objects import SOUNDS
    SOUNDS["entity_die"].play()

    points = []
    for i in range(-1, 3):
        for j in range(-1, 3):
            points.append([self.position[0]+i, self.position[1]+j])

    for point in points:
        tgt = engine.collides(point=point, target="entity")
        for t in tgt:
            t.hurt(self, 2)
    self.dead = True

def sell_collision(self, engine, user):
    from pygame_objects import SPRITES
    if user._sprite == SPRITES["item_beer"]:
        engine.entities = [entity for entity in engine.entities if entity != user]
        engine.money = engine.money + (5 if user.data["planet"] == engine.planet else 10)
        from pygame_objects import SOUNDS
        SOUNDS["player_buy"].play()

SHOP_CATALOG = {
        "gun": {
            "name": "item_gun",
            "count": 1,
            "cost": 20
            },
        "jump_pad": {
            "name": "item_jump_pad",
            "count": 1,
            "cost": 30
            },
        "heal": {
            "name": "item_heal",
            "count": 3,
            "cost": 5
            },
        "warudo": {
            "name": "item_warudo",
            "count": 1,
            "cost": 40
            },
        "mine": {
            "name": "item_mine",
            "count": 2,
            "cost": 10
            },
        "adrenaline": {
            "name": "item_adrenaline",
            "count": 1,
            "cost": 60
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
        return Item(position, sprite, on_use=drop, collider=True, health=2, collision_damage=1, **kwargs)

    def item_warudo(position, **kwargs):
        sprite = "item_warudo"
        return Item(position, sprite, on_use=stop_time, **kwargs)

    def item_adrenaline(position, **kwargs):
        sprite = "item_syringe"
        return Item(position, sprite, on_use=speed_up, **kwargs)

    def item_jump_pad(position, **kwargs):
        sprite = "item_jump_pad"
        return Item(position, sprite, on_collision=jump_pad_collision, on_use=drop, can_pickup=False, weight=1, **kwargs)

    def item_gun(position, **kwargs):
        sprite = "item_gun"
        return Item(position, sprite, on_use=gun_shoot, speed=6, **kwargs)

    def item_heal(position, **kwargs):
        sprite = "item_heal"
        return Item(position, sprite, on_use=heal, **kwargs)

    def item_mine(position, **kwargs):
        sprite = "item_mine"
        return Item(position, sprite, can_pickup=False, on_collision=explode, on_use=drop, weight=1, **kwargs)

    def item_shop(position, item=None, **kwargs):
        sprite = "item_shop"
        i = SHOP_CATALOG[choice([product for product in SHOP_CATALOG.keys() if product != "box"])] if not item else SHOP_CATALOG[item]
        return Item(position, sprite, data={"item": i["name"], "itemcount": i["count"], "cost": i["cost"]}, collider=False, sprite_updated=True, **kwargs)

    def item_console(position, **kwargs):
        sprite = "item_console"
        return Item(position, sprite, data={"console": True}, collider=False, **kwargs)

    def item_sell(position, **kwargs):
        sprite = "item_sell"
        return Item(position, sprite, collider=False, on_collision=sell_collision, **kwargs)

    return  {
            "item_beer": item_beer,
            "item_jump_pad": item_jump_pad,
            "item_gun": item_gun,
            "item_warudo": item_warudo,
            "item_heal": item_heal,
            "item_mine": item_mine,
            "item_adrenaline": item_adrenaline,

            "item_shop": item_shop,
            "item_sell": item_sell,
            "item_console": item_console,
            }

ITEMS = create_collection()
