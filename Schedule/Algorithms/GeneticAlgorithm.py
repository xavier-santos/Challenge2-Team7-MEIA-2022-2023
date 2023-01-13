from random import choices, randint, random
from typing import List, Tuple
from Models.week import Week

# Genetic Algorithm
# =================
# Applied to the problem of assigning engine maintenance tasks to workers in a week


Population = List[Week]


def rank_engines(engines):
    max_ttf = max(engine.ttf for engine in engines)
    for engine in engines:
        engine.rank_engine(max_ttf)
    return engines


def generate_genome(engines, workers, chance=0.10, chance_increase=0.10):
    week = Week(workers)
    while week.has_empty_days() & (chance < 1.0):
        for worker in workers:
            for day in range(0, 6):
                for engine in engines:
                    if random() < chance:
                        week.add_engine(engine, day, worker)
        chance += chance_increase
    return week


def generate_population(size: int, engines, workers) -> Population:
    rank_engines(engines)
    return [generate_genome(engines, workers) for _ in range(size)]


def fitness_func(genome, empty_penalty=1000) -> int:
    fitness = 0
    if genome.has_empty_days():
        fitness -= empty_penalty
    fitness += genome.get_rank()
    fitness -= genome.get_unassigned_time()
    return fitness


def single_point_crossover(week_a, week_b, workers):
    worker_cutoff = randint(0, len(workers)-1)
    child_a, child_b = Week(workers), Week(workers)

    for x in range(0, worker_cutoff):
        worker = workers[x]
        worker_week_a = week_a.get_workers_weeks_list()[x]
        worker_week_b = week_b.get_workers_weeks_list()[x]
        for y in range(0, 7):
            day_a = worker_week_a.get_day(y)
            day_b = worker_week_b.get_day(y)
            for engine in day_a.get_assigned_engine_list():
                child_a.add_engine(engine, y, worker)
            for engine in day_b.get_assigned_engine_list():
                child_b.add_engine(engine, y, worker)

    for x in range(worker_cutoff, len(workers)):
        worker = workers[x]
        worker_week_a = week_a.get_workers_weeks_list()[x]
        worker_week_b = week_b.get_workers_weeks_list()[x]
        for y in range(0, 7):
            day_a = worker_week_a.get_day(y)
            day_b = worker_week_b.get_day(y)
            for engine in day_b.get_assigned_engine_list():
                child_a.add_engine(engine, y, worker)
            for engine in day_a.get_assigned_engine_list():
                child_b.add_engine(engine, y, worker)

    return child_a, child_b


def mutation(week, engines, workers, day_count=7, num: int = 1, probability: float = 0.5):
    temp_engines = engines.copy()
    for _ in range(num):
        if random() > probability:
            worker_pos = randint(0, len(workers)-1)
            day_pos = randint(0, day_count-1)
            engine_pos = randint(0, len(temp_engines)-1)
            engine = temp_engines[engine_pos]
            if not week.add_engine(engine, day_pos, workers[worker_pos]):
                temp_engines.remove(engine)
    return week


def population_fitness(population: Population) -> int:
    return sum([fitness_func(genome) for genome in population])


def selection_pair(population: Population) -> Population:
    return choices(
        population=population,
        weights=[fitness_func(gene) for gene in population],
        k=2
    )


def sort_population(population: Population) -> Population:
    return sorted(population, key=fitness_func, reverse=True)


def print_stats(population: Population, generation_id: int):
    print("GENERATION %02d" % generation_id)
    print("=============")
    print("Avg. Fitness: %f" % (population_fitness(population, ) / len(population)))
    sorted_population = sort_population(population)
    print("Best: %f" % fitness_func(sorted_population[0]))
    print("Worst: %f" % fitness_func(sorted_population[-1]))
    print("")

    return sorted_population[0]


def run_evolution(workers, engines, population_size=10, fitness_limit=9223372036854775807,
                  generation_limit: int = 100) -> Tuple[Population, int]:

    population = generate_population(population_size, engines, workers)

    for i in range(generation_limit):
        population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)

        if print_stats is not None:
            print_stats(population, i)

        if fitness_func(population[0]) >= fitness_limit:
            break

        next_generation = population[0:2]

        for j in range(int(len(population) / 2) - 1):
            parents = selection_pair(population)
            offspring_a, offspring_b = single_point_crossover(parents[0], parents[1], workers)
            offspring_a = mutation(offspring_a, engines, workers)
            offspring_b = mutation(offspring_b, engines, workers)
            next_generation += [offspring_a, offspring_b]

        population = next_generation

    best_fitness = population_fitness(population)

    return population, best_fitness
