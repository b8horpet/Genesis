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
        o.Frics=0.1,
        theWorld.Objects.append(o)
c=Physics.Creature()
alpha=np.pi*1.5
#alpha+=np.random.uniform(-0.5,0.5)
D=3
c.Pos.x=D*np.cos(alpha)
c.Pos.y=D*np.sin(alpha)
c.Vel=-2.5*c.Pos
c.Vel.y-=0.2
c.Vel.x-=0.2
c.Radius/=2.0
c.Mass*=1
c.Frics=0.1,
theWorld.Objects.append(c)
theWorld.Creatures.append(c)
s=Graphics.Surface2D.OpenGL.OpenGL2DSurface(Graphics.SurfaceCommon.Surface.renderfunctor(theWorld,Physics.World.GetRenderData))
#s=Graphics.Surface2D.MatPlotLib.MatplotLibSurface(Graphics.SurfaceCommon.Surface.renderfunctor(theWorld,Physics.World.GetRenderData))
# should be on other thread, or the physics must be on the render call
s.StartRender()

print("genesis project placeholder")
