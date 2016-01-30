__author__ = 'b8horpet'

import NeuralNet
import Physics
import Graphics
import numpy as np

theWorld=Physics.World()
s=Graphics.Surface2D.OpenGL.OpenGL2DSurface(Graphics.SurfaceCommon.Surface.memberfunctor(theWorld, Physics.World.GetRenderData))
#s=Graphics.Surface2D.MatPlotLib.MatplotLibSurface(Graphics.SurfaceCommon.Surface.memberfunctor(theWorld,Physics.World.GetRenderData))
# should be on other thread, or the physics must be on the render call
s.StartRender()

print("genesis project placeholder")
