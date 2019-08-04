from enemy import Enemy
from projectile_collection import PROJECTILES

from random import choice, getrandbits

def bat_shoot(self, engine):
    if not self.fatigue:
        bullet = PROJECTILES["projectile_alien_down"](self.down)

        if engine.place(bullet, target="tile"):
            bullet.velocity = [0, 1]
            self.fatigue += self.speed

def turret_shoot(self, engine, direction, sprite):
    if not self.fatigue:
        bullet = PROJECTILES[sprite]([direction[i]+self.position[i] for i in range(2)])
        if direction == [1, 0]:
            bullet.facing_right = True

        if engine.place(bullet, target="tile"):
            bullet.velocity = direction
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
        return Enemy(ai_base, "alien_base", position, 1, 4, health=1, sprite_updated=True, **kwargs)

    def alien_fly(position, **kwargs):
        def ai_fly(self, engine):
            if self.position[0] == engine.player.position[0]:
                bat_shoot(self, engine)
            elif self.move(engine, amount=1, direction=self.forwards):
                if self.move(engine, amount=1, direction=[0, -1]):
                    self.facing_right = not self.facing_right
                    if self.move(engine, amount=1, direction=self.forwards):
                        self.dead = True

        return Enemy(ai_fly, "alien_fly", position, -1, 3, health=1, sprite_updated=True, **kwargs)

    def alien_turret(position, **kwargs):
        def ai_turret(self, engine):
            if self.position[0] == engine.player.position[0]:
                direction = [0, -1]
                sprite = "projectile_alien_up"
            else:
                direction = [[-1, 1][self.position[0]<engine.player.position[0]], 0]
                sprite = "projectile_alien"
                self.facing_right = self.position[0]<engine.player.position[0]
            turret_shoot(self, engine, direction, sprite)

        return Enemy(ai_turret, "alien_turret", position, 1, 5, health=1, sprite_updated=True, **kwargs)

    def alien_spawner(position, **kwargs):
        def ai_spawner(self, engine):
            self.hurt(engine, 1)

        def spawn(self, engine, player):
            mob = choice([alien_base, alien_fly, alien_turret])(self.position)
            mob.facing_right = bool(getrandbits(1))
            engine.place(mob, exclude=[self])

        return Enemy(ai_spawner, "alien_spawner", position, 0, 2, health=5, on_death=spawn, sprite_updated=True, **kwargs)

    def alien_roadroller(position, **kwargs):
        def ai_roadroller(self, engine):
            target_direction = engine.player.position[0] - self.position[0] 

            engine.roadroll([[self.forwards[i] + [0, j][i] for i in range(2)] for j in range(-1, 4)])
            self.move(engine, amount=1, direction=[self.forwards[i] - self.position[i] for i in range(2)])
            
            if target_direction:
                direction = target_direction < 0
                
                if direction == self.facing_right:
                    # Turn 
                    self.facing_right = not direction



        return Enemy(ai_roadroller, "alien_big", position, 2, 3, health=3, sprite_updated=True, width=2, height=2, **kwargs)

    def alien_spawner_big(position, **kwargs):
        def ai_spawner(self, engine):
            self.hurt(engine, 1)

        def spawn(self, engine, player):
            mob = alien_roadroller(self.position)
            mob.facing_right = bool(getrandbits(1))
            engine.place(mob, exclude=[self])

        return Enemy(ai_spawner, "alien_spawner_big", position, 0, 2, health=1, on_death=spawn, sprite_updated=True, width=2, height=2, **kwargs)

    return  {
            "alien_base": alien_base,
            "alien_fly": alien_fly,
            "alien_turret": alien_turret,
            "alien_spawner": alien_spawner,
            "alien_spawner_big": alien_spawner_big
            }

ENEMIES = create_collection()
