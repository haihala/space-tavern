from enemy import Enemy

def create_collection():
    def alien_base(position, **kwargs):
        def ai_base(self, engine):
            self.move(engine, target=engine.player.position)
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
