#author: b8horpet


from Physics.Basics import *
from Physics.Object import *


class Creature(Sphere): # one cell, spheric (for now)
    def __init__(self):
        super(Creature,self).__init__()
        self.Alive=True

    def Logic(self):
        pass