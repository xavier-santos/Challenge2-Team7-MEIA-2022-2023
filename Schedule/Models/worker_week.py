# Definition of the worker_week class
# Properties:
#   - assigned_engine_list: list of engines assigned to the workers in the week
#   - assigned_time: number of assigned hours in the week
#   - unassigned_time: number of unassigned hours in the week
#   - worker: worker assigned to the week
#   - day_list: list of days in the week
#   - number_of_days: number of days in the week

from Models.day import Day

# Definition of the dictionary of weekdays
week_days_dict = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}


class WorkerWeek:
    def __init__(self, worker):
        self.work_hours = worker.end_time - worker.start_time - 1
        self.week_days_count = (week_days_dict.__len__() - worker.excluded_weekdays.__len__())
        self.assigned_engine_list = []
        self.assigned_time = 0
        self.unassigned_time = self.work_hours * self.week_days_count
        self.worker = worker
        self.day_list = []
        for i in week_days_dict:
            if i not in self.worker.excluded_weekdays:
                self.day_list.append(Day(8, 0, []))
            else:
                self.day_list.append(Day(0, 0, []))
        
    def get_assigned_engine_list(self):
        return self.assigned_engine_list
    
    def get_assigned_time(self):
        return self.assigned_time

    def get_unassigned_time(self):
        return self.unassigned_time
    
    def get_day_list(self):
        return self.day_list

    def get_day(self, day_index):
        return self.day_list[day_index]
    
    def get_worker(self):
        return self.worker

    def add_engine(self, engine, day) -> bool:
        if (engine not in self.assigned_engine_list) & engine.maintenance_time <= self.unassigned_time:
            self.unassigned_time -= engine.maintenance_time
            self.assigned_time += engine.maintenance_time
            self.assigned_engine_list.append(engine)
            self.day_list[day].add_engine(engine)
            return True
        return False

    def remove_engine(self, engine, day):
        if engine not in self.assigned_engine_list:
            return
        self.assigned_engine_list.remove(engine)
        self.unassigned_time += engine.maintenance_time
        self.assigned_time -= engine.maintenance_time
        self.day_list[day].remove_engine(engine)

    # Rank is higher if the engine is assigned to an earlier day
    def get_rank(self):
        rank = 0
        for day in self.day_list:
            rank += day.get_rank() * (7-self.day_list.index(day))
        return rank

    def is_empty_days(self):
        for day in self.day_list:
            if day.get_assigned_engine_list().__len__() <= 0:
                return True
        return False
