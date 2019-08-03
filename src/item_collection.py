from item import Item

def drop(self, engine, user):
    if engine.place(user, self):
        user.inventory = None

def jump_pad_collision(self, engine, user):
    user.move(engine, amount=5, direction=[0, -1])

def create_collection():

    def item_beer(position, **kwargs):
        sprite = "item_beer"
        return Item(position, sprite, drop, **kwargs)

    def item_jump_pad(position, **kwargs):
        sprite = "item_jump_pad"
        return Item(position, sprite, jump_pad_collision, drop, **kwargs)

    def item_door(position, **kwargs):
        sprite = "item_door"
        return Item(position, sprite, **kwargs)

    return  {

            "item_beer": item_beer,
            "item_jump_pad": item_beer,
            "item_door": item_beer,

            }

ITEMS = create_collection()
