__author__ = 'b8horpet'

import NeuralNet
import Physics
import Graphics
import numpy as np
import pickle

# Crossover must always happn synchronized, thus, using
# a global random state does not affect determinism.
EvolutionRandom = np.random.RandomState(seed=0)

def SelectParents(possibleParents):
    def WeightedChoice(weights):
        totalWeights = sum(weights)
        r = EvolutionRandom.uniform(0, totalWeights)
        for i, p in enumerate(weights):
            if totalWeights - p < r:
                return i
            totalWeights -= p
        assert(False)

    weights = list(p[0] for p in possibleParents)
    p1index=WeightedChoice(weights)
    weights.pop(p1index)
    p2index=WeightedChoice(weights)
    if p2index>=p1index:
        p2index+=1
    return p1index, p2index

def CrossoverBrains(creature, parents):
    for i,hl in enumerate(creature.Brain.HiddenLayers):
        for j,hn in enumerate(hl.Neurons):
            for k,s in enumerate(hn.Inputs):
                p=EvolutionRandom.choice(parents)
                s.Weight=p.Brain.HiddenLayers[i].Neurons[j].Inputs[k].Weight
    for j,hn in enumerate(creature.Brain.OutputLayer.Neurons):
        for k,s in enumerate(hn.Inputs):
            p=EvolutionRandom.choice(parents)
            s.Weight=p.Brain.OutputLayer.Neurons[j].Inputs[k].Weight

GenerationCount=1#00
secs=50
CreatureCount=5
ObstacleCount=6

generation=[Physics.Creature() for i in range(0, CreatureCount)]

for g in range(0, GenerationCount):
    print("gen #%d" % (g))
    for i in range(0,len(generation)):
        worldRandom = np.random.RandomState(seed=0)
        theWorld=Physics.World(worldRandom)
        for o in range(0, ObstacleCount):
            obs=Physics.Obstacle()
            alpha=np.pi * 2 * o / ObstacleCount
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
    for i in range(0, CreatureCount):
        print("#%d fittness= %f" % (i,generation[i].Fittness))

    # create the next generation
    nextgen=[Physics.Creature() for i in range(0, CreatureCount)]
    
    for nextCreature in nextgen:
        parentgen = [(g.Fittness, g) for g in generation]
        p1index, p2index = SelectParents (parentgen)
        print((p1index,p2index))

        p1 = parentgen[p1index][1]
        p2 = parentgen[p2index][1]
        CrossoverBrains(nextCreature, [p1, p2])
    
    generation=nextgen

#s=Graphics.Surface2D.OpenGL.OpenGL2DSurface(Physics.memberfunctor(theWorld, Physics.World.GetRenderData))
#s=Graphics.Surface2D.MatPlotLib.MatplotLibSurface(Physics.memberfunctor(theWorld,Physics.World.GetRenderData))
# should be on other thread, or the physics must be on the render call
#s.StartRender()

print("genesis project placeholder")
