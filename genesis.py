__author__ = 'b8horpet'

import NeuralNet
import Physics
import Graphics
import numpy as np

theWorld=Physics.World()
c=Physics.Creature()
c.Frics=0.1,0.1
theWorld.AddObject(c)
for i in range(0,6):
    f=Physics.Food()
    d=np.random.uniform(3.0,7.0)
    a=i*np.pi/3.0
    f.Frics=0.1,0.1
    f.Pos.x=d*np.cos(a)
    f.Pos.y=d*np.sin(a)
    theWorld.AddObject(f)
#s=Graphics.Surface2D.OpenGL.OpenGL2DSurface(Graphics.SurfaceCommon.Surface.renderfunctor(theWorld,Physics.World.GetRenderData))
s=Graphics.Surface2D.MatPlotLib.MatplotLibSurface(Graphics.SurfaceCommon.Surface.renderfunctor(theWorld,Physics.World.GetRenderData))
# should be on other thread, or the physics must be on the render call
s.StartRender()

print("genesis project placeholder")
