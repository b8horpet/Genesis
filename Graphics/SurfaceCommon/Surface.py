#author: b8horpet

def renderfunctor(this,func):
    def f():
        return func(this)
    return f


class SurfaceInterface:
    def __init__(self,u):
        pass

    def StartRender(self):
        pass