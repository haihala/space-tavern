

class Entity():
    def __init__(self):
        self.fatigue = 0

    def ai(self, engine):
        return None

    def tick(self, engine, action=None):
        self.fatigue = max(0, self.fatigue-1)
        if not self.fatigue:
            if action == None:
                return self.ai(engine)

