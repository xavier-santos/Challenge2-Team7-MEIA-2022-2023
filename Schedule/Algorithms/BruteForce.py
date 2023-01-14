# Applies the brute force algorithm to the scheduling of engines to workers
#
# @param workers: list of workers
# @param engines: list of engines

from itertools import product
from Models.week import Week
import numpy as np


def fitness_func(genome, empty_penalty=1000) -> int:
    fitness = 0
    if genome.has_empty_days():
        fitness -= empty_penalty
    fitness += genome.get_rank()
    fitness -= genome.get_unassigned_time()
    return fitness


def bytes_to_week(possible, workers, engines):
    week = Week(workers)
    decision = 0
    for x in range(0, len(workers)):
        for y in range(0, 7):
            for z in range(0, len(engines)):
                if possible[decision] == 1:
                    week.add_engine(engines[z], y, workers[x])
                decision +=1
    return week


def generate_all_possibilities(size):
    return list(product([0, 1], repeat=size))


def bruteforce(workers, engines):
    print("Generating all possibilities (This may take a while)")
    possibilities = generate_all_possibilities(len(workers)*7*len(engines))
    print("All possibilities generated")
    best_week = None
    best_score = 0
    i = 1
    for possibility in possibilities:
        possible = np.asarray(possibility)
        week = bytes_to_week(possible, workers, engines)
        fitness = fitness_func(week)
        if fitness > best_score:
            best_score = fitness
            best_week = week
        print(f"Progress {i} out of {len(possibilities)} possibilities")
        i += 1
    print("Bruteforce finished")
    return best_week, best_score
