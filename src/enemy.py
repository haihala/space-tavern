from entity import Entity

class Enemy(Entity):
    def ai(self, engine):
        return None
    
    def tick(self, engine):
        if super().tick(engine):
            return None

        if action == None:
            return self.ai(engine)

