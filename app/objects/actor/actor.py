# from app.journal.journal import Logging


# class Actor(Logging):
class Actor:
    def __init__(self, name: str = None):
        self.active = True
        self.name = name
