# Definition of the day class
# Properties:
#   - unassigned_time: Number of unassigned hours in the day subtracting the time of the assigned engines
#   - assigned_time: Number of assigned hours in the day
#   - assigned_engine_list: List of engines in the day by priority

class Day:
    def __init__(self, unassigned_time, assigned_time, assigned_engine_list):
        self.unassigned_time = unassigned_time
        self.assigned_time = assigned_time
        self.assigned_engine_list = assigned_engine_list

    def get_unassigned_time(self):
        return self.unassigned_time

    def get_assigned_engine_list(self):
        return self.assigned_engine_list

    def add_engine(self, engine) -> bool:
        if (engine not in self.assigned_engine_list) & engine.maintenance_time <= self.unassigned_time:
            self.unassigned_time -= engine.maintenance_time
            self.assigned_time += engine.maintenance_time
            self.assigned_engine_list.append(engine)
            return True
        return False

    def remove_engine(self, engine):
        self.assigned_engine_list.remove(engine)
        self.unassigned_time += engine.maintenance_time
        self.assigned_time -= engine.maintenance_time

    def order_engine_list(self):
        self.assigned_engine_list.sort(key=lambda x: x.ttf)
    
    def get_rank(self):
        rank = 0
        for engine in self.assigned_engine_list:
            rank += engine.rank
        return rank
