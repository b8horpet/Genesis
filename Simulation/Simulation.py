#author: b8horpet

from Physics import World,Creature,Obstacle
from Simulation import Task,TaskManager
import numpy as np
import pickle
import itertools as it
import multiprocessing as mp


class MultiProcessingParamsForCreature(object):
    def __init__(self, id, r, c, b, s, simu):
        self.id = id
        self.random = r
        self.color = c
        self.brain = b
        self.ws = s
        self.simulation=simu


def SimulateWrapperForMultiProcessing(params, results):
    c = Creature(mpParameters=params)
    u = params.simulation.CreateUniverse(c)
    w, c = params.simulation.SimulateOneGeneration(*u)
    results[c.ID] = c.Fittness


class Simulation:
    def __init__(self):
        # Global constants
        # #self.Secs=150
        # self.GenerationCount=50
        # self.CreatureCount=64
        # self.ObstacleCount=6
        # self.SecsMultiplier=3
        # self.ProcessCount=mp.cpu_count()

        self.GenerationCount=2
        self.CreatureCount=3
        self.ObstacleCount=6
        self.SecsMultiplier=0
        self.ProcessCount=mp.cpu_count()


        self.TaskManager=TaskManager()
        # Crossover must always happn synchronized, thus, using
        # a global random state does not affect determinism.
        self.EvolutionRandom = np.random.RandomState(seed=0)

    def SelectParents(self,possibleParentsFittnesses):
        def WeightedChoice(weights):
            totalWeights = sum(weights)
            r = self.EvolutionRandom.uniform(0, totalWeights)
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

    def CrossoverBrains(self ,creature, parents):
        for i,hl in enumerate(creature.Brain.HiddenLayers):
            for j,hn in enumerate(hl.Neurons):
                for k,s in enumerate(hn.Inputs):
                    p=self.EvolutionRandom.choice(parents)
                    s.Weight=p.Brain.HiddenLayers[i].Neurons[j].Inputs[k].Weight
                    s.Weight+=creature.Random.normal(0,0.1)
        for j,hn in enumerate(creature.Brain.OutputLayer.Neurons):
            for k,s in enumerate(hn.Inputs):
                p=self.EvolutionRandom.choice(parents)
                s.Weight=p.Brain.OutputLayer.Neurons[j].Inputs[k].Weight
                s.Weight+=creature.Random.normal(0,0.1)

    def CreateUniverse(self, creature):
        """
        Universe is an ordered pair of a world and a creature
        where the creature is also added to the world.
        """

        worldRandom = np.random.RandomState(seed=creature.par.ws)

        world=World(worldRandom)
        a0=worldRandom.uniform(0,np.pi*2)
        for o in range(0, self.ObstacleCount):
            obs=Obstacle()
            alpha=(np.pi * 2 * o / self.ObstacleCount)+a0
            dist=worldRandom.uniform(10,20)
            obs.Pos.x=np.cos(alpha)*dist
            obs.Pos.y=np.sin(alpha)*dist
            world.AddObject(obs)

        world.AddObject(creature)

        return (world, creature)

    def SimulateOneGeneration(self, world, creature):
        Secs = 50+creature.par.ws*self.SecsMultiplier
        for t in range(0, Secs * 20):
            world.Activate()
            if not creature.IsAlive():
                creature.Fittness = t / 20
                break

        if creature.IsAlive():
            creature.Fittness=Secs+(creature.Health+1)*(creature.Energy+1)
        return (world, creature)


    def RunSimulations(self):
        initialCreatures = [Creature () for i in range(0, self.CreatureCount)]
        generation = [self.CreateUniverse(i) for i in initialCreatures]

        print()
        print("Running simulation with global values:")
        #print("\tself.Secs = %d" % Secs)
        print("\tGenerationCount = %d" % self.GenerationCount)
        print("\tCreatureCount = %d" % self.CreatureCount)
        print("\tObstacleCount = %d" % self.ObstacleCount)
        print("\tProcessCount = %d" % self.ProcessCount)

        with mp.Pool(self.ProcessCount) as processPool:
            for g in range(0, self.GenerationCount):
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

                    params = [(MultiProcessingParamsForCreature(c.ID, c.Random, c.Color, c.Brain, g, self), results) for w, c in generation]
                    processPool.starmap(SimulateWrapperForMultiProcessing, params)
                    # print(results)
                    for _, creature in generation:
                        creature.Fittness = results[creature.ID]

                print("Generation #%d ended" % g)

                for i, (_, creature) in enumerate(generation):
                    survived = creature.Fittness > 50+g*self.SecsMultiplier
                    with open("creature_%d_%d.dat" % (g,i), "wb") as f:
                        pickle.dump(creature.Brain,f)
                    print("\t%d fittness = %f\t\t(Creature #%d\t%s)" % (i, creature.Fittness, creature.ID, "survived" if survived else "dead"))

                # create the next generation
                print("Creating next generation")
                nextgen = [Creature() for i in range(0, self.CreatureCount)]
                for nextCreature in nextgen:
                    parentFittnesses = [c.Fittness for w, c in generation]
                    p1index, p2index = self.SelectParents(parentFittnesses)
                    p1 = generation[p1index][1]
                    p2 = generation[p2index][1]
                    self.CrossoverBrains(nextCreature, [p1, p2])

                    print("\t%d x %d\t\t(Creature #%d x Creature #%d -> Creature #%d)" %
                        (p1index, p2index, p1.ID, p2.ID, nextCreature.ID))


                generation = [self.CreateUniverse(i) for i in nextgen]

            #s=Graphics.Surface2D.OpenGL.OpenGL2DSurface(Physics.memberfunctor(theWorld, Physics.World.GetRenderData))
            #s=Graphics.Surface2D.MatPlotLib.MatplotLibSurface(Physics.memberfunctor(theWorld,Physics.World.GetRenderData))
            # should be on other thread, or the physics must be on the render call
            #s.StartRender()
