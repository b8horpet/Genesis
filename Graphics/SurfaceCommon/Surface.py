#author: b8horpet

def memberfunctor(this, func):
    def f(*args,**kwargs):
        return func(this,*args,**kwargs)
    return f


class SurfaceInterface:
    def __init__(self,u):
        pass

    def StartRender(self):
        pass