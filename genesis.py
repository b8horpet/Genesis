__author__ = 'b8horpet'

import NeuralNet
import Physics
import Graphics.Surface2D
import numpy as np

theWorld=Physics.World()
#N=10
for i in range(0,5):
    for j in range(0,i+1):
        o=Physics.Sphere()
        o.Pos.x=j-(i/2.0)
        o.Pos.y=i*(np.sqrt(3)/2.0)
        theWorld.Objects.append(o)
c=Physics.Creature()
alpha=np.random.uniform(0,np.pi*2.0)
D=10
c.Pos.x=D*np.cos(alpha)
c.Pos.y=D*np.sin(alpha)
c.Acc=-5.0*c.Pos
c.Radius/=2.0
theWorld.Objects.append(c)
theWorld.Creatures.append(c)
def renderfunctor(this,func):
    def f():
        return func(this)
    return f
s=Graphics.Surface2D.MatPlotLib.MatplotLibSurface(renderfunctor(theWorld,Physics.World.GetRenderData))
# should be on other thread, or the physics must be on the render call
s.StartRender()

print("genesis project placeholder")
