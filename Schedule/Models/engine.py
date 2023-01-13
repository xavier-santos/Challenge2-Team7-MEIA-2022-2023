# Definition of the engine class
# Properties:
#   - id: unique identifier of the engine
#   - ttf: time to failure of the engine
#   - maintenance_time: time needed to perform the maintenance of the engine
#   - rank: rank of the engine

class Engine:
    def __init__(self, engine_id, ttf, maintenance_time):
        self.id = engine_id
        self.ttf = ttf
        self.maintenance_time = maintenance_time
        self.rank = 0
    
    def rank_engine(self, max_ttf: int):
        self.rank = max_ttf - self.ttf + 1
