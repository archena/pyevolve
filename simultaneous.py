# Systems of simultaneous equations
# This example demonstrates the use of a Gaussian mutator suitable for floating-point
# genomes, however it is not a great example of genetic algorithms;
# traditional numerical methods are likely to be more accurate for this problem!

from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Mutators
from pyevolve import Consts
import math

def eval_func(chromosome):
    x = chromosome[0]
    y = chromosome[1]

    # This system has two solutions: x, y = (-1.5, -0.25) and x, y = (0.5, 4.25)
    e1 = x**2 + 3*x + 2
    e2 = 2*x + 3

    # The fitness is the summed error for each equation
    # So the GA needs to be configured to *minimize* scores
    return abs(e1 - y) + abs(e2 - y)

# Pyevolve setup
genome = G1DList.G1DList(2)
genome.setParams(rangemin=-5.0, rangemax=5.0)
genome.mutator.set(Mutators.G1DListMutatorRealGaussian)
genome.evaluator.set(eval_func)

ga = GSimpleGA.GSimpleGA(genome)
ga.selector.set(Selectors.GRouletteWheel)
ga.minimax = Consts.minimaxType["minimize"]
ga.setPopulationSize(50)
ga.setGenerations(400)

ga.evolve(freq_stats=10)
print ga.bestIndividual()
