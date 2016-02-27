__author__ = 'b8horpet'

import NeuralNet
import Physics
import Graphics

import numpy as np
import pickle
import itertools as it
import multiprocessing as mp

# Crossover must always happn synchronized, thus, using
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

    worldRandom = np.random.RandomState(seed=0)

    world=Physics.World(worldRandom)
    for o in range(0, ObstacleCount):
        obs=Physics.Obstacle()
        alpha=np.pi * 2 * o / ObstacleCount
        dist=worldRandom.uniform(10,20)
        obs.Pos.x=np.cos(alpha)*dist
        obs.Pos.y=np.sin(alpha)*dist
        world.AddObject(obs)
    
    world.AddObject(creature)

    return (world, creature)

# Global constants
Secs=150
GenerationCount=10#0
CreatureCount=8
ObstacleCount=6

ProcessCount=mp.cpu_count()

def SimulateOneGeneration(world, creature):
    for t in range(0, Secs * 20):
        world.Activate()
        if not creature.IsAlive():
            creature.Fittness = t / 20
            break

    if creature.IsAlive():
        creature.Fittness=Secs+(creature.Health+1)*(creature.Energy+1)
    return (world, creature)


class MultiProcessingParamsForCreature(object):
    def __init__(self, id, r, c, b):
        self.id = id
        self.random = r
        self.color = c
        self.brain = b

def SimulateWrapperForMultiProcessing(params, results):
    c = Physics.Creature(mpParameters=params)
    u = CreateUniverse (c)
    w, c = SimulateOneGeneration (*u)
    results[c.ID] = c.Fittness

if __name__ == "__main__":
    initialCreatures = [Physics.Creature () for i in range(0, CreatureCount)]
    generation = list(map(CreateUniverse, initialCreatures))

    print()
    print("Running simulation with global values:")
    print("\tSecs = %d" % Secs)
    print("\tGenerationCount = %d" % GenerationCount)
    print("\tCreatureCount = %d" % CreatureCount)
    print("\tObstacleCount = %d" % ObstacleCount)
    print("\tProcessCount = %d" % ProcessCount)    

    with mp.Pool(ProcessCount) as processPool:
        for g in range(0, GenerationCount):
            print()
            print("Generation #%d started" % (g))
            
            # Iterative solution
            # iterativeGeneration = it.starmap(SimulateOneGeneration, generation)
            # generation = list(iterativeGeneration)
            
            # Multpiprocess solution

            # Default method is 'fork' on linux, 'spawn' on windows
            # mp.set_start_method('spawn')
            with mp.Manager() as manager:
                results = manager.dict()

                params = [(MultiProcessingParamsForCreature (c.ID, c.Random, c.Color, c.Brain), results) for w, c in generation]
                processPool.starmap(SimulateWrapperForMultiProcessing, params)
                # print(results)
                for _, creature in generation:
                    creature.Fittness = results[creature.ID]

            print("Generation #%d ended" % g)

            for i, (_, creature) in enumerate(generation):
                survived = creature.Fittness > Secs
                print("\t%d fittness = %f\t\t(Creature #%d\t%s)" % (i, creature.Fittness, creature.ID, "survived" if survived else "dead"))

            # create the next generation
            print("Creating next generation")
            nextgen = [Physics.Creature() for i in range(0, CreatureCount)]
            for nextCreature in nextgen:
                parentFittnesses = [c.Fittness for w, c in generation]
                p1index, p2index = SelectParents (parentFittnesses)
                p1 = generation[p1index][1]
                p2 = generation[p2index][1]
                CrossoverBrains(nextCreature, [p1, p2])

                print("\t%d x %d\t\t(Creature #%d x Creature #%d -> Creature #%d)" %
                    (p1index, p2index, p1.ID, p2.ID, nextCreature.ID))

            
            generation = list(map(CreateUniverse, nextgen))

        #s=Graphics.Surface2D.OpenGL.OpenGL2DSurface(Physics.memberfunctor(theWorld, Physics.World.GetRenderData))
        #s=Graphics.Surface2D.MatPlotLib.MatplotLibSurface(Physics.memberfunctor(theWorld,Physics.World.GetRenderData))
        # should be on other thread, or the physics must be on the render call
        #s.StartRender()

    print("Genesis ended")