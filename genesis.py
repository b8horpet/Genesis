__author__ = 'b8horpet'

import NeuralNet
import Physics
import Graphics
import numpy as np
import pickle

N=1#00
secs=200
C=5
O=6
generation=[]
NeuralNet.NeuralRandom.seed(0)
for i in range(0,C):
    generation.append(Physics.Creature())
for g in range(0,N):
    NeuralNet.NeuralRandom.seed(g)
    for i in range(0,len(generation)):
        theWorld=Physics.World()
        Physics.PhysicsRandom.seed(0) # same world for everyone
        for o in range(0,O):
            obs=Physics.Obstacle()
            alpha=np.pi*2*o/O
            dist=Physics.PhysicsRandom.uniform(10,20)
            obs.Pos.x=np.cos(alpha)*dist
            obs.Pos.y=np.sin(alpha)*dist
            theWorld.AddObject(obs)
        print(i)
        theWorld.AddObject(generation[i])
        Log=[theWorld.Dump()]
        for t in range(0,secs*20):
            theWorld.Activate()
            Log.append(theWorld.Dump())
        with open("run_%d_%d.dat" % (g,i),"wb") as f:
            pickle.dump(Log,f)
    for i in range(0,len(generation)):
        print("#%d is alive? %s" % (i,generation[i].Alive))
    # create the next generation
#s=Graphics.Surface2D.OpenGL.OpenGL2DSurface(Physics.memberfunctor(theWorld, Physics.World.GetRenderData))
#s=Graphics.Surface2D.MatPlotLib.MatplotLibSurface(Physics.memberfunctor(theWorld,Physics.World.GetRenderData))
# should be on other thread, or the physics must be on the render call
#s.StartRender()

print("genesis project placeholder")
