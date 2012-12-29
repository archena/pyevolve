import random
from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Crossovers

def get_eval_fn(ga, payoff_matrix):
    def eval_fn(player):
        # Try this player against every other player in the current population
        time = 0
        betrayalcount = 0
        for opponent in ga.getPopulation():
            # 0 codes for cooperation
            # 1 codes for betrayal
            time += payoff_matrix[player[0]][opponent[0]]

        maxtime = 12 * len(ga.getPopulation())

        print "Player %s and gets %d months. Score %f"\
            % ("betrays" if player[0] == 1 else "cooperates",
               time, maxtime - time)

        return maxtime - time
        
    return eval_fn

genome = G1DList.G1DList(1)
ga = GSimpleGA.GSimpleGA(genome)

ga.selector.set(Selectors.GRouletteWheel)
ga.setPopulationSize(10)
ga.setGenerations(15)

# The payoff matrix for the Prisoner's Dilemma
payoff = ((1, 12),
          (0,  3))

genome.evaluator.set(get_eval_fn(ga, payoff))
genome.crossover.set(Crossovers.G1DListCrossoverUniform)
genome.setParams(rangemin=0, rangemax=1)

ga.evolve(freq_stats=0)
print ga.bestIndividual()
