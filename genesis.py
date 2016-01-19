__author__ = 'b8horpet'

import NeuralNet
import Physics
import Graphics.Surface2D

s=Graphics.Surface2D.MatPlotLib.MatplotLibSurface()
theWorld=Physics.World()
N=10
for i in range(0,N):
    theWorld.Creatures.append(NeuralNet.Brain())

print("genesis project placeholder")
