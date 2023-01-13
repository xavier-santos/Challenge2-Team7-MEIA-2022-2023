# Definition of the week class
# Properties:
#   - assigned_engine_list: list of engines assigned to the workers in the week
#   - assigned_time: number of assigned hours in the week
#   - unassigned_time: number of unassigned hours in the week
#   - workers: list of workers assigned to the week
#   - workers_weeks_list: list of workers week assigned to the week

from Models.worker_week import WorkerWeek


class Week:
    def __init__(self, workers):
        self.assigned_engine_list = []
        self.assigned_time = 0
        self.unassigned_time = 0
        self.workers = workers
        self.workers_weeks_list = []
        for worker in workers:
            self.workers_weeks_list.append(WorkerWeek(worker))
            self.unassigned_time += self.workers_weeks_list[-1].unassigned_time
        
    def get_assigned_engine_list(self):
        return self.assigned_engine_list
    
    def get_assigned_time(self):
        return self.assigned_time
    
    def get_unassigned_time(self):
        return self.unassigned_time

    def get_workers_weeks_list(self):
        return self.workers_weeks_list
    
    def get_workers(self):
        return self.workers

    def add_engine(self, engine, day, worker) -> bool:

        if (engine in self.assigned_engine_list) | engine.maintenance_time > self.unassigned_time:
            return False

        if self.workers_weeks_list[self.get_worker_index(worker)].add_engine(engine, day):
            self.unassigned_time -= engine.maintenance_time
            self.assigned_time += engine.maintenance_time
            self.assigned_engine_list.append(engine)
            return True

        return False

    def get_worker_index(self, worker):
        for i in range(self.workers.__len__()):
            if self.workers[i].worker_id == worker.worker_id:
                return i
        return -1

    def get_rank(self):
        rank = 0
        for worker_week in self.workers_weeks_list:
            rank += worker_week.get_rank()
        return rank

    def has_empty_days(self):
        for worker_week in self.workers_weeks_list:
            if worker_week.has_empty_days():
                return True
        return False
