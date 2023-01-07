from model import *
from random import choices, randint, randrange, random, getrandbits
from algorithm import *
from typing import List, Optional, Callable, Tuple
from functools import partial

# Worker work_period size is max bag weight
# Maintenance time is weight
# Genome is [ Worker1 - Machine1, Worker 1 - Machine2, Worker2 - Machine1, Worker2 - Machine2]
# When mutate Machine cant be 1 in 2 workers. When an index changes all others with same machine must change
# Chromosome value can be 0 or 1. Initialized as 2 and randomizing fields worker one by one can only randomize where 2
# Crossover????? Dont know
# Evaluation function based on NO worker at max weight and min ttf also No invalids penalty por engine n atribuid
# Inverter ttf - atual = maior - atual + 1
# validar nr de horas
# testar algoritmo genetico
# testar varios dias
from model.jsonimporter import import_engines, import_workers

Genome = List[int]
Population = List[Genome]


def decide(probability):
    return random() < probability


def generate_genome(engines_count: int, workers_count: int) -> Genome:
    genome = [2] * (workers_count * engines_count)
    genome_range = range(0, len(genome))

    inverse = bool(getrandbits(1))
    if inverse:
        genome_range = range(len(genome) - 1, -1, -1)

    for i in genome_range:
        if genome[i] == 2:
            decision = decide(0.01)
            if decision == 1:
                genome = remove_assigned_engines(genome, i, engines_count, workers_count)
            genome[i] = decision
    return genome


def remove_assigned_engines(genome: [int], engine_index: int, engines_count: int, workers_count: int) -> [int]:
    while True:
        if engine_index - engines_count >= 0:
            engine_index -= engines_count
        else:
            break
    for i in range(workers_count):
        genome[engine_index] = 0
        engine_index = engine_index + engines_count
        if engine_index >= len(genome):
            break
    return genome


def generate_population(size: int, engines_count: int, workers_count: int) -> Population:
    return [generate_genome(engines_count, workers_count) for _ in range(size)]


def mutation(genome: Genome, engines_count: int, workers_count: int, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        index = randrange(len(genome))
        decision = genome[index] if random() > probability else abs(genome[index] - 1)
        if decision == 1:
            genome = remove_assigned_engines(genome, index, engines_count, workers_count)
            genome[index] = decision
    return genome


def crossover(a: Genome, b: Genome, engines_count: int, workers_count: int) -> Tuple[Genome, Genome]:
    if len(a) != len(b):
        raise ValueError("Genomes a and b must be of same length")

    length = len(a)
    if length < 2:
        return a, b

    p = randint(1, length - 1)
    new_genome_a, new_genome_b = a[0:p] + b[p:], b[0:p] + a[p:]

    genome_range = range(0, len(new_genome_a))
    inverse = bool(getrandbits(1))
    if inverse:
        genome_range = range(len(new_genome_a) - 1, -1, -1)

    for i in genome_range:
        if new_genome_a[i] == 1:
            new_genome_a = remove_assigned_engines(new_genome_a, i, engines_count, workers_count)

    # duplicated code
    genome_range = range(0, len(new_genome_b))
    inverse = bool(getrandbits(1))
    if inverse:
        genome_range = range(len(new_genome_b) - 1, -1, -1)

    for i in genome_range:
        if new_genome_b[i] == 1:
            new_genome_b = remove_assigned_engines(new_genome_b, i, engines_count, workers_count)

    return new_genome_a, new_genome_b


# Fitness function
# Genome is [Worker1 - Engine1, Worker1 - Engine2, Worker2 - Engine1, Worker2 - Engine2]
#  if 1 the engine is assigned to the worker
# If workday is not possible returns 0
# If the same engine is assigned twice returns 0
# Returns a higher fitness value if the most number of engines with the lowest ttf are assigned
def calculate_fitness(genome: Genome, engines_list: [Engine], workers_list: [Worker]) -> int:
    if check_duplicate_engine(genome, len(engines_list), len(workers_list)):
        return 0

    workers_days = genome_to_worker_days(genome, engines_list, workers_list)
    if workers_days is None:
        return 0

    fitness = 0
    for worker_day in workers_days:
        fitness += worker_day.get_fitness()
    return fitness


# Transforms Genome into a list of WorkerDay
def genome_to_worker_days(genome: Genome, engines_list: [Engine], workers_list: [Worker]) -> [WorkerDay]:
    workers_days = []
    current_worker_index = 0
    for current_worker in workers_list:
        genome_engines = genome[current_worker_index:current_worker_index + len(engines_list)]
        current_engine_index = 0
        assigned_engines = []
        for current_engine in engines_list:
            if genome_engines[current_engine_index] == 1:
                assigned_engines.append(current_engine)
            current_engine_index += 1
        worker_day = WorkerDay(current_worker, assigned_engines)
        if not worker_day.is_possible:
            return None
        workers_days.append(worker_day)
        current_worker_index += len(engines_list)
    return workers_days


def check_duplicate_engine(genome: Genome, engines_count: int, workers_count: int) -> bool:
    for i in range(engines_count):
        assigned = 0
        for j in range(workers_count):
            if genome[i + j * engines_count] == 1:
                assigned += 1
        if assigned > 1:
            return True
    return False


# Calls all the engines rank method and returns the list in the original order
def rank_engines(engines_list: [Engine]) -> [Engine]:
    max_engine_ttf = 0
    list_of_engines = []
    for current_engine in engines_list:
        if current_engine.ttf > max_engine_ttf:
            max_engine_ttf = current_engine.ttf
    for current_engine in engines_list:
        current_engine.rank_engine(max_engine_ttf)
        list_of_engines.append(current_engine)
    return list_of_engines


if __name__ == '__main__':
    engines = import_engines()
    engines = rank_engines(engines)
    workers = import_workers()
    evo, x = run_evolution(
        populate_func=partial(generate_population, size=10, engines_count=len(engines), workers_count=len(workers)),
        fitness_func=partial(calculate_fitness, engines_list=engines, workers_list=workers),
        fitness_limit=0,
        crossover_func=partial(crossover, engines_count=len(engines), workers_count=len(workers)),
        mutation_func=partial(mutation, engines_count=len(engines), workers_count=len(workers)))
    print("end")
