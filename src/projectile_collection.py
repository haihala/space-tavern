from entity import Entity

def bullet_hit(self, engine, target):
    self.dead = True
    target.hurt(engine, 1)

def create_collection():
    def projectile_gun(position, **kwargs):
        sprite = "projectile_gun"
        return Entity(position=position, sprite=sprite, on_collision=bullet_hit, collider=False, drag=0, weight=0, **kwargs)

    def projectile_alien(position, **kwargs):
        sprite = "projectile_alien"
        return Entity(position=position, sprite=sprite, on_collision=bullet_hit, collider=False, drag=0, weight=0, **kwargs)

    def projectile_alien_down(position, **kwargs):
        sprite = "projectile_alien_down"
        return Entity(position=position, sprite=sprite, on_collision=bullet_hit, collider=False, drag=0, weight=0, **kwargs)
    return  {
            "projectile_gun": projectile_gun,
            "projectile_alien": projectile_alien,
            "projectile_alien_down": projectile_alien_down
            }

PROJECTILES = create_collection()
