class Engine:
    def __init__(self, engine_id, ttf, maintenance_time):
        self.id = engine_id
        self.ttf = ttf
        self.maintenance_time = maintenance_time
        self.rank = 0
    
    def rank_engine(self, max_ttf: int):
        self.rank = max_ttf - self.ttf + 1
