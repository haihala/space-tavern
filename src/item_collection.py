from item import Item

def drop(self, engine, user):
    if engine.place(user.forwards, self):
        from pygame_objects import SOUNDS
        SOUNDS["item_drop"].play()
        user.inventory = None

def jump_pad_collision(self, engine, user):
    user.move(engine, amount=5, direction=[0, -1])

def create_collection():
    def item_beer(position, **kwargs):
        sprite = "item_beer"
        return Item(position, sprite, on_use=drop, collider=True, **kwargs)

    def item_jump_pad(position, **kwargs):
        sprite = "item_jump_pad"
        return Item(position, sprite, on_collision=jump_pad_collision, on_use=drop, **kwargs)

    def item_door(position, **kwargs):
        sprite = "item_door"
        return Item(position, sprite, collider=True, can_pickup=False, **kwargs)

    def item_gun(position, **kwargs):
        sprite = "item_gun"
        return Item(position, sprite, **kwargs)

    return  {
            "item_beer": item_beer,
            "item_jump_pad": item_jump_pad,
            "item_door": item_door,
            "item_gun": item_gun
            }

ITEMS = create_collection()
