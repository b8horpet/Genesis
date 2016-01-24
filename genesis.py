__author__ = 'b8horpet'

import NeuralNet
import Physics
import Graphics
import numpy as np

theWorld=Physics.World()
N=5
for i in range(0,N):
    for j in range(0,i+1):
        o=Physics.Sphere()
        o.Pos.x=(j-(i/2.0))
        o.Pos.y=i*(np.sqrt(3)/2.0+0.01)
        o.Frics=0,
        o.Mass*=10
        theWorld.Objects.append(o)
c=Physics.Creature()
alpha=np.pi*1.5
#alpha+=np.random.uniform(-1.0,-1.0)
D=20
c.Pos.x=D*np.cos(alpha)
c.Pos.y=D*np.sin(alpha)
c.Vel=-0.5*c.Pos
c.Vel.y-=0.2
c.Vel.x-=0.68
c.Mass*=1.0
c.Frics=0,
c.Vel*=5.0
theWorld.Objects.append(c)
theWorld.Creatures.append(c)
s=Graphics.Surface2D.OpenGL.OpenGL2DSurface(Graphics.SurfaceCommon.Surface.renderfunctor(theWorld,Physics.World.GetRenderData))
#s=Graphics.Surface2D.MatPlotLib.MatplotLibSurface(Graphics.SurfaceCommon.Surface.renderfunctor(theWorld,Physics.World.GetRenderData))
# should be on other thread, or the physics must be on the render call
s.StartRender()

print("genesis project placeholder")
