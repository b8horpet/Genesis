__author__ = 'b8horpet'

import NeuralNet
import Physics
import Graphics
import numpy as np
import pickle

GlobalRandom=np.random.RandomState()
GlobalRandom.seed(0)
def WeightedChoice(l):
    total = sum(x[0] for x in l)
    r=GlobalRandom.uniform(0,total)
    for n, i in enumerate(l):
        if total-i[0] < r:
            return n
        total-=i[0]
    print("omg")

N=1#00
secs=50
C=5
O=6
generation=[]
NeuralNet.NeuralRandom.seed(0)

# random seed and sequence is currently irrelevant
CreatureColorRandom = np.random.RandomState(seed=0)
def GetRandomColor ():
    return (CreatureColorRandom.uniform(0.0, 0.3), CreatureColorRandom.uniform(0.2, 0.8), CreatureColorRandom.uniform(0.0, 0.3), 1)

for i in range(0,C):
    generation.append(Physics.Creature(GetRandomColor ()))

for g in range(0,N):
    print("gen #%d" % (g))
    NeuralNet.NeuralRandom.seed(g)
    for i in range(0,len(generation)):
        worldRandom = np.random.RandomState(seed=0)
        theWorld=Physics.World(worldRandom)
        for o in range(0,O):
            obs=Physics.Obstacle()
            alpha=np.pi*2*o/O
            dist=worldRandom.uniform(10,20)
            obs.Pos.x=np.cos(alpha)*dist
            obs.Pos.y=np.sin(alpha)*dist
            theWorld.AddObject(obs)
        print(i)
        theWorld.AddObject(generation[i])
        #Log=[theWorld.Dump()]

        for t in range(0,secs*20):
            theWorld.Activate()
            #Log.append(theWorld.Dump())
            if not generation[i].IsAlive():
                print("dead")
                generation[i].Fittness=t/20
                break
        if generation[i].IsAlive():
            generation[i].Fittness=secs+(generation[i].Health+1)*(generation[i].Energy+1)
        #with open("run_%d_%d.dat" % (g,i),"wb") as f:
        #    pickle.dump(Log,f)
    for i in range(0,len(generation)):
        print("#%d fittness= %f" % (i,generation[i].Fittness))
    # create the next generation
    nextgen=[Physics.Creature(GetRandomColor ()) for i in range(0,C)]
    
    for i in nextgen:
        parentgen = [(g.Fittness, g) for g in generation]
        p1index=WeightedChoice(parentgen)
        p1 = parentgen.pop(p1index)
        p2index=WeightedChoice(parentgen)
        p2 = parentgen[p2index]
        if p2index>=p1index:
            p2index+=1
        print((p1index,p2index))
        i.InheritGenom([p1[1], p2[1]])
    generation=nextgen

#s=Graphics.Surface2D.OpenGL.OpenGL2DSurface(Physics.memberfunctor(theWorld, Physics.World.GetRenderData))
#s=Graphics.Surface2D.MatPlotLib.MatplotLibSurface(Physics.memberfunctor(theWorld,Physics.World.GetRenderData))
# should be on other thread, or the physics must be on the render call
#s.StartRender()

print("genesis project placeholder")
