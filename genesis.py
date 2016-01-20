__author__ = 'b8horpet'

import NeuralNet
import Physics
import Graphics.Surface2D
import numpy as np

theWorld=Physics.World()
N=10
for i in range(0,N):
    c=Physics.Creature()
    c.Pos.x=np.random.uniform(-10,10)
    c.Pos.y=np.random.uniform(-10,10)
    c.Vel.x=np.random.uniform(-10,10)
    #c.Vel.y=np.random.uniform(-10,10)
    theWorld.Creatures.append(c)
def renderfunctor(this,func):
    def f():
        return func(this)
    return f
s=Graphics.Surface2D.MatPlotLib.MatplotLibSurface(renderfunctor(theWorld,Physics.World.GetRenderData))
# should be on other thread, or the physics must be on the render call
s.StartRender()

print("genesis project placeholder")
