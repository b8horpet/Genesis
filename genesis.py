__author__ = 'b8horpet'

import NeuralNet
import Physics
import Graphics
import numpy as np
import pickle

# Crossover must always happen synchronized, thus, using
# a global random state does not affect determinism.
EvolutionRandom = np.random.RandomState(seed=0)

def SelectParents(possibleParentsFittnesses):
    def WeightedChoice(weights):
        totalWeights = sum(weights)
        r = EvolutionRandom.uniform(0, totalWeights)
        for i, p in enumerate(weights):
            if totalWeights - p < r:
                return i
            totalWeights -= p
        assert(False)

    weights = list(possibleParentsFittnesses)
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


def CreateUniverse(creature):
    """
    Universe is an ordered pair of a world and a creature
    where the creature is also added to the world.
    """

    worldRandom = np.random.RandomState(seed=creature.ID+1)

    world=Physics.World(worldRandom)
    for o in range(0, ObstacleCount):
        alpha=np.pi * 2.0 * o / ObstacleCount
        #dist=worldRandom.uniform(5,20)
        #obs=Physics.Obstacle(Physics.Vector3D(np.cos(alpha)*dist,np.sin(alpha)*dist,0))
        obs=Physics.Obstacle(Physics.Vector3D(worldRandom.uniform(-30,30),worldRandom.uniform(-30,30),0))
        world.AddObject(obs)
    
    world.AddObject(creature)

    return (world, creature)

if __name__ == "__main__":
    CreatureCount=1
    ObstacleCount=50
    Secs=50

    initialCreatures = [Physics.Creature() for i in range(0, CreatureCount)]
    #generation = list(map(CreateUniverse, initialCreatures))

    print("generating universe")
    world,_ = CreateUniverse(initialCreatures[0])
    print("stepping")
    for asd in range(100):
        print("step %d" % asd)
        world.Activate()
    print("collision tests: %d collisions: %d" % (Physics.Object.NumCollTests,Physics.Object.NumColls))
#    for t in range(0,Secs * 20):
#        print("step %d" % t )
#        world.Activate()
#        if len(world.Objects) == 0:
#            print ("\tNo more creatures alive")
#            break

    #s=Graphics.Surface2D.OpenGL.OpenGL2DSurface(Physics.memberfunctor(world, Physics.World.GetRenderData))
    #s=Graphics.Surface2D.MatPlotLib.MatplotLibSurface(Physics.memberfunctor(world,Physics.World.GetRenderData))
    # should be on other thread, or the physics must be on the render call
    #s.StartRender()

    print("Genesis ended")
