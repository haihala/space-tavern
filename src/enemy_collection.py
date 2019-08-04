from enemy import Enemy
from projectile_collection import PROJECTILES

from random import choice, getrandbits

def bat_shoot(self, engine):
    if not self.fatigue:
        bullet = PROJECTILES["projectile_alien_down"](self.down)

        if engine.place(self.down, bullet, target="tile"):
            bullet.velocity = [0, 1]
            self.fatigue += self.speed

def create_collection():
    def alien_base(position, **kwargs):
        def ai_base(self, engine):
            if engine.player.position[1] < self.position[1] and self.grounded:
                direction = [0, -1]
                self.move(engine, direction=direction, amount=self.jump_height)
            elif engine.player.position[0] != self.position[0]:
                direction = [1 if engine.player.position[0] > self.position[0] else -1, 0]
                self.move(engine, direction=direction, amount=1)
            # Shoot
        return Enemy(ai_base, "alien_base", position, 1, 4, health=1, **kwargs)

    def alien_fly(position, **kwargs):
        def ai_fly(self, engine):
            if self.position[0] == engine.player.position[0]:
                bat_shoot(self, engine)
            elif self.move(engine, amount=1, direction=[int(self.facing_right)*2-1, 0]):
                if self.move(engine, amount=1, direction=[0, -1]):
                    self.facing_right = not self.facing_right
                    if self.move(engine, amount=1, direction=[int(self.facing_right)*2-1, 0]):
                        self.dead = True

        return Enemy(ai_fly, "alien_fly", position, -1, 3, health=1, **kwargs)

    def alien_brain(position, **kwargs):
        def ai_brain(self, engine):
            pass
        return Enemy(ai_brain, "alien_brain", position, 1, 10, health=1, **kwargs)

    def alien_spawner(position, **kwargs):
        def ai_spawner(self, engine):
            self.hurt(engine, 1)

        def spawn(self, engine, player):
            mob = choice([alien_base, alien_fly, alien_brain])(self.position)
            mob.facing_right = bool(random.getrandbits(1))
            engine.place(self.position, mob, exclude=[self])

        return Enemy(ai_spawner, "alien_spawner", position, 0, 2, health=5, on_death=spawn, **kwargs)

    return  {

            "alien_base": alien_base,
            "alien_fly": alien_fly,
            "alien_brain": alien_brain,
            "alien_spawner": alien_spawner

            }

ENEMIES = create_collection()
