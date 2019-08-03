from item import Item

def create_collection():

    def item_beer(position, **kwargs):
        sprite = "item_beer"
        on_collision = None
        on_use = None
        return Item(position, sprite, on_collision, on_use, **kwargs)

    def item_jump_pad(position, **kwargs):
        sprite = "item_jump_pad"
        on_collision = None
        on_use = None
        return Item(position, sprite, on_collision, on_use, **kwargs)

    def item_door(position, **kwargs):
        sprite = "item_door"
        on_collision = None
        on_use = None
        return Item(position, sprite, on_collision, on_use, **kwargs)

    return  {

            "item_beer": item_beer,
            "item_jump_pad": item_beer,
            "item_door": item_beer,

            }

ITEMS = create_collection()
