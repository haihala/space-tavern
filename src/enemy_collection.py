from enemy import Enemy

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
        return Enemy(ai_base, "alient_fly", position, -1, 6, health=1, **kwargs)

    def alien_brain(position, **kwargs):
        def ai_brain(self, engine):
            pass
        return Enemy(ai_base, "alient_brain", position, 5, 10, health=1, **kwargs)


    return  {

            "alien_base": alien_base,
            "alien_fly": alien_fly,
            "alien_brain": alien_brain

            }

ENEMIES = create_collection()
