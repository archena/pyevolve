# Finding solutions to satisfiability problems

from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors

# Any formula in conjunctive or disjunctive normal form will do here
def eval_func(chromosome):
    x1 = bool(chromosome[0])
    x2 = bool(chromosome[1])
    x3 = bool(chromosome[2])
    x4 = bool(chromosome[3])
    x5 = bool(chromosome[4])
    x6 = bool(chromosome[5])
    #    return (p or not q) and (not p or not q) and (p or q) and (q or r)
    return (x1 or not x2 or not x3) and \
        (x3 or not x5 or x6) and \
        (x3 or not x6 or x4) and \
        (x4 or x5 or x6)

# Pyevolve setup
genome = G1DList.G1DList(6)
genome.evaluator.set(eval_func)
genome.setParams(rangemin=0, rangemax=1)

ga = GSimpleGA.GSimpleGA(genome)
ga.selector.set(Selectors.GRouletteWheel)

ga.evolve(freq_stats=10)
print ga.bestIndividual()
