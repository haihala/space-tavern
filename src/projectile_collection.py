from entity import Entity

def bullet_hit(self, engine, target):
    self.dead = True
    target.hurt(engine, 1)

def create_collection():
    def projectile_gun(position, **kwargs):
        sprite = "projectile_gun"
        return Entity(position=position, sprite=sprite, on_collision=bullet_hit, collider=False, weight=0, **kwargs)

    return  {
            "projectile_gun": projectile_gun
            }

PROJECTILES = create_collection()
