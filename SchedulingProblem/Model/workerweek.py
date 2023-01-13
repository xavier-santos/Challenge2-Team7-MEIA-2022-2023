from model import Worker, Engine


class WorkerWeek:
    def __init__(self, worker: Worker, engines: [Engine]):
        self.worker = worker
        self.engines = engines
        self.work_time = worker.work_hours
        self.maintenance_time = 0
        for engine in engines:
            self.maintenance_time += engine.maintenance_time
        if self.maintenance_time > self.work_time:
            self.is_possible = False
        else:
            self.is_possible = True

    # Calculates fitness which is the sum of the ranks of the assigned engines
    def get_fitness(self) -> int:
        fitness = 0
        for engine in self.engines:
            fitness += engine.rank
        return fitness
