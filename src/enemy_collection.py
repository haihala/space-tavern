from enemy import Enemy
from random import choice

def create_collection():
    def alien_base(position, **kwargs):
        def ai_base(self, engine):
            #self.move(engine, target=engine.player.position)

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
            pass
        return Enemy(ai_fly, "alien_fly", position, -1, 6, health=1, **kwargs)

    def alien_brain(position, **kwargs):
        def ai_brain(self, engine):
            pass
        return Enemy(ai_brain, "alien_brain", position, 1, 10, health=1, **kwargs)

    def alien_spawner(position, **kwargs):
        def ai_spawner(self, engine):
            self.hurt(engine, 1)

        def spawn(self, engine, player):
            mob = choice([alien_base, alien_fly, alien_brain])(self.position)
            engine.place(self.position, mob, exclude=[self])

        return Enemy(ai_spawner, "alien_spawner", position, 0, 2, health=5, on_death=spawn, **kwargs)

    return  {

            "alien_base": alien_base,
            "alien_fly": alien_fly,
            "alien_brain": alien_brain,
            "alien_spawner": alien_spawner

            }

ENEMIES = create_collection()
