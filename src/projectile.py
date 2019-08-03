from entity import Entity

class Projectile(Entity):
    def __init__(self, on_hit, **kwargs):
        super().__init__(**kwargs)
        if "drag" in kwargs:
            self.drag = kwargs["drag"]
        else:
            self.drag = 0

        self.on_hit = on_hit

