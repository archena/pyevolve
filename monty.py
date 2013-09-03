import random
from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Crossovers

def eval_monty(chromosome):
    # The game is set up by randomly permutating two goats and a car, which is great fun.
    choices = ["Goat", "Car", "Goat"]
    random.shuffle(choices)
    
    # The player picks a door but may not see behind it
    choice = random.sample(choices, 1)[0]

    # The host, knowing which doors have goats behind them, opens another door to reveal a goat
    choices.remove("Goat")

    # The player is given a choice: keep their original door, or switch to the remaining unopened door
    # Does this player switch? (a '1' signifies a switching strategy)
    switch = chromosome[0] == 1
    
    if switch:
        choices.remove(choice)
        choice = choices[0]
    
    # Now the player can see if they won
    # n.b. this assumes the player actually wants to win the car and not the goat!
    return 1 if choice == "Car" else 0

# Pyevolve setup
genome = G1DList.G1DList(1)
genome.evaluator.set(eval_monty)
genome.setParams(rangemin=0, rangemax=1)
genome.crossover.set(Crossovers.G1DListCrossoverUniform)

ga = GSimpleGA.GSimpleGA(genome)
ga.selector.set(Selectors.GRouletteWheel)

ga.evolve(freq_stats=10)
print ga.bestIndividual()
