from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Crossovers
import random

class GameRunner:
   def __init__(self, ga, payoff_matrix, memory):
      self.ga = ga
      self.payoff_matrix = payoff_matrix
      self.memory = memory

   def get_eval_fn(self, max_rounds):
      def eval_fn(player):
         payoff = 0
         opp = 0
         for opponent in self.ga.getPopulation():
            if id(opponent) != id(player):
               opp += 1
               payoff += self.play(player, opponent, max_rounds)

         #print "Played %d opponents %d rounds for total payoff %d\n"\
         #   % (opp, max_rounds, payoff)
         
         return payoff

      return eval_fn

   def play(self, plrA, plrB, max_rounds):
      payoff = 0

      # The initial history is randomised so as to decrease chance of unreached histories
      prevA = [random.randint(0, 1) for _ in range(self.memory)]
      prevB = [random.randint(0, 1) for _ in range(self.memory)]
      #print "History B " + str(prevB[-self.memory:]) + " - History A " + str(prevA[-self.memory:])

      for i in range(max_rounds):
         # 0 codes for cooperation
         # 1 codes for betrayal
         idxA = self.encodeHistory(prevB[-self.memory:])
         idxB = self.encodeHistory(prevA[-self.memory:])
         
         #print "Round " + str(i) + ": A selects " + str(idxA) + " - B selects " + str(idxB)

         payoff += self.payoff_matrix[plrA[idxA]][plrB[idxB]]
         # The ith position in the vector states what the plrA's
         # move will be, given that the plrB previously made move i

         prevA.append(plrA[idxA])
         prevB.append(plrB[idxB])

         #print "History B " + str(prevB[-self.memory:]) + " - History A " + str(prevA[-self.memory:])
      return payoff

   def encodeHistory(self, history):
      l = len(history) - 1
      return sum([history[l-k] * 2**k for k in range(l+1)])


# For game memory m, need at least 2**m rounds in order for all histories to be reachable
game_memory = 3
game_rounds = 8

genome = G1DList.G1DList(2**game_memory)
ga = GSimpleGA.GSimpleGA(genome)

ga.selector.set(Selectors.GRouletteWheel)
ga.setPopulationSize(20)
ga.setGenerations(1000)

# The payoff matrix for the Prisoner's Dilemma
# In terms of player A's gains over player B
pd_payoff = ((1,  0),
             (12, 3))

gr = GameRunner(ga, pd_payoff, game_memory)

genome.evaluator.set(gr.get_eval_fn(game_rounds))
genome.crossover.set(Crossovers.G1DListCrossoverUniform)
genome.setParams(rangemin=0, rangemax=1)

ga.evolve(freq_stats=5)
print ga.bestIndividual()
