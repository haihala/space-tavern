from enemy import Enemy

def create_collection():

    def alien_base(positon, **kwargs):
        def ai_base(self, engine):
            pass

        return Enemy(ai_base, "alien_base", positon, **kwargs)

    return  {

            "alien_base": alien_base

            }

ENEMIES = create_collection()
